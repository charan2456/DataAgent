import traceback
from typing import Dict, List, Union
from flask import Response, request, stream_with_context

from backend.api.file import _get_file_path_from_node
from backend.api.language_model import get_llm
from backend.app import app
from backend.main import (
    grounding_source_pool,
    jupyter_kernel_pool,
    logger,
    message_id_register,
    message_pool,
)
from backend.schemas import DEFAULT_USER_ID, OVERLOAD, UNAUTH, NEED_CONTINUE_MODEL, APP_TYPE
from backend.utils.utils import create_personal_folder
from backend.utils.charts import polish_echarts
from backend.utils.streaming import (
    single_round_chat_with_executor,
    single_round_chat_with_agent_streaming,
)
from backend.utils.utils import get_data_summary_cls
from real_agents.adapters.llm import BaseLanguageModel
from real_agents.adapters.agent_helpers import AgentExecutor, Tool
from real_agents.adapters.callbacks import AgentStreamingStdOutCallbackHandler
from real_agents.adapters.data_model import DatabaseDataModel, DataModel, JsonDataModel, TableDataModel
from real_agents.adapters.executors import ChatExecutor
from real_agents.adapters.interactive_executor import initialize_agent
from real_agents.data_agent import CodeGenerationExecutor, KaggleDataLoadingExecutor
from real_agents.adapters.memory import ConversationReActBufferMemory, ReadOnlySharedStringMemory


