# Code Assist – Sandboxed AI Coding Agent

Code Assist is a lightweight, end-to-end AI coding agent that automates code edits in a GitHub repository based on user instructions. It clones the target repository, interprets the prompt using a large language model (LLM), identifies relevant files, applies structured edits, commits the changes, and opens a pull request – all within a sandboxed environment.

---

## Key Features

- Clone public or private GitHub repositories
- Use prompt chaining or finite-state logic for task decomposition
- Identify affected files and functions using natural language reasoning
- Apply code edits (insert, replace, delete) using structured plans
- Generate and commit code changes with meaningful messages
- Push changes to a new branch and create pull requests automatically
- Stream real-time progress updates to the frontend (via SSE)

---

## System Architecture Flow

```plaintext
                          +------------------+
                          |   User Request   |
                          | (repo + prompt)  |
                          +--------+---------+
                                   |
                                   v
                          +--------+---------+
                          |  Clone Git Repo  |
                          +--------+---------+
                                   |
                                   v
                          +--------+---------+
                          |  Prompt Chain /  |
                          |  FSM Task Agent  |
                          +--------+---------+
                                   |
                                   v
                          +--------+---------+
                          |   Analyze Files  |
                          +--------+---------+
                                   |
                                   v
                          +--------+---------+
                          |   Apply Edits    |
                          | (edit_ops.py)    |
                          +--------+---------+
                                   |
                                   v
                          +--------+---------+
                          | Commit + Push PR |
                          +--------+---------+
                                   |
                                   v
                          +--------+---------+
                          | Emit PR URL      |
                          +------------------+
````

---

## Project Structure

```
code-assist/
├── app/
│   ├── agents/
│   │   ├── prompt_chain.py      # Handles multi-step reasoning via LLM
│   │   ├── apply_rules.py       # Applies logic for different phases
│   │   ├── edit_ops.py          # Applies insert/replace/delete edits
│   │   ├── llm_utils.py         # Wrapper for OpenAI/Groq calls
│   │   └── utils.py             # File I/O and helper utilities
│   ├── api/
│   │   └── code.py              # FastAPI SSE endpoint to trigger agent
│   ├── github/
│   │   └── pr_utils.py          # GitHub repo cloning, commit, PR creation
│   ├── main.py                  # FastAPI entrypoint
│   ├── config.py                # Settings and environment loading
│   └── models.py                # Pydantic models
├── .env                         # Environment variables (tokens, keys)
├── requirements.txt             # Python dependencies
├── README.md
└── tests/                       # (Optional) unit tests and assertions
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/code-assist.git
cd code-assist
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_key
```

---

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API server will be available at `http://127.0.0.1:8000`.

---

## API Usage

### Endpoint: `POST /api/code/apply`

#### Request Body

```json
{
  "repo_url": "https://github.com/user/repo",
  "task_prompt": "Convert the legacy login endpoint to use async syntax.",
  "model": "gpt-4o"
}
```

#### Response

* Server-Sent Event (SSE) stream with real-time progress messages
* Final message includes a GitHub Pull Request URL with changes applied

---

## Internal Workflow

1. **Clone Repository:**
   GitHub repo is cloned to a temporary directory.

2. **Prompt Interpretation (Phase 3):**
   LLM-based prompt chaining identifies task goals, affected files, and required modifications.

3. **Code Edit Planning and Application:**
   Edits (insert/replace/delete) are generated and applied using `edit_ops.py`.

4. **Git Commit and PR (Phase 4):**
   Changes are committed on a new branch, pushed, and a pull request is created.

---

## Example Usage (cURL)

```bash
curl -N -X POST http://localhost:8000/api/code/apply \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/your-user/repo", "task_prompt": "Update API routes to use FastAPI"}'
```

---

## Supported LLMs

* OpenAI (`gpt-4o`, `gpt-4`, `gpt-3.5-turbo`)
* Groq (LLama3 support)
* Anthropic / OpenRouter (via `llm_utils.py`)

To add custom providers, extend `llm_utils.py`.

---

## Testing

```bash
pytest tests/
```

---

## Development Roadmap

* [x] Prompt chaining and task planning
* [x] Code editing using structured edit operations
* [x] Git commit and pull request automation
* [x] SSE streaming output
* [ ] Frontend UI for task input and PR viewing
* [ ] Unit tests and safety checks
* [ ] Secure sandboxing of generated code
* [ ] Diff visualization and approval UI

---

## Contributing

To contribute, fork the repository, create a feature branch, and open a pull request. For major changes, please open an issue first to discuss the proposal.

---

## License

This project is licensed under the MIT License.

---

## Author

**Sanchita Kiran**
