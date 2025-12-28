# Data Agent

An AI-powered platform for intelligent data analysis, code generation, and visualization. Transform natural language queries into executable Python and SQL code with real-time execution and interactive visualizations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/charan2456/data-agent.git
cd data-agent

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

## Features

- **Natural Language to Code**: Convert your data questions into Python or SQL code automatically
- **Interactive Visualizations**: Create charts and graphs using ECharts with simple text descriptions
- **Data Processing**: Upload and analyze CSV, Excel, and database files
- **Kaggle Integration**: Search and load datasets directly from Kaggle
- **Real-time Execution**: See code execution results streamed in real-time
- **Conversation History**: Maintain context across multiple interactions

## Tech Stack

### Backend
- **Flask** - Web framework
- **LangChain** - Agent framework
- **Jupyter/IPython** - Code execution engine
- **MongoDB** - Persistent storage
- **Redis** - Caching layer

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type safety
- **Material-UI** - UI components
- **ECharts** - Data visualization
- **CodeMirror** - Code editor
- **Tailwind CSS** - Styling

## Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB
- Redis
- OpenAI API Key (or compatible LLM API)

## Installation

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
export CODE_EXECUTION_MODE=local
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

4. Open browser:
```
http://localhost:3000
```

## Usage

1. **Upload Data**: Click the file upload button to add CSV, Excel, or database files
2. **Ask Questions**: Type natural language questions about your data
3. **View Results**: See generated code, execution results, and visualizations
4. **Iterate**: Continue the conversation to refine your analysis

## Available Tools

- **PythonCodeBuilder**: Generate and execute Python code for data manipulation and analysis
- **SQLQueryBuilder**: Create and run SQL queries on your databases
- **Echarts**: Create interactive visualizations (scatter, bar, line, pie charts)
- **KaggleDataLoader**: Search and load datasets from Kaggle

## API Endpoints

- `POST /api/chat` - Main chat endpoint for data analysis
- `POST /api/conversation` - Get conversation history
- `POST /api/conversations/get_conversation_list` - List all conversations
- `POST /api/upload` - Upload data files
- `GET /api/llm_list` - Get available language models

## Configuration

### Code Execution Modes

- **local**: Code runs directly on the server (default)
- **docker**: Code runs in isolated Docker containers (recommended for production)

Set via environment variable:
```bash
export CODE_EXECUTION_MODE=docker
```

### Supported Language Models

- GPT-3.5-turbo-16k
- GPT-4
- Claude v1
- Claude v2
- Azure OpenAI
- Custom OpenAI-compatible endpoints

## Docker Deployment

1. Update environment variables in `docker-compose.yml`:
```yaml
environment:
  - OPENAI_API_KEY=your_key_here
```

2. Build and start:
```bash
docker-compose build
docker-compose up -d
```

## Project Structure

```
data-agent/
├── backend/          # Flask backend
│   ├── api/         # API endpoints
│   ├── utils/       # Utility functions
│   └── ...
├── frontend/         # Next.js frontend
│   ├── components/  # React components
│   ├── pages/       # Next.js pages
│   └── ...
└── real_agents/      # Agent implementations
    ├── adapters/    # Shared adapters
    └── data_agent/  # Data agent logic
```

## Customization

The frontend uses Tailwind CSS for easy customization. You can modify colors, fonts, and styling by editing:
- `frontend/styles/globals.css` - Global styles and CSS variables
- `frontend/tailwind.config.js` - Tailwind theme configuration
- Component files in `frontend/components/` - Individual component styles

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- UI components from [Material-UI](https://mui.com/)
- Visualization powered by [ECharts](https://echarts.apache.org/)

## 📧 Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/charan2456/data-agent/issues)
