# Multi-Agent System for Query Processing

This project implements a multi-agent system designed to interpret user queries, break them down into actionable steps, and execute them using a suite of tools. The system is built to be robust, featuring tool execution with caching, retries, and timeouts. Every action is logged in a structured JSON format for traceability and analysis.

This implementation directly follows the technical specification provided for the assignment.

## 1. Features

* **Multi-Agent Architecture**: A coordinator agent that uses a planner and tool executors.
* **Step-Based Planning**: Deconstructs user queries into a sequence of tool calls.
* **Tool Suite**: Includes a Retriever, Policy Lookup, a safe Calculator, and String Tools.
* **Robust Tool Execution**: The `Executor` layer provides:
  * **Caching**: In-memory TTL caching to avoid re-running expensive tool calls.
  * **Retries**: Exponential backoff strategy to handle transient failures.
  * **Timeouts**: Prevents long-running tool calls from blocking the system.
* **Structured JSON Logging**: Detailed logs for every stage of the query processing lifecycle, from planning to final answer generation.
* **BM25 Retriever**: Utilizes a `rank_bm25` retriever for efficient and effective text retrieval from the knowledge base.

## 2. Project Structure

```
/
├── agent/
│   ├── agent.py            # Main orchestrator
│   ├── planner.py
│   ├── executor.py
│   ├── logger.py
│   ├── kb_loader.py
│   └── tools/
│       ├── __init__.py
│       ├── retriever.py
│       ├── policy_lookup.py
│       ├── calculator.py
│       └── string_tools.py
├── tests/
│   ├── test_executor.py
│   └── test_tools.py
├── knowledgeBase.txt
├── logs.json               # Sample run logs for 5 queries
├── requirements.txt
└── README.md
```

## 3. Setup and Installation

The project is built with Python 3.10+.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/surya-0704/llumoAgent
    cd llumoAgent
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 4. How to Run

You can run the agent directly from the command line.

**Run with a specific query:**
```bash
python -m agent.agent --query "What is the policy for refunds? And calculate 10% of 2450."
```

**Run the default example query:**
```bash
python -m agent.agent
```

The agent will process the query, print the final answer to the console, and append a detailed execution log to `logs.json`.

## 5. System Design Choices

### Retriever
The system uses a **BM25 (Best Matching 25)** retrieval model.

* **Rationale**: BM25 is a keyword-based retrieval algorithm that works exceptionally well for its simplicity and speed. It doesn't require expensive embedding generation or vector databases, making it a perfect lightweight choice for the provided `knowledgeBase.txt`. It's highly effective for matching queries that contain keywords present in the documents. For a more advanced system dealing with semantic meaning, a `sentence-transformers` based model with a FAISS index would be the next logical step.

### Planner
The planner is **rule-based**.

* **Rationale**: The planner uses a series of regular expressions and keyword checks to map user queries to a sequence of tool calls. This approach is deterministic, fast, and easy to test and debug. For the defined scope of tools, a rule-based planner is sufficient and avoids the complexity, cost, and non-determinism of an LLM-based planner.

### Caching, Retries, and Timeouts

-   **Caching**: An in-memory `cachetools.TTLCache` is used. The default TTL is 300 seconds. This is configurable in the `Executor`.
-   **Retries**: The system uses an exponential backoff algorithm with jitter to space out retries. Default max retries is 2.
-   **Timeouts**: Tool calls are executed in a separate thread to enforce timeouts without blocking the main agent loop. Default timeouts are aggressive (e.g., 2000ms for retriever) to ensure responsiveness.

## 6. Logging

All agent activities are logged to `logs.json`. Each query gets a unique `query_id`, and the log entry contains the plan, a timeline of events (tool calls, results, errors), and the final answer. This structured format is ideal for debugging and analysis.

## 7. How to Run Tests

The project uses `pytest` for unit testing critical components.

To run the tests, execute the following command from the root directory:
```bash
pytest
```

The tests cover:
-   **Executor**: Caching, retry, and timeout logic.
-   **Tools**: Correctness of the Calculator, StringTools, and Retriever.

## 8. Assumptions & Limitations

-   The system assumes the `knowledgeBase.txt` file exists in the root directory.
-   The Planner is designed for relatively simple queries that map directly to the available tools. It cannot handle highly complex, multi-step reasoning that doesn't fit its rules.
-   Caching is in-memory and therefore not persistent across agent restarts. For a production system, a distributed cache like Redis would be more appropriate.
-   The Critic/Validator logic is currently simple (checking for `success: false`). A more advanced implementation would inspect tool output for relevance and correctness.a
