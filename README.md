🤖 AI Advance COO Agent

An AI-powered Chief Operating Officer (COO) that understands natural-language requests and uses Gemini tool calling to select and execute specialized tools for real-world tasks.

The system combines FastAPI, Gemini, SQLModel, Google APIs, and a registry-based tool architecture to create an extensible agent that can interact with external services instead of simply generating text.

Core idea: Let the LLM decide which capability is required, while deterministic Python tools handle the actual execution.

🚀 What This Project Does

The AI COO can understand requests such as:

"What's the weather in Karachi?"

"Send an email to Ali about tomorrow's meeting."

"Schedule a meeting tomorrow at 10 AM."

"Give me the latest technology news."

"Remember that Ahmed's email is ahmed@example.com."

Based on the request, Gemini can select the appropriate registered tool and provide the arguments required for execution.

Current capabilities
📧 Send emails through Gmail
📅 Create calendar events
👥 Manage contacts
🧠 Store and retrieve memory
🎯 Manage goals
🌤️ Retrieve weather information
📰 Retrieve news
🤖 Select and orchestrate tools using Gemini tool calling
🔌 Extensible tool registry and executor architecture
🏗️ Architecture
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │    API Layer     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   COO Agent      │
                         │  Orchestrator    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Gemini / Planner │
                         │  Tool Calling    │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
               Tool Registry  Tool Executor   Memory
                    │             │             │
          ┌─────────┼─────────┐    │        SQLModel
          │         │         │    │
          ▼         ▼         ▼    ▼
       Gmail    Calendar   Weather  News
          │         │         │     │
          └─────────┴─────────┴─────┘
                    │
                    ▼
             External APIs
Request flow
User Request
     │
     ▼
 FastAPI
     │
     ▼
 COO Orchestrator
     │
     ▼
 Gemini
     │
     ├── Select Tool
     │
     ▼
 Tool Executor
     │
     ▼
 Registered Python Tool
     │
     ▼
 External API / Database
     │
     ▼
 Tool Result
     │
     ▼
 Gemini
     │
     ▼
 Final Response
🧠 Why Gemini Tool Calling?

A traditional implementation could route every request using hard-coded conditions:

if request_type == "weather":
    weather_tool()

elif request_type == "email":
    gmail_tool()

elif request_type == "calendar":
    calendar_tool()

This becomes difficult to maintain as the number of capabilities grows.

Instead, this project gives Gemini access to a registry of available tools.

Gemini determines which tool is appropriate and supplies the required arguments.

For example:

User:
What's the weather in Karachi?

        ↓

Gemini

        ↓

weather_tool(
    city="Karachi"
)

        ↓

Weather API

        ↓

Weather Result

        ↓

Gemini

        ↓

Final Response

This creates a clear separation between:

Layer	Responsibility
Gemini	Reasoning and tool selection
COO	Orchestration
Tool Registry	Available capabilities
Tool Executor	Tool execution
Python Tools	Deterministic operations
SQLModel	Persistent application state
External APIs	Real-world actions/data
🔧 Tool Architecture

Tools are located under:

app/tools/
Base Tool

app/tools/base.py

Provides the common interface used by the system's tools.

Conceptually:

class BaseTool:
    def name(self):
        ...

    def run(self, input: dict):
        ...

This allows different capabilities to follow a consistent interface.

Tool Registry

app/tools/registry.py

The registry maintains the available tools in one place.

Tool Registry
     │
     ├── Gmail
     ├── Calendar
     ├── Weather
     ├── News
     └── Other Tools

Adding a new capability primarily involves implementing the tool and registering it rather than rewriting the core orchestration logic.

Tool Executor

app/tools/executor.py

The executor receives the tool selected by Gemini and invokes the corresponding Python implementation.

Gemini
   │
   │ Tool Call
   ▼
Tool Executor
   │
   ▼
Registered Tool
   │
   ▼
Tool Result

This separation keeps LLM decision-making separate from deterministic application execution.

📧 Gmail Integration

app/tools/gmail.py

The Gmail tool integrates with the Gmail API using Google's OAuth 2.0 authentication flow.

Current capability:

Send emails through Gmail

Example request:

Send an email to Ali saying the meeting has been moved to tomorrow.

The agent can identify the Gmail tool, generate the required arguments, and execute the email operation.

📅 Google Calendar Integration

app/tools/calendar.py

The Calendar tool integrates with Google Calendar.

Example:

Schedule a meeting tomorrow at 10 AM.

The agent identifies the calendar capability and passes the required event information to the tool.

🌤️ Weather Tool

app/tools/weather.py

Retrieves weather information through an external weather API.

Example:

What's the weather in Islamabad?

Gemini can generate a tool call such as:

{
  "city": "Islamabad"
}

The tool then retrieves the corresponding weather data.

📰 News Tool

app/tools/news.py

Retrieves current news based on a requested topic or category.

Example:

Give me the latest AI and technology news.

The news tool retrieves the relevant information and returns it to the agent.

🧠 Memory & State

The memory layer is located under:

app/memory/

It currently contains:

app/memory/
├── db.py
├── memory.py
└── models.py

SQLModel models are used for persistent application state.

Contact

Stores contact information such as:

name
email
Memory

Stores information such as:

type
content
Goal

Tracks user objectives and their status.