def create_data_agent_executor(
        grounding_source_dict: Dict[str, DataModel],
        code_interpreter_languages: List[str],
        code_interpreter_tools: List[str],
        llm: BaseLanguageModel,
        llm_name: str,
        user_id: str = None,
        chat_id: str = None,
        code_execution_mode: str = "local",
) -> AgentExecutor:
    """Creates a data agent executor for data analysis tasks.

    Args:
        grounding_source_dict: Dictionary mapping file paths to data models.
        code_interpreter_languages: List of programming languages to enable.
        code_interpreter_tools: List of data analysis tools to enable.
        llm: Language model instance.
        llm_name: Name of the language model.
        user_id: User identifier.
        chat_id: Chat session identifier.
        code_execution_mode: Execution mode - "local" or "docker".

    Returns:
        Configured agent executor for data analysis.
    """
    # Initialize conversation memory
    memory = ConversationReActBufferMemory(
        memory_key="chat_history", return_messages=True, llm=llm, max_token_limit=3500
    )
    read_only_memory = ReadOnlySharedStringMemory(memory=memory)

    # Initialize code generation executors
    basic_chat_executor = ChatExecutor()
    python_code_executor = CodeGenerationExecutor(
        programming_language="python", memory=read_only_memory)
    sql_code_executor = CodeGenerationExecutor(
        programming_language="sql", memory=read_only_memory)
    echart_code_executor = CodeGenerationExecutor(
        programming_language="python", memory=read_only_memory, usage="echarts"
    )
    kaggle_data_loader = KaggleDataLoadingExecutor()

    def run_python_code_builder(term: str) -> Union[Dict, DataModel]:
        """Executes Python code generation and execution."""
        try:
            input_grounding_source = [gs for gs in grounding_source_dict.values()]
            results = python_code_executor.run(
                user_intent=term,
                llm=llm,
                grounding_source=input_grounding_source,
                user_id=user_id,
                chat_id=chat_id,
                code_execution_mode=code_execution_mode,
                jupyter_kernel_pool=jupyter_kernel_pool,
            )

            logger.bind(msg_head=f"PythonCodeBuilder results").debug(results)

            if results["result"]["success"]:
                if results["result"]["result"] is not None:
                    raw_output = results["result"]["result"]
                elif results["result"]["stdout"] != "":
                    raw_output = results["result"]["stdout"]
                else:
                    raw_output = ""
                observation = JsonDataModel.from_raw_data(
                    {
                        "success": True,
                        "result": raw_output,
                        "images": results["result"]["outputs"] if ".show()" in results[
                            "intermediate_steps"] else [],
                        "intermediate_steps": results["intermediate_steps"],
                    },
                    filter_keys=["images"],
                )
            else:
                observation = JsonDataModel.from_raw_data(
                    {
                        "success": False,
                        "result": results["result"]["error_message"],
                        "intermediate_steps": results["intermediate_steps"],
                    }
                )
            return observation
        except Exception as e:
            logger.bind(msg_head=f"PythonCodeBuilder error").error(str(e))
            traceback.print_exc()
            results = basic_chat_executor.run(user_intent=term, llm=llm)
            return results["result"]

    def run_sql_code_builder(term: str) -> Union[Dict, DataModel]:
        """Executes SQL query generation and execution."""
        try:
            def convert_grounding_source_as_db(
                    grounding_source_dict: Dict[str, DataModel]
            ) -> Union[List[TableDataModel], DatabaseDataModel]:
                db_grounding_source = [
                    gs for _, gs in grounding_source_dict.items() if
                    isinstance(gs, DatabaseDataModel)
                ]
                table_grounding_source = [
                    gs for _, gs in grounding_source_dict.items() if
                    isinstance(gs, TableDataModel)
                ]
                assert len(db_grounding_source) <= 1
                if len(table_grounding_source) == 0:
                    return db_grounding_source[0]
                else:
                    for t_gs in table_grounding_source:
                        if len(db_grounding_source) == 0:
                            if t_gs.db_view is None:
                                t_gs.set_db_view(
                                    DatabaseDataModel.from_table_data_model(t_gs))
                            db_gs = t_gs.db_view
                            db_grounding_source.append(db_gs)
                        else:
                            db_gs = db_grounding_source[0]
                            db_gs.insert_table_data_model(t_gs)
                    return db_gs

            input_grounding_source = convert_grounding_source_as_db(grounding_source_dict)
            results = sql_code_executor.run(
                user_intent=term,
                grounding_source=input_grounding_source,
                llm=llm,
            )

            logger.bind(msg_head=f"SQLQueryBuilder results").debug(results)

            if results["result"]["success"]:
                observation = JsonDataModel.from_raw_data({
                    "success": True,
                    "result": results["result"]["result"],
                    "intermediate_steps": results["intermediate_steps"],
                })
            else:
                observation = JsonDataModel.from_raw_data({
                    "success": False,
                    "result": results["result"]["error_message"],
                    "intermediate_steps": results["intermediate_steps"],
                })
            return observation
        except Exception as e:
            logger.bind(msg_head=f"SQLQueryBuilder error").error(str(e))
            traceback.print_exc()
            results = basic_chat_executor.run(user_intent=term, llm=llm)
            return results["result"]

    def run_echarts_visualization(term: str) -> Union[Dict, DataModel]:
        """Generates interactive ECharts visualizations."""
        try:
            input_grounding_source = [gs for _, gs in grounding_source_dict.items() if
                                      isinstance(gs, TableDataModel)]
            results = echart_code_executor.run(
                user_intent=term,
                llm=llm,
                grounding_source=input_grounding_source,
                user_id=user_id,
                chat_id=chat_id,
                code_execution_mode=code_execution_mode,
                jupyter_kernel_pool=jupyter_kernel_pool,
            )

            logger.bind(msg_head=f"EchartsVisualization results").debug(results)

            if results["result"]["success"]:
                results = JsonDataModel.from_raw_data(
                    {
                        "success": True,
                        "result": "",
                        "echarts": polish_echarts(results["result"]["stdout"]),
                        "intermediate_steps": results["intermediate_steps"],
                    },
                    filter_keys=["result", "echarts"],
                )
            else:
                results = JsonDataModel.from_raw_data(
                    {
                        "success": False,
                        "result": results["result"]["error_message"],
                        "intermediate_steps": results["intermediate_steps"],
                    }
                )
            return results
        except Exception as e:
            logger.bind(msg_head=f"EchartsVisualization error").error(str(e))
            results = basic_chat_executor.run(user_intent=term, llm=llm)
            return results["result"]

    def run_kaggle_data_loader(term: str) -> Union[Dict, DataModel]:
        """Loads and searches Kaggle datasets."""
        try:
            results = kaggle_data_loader.run(
                user_intent=term,
                llm=llm,
            )
            logger.bind(msg_head=f"KaggleDataLoader results").debug(results)

            results = JsonDataModel.from_raw_data(
                {
                    "success": True,
                    "kaggle_action": results["kaggle_action"],
                    "kaggle_output_info": results["kaggle_output_info"],
                },
            )
            return results
        except Exception as e:
            logger.bind(msg_head=f"KaggleDataLoader error").error(str(e))
            traceback.print_exc()
            results = basic_chat_executor.run(user_intent=term, llm=llm)
            return results["result"]

    # Define available tools
    tool_dict = {
        "PythonCodeBuilder": Tool(
            name="PythonCodeBuilder",
            func=run_python_code_builder,
            description="""
Description: Converts natural language problems into Python code and executes it. Ideal for mathematics, data manipulation, computational tasks, and basic visualizations using matplotlib. Does not generate database queries.
Input: A natural language problem or question.
Output: Python code and its execution results.
Note: Use this tool whenever you need to generate and execute Python code.
            """,
        ),
        "SQLQueryBuilder": Tool(
            name="SQLQueryBuilder",
            func=run_sql_code_builder,
            description="""
Description: Specialized for database operations. Converts natural language queries into SQL code and executes them. Best suited for database queries, but cannot solve mathematical problems or perform data manipulations outside SQL context. Always specify the table name.
Input: A natural language query about database operations, including the target table name.
Output: SQL code and its execution results.
Note: Always use this tool when you need to generate and execute SQL queries.
            """,
        ),
        "Echarts": Tool(
            name="Echarts",
            func=run_echarts_visualization,
            description="""
Description: Creates interactive data visualizations using ECharts. Supports scatter plots, bar charts, line charts, and pie charts. Automatically selects appropriate labels and titles.
Input: A natural language description of the desired visualization.
Output: ECharts code that generates an interactive chart.
Note: Currently supports only the listed chart types. Ensure your visualization requirements match these options.
            """,
        ),
        "KaggleDataLoader": Tool(
            name="KaggleDataLoader",
            func=run_kaggle_data_loader,
            description="""
Description: Connects to Kaggle datasets. Can load specific datasets by path or search for datasets based on keywords and descriptions.
Input: Natural language intent mentioning a Kaggle dataset path, keywords, or dataset description.
Output: The action performed and either the dataset path or search results.
            """,
        ),
    }
    
    # Data profiling tool is not activated in the agent
    IGNORE_TOOLS = ["DataProfiling"]
    
    # Activate tools based on user selection
    tools = [tool_dict[lang["name"]] for lang in code_interpreter_languages]
    for tool in code_interpreter_tools:
        if tool["name"] not in IGNORE_TOOLS:
            tools.append(tool_dict[tool["name"]])

    # Build the data agent with LLM and tools
    continue_model = llm_name if llm_name in NEED_CONTINUE_MODEL else None
    agent_executor = initialize_agent(tools, llm, continue_model, memory=memory, verbose=True)
    return agent_executor


