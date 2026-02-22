<div align="center">

# 🤖 Data Agent

### Autonomous Conversational Analytics Platform

An **Agentic AI system** that converts natural language into executable Python & SQL using LangChain ReAct agents — featuring autonomous tool selection, sandboxed code execution, persistent memory, and real-time streaming of reasoning steps.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Agent_Framework-orange)](https://github.com/langchain-ai/langchain)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](https://www.docker.com/)

</div>

---

## 💡 Why I Built This

Most data analysis tools fall into two camps: **rigid BI dashboards** that can't handle ad-hoc questions, or **notebook environments** that require coding expertise. Neither works for the 90% of business users who have data questions but can't write SQL or Python.

**Data Agent** bridges this gap by turning an LLM into an autonomous analyst that can:
- Understand a vague business question ("*What's our best-performing product category this quarter?*")
- Autonomously decide which tool to use (SQL query? Python analysis? Visualization?)
- Execute code in a sandboxed environment and iterate if the first attempt fails
- Stream its reasoning process in real-time so users can follow along

This isn't just a ChatGPT wrapper — it's a **full agentic pipeline** with tool orchestration, memory management, and production-grade execution.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA AGENT SYSTEM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐     ┌──────────────────────────────────────────────────┐  │
│  │   Frontend    │     │              Agent Core (ReAct Loop)             │  │
│  │              │     │                                                  │  │
│  │  Next.js     │────▶│  User Query                                      │  │
│  │  TypeScript  │     │      │                                           │  │
│  │  Material-UI │     │      ▼                                           │  │
│  │  ECharts     │     │  ┌────────────────────┐                          │  │
│  │  CodeMirror  │     │  │  ConversationalChat │                         │  │
│  │              │     │  │      Agent          │                         │  │
│  └──────────────┘     │  │  (LangChain ReAct)  │                         │  │
│        ▲              │  └─────────┬──────────┘                          │  │
│        │              │            │                                      │  │
│        │              │            ▼                                      │  │
│  ┌─────┴────────┐     │  ┌─────────────────────────────────────┐         │  │
│  │   Flask API   │     │  │        Thought → Action → Observe   │         │  │
│  │              │◀───▶│  │                                     │         │  │
│  │  /api/chat   │     │  │  ┌─────────┐  ┌──────────┐         │         │  │
│  │  /api/upload │     │  │  │ Thought  │─▶│  Action   │         │         │  │
│  │  /api/conv.  │     │  │  └─────────┘  └────┬─────┘         │         │  │
│  └──────────────┘     │  │                    │               │         │  │
│                       │  │         ┌──────────┴──────────┐    │         │  │
│                       │  │         ▼          ▼          ▼    │         │  │
│                       │  │  ┌──────────┐┌──────────┐┌───────┐ │         │  │
│                       │  │  │  Python   ││   SQL    ││ECharts│ │         │  │
│                       │  │  │  Code     ││  Query   ││Viz    │ │         │  │
│                       │  │  │  Builder  ││  Builder ││Builder│ │         │  │
│                       │  │  └─────┬────┘└────┬─────┘└───┬───┘ │         │  │
│                       │  │        │          │          │     │         │  │
│                       │  │        ▼          ▼          ▼     │         │  │
│                       │  │  ┌──────────────────────────────┐  │         │  │
│                       │  │  │     Observation (Results)     │  │         │  │
│                       │  │  └──────────────────────────────┘  │         │  │
│                       │  └─────────────────────────────────────┘         │  │
│                       └──────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        Infrastructure Layer                          │   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────┐  ┌───────────────┐  │   │
│  │  │ MongoDB  │  │  Redis   │  │ Jupyter/IPython│  │    Docker     │  │   │
│  │  │          │  │          │  │   Kernel       │  │  (Sandboxed   │  │   │
│  │  │ Messages │  │ Caching  │  │   Execution    │  │   Execution)  │  │   │
│  │  │ History  │  │ Session  │  │   Engine       │  │               │  │   │
│  │  │ Users    │  │ State    │  │                │  │               │  │   │
│  │  └──────────┘  └──────────┘  └────────────────┘  └───────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### How the ReAct Agent Loop Works

```
User: "Show me the top 5 products by revenue"
  │
  ▼
┌──────────────────────────────────────────────────────────────────┐
│ THOUGHT: I need to query the data to find product revenue.      │
│          The user uploaded a CSV file. I'll use Python to        │
│          analyze it with pandas.                                 │
│                                                                  │
│ ACTION:  PythonCodeBuilder                                       │
│ INPUT:   "Load the uploaded CSV, group by product, sum revenue,  │
│           sort descending, take top 5"                           │
│                                                                  │
│ ──── Code Execution (Sandboxed Jupyter Kernel) ────              │
│ │  import pandas as pd                                         │ │
│ │  df = pd.read_csv('uploaded_data.csv')                       │ │
│ │  top5 = df.groupby('product')['revenue'].sum()               │ │
│ │         .sort_values(ascending=False).head(5)                 │ │
│ └──────────────────────────────────────────────────────────────── │
│                                                                  │
│ OBSERVATION: Successfully returned top 5 products DataFrame      │
│                                                                  │
│ THOUGHT: Now I should visualize this as a bar chart for clarity  │
│                                                                  │
│ ACTION:  ECharts                                                 │
│ INPUT:   "Create a bar chart from the top 5 products data"       │
│                                                                  │
│ OBSERVATION: Chart rendered successfully                         │
│                                                                  │
│ FINAL ANSWER: "Here are your top 5 products by revenue..."       │
└──────────────────────────────────────────────────────────────────┘
```

> The agent **autonomously decides** which tools to invoke, chains multiple steps together, and self-corrects on errors — all without hardcoded workflow logic.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **ReAct Agent Loop** | Autonomous Thought → Action → Observation cycle using LangChain agents |
| 🔧 **Dynamic Tool Selection** | Agent chooses between Python, SQL, visualization, and data loading tools |
| 🐍 **Sandboxed Code Execution** | Python/SQL runs in isolated Jupyter kernels (local or Docker) |
| 📊 **Auto-Visualization** | Generates interactive ECharts visualizations from natural language |
| 💬 **Conversational Memory** | Persistent context across multi-turn conversations via MongoDB |
| ⚡ **Real-time Streaming** | Stream agent reasoning steps and code execution results live |
| 📁 **Multi-format Data Input** | CSV, Excel, databases, and Kaggle dataset integration |
| 🔒 **Production Security** | Docker-based sandboxed execution for untrusted code |

---

## 🛠️ Tech Stack

### Agent & AI Layer
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent Framework | **LangChain** | ReAct agent orchestration, tool management, prompt chaining |
| LLM Support | **GPT-4, GPT-3.5, Claude v1/v2, Azure OpenAI** | Multi-model support with configurable endpoints |
| Code Execution | **Jupyter/IPython Kernels** | Sandboxed, stateful Python execution with variable persistence |
| Prompt Engineering | **Custom ReAct prompts** | Structured Thought/Action/Observation format with tool routing |

### Backend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | **Flask** | REST API server with streaming support |
| Database | **MongoDB** | Persistent storage for conversations, messages, and users |
| Caching | **Redis** | Session state, kernel management, and performance caching |
| Process Management | **Multiprocess + Threading** | Concurrent kernel execution and background task management |

### Frontend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | **Next.js + TypeScript** | Server-side rendering, type safety |
| UI Library | **Material-UI** | Professional component library |
| Visualization | **ECharts** | Interactive, responsive data visualizations |
| Code Editor | **CodeMirror** | Syntax-highlighted code display and editing |
| Styling | **Tailwind CSS** | Utility-first responsive styling |

---

## 🔧 Agent Tools Deep Dive

Each tool is autonomously selected by the agent based on the user's intent:

### `PythonCodeBuilder`
```
Trigger:  "Analyze this data", "Calculate the average", "Clean the dataset"
Process:  Generates Python code → Executes in Jupyter kernel → Returns results
Capable:  pandas, numpy, scikit-learn, matplotlib — full data science stack
```

### `SQLQueryBuilder`
```
Trigger:  "Query the database", "Find all records where...", "Join these tables"
Process:  Generates SQL → Validates syntax → Executes against connected DB → Returns results
Capable:  Complex JOINs, aggregations, window functions, subqueries
```

### `ECharts (Visualization)`
```
Trigger:  "Show me a chart", "Visualize this", "Plot the trend"
Process:  Analyzes data shape → Selects chart type → Generates ECharts config → Renders interactive chart
Capable:  Bar, line, scatter, pie, heatmap, and custom chart types
```

### `KaggleDataLoader`
```
Trigger:  "Find a dataset about...", "Load the Titanic dataset"
Process:  Searches Kaggle API → Downloads dataset → Loads into session → Ready for analysis
Capable:  Search by keyword, download by URL, automatic CSV/Excel parsing
```

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/charan2456/DataAgent.git
cd DataAgent

# Setup backend
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
python main.py

# Setup frontend (in new terminal)
cd frontend
npm install
export NEXT_PUBLIC_BACKEND_ENDPOINT=http://localhost:8000
npm run dev
```

Visit `http://localhost:3000` to start using Data Agent!

---

## 📦 Installation (Detailed)

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB
- Redis
- OpenAI API Key (or compatible LLM API)

### Backend Setup

1. Create Python environment:
```bash
conda create -n data-agent python=3.10
conda activate data-agent
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY=your_key_here
export MONGO_SERVER=127.0.0.1
export REDIS_SERVER=127.0.0.1
export CODE_EXECUTION_MODE=local  # or "docker" for production
```

4. Initialize MongoDB:
```bash
mongosh
> use data_agent
> db.createCollection("user")
> db.createCollection("message")
> db.createCollection("conversation")
> db.createCollection("folder")
```

5. Run backend:
```bash
python main.py
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set environment variables:
```bash
export NEXT_PUBLIC_BACKEND_ENDPOINT=http://localhost:8000
```

3. Run frontend:
```bash
npm run dev
```

4. Open browser at `http://localhost:3000`

---

## 🐳 Docker Deployment

```bash
# Update environment variables in docker-compose.yml
# Then build and start:
docker-compose build
docker-compose up -d
```

### Code Execution Modes

| Mode | Security | Performance | Use Case |
|------|----------|-------------|----------|
| `local` | ⚠️ Code runs on host | ⚡ Fast | Development, trusted environments |
| `docker` | ✅ Isolated containers | Normal | **Production** — sandboxed execution |

```bash
export CODE_EXECUTION_MODE=docker  # Recommended for production
```

---

## 📡 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Main chat endpoint — sends user query, returns agent response with streaming |
| `/api/conversation` | POST | Retrieve full conversation history by ID |
| `/api/conversations/get_conversation_list` | POST | List all conversations for a user |
| `/api/upload` | POST | Upload CSV, Excel, or database files for analysis |
| `/api/llm_list` | GET | Get available language models |

---

## 🧩 Project Structure

```
DataAgent/
├── backend/                    # Flask API Server
│   ├── api/                   # REST API endpoints
│   ├── main.py                # Application entry point & memory pool initialization
│   ├── app.py                 # Flask app configuration
│   ├── schemas.py             # Request/response schemas
│   └── utils/                 # Utility functions
│
├── real_agents/                # 🧠 Agent Intelligence Layer
│   ├── adapters/              # Shared infrastructure
│   │   ├── llm.py            # Custom LLMChain with DataModel support
│   │   ├── agent_helpers/    # Agent base classes & output parsing
│   │   ├── callbacks/        # Streaming & logging callbacks
│   │   ├── data_model/       # Data model abstractions (25 files)
│   │   ├── executors/        # Tool execution engines
│   │   ├── memory/           # Conversation memory management
│   │   └── models/           # LLM model configurations
│   │
│   └── data_agent/            # Data Agent implementation
│       ├── copilot.py        # ConversationalChatAgent (ReAct agent core)
│       ├── copilot_prompt.py # System prompts & ReAct format instructions
│       ├── executors/        # Tool-specific executors
│       │   ├── code_generation_executor.py
│       │   ├── data_summary_executor.py
│       │   └── kaggle_data_loading_executor.py
│       ├── python/           # Python code execution tools
│       ├── sql/              # SQL query execution tools
│       └── evaluation/       # Response evaluation
│
├── frontend/                   # Next.js Frontend (107 files)
│   ├── components/            # React UI components
│   ├── pages/                 # Next.js pages
│   └── styles/                # Tailwind CSS configuration
│
├── docker-compose.yml          # Multi-container Docker deployment
├── Dockerfile                  # Backend container definition
└── TECHNICAL_DOCUMENTATION.md  # In-depth technical reference
```

---

## 🔬 Technical Highlights

### 1. Custom ReAct Implementation
Unlike basic LangChain agent setups, Data Agent implements a **custom `ConversationalChatAgent`** that extends the base agent with:
- **Scratchpad optimization** — Constructs AI message history efficiently to minimize token usage
- **Token budget management** — Dynamic truncation of chat history to stay within model context limits (8K tokens)
- **Continue prompts** — Model-specific continuation strategies for long-running reasoning chains
- **Tool response templating** — Structured observation format that guides the agent's next reasoning step

### 2. Stateful Code Execution
The Jupyter/IPython kernel maintains **state across turns**, meaning:
```
Turn 1: "Load this CSV"           → df variable persists
Turn 2: "Filter rows where x > 5" → Operates on existing df
Turn 3: "Plot the results"         → Uses filtered df from Turn 2
```

### 3. Multi-Model Architecture
The LLM layer supports **hot-swapping models** between:
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude v1, v2)
- Azure OpenAI
- Any OpenAI-compatible endpoint (local LLMs via Ollama, vLLM, etc.)

### 4. Memory Architecture
```
MongoDB (Persistent)           Redis (Session)
├── Conversations             ├── Active kernel sessions
├── Messages                  ├── Cached query results
├── User profiles             └── Temporary state
└── Uploaded file metadata
```

---

## 📊 Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Agent Response Time | ~3-8s | Depends on LLM model and tool complexity |
| Code Execution | <2s | Average for standard pandas operations |
| Visualization Render | <1s | ECharts client-side rendering |
| Context Window | 8K tokens | With dynamic truncation for longer conversations |
| Concurrent Users | Multi-user | Thread-safe kernel pool management |
| Supported File Sizes | Up to 100MB | CSV/Excel file processing |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- UI components from [Material-UI](https://mui.com/)
- Visualization powered by [ECharts](https://echarts.apache.org/)

## 📧 Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/charan2456/DataAgent/issues)