Example:

Goal:
Learn AI Agent Development

Status:
active
🔄 Multi-Tool Workflow

One of the interesting aspects of the architecture is that a single natural-language request can require multiple capabilities.

For example:

Find Ali's email and send him an email
about tomorrow's meeting.

A possible execution flow is:

                  Gemini
                    │
                    ▼
              get_contact()
                    │
                    ▼
              Contact Result
                    │
                    ▼
              send_email()
                    │
                    ▼
                Gmail API
                    │
                    ▼
              Final Response

This demonstrates how tool calling can be used to coordinate multiple deterministic operations from a single natural-language request.

📁 Project Structure
AI-Advance-COO-Agent/
│
├── app/
│   ├── agents/
│   │   └── planner_agent.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── gemini.py
│   │
│   ├── memory/
│   │   ├── db.py
│   │   ├── memory.py
│   │   └── models.py
│   │
│   ├── orchestrator/
│   │   └── coo.py
│   │
│   └── tools/
│       ├── base.py
│       ├── calendar.py
│       ├── executor.py
│       ├── gmail.py
│       ├── news.py
│       ├── registry.py
│       └── weather.py
│
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock

Runtime files such as OAuth tokens, .env, credentials, virtual environments, and __pycache__ should remain outside version control.

🛠️ Tech Stack
Technology	Purpose
Python	Core application development
FastAPI	API layer
Gemini	LLM reasoning and tool calling
SQLModel	Database models and persistence
Gmail API	Email operations
Google Calendar API	Calendar operations
Weather API	Weather retrieval
News API	News retrieval
OAuth 2.0	Google service authentication
uv	Python dependency/environment management
⚙️ Setup
1. Clone the repository
git clone https://github.com/Shazil91/AI-Advance-COO-Agent.git

cd AI-Advance-COO-Agent
2. Create the environment

Using uv:

uv sync

Or using Python's built-in virtual environment:

Windows
python -m venv .venv

.venv\Scripts\activate
Linux/macOS
python3 -m venv .venv

source .venv/bin/activate
🔐 Environment Variables

Create a .env file locally.

Example:

GEMINI_API_KEY=your_gemini_api_key
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key

Add any additional variables required by the tools you enable.

⚠️ Security

Never commit secrets or OAuth credentials to GitHub.

Your .gitignore should include:

.env
credentials.json
token.json
token_calendar.json
.venv/
__pycache__/
*.pyc

OAuth credentials and generated tokens should always remain local.

🔑 Google OAuth Setup

The Gmail and Calendar integrations use Google's OAuth authentication.

You need to:

Create a project in Google Cloud.
Enable the Gmail API.
Enable the Google Calendar API.
Configure OAuth consent.
Create OAuth client credentials.
Download the credentials file.
Store it locally as:
credentials.json

The first authentication generates local token files.

These files should never be committed to the repository.

▶️ Run the Application

Start the FastAPI server:

uv run uvicorn main:app --reload

Or, if your environment is already activated:

uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs
🧪 Example Requests

Examples of natural-language requests the COO can handle:

What's the weather in Karachi?
Give me the latest technology news.
Send an email to Ahmed about tomorrow's meeting.
Schedule a meeting tomorrow at 10 AM.
Remember that Ali's email is ali@gmail.com.
Find Ali's email and send him an email about tomorrow's meeting.
🎯 Design Principles
1. LLM as the Decision Layer

Gemini determines which registered capability is required.

2. Deterministic Tool Execution

Actual external API calls and application operations are performed by Python tools.

3. Registry-Based Architecture

Tools are registered centrally, making the system easier to extend.

4. Separation of Concerns

The system separates:

API
 ↓
Orchestration
 ↓
LLM / Planning
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
External Services
5. Persistent Application State

SQLModel-backed models provide structured persistence for contacts, memories, and goals.

🔮 Future Improvements

Potential future improvements include:

Persistent conversation memory
PostgreSQL production deployment
Redis caching
More robust multi-step tool execution
Human approval for sensitive actions
Authentication and authorization
Tool execution logging
Background jobs
Scheduled autonomous tasks
LangGraph-based orchestration
RAG / vector-based memory
Docker deployment
Kubernetes deployment
Monitoring and observability
Web frontend
Voice interface

These are future enhancements, not claims about the current implementation.

💡 Key Engineering Takeaway

The main engineering challenge in this project was not simply connecting an LLM to an API.

It was designing a boundary between:

             LLM
              │
              │ Reasoning
              │ Tool Selection
              ▼
        ┌─────────────┐
        │ Tool System │
        └──────┬──────┘
               │
               │ Deterministic Execution
               ▼
       External Services

The LLM decides what should happen.

The application determines how it happens.

This separation makes the system easier to extend with additional tools while keeping external operations inside deterministic application code.

📌 Project Status

Status: Completed working project

This project is primarily a demonstration of:

Agentic AI architecture
Gemini tool/function calling
LLM-driven tool selection
Tool registry design
Deterministic tool execution
FastAPI AI backends
External API integrations
SQLModel-based persistence
Multi-tool workflows
👨‍💻 Author

Shazil Ali

AI Engineer focused on:

Agentic AI · LLM Applications · RAG · AI Agents · Python · FastAPI · Cloud Engineering

GitHub:

https://github.com/Shazil91
