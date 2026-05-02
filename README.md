
# Agentic Research Assistant

A multi-agent system built with **LangGraph** and **Streamlit** designed to automate deep-dive research workflows. This project demonstrates modular AI orchestration, stateful memory management, and human-in-the-loop validation.

## 🏗️ Technical Architecture

The system utilizes a directed acyclic graph (DAG) to coordinate three specialized agents:

*   **Planner Agent**: Decomposes the research topic into a structured 3-point outline.
*   **Researcher Agent**: Executes the deep-dive content generation based on the approved plan.
*   **Reviewer Agent**: Performs self-correction and quality checks on the final output.

### Key Engineering Implementation
*   **Stateful Persistence**: Implements `MemorySaver` to maintain thread-specific history across user sessions[cite: 1].
*   **Human-in-the-Loop (HITL)**: Uses graph interruptions to require user approval before moving from planning to execution.
*   **Modular Design**: Separates concerns into distinct modules: `/agents`, `/graph`, and `/state`.
*   **Asynchronous Orchestration**: Leverages LangGraph’s streaming capabilities to provide real-time UI updates during long-running research tasks.

## 📺 App Preview

<img width="800" height="391" alt="2026-05-0219-45-27-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/8d545760-0f8f-4a41-8839-c87dff01ede7" />


## 🛠️ Tech Stack

*   **Frameworks**: LangGraph, LangChain
*   **LLM**: Gemini 3.1 Flash-Lite Preview
*   **Interface**: Streamlit
*   **Export**: FPDF (Custom Markdown-to-PDF engine)

## 🚀 Quick Start

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/althaffazil/multiagent-research-assistant
    cd multiagent-research-assistant
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure environment**:
    Create a `.env` file and add your `GOOGLE_API_KEY`.

4.  **Run**:
    ```bash
    streamlit run app.py
    ```

## 📜 Research History
The application features a persistent history sidebar that allows users to reload previous research threads and re-export reports without re-running the agentic workflow. This is managed by mapping unique `thread_id` values to local session storage.

