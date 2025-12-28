from __future__ import annotations

from typing import Any, Optional, Sequence

from langchain.base_language import BaseLanguageModel
from langchain.tools.base import BaseTool

from real_agents.adapters.agent_helpers import AgentExecutor
from real_agents.data_agent.copilot import ConversationalChatAgent


def initialize_agent(
    tools: Sequence[BaseTool],
    llm: BaseLanguageModel,
    continue_model: str = None,
    agent_kwargs: Optional[dict] = None,
    return_intermediate_steps: Optional[bool] = True,
    **kwargs: Any,
) -> AgentExecutor:
    """Initialize a data agent executor with the given tools and language model.

    Args:
        tools: List of tools the agent has access to.
        llm: Language model to use as the agent.
        continue_model: Model name if continuation prompts are needed.
        agent_kwargs: Additional keyword arguments for the agent executor.
        return_intermediate_steps: Whether to return intermediate steps in the agent execution.
        **kwargs: Additional keyword arguments passed to the agent executor.

    Returns:
        An initialized agent executor for data analysis tasks.
    """

    agent_kwargs = agent_kwargs or {}
    agent_obj = ConversationalChatAgent.from_llm_and_tools(
        llm=llm, tools=tools, continue_model=continue_model, **agent_kwargs
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        return_intermediate_steps=return_intermediate_steps,
        **kwargs,
    )
    return agent_executor
