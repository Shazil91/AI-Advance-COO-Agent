🤖 AI Advance COO Agent

An AI-powered Chief Operating Officer (COO) that understands natural-language requests and uses Gemini tool calling to select and execute specialized tools for real-world tasks.

The project demonstrates how an LLM can act as a decision-making layer while deterministic Python tools handle the actual execution.

🚀 What It Can Do
📧 Send emails through Gmail
📅 Create Google Calendar events
👥 Manage contacts
🧠 Store and retrieve memories
🎯 Manage goals
🌤️ Retrieve weather information
📰 Retrieve news
🤖 Dynamically select tools using Gemini tool calling
🔌 Easily extend the system with additional tools
🏗️ Architecture
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         └───────┬───────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │  COO Orchestrator │
                       └─────────┬─────────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │ Gemini / Planner  │
                       │   Tool Calling    │
                       └─────────┬─────────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │   Tool Registry   │
                       └─────────┬─────────┘
                                 │
                                 ▼
                       ┌───────────────────┐
                       │   Tool Executor   │
                       └─────────┬─────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
           Gmail             Calendar         Weather / News
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
                         External Services
🧠 Why Tool Calling?

Instead of building a large routing system with hard-coded conditions such as:

if request_type == "weather":
    weather_tool()

elif request_type == "email":
    gmail_tool()

elif request_type == "calendar":
    calendar_tool()

this system allows Gemini to determine which registered tool is appropriate for the user's request.

For example:

User
 │
 │ "What's the weather in Karachi?"
 ▼
Gemini
 │
 │ Selects weather tool
 ▼
weather_tool(city="Karachi")
 │
 ▼
Weather API
 │
 ▼
Tool Result
 │
 ▼
Gemini
 │
 ▼
Final Response

This creates a clear separation of responsibilities:

Component	Responsibility
Gemini	Reasoning and tool selection
COO Orchestrator	Coordinates the agent workflow
Tool Registry	Maintains available tools
Tool Executor	Executes selected tools
Python Tools	Deterministic operations
SQLModel	Application state and persistence
External APIs	Real-world data and actions
🔄 Multi-Tool Workflow

The agent can handle requests that require more than one tool.

Example:

"Find Ali's email and send him an email
about tomorrow's meeting."

Possible workflow:

Gemini
   │
   ▼
get_contact()
   │
   ▼
Contact Information
   │
   ▼
send_email()
   │
   ▼
Gmail API
   │
   ▼
Final Response

The LLM determines what needs to happen, while the application controls how the operation is executed.

🧩 Tool Architecture

Tools follow a common interface and are registered centrally.

app/
└── tools/
    ├── base.py
    ├── registry.py
    ├── executor.py
    ├── gmail.py
    ├── calendar.py
    ├── weather.py
    └── news.py

Adding a new capability involves implementing the tool and registering it with the tool system rather than adding another large routing branch.

🧠 Memory & Application State

The project uses SQLModel for structured application state.

Current models support areas such as:

Contacts
Memories
Goals
app/
└── memory/
    ├── db.py
    ├── memory.py
    └── models.py
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
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
🛠️ Tech Stack
Technology	Purpose
Python	Core application
FastAPI	Backend/API layer
Gemini	LLM reasoning and tool calling
SQLModel	Database models and persistence
Gmail API	Email integration
Google Calendar API	Calendar integration
Weather API	Weather information
News API	News retrieval
Google OAuth 2.0	Authentication for Google services
uv	Python dependency management
⚙️ Getting Started
1. Clone the repository
git clone https://github.com/Shazil91/AI-Advance-COO-Agent.git

cd AI-Advance-COO-Agent
2. Install dependencies

Using uv:

uv sync

Or create a standard Python virtual environment:

Windows

python -m venv .venv
.venv\Scripts\activate

Linux/macOS

python3 -m venv .venv
source .venv/bin/activate
3. Configure environment variables

Create a local .env file:

GEMINI_API_KEY=your_gemini_api_key
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key

Add any additional credentials required by the integrations you enable.

4. Configure Google APIs

For Gmail and Calendar functionality:

Create a project in Google Cloud.
Enable the Gmail API.
Enable the Google Calendar API.
Configure OAuth consent.
Create OAuth credentials.
Download the credentials file.
Store it locally as credentials.json.

Never commit OAuth credentials or generated tokens to GitHub.

5. Run the application
uv run uvicorn main:app --reload

API:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
🔐 Security

Keep secrets and OAuth files out of version control.

Recommended .gitignore entries:

.env
credentials.json
token.json
token_calendar.json
.venv/
__pycache__/
*.pyc

Never expose API keys, OAuth credentials, access tokens, or other secrets in source code.

💡 Key Engineering Concepts Demonstrated

This project focuses on practical AI engineering concepts including:

Agentic AI architecture
LLM tool/function calling
LLM-driven tool selection
Tool registry design
Deterministic tool execution
Multi-tool workflows
FastAPI-based AI backends
External API integrations
Google OAuth integration
SQLModel-based persistence
Separation of LLM reasoning from application execution

The central design principle is:

LLM
 │
 │ Decides WHAT to do
 ▼
Tool System
 │
 │ Determines HOW to execute it
 ▼
Deterministic Python Code
 │
 ▼
External Service / Database
🔮 Future Improvements

Potential future enhancements include:

Persistent conversation memory
PostgreSQL production deployment
Redis caching
Human approval for sensitive actions
Authentication and authorization
Tool execution logging
Background jobs
Scheduled autonomous tasks
RAG-based memory
Docker deployment
Kubernetes deployment
Monitoring and observability
Web interface
Voice interface
📌 Project Status

Status: Completed working project

This project was built as a practical exploration of Agentic AI, Gemini tool calling, AI orchestration, external API integration, and AI application architecture.

👨‍💻 Author

Shazil Ali

AI Engineer focused on:

Agentic AI · LLM Applications · AI Agents · RAG · Python · FastAPI · Cloud Engineering

GitHub:
https://github.com/Shazil91

⭐ If You Find This Project Useful

Feel free to explore the repository, experiment with the tools, and use the architecture as a starting point for building your own agentic AI applications.