@app.route("/api/chat", methods=["POST"])
def chat() -> Response:
    """Handles chat requests for data analysis tasks."""
    try:
        # Extract request parameters
        request_json = request.get_json()
        user_id = request_json.pop("user_id", DEFAULT_USER_ID)
        chat_id = request_json["chat_id"]
        user_intent = request_json["user_intent"]
        parent_message_id = int(request_json["parent_message_id"])
        code_interpreter_languages = request_json.get("code_interpreter_languages", [])
        code_interpreter_tools = request_json.get("code_interpreter_tools", [])
        api_call = request_json.get("api_call", None)
        llm_name = request_json["llm_name"]
        temperature = request_json.get("temperature", 0.7)
        stop_words = ["[RESPONSE_BEGIN]", "TOOL RESPONSE"]
        kwargs = {
            "temperature": temperature,
            "stop": stop_words,
        }

        # Initialize language model
        stream_handler = AgentStreamingStdOutCallbackHandler()
        llm = get_llm(llm_name, **kwargs)

        logger.bind(user_id=user_id, chat_id=chat_id, api="/chat",
                    msg_head="Request received").debug(request_json)

        if api_call:
            # Handle data profiling API call
            grounding_source_dict = grounding_source_pool.get_pool_info_with_id(
                user_id, chat_id, default_value={})

            activated_message_list = message_pool.get_activated_message_list(
                user_id, chat_id, default_value=list(),
                parent_message_id=parent_message_id
            )
            assert api_call["api_name"] == "DataProfiling"
            ai_message_id = message_id_register.add_variable("")
            file_node = api_call["args"]["activated_file"]

            folder = create_personal_folder(user_id)
            file_path = _get_file_path_from_node(folder, file_node)
            executor = get_data_summary_cls(file_path)()
            gs = grounding_source_dict[file_path]
            return stream_with_context(
                Response(
                    single_round_chat_with_executor(
                        executor,
                        user_intent=gs,
                        human_message_id=None,
                        ai_message_id=ai_message_id,
                        user_id=DEFAULT_USER_ID,
                        chat_id=api_call["args"]["chat_id"],
                        message_list=activated_message_list,
                        parent_message_id=api_call["args"]["parent_message_id"],
                        llm=llm,
                        app_type=APP_TYPE,
                    ),
                    content_type="application/json",
                )
            )
        else:
            # Handle regular chat request
            grounding_source_dict = grounding_source_pool.get_pool_info_with_id(
                user_id, chat_id, default_value={})
            
            # Create agent executor
            agent_executor = create_data_agent_executor(
                grounding_source_dict=grounding_source_dict,
                code_interpreter_languages=code_interpreter_languages,
                code_interpreter_tools=code_interpreter_tools,
                llm=llm,
                llm_name=llm_name,
                user_id=user_id,
                chat_id=chat_id,
                code_execution_mode=app.config["CODE_EXECUTION_MODE"],
            )
            
            # Load conversation history
            activated_message_list = message_pool.get_activated_message_list(
                user_id, chat_id, default_value=list(),
                parent_message_id=parent_message_id
            )
            message_pool.load_agent_memory_from_list(agent_executor.memory, activated_message_list)
            
            human_message_id = message_id_register.add_variable(user_intent)
            ai_message_id = message_id_register.add_variable("")
            
            return stream_with_context(
                Response(
                    single_round_chat_with_agent_streaming(
                        interaction_executor=agent_executor,
                        user_intent=user_intent,
                        human_message_id=human_message_id,
                        ai_message_id=ai_message_id,
                        user_id=user_id,
                        chat_id=chat_id,
                        message_list=activated_message_list,
                        parent_message_id=parent_message_id,
                        llm_name=llm_name,
                        stream_handler=stream_handler,
                        app_type=APP_TYPE
                    ),
                    content_type="application/json",
                )
            )

    except Exception as e:
        try:
            logger.bind(user_id=user_id, chat_id=chat_id, api="/chat",
                        msg_head="Chat error").error(str(e))
            import traceback
            traceback.print_exc()
        except:
            return Response(response=None, status=f"{UNAUTH} Invalid Authentication")
        return Response(response=None, status=f"{OVERLOAD} Server is currently overloaded")

