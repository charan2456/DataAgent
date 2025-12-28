# Data Agent - Technical Documentation

## Executive Summary

**Data Agent** is an AI-powered conversational data analysis platform that transforms natural language queries into executable code (Python and SQL), executes that code in real-time, and presents results through interactive visualizations. It serves as an intelligent intermediary between business users and complex data analysis workflows, eliminating the need for technical programming knowledge while maintaining the power and flexibility of code-based analysis.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [How It Works - Detailed Flow](#how-it-works---detailed-flow)
5. [Tools and Capabilities](#tools-and-capabilities)
6. [Detailed Examples](#detailed-examples)
7. [Technical Implementation](#technical-implementation)
8. [Data Flow Architecture](#data-flow-architecture)
9. [Security and Execution Modes](#security-and-execution-modes)
10. [Use Cases](#use-cases)

---

## Overview

### What is Data Agent?

Data Agent is a **conversational AI agent** built on the LangChain framework that specializes in data analysis tasks. Unlike traditional BI tools that require predefined queries or dashboards, Data Agent allows users to:

- **Ask questions in natural language** about their data
- **Automatically generate and execute code** (Python/SQL) to answer those questions
- **Receive real-time results** with interactive visualizations
- **Maintain conversation context** across multiple interactions
- **Work with various data sources** (CSV, Excel, databases, Kaggle datasets)

### Key Differentiators

1. **Code Generation & Execution**: Unlike query builders or drag-and-drop tools, Data Agent generates actual executable code, providing unlimited flexibility
2. **Conversational Interface**: Maintains context across multiple questions, allowing iterative analysis
3. **Real-time Execution**: Code is executed immediately, with results streamed back to the user
4. **Multi-modal Output**: Supports tables, charts, images, and text responses
5. **Self-contained**: Includes code execution engine, memory management, and visualization capabilities

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Chat UI    │  │  File Upload │  │ Visualizations│     │
│  └──────┬───────┘  └──────┬──────┘  └──────┬───────┘      │
└─────────┼──────────────────┼─────────────────┼────────────┘
           │                  │                 │
           │ HTTP/REST API    │                 │
           │                  │                 │
┌──────────▼──────────────────▼─────────────────▼────────────┐
│                  Backend (Flask)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         API Layer (chat.py, file.py)                 │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │      Data Agent Executor (LangChain Agent)            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │   LLM        │  │   Tools      │  │  Memory    │ │  │
│  │  │ (GPT-4/Claude)│  │ (Code Gen)  │  │ (Context)  │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │         Code Execution Engine (IPython/Jupyter)       │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┼──────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼────┐  ┌─────▼─────┐  ┌───▼──────┐
│  MongoDB   │  │   Redis   │  │  Files   │
│ (Storage)  │  │  (Cache)   │  │ (Data)   │
└────────────┘  └────────────┘  └──────────┘
```

### Component Breakdown

#### 1. **Frontend Layer** (Next.js + TypeScript)
- **Purpose**: User interface and interaction
- **Key Technologies**: React, Next.js, Material-UI, ECharts, CodeMirror
- **Responsibilities**:
  - Render chat interface
  - Handle file uploads
  - Display code, results, and visualizations
  - Manage conversation state
  - Stream real-time updates from backend

#### 2. **Backend API Layer** (Flask)
- **Purpose**: HTTP API endpoints and request handling
- **Key Endpoints**:
  - `POST /api/chat` - Main chat endpoint
  - `POST /api/upload` - File upload
  - `POST /api/conversation` - Conversation history
  - `GET /api/llm_list` - Available models

#### 3. **Agent Layer** (LangChain)
- **Purpose**: Core intelligence - interprets queries and orchestrates tools
- **Components**:
  - **LLM Integration**: Connects to GPT-4, Claude, or other models
  - **Agent Executor**: Manages the ReAct (Reasoning + Acting) loop
  - **Memory System**: Maintains conversation context
  - **Tool Selection**: Chooses appropriate tools based on query

#### 4. **Execution Layer** (IPython/Jupyter)
- **Purpose**: Execute generated code safely
- **Modes**:
  - **Local**: Direct execution on server
  - **Docker**: Sandboxed execution in containers
- **Capabilities**: Python, SQL, visualization generation

#### 5. **Storage Layer**
- **MongoDB**: Persistent storage for conversations, messages, users
- **Redis**: Caching and session management
- **File System**: Uploaded data files (CSV, Excel, etc.)

---

## Core Components

### 1. ConversationalChatAgent

The core agent class that extends LangChain's Agent framework.

**Location**: `real_agents/data_agent/copilot.py`

**Key Features**:
- Implements ReAct (Reasoning + Acting) pattern
- Maintains conversation history
- Selects and executes tools based on user intent
- Handles multi-turn conversations

**How it works**:
```python
class ConversationalChatAgent(Agent):
    """
    Agent that:
    1. Receives user query
    2. Analyzes intent using LLM
    3. Selects appropriate tool (Python, SQL, ECharts, etc.)
    4. Executes tool with generated code
    5. Returns result to user
    6. Maintains context for next query
    """
```

### 2. Code Generation Executors

Specialized executors that generate and execute code in different languages.

#### PythonCodeBuilder
- **Purpose**: Generate and execute Python code for data analysis
- **Capabilities**:
  - Data loading and manipulation (pandas, numpy)
  - Statistical analysis
  - Machine learning (scikit-learn)
  - Image processing
  - Custom Python logic

#### SQLQueryBuilder
- **Purpose**: Generate and execute SQL queries
- **Capabilities**:
  - Query generation from natural language
  - Database schema understanding
  - Complex joins and aggregations
  - Query optimization

#### EchartsVisualization
- **Purpose**: Generate interactive visualizations
- **Capabilities**:
  - Bar charts, line charts, scatter plots
  - Pie charts, heatmaps
  - Custom ECharts configurations
  - Interactive features (zoom, pan, tooltips)

### 3. Memory System

**ConversationReActBufferMemory**:
- Stores conversation history
- Maintains context across multiple turns
- Token-aware truncation (max 3500 tokens)
- Preserves tool execution results

**ReadOnlySharedStringMemory**:
- Provides read-only access to memory
- Used by code executors to understand context
- Prevents memory corruption during execution

### 4. Data Models

Abstraction layer for different data types:

- **TableDataModel**: Represents tabular data (CSV, Excel)
- **DatabaseDataModel**: Represents database connections
- **JsonDataModel**: Represents JSON data
- **ImageDataModel**: Represents image data
- **MessageDataModel**: Represents chat messages

---

## How It Works - Detailed Flow

### Step-by-Step Execution Flow

#### **Step 1: User Query Reception**

```
User types: "What are the top 5 products by sales in 2023?"
    ↓
Frontend sends POST request to /api/chat
    ↓
Backend receives query with:
    - User message text
    - Conversation ID (for context)
    - User ID
    - Attached files (if any)
```

#### **Step 2: Context Loading**

```
Backend loads:
    - Previous conversation messages from MongoDB
    - Uploaded data files (CSV, Excel, etc.)
    - Database connections (if any)
    - User preferences
    ↓
Creates "grounding_source_dict" mapping file paths to DataModel objects
```

#### **Step 3: Agent Initialization**

```
Creates Data Agent Executor with:
    - LLM instance (GPT-4/Claude)
    - Available tools (Python, SQL, ECharts, Kaggle)
    - Memory system (loaded with conversation history)
    - Code execution mode (local/docker)
```

#### **Step 4: LLM Reasoning (ReAct Loop)**

```
LLM receives:
    - User query
    - Conversation history
    - Available tools list
    - Data schema information
    ↓
LLM analyzes and decides:
    "I need to:
     1. Load the sales data
     2. Filter for 2023
     3. Group by product
     4. Sum sales
     5. Sort descending
     6. Take top 5
     7. Display as table"
    ↓
LLM selects tool: "PythonCodeBuilder"
```

#### **Step 5: Code Generation**

```
PythonCodeExecutor receives:
    - User intent: "top 5 products by sales in 2023"
    - Grounding sources: [sales_data.csv]
    - Conversation history
    ↓
PythonCodeExecutor uses LLM to generate code:
    
    import pandas as pd
    df = pd.read_csv('sales_data.csv')
    df_2023 = df[df['year'] == 2023]
    top_5 = df_2023.groupby('product')['sales'].sum().sort_values(ascending=False).head(5)
    print(top_5)
```

#### **Step 6: Code Execution**

```
Code is sent to IPython kernel:
    - Kernel executes code line by line
    - Captures stdout, stderr, and return values
    - Handles errors gracefully
    ↓
Execution result:
    {
        "success": true,
        "result": "Product A: $1,250,000\nProduct B: $980,000\n...",
        "stdout": "...",
        "variables": {"df": DataFrame, "top_5": Series}
    }
```

#### **Step 7: Result Processing**

```
Result is processed:
    - If DataFrame/Series: Converted to JSON for display
    - If visualization: ECharts configuration generated
    - If error: Error message extracted and explained
    ↓
Formatted response created:
    {
        "type": "table",
        "data": [...],
        "code": "...",
        "explanation": "Here are the top 5 products..."
    }
```

#### **Step 8: Streaming Response**

```
Response is streamed to frontend:
    - Tool selection notification
    - Code generation progress
    - Execution status
    - Results (table/chart/text)
    ↓
Frontend updates UI in real-time:
    - Shows generated code
    - Displays results
    - Updates conversation history
```

#### **Step 9: Memory Update**

```
Conversation is saved to MongoDB:
    - User message
    - Generated code
    - Execution results
    - Agent response
    ↓
Memory updated for next query:
    - Context preserved
    - Variables available for next query
    - Previous results can be referenced
```

---

## Tools and Capabilities

### 1. PythonCodeBuilder

**Purpose**: Generate and execute Python code for data analysis

**When Used**:
- Data manipulation and transformation
- Statistical analysis
- Machine learning tasks
- Custom calculations
- File operations

**Example Capabilities**:
```python
# User: "Calculate the average age by department"
# Generated Code:
import pandas as pd
df = pd.read_csv('employees.csv')
result = df.groupby('department')['age'].mean()
print(result)

# User: "Create a correlation matrix for numeric columns"
# Generated Code:
import pandas as pd
import seaborn as sns
df = pd.read_csv('data.csv')
correlation = df.select_dtypes(include=['number']).corr()
sns.heatmap(correlation, annot=True)
plt.show()
```

**Key Features**:
- Automatic library imports (pandas, numpy, matplotlib, etc.)
- Context-aware variable reuse
- Error handling and retry logic
- Support for visualization libraries

### 2. SQLQueryBuilder

**Purpose**: Generate and execute SQL queries

**When Used**:
- Querying databases
- Complex joins and aggregations
- Data filtering and sorting
- Database-specific operations

**Example Capabilities**:
```sql
-- User: "Show me customers who bought more than $1000 worth of products"
-- Generated SQL:
SELECT 
    c.customer_id,
    c.customer_name,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(o.total_amount) > 1000
ORDER BY total_spent DESC;
```

**Key Features**:
- Schema-aware query generation
- Support for multiple database types (PostgreSQL, MySQL, SQLite)
- Query optimization
- Safe parameterization

### 3. EchartsVisualization

**Purpose**: Create interactive data visualizations

**When Used**:
- Creating charts and graphs
- Data exploration
- Presentation of analysis results
- Interactive dashboards

**Example Capabilities**:
```python
# User: "Create a bar chart showing sales by region"
# Generated ECharts Configuration:
{
    "title": {"text": "Sales by Region"},
    "xAxis": {"type": "category", "data": ["North", "South", "East", "West"]},
    "yAxis": {"type": "value"},
    "series": [{
        "type": "bar",
        "data": [120000, 98000, 145000, 110000]
    }]
}
```

**Supported Chart Types**:
- Bar charts (vertical/horizontal)
- Line charts
- Scatter plots
- Pie charts
- Heatmaps
- 3D visualizations

### 4. KaggleDataLoader

**Purpose**: Search and load datasets from Kaggle

**When Used**:
- Finding relevant datasets
- Loading public datasets
- Data exploration

**Example**:
```
User: "Load the Titanic dataset from Kaggle"
    ↓
Agent searches Kaggle for "Titanic"
    ↓
Downloads dataset
    ↓
Loads into pandas DataFrame
    ↓
Provides summary statistics
```

---

## Detailed Examples

### Example 1: Sales Analysis Workflow

**Scenario**: A business analyst wants to analyze quarterly sales performance.

#### Query 1: "Load the sales data from sales_2023.csv"

**Agent Process**:
1. **Tool Selection**: PythonCodeBuilder
2. **Code Generation**:
   ```python
   import pandas as pd
   df = pd.read_csv('sales_2023.csv')
   print(f"Loaded {len(df)} rows")
   print(df.head())
   print(df.info())
   ```
3. **Execution**: Code runs, loads CSV file
4. **Result**: 
   - Table preview (first 5 rows)
   - Data shape: (10,000 rows, 8 columns)
   - Column names and types
5. **Memory Update**: Variable `df` stored for future queries

#### Query 2: "What are the total sales by quarter?"

**Agent Process**:
1. **Context Awareness**: Agent knows `df` exists from previous query
2. **Tool Selection**: PythonCodeBuilder
3. **Code Generation**:
   ```python
   # Using existing df variable
   df['date'] = pd.to_datetime(df['date'])
   df['quarter'] = df['date'].dt.quarter
   quarterly_sales = df.groupby('quarter')['sales_amount'].sum()
   print(quarterly_sales)
   ```
4. **Execution**: Processes data, calculates quarterly totals
5. **Result**:
   ```
   Quarter  Sales
   1        $2,450,000
   2        $2,680,000
   3        $2,890,000
   4        $3,120,000
   ```

#### Query 3: "Show me a bar chart of quarterly sales"

**Agent Process**:
1. **Context**: Knows `quarterly_sales` variable exists
2. **Tool Selection**: EchartsVisualization
3. **Code Generation**:
   ```python
   import json
   chart_config = {
       "title": {"text": "Quarterly Sales 2023"},
       "xAxis": {"type": "category", "data": ["Q1", "Q2", "Q3", "Q4"]},
       "yAxis": {"type": "value"},
       "series": [{
           "type": "bar",
           "data": [2450000, 2680000, 2890000, 3120000],
           "itemStyle": {"color": "#4F46E5"}
       }]
   }
   print(json.dumps(chart_config))
   ```
4. **Execution**: Generates ECharts configuration
5. **Result**: Interactive bar chart displayed in UI

#### Query 4: "Which product category had the highest growth from Q1 to Q4?"

**Agent Process**:
1. **Context**: Uses existing `df` with quarterly data
2. **Tool Selection**: PythonCodeBuilder
3. **Code Generation**:
   ```python
   # Calculate growth by category
   q1_sales = df[df['quarter'] == 1].groupby('category')['sales_amount'].sum()
   q4_sales = df[df['quarter'] == 4].groupby('category')['sales_amount'].sum()
   growth = ((q4_sales - q1_sales) / q1_sales * 100).sort_values(ascending=False)
   print("Category Growth (Q1 to Q4):")
   print(growth)
   print(f"\nHighest growth: {growth.index[0]} with {growth.iloc[0]:.2f}%")
   ```
4. **Execution**: Calculates growth percentages
5. **Result**:
   ```
   Category Growth (Q1 to Q4):
   Electronics    45.2%
   Clothing       32.8%
   Home           28.5%
   ...
   
   Highest growth: Electronics with 45.2%
   ```

**Key Observations**:
- **Context Preservation**: Each query builds on previous results
- **Variable Reuse**: No need to reload data
- **Progressive Analysis**: From loading → aggregation → visualization → insights
- **Natural Language**: No SQL or Python knowledge required

---

### Example 2: Database Query Workflow

**Scenario**: Querying a customer database for insights.

#### Query 1: "Connect to the customer database and show me the schema"

**Agent Process**:
1. **Tool Selection**: SQLQueryBuilder
2. **Code Generation**:
   ```sql
   -- Get table names
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public';
   
   -- Get columns for customers table
   SELECT column_name, data_type 
   FROM information_schema.columns 
   WHERE table_name = 'customers';
   ```
3. **Execution**: Queries database metadata
4. **Result**: Schema information displayed

#### Query 2: "Find customers who haven't placed an order in the last 6 months"

**Agent Process**:
1. **Tool Selection**: SQLQueryBuilder
2. **Code Generation**:
   ```sql
   SELECT 
       c.customer_id,
       c.customer_name,
       c.email,
       MAX(o.order_date) as last_order_date,
       CURRENT_DATE - MAX(o.order_date) as days_since_last_order
   FROM customers c
   LEFT JOIN orders o ON c.customer_id = o.customer_id
   GROUP BY c.customer_id, c.customer_name, c.email
   HAVING MAX(o.order_date) IS NULL 
      OR MAX(o.order_date) < CURRENT_DATE - INTERVAL '6 months'
   ORDER BY days_since_last_order DESC NULLS LAST;
   ```
3. **Execution**: Complex join with date filtering
4. **Result**: List of inactive customers

#### Query 3: "Create a visualization showing customer acquisition by month"

**Agent Process**:
1. **Tool Selection**: SQLQueryBuilder + EchartsVisualization
2. **Code Generation**:
   ```sql
   SELECT 
       DATE_TRUNC('month', created_at) as month,
       COUNT(*) as new_customers
   FROM customers
   WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
   GROUP BY month
   ORDER BY month;
   ```
3. **Execution**: Aggregates customer data by month
4. **Visualization**: Line chart showing acquisition trends

---

### Example 3: Machine Learning Workflow

**Scenario**: Building a predictive model.

#### Query 1: "Load the housing prices dataset and show me the first few rows"

**Agent Process**:
1. **Tool**: PythonCodeBuilder
2. **Code**:
   ```python
   import pandas as pd
   df = pd.read_csv('housing_prices.csv')
   print(df.head())
   print(f"\nDataset shape: {df.shape}")
   print(f"\nMissing values:\n{df.isnull().sum()}")
   ```
3. **Result**: Data preview and summary

#### Query 2: "Build a linear regression model to predict house prices"

**Agent Process**:
1. **Tool**: PythonCodeBuilder
2. **Code**:
   ```python
   from sklearn.model_selection import train_test_split
   from sklearn.linear_model import LinearRegression
   from sklearn.metrics import mean_squared_error, r2_score
   import pandas as pd
   
   # Prepare data
   X = df[['bedrooms', 'bathrooms', 'sqft', 'year_built']]
   y = df['price']
   
   # Split data
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
   # Train model
   model = LinearRegression()
   model.fit(X_train, y_train)
   
   # Evaluate
   y_pred = model.predict(X_test)
   mse = mean_squared_error(y_test, y_pred)
   r2 = r2_score(y_test, y_pred)
   
   print(f"Model Performance:")
   print(f"R² Score: {r2:.4f}")
   print(f"RMSE: ${(mse**0.5):,.2f}")
   print(f"\nCoefficients:")
   for feature, coef in zip(X.columns, model.coef_):
       print(f"  {feature}: ${coef:,.2f}")
   ```
3. **Execution**: Trains and evaluates model
4. **Result**: Model performance metrics and coefficients

#### Query 3: "Visualize the predicted vs actual prices"

**Agent Process**:
1. **Tool**: EchartsVisualization
2. **Code**:
   ```python
   import json
   chart_config = {
       "title": {"text": "Predicted vs Actual House Prices"},
       "xAxis": {"type": "value", "name": "Actual Price"},
       "yAxis": {"type": "value", "name": "Predicted Price"},
       "series": [{
           "type": "scatter",
           "data": [[actual, pred] for actual, pred in zip(y_test, y_pred)],
           "symbolSize": 8
       }]
   }
   print(json.dumps(chart_config))
   ```
3. **Result**: Scatter plot visualization

---

## Technical Implementation

### Agent Architecture (ReAct Pattern)

The Data Agent implements the **ReAct (Reasoning + Acting)** pattern:

```
┌─────────────────────────────────────────┐
│           User Query                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Thought: Analyze Intent            │
│  "User wants sales analysis. Need to:   │
│   1. Load data                          │
│   2. Filter by date                     │
│   3. Aggregate by product               │
│   4. Sort and display top 5"            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Action: Select Tool                 │
│  Tool: PythonCodeBuilder                │
│  Input: "Load sales data and find..."    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Observation: Tool Result            │
│  Code executed successfully              │
│  Result: Top 5 products displayed        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Thought: Result Complete           │
│  "I have the answer. Can provide final   │
│   response to user."                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Final Answer                       │
│  "Here are the top 5 products..."       │
└─────────────────────────────────────────┘
```

### Code Execution Flow

```
┌─────────────────────────────────────────┐
│   Generated Python Code                  │
│   import pandas as pd                    │
│   df = pd.read_csv('data.csv')          │
│   ...                                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   IPython Kernel                         │
│   - Parses code                          │
│   - Executes line by line                │
│   - Captures output                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Execution Result                       │
│   {                                      │
│     "success": true,                    │
│     "stdout": "...",                    │
│     "result": DataFrame,                 │
│     "variables": {...}                   │
│   }                                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Result Processing                      │
│   - Convert DataFrame to JSON            │
│   - Format for display                 │
│   - Add metadata                         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Stream to Frontend                     │
│   - Real-time updates                    │
│   - Code display                         │
│   - Results rendering                    │
└─────────────────────────────────────────┘
```

### Memory Management

**Token-Aware Truncation**:
- Maximum context: 3500 tokens
- Conversation history prioritized
- Older messages truncated if needed
- Tool results summarized

**Variable Persistence**:
- Python variables stored in kernel
- Available across queries
- Automatic cleanup on session end

**Conversation Storage**:
- MongoDB: Persistent storage
- Redis: Session cache
- File system: Uploaded data files

---

## Data Flow Architecture

### Request Flow

```
1. User Input
   │
   ├─→ Frontend (Next.js)
   │   ├─→ Validates input
   │   ├─→ Formats request
   │   └─→ Sends HTTP POST
   │
   ├─→ Backend API (Flask)
   │   ├─→ Authenticates user
   │   ├─→ Loads conversation history
   │   ├─→ Loads data files
   │   └─→ Creates agent executor
   │
   ├─→ Agent Executor (LangChain)
   │   ├─→ LLM analyzes query
   │   ├─→ Selects tool
   │   ├─→ Generates code/query
   │   └─→ Executes tool
   │
   ├─→ Code Executor (IPython)
   │   ├─→ Executes code
   │   ├─→ Captures output
   │   └─→ Returns results
   │
   └─→ Response Processing
       ├─→ Formats results
       ├─→ Streams to frontend
       └─→ Updates memory
```

### Data Storage Flow

```
Uploaded Files
   │
   ├─→ File System Storage
   │   └─→ /backend/data/
   │
   ├─→ Metadata → MongoDB
   │   └─→ files collection
   │
   └─→ Data Models
       └─→ TableDataModel/DatabaseDataModel

Conversation Data
   │
   ├─→ Messages → MongoDB
   │   └─→ messages collection
   │
   ├─→ Conversations → MongoDB
   │   └─→ conversations collection
   │
   └─→ Context → Redis
       └─→ Session cache
```

---

## Security and Execution Modes

### Code Execution Modes

#### 1. Local Mode (Default)
- **Description**: Code executes directly on server
- **Use Case**: Development, trusted environments
- **Pros**: Fast, simple setup
- **Cons**: Security risks, resource limits

#### 2. Docker Mode (Production)
- **Description**: Code executes in isolated containers
- **Use Case**: Production, untrusted users
- **Pros**: Security isolation, resource limits
- **Cons**: Slightly slower, requires Docker

**Configuration**:
```bash
export CODE_EXECUTION_MODE=docker
```

### Security Measures

1. **Code Validation**:
   - Blocks dangerous operations (file deletion, system calls)
   - Limits execution time
   - Memory constraints

2. **Sandboxing** (Docker mode):
   - Isolated containers
   - Network restrictions
   - File system isolation

3. **Input Sanitization**:
   - SQL injection prevention
   - Code injection prevention
   - File upload validation

---

## Use Cases

### 1. Business Intelligence
- **Scenario**: Non-technical users need data insights
- **Example**: "Show me sales trends for the last quarter"
- **Benefit**: No SQL/Python knowledge required

### 2. Data Exploration
- **Scenario**: Analysts exploring new datasets
- **Example**: "What's the distribution of customer ages?"
- **Benefit**: Rapid iteration, interactive exploration

### 3. Ad-hoc Reporting
- **Scenario**: One-off analysis requests
- **Example**: "Which products had the highest return rate?"
- **Benefit**: No need to build permanent dashboards

### 4. Data Cleaning
- **Scenario**: Preparing data for analysis
- **Example**: "Remove duplicates and fill missing values"
- **Benefit**: Conversational data preparation

### 5. Predictive Analytics
- **Scenario**: Building ML models
- **Example**: "Build a model to predict customer churn"
- **Benefit**: End-to-end ML workflow in natural language

### 6. Database Querying
- **Scenario**: Querying production databases
- **Example**: "Find all customers who haven't ordered in 6 months"
- **Benefit**: Natural language SQL generation

---

## Technical Specifications

### Performance Characteristics

- **Response Time**: 2-10 seconds (depending on query complexity)
- **Code Execution**: Real-time streaming
- **Concurrent Users**: Supports multiple sessions
- **Memory Usage**: ~500MB per active session
- **Database**: MongoDB for persistence, Redis for caching

### Scalability

- **Horizontal Scaling**: Stateless backend, can scale horizontally
- **Database**: MongoDB sharding support
- **Caching**: Redis cluster support
- **Load Balancing**: Compatible with standard load balancers

### Limitations

1. **Code Execution**: Limited to Python and SQL
2. **File Size**: Large files (>100MB) may cause performance issues
3. **Complex Queries**: Very complex queries may timeout
4. **LLM Dependency**: Requires API access to LLM services

---

## Conclusion

Data Agent represents a paradigm shift in data analysis tools, combining the flexibility of code-based analysis with the accessibility of natural language interfaces. By leveraging advanced LLMs and code execution capabilities, it enables users of all technical levels to perform sophisticated data analysis tasks through simple conversations.

The architecture is designed for:
- **Flexibility**: Supports multiple data sources and analysis types
- **Scalability**: Can handle multiple users and large datasets
- **Security**: Sandboxed execution for production use
- **Extensibility**: Easy to add new tools and capabilities

For technical managers, Data Agent offers:
- Reduced dependency on data engineering teams
- Faster time-to-insight for business users
- Self-service analytics capabilities
- Cost-effective alternative to traditional BI tools

---

## Appendix: Key Files and Locations

- **Agent Core**: `real_agents/data_agent/copilot.py`
- **Code Executors**: `real_agents/data_agent/executors/`
- **API Endpoints**: `backend/api/chat.py`
- **Frontend Chat**: `frontend/components/Chat/Chat.tsx`
- **System Prompts**: `real_agents/data_agent/python/system_prompt.py`
- **Data Models**: `real_agents/adapters/data_model/`

---

*Document Version: 1.0*  
*Last Updated: December 2024*

