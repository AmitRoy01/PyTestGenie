# PyTestGenie

PyTestGenie is a web app that generates Python unit tests for user-provided code. It supports two generation modes:

- Pynguin (automatic) — runs the Pynguin test generator in the backend and streams logs back to the frontend while generating tests.
- AI-powered (OpenAI via HuggingFace router) — sends the code to an LLM to generate pytest-style tests.

This README shows how to set up and run the project locally.

**Repository layout**

- `backend/` — Flask backend that runs Pynguin, streams logs (SSE), and exposes an AI test-generation endpoint.
  - `app.py` — main Flask app and streaming task runner
  - `ai_test_generator.py` — AI-based test generation via OpenAI client (HuggingFace router)
  - `requirements.txt` — backend Python dependencies
- `frontend/` — React frontend built with Create React App style structure
  - `src/App.jsx` — main UI (test input, run controls, logs, results)


**Prerequisites**

- Python 3.10+ (or the Python version you use for this project)
- Node.js (LTS) and npm
- (Optional) A HuggingFace API token if you want to use the AI generator


## Setup (Backend)

1. Create and activate a virtual environment (recommended):

```powershell
cd d:\SPL_3_experiment\pynguin_webapp\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Configure environment variables:

- Copy `.env.example` (or create `.env`) and add your HuggingFace token if you plan to use AI generation:

```powershell
copy .env.example .env
# then edit .env and set HF_TOKEN=<your_token>
```

Notes:
- If you don't set `HF_TOKEN`, the AI endpoint will raise an error when called.


## Setup (Frontend)

1. Install frontend dependencies and start the dev server:

```powershell
cd d:\SPL_3_experiment\pynguin_webapp\frontend
npm install
npm start
```

2. The frontend dev server typically runs at `http://localhost:3000/`.


## Running the Backend

Start the Flask backend (from the `backend/` directory):

```powershell
cd d:\SPL_3_experiment\pynguin_webapp\backend
# (activate virtualenv if used)
python app.py
```

The backend default host is `127.0.0.1:5000`.


## How to Use

- Open the frontend in your browser.
- Paste Python code into the textarea.
- Choose a generation mode:
  - "Use Pynguin (Automatic)" — streams generation logs and returns tests once done.
  - "Use AI (OpenAI/HuggingFace)" — sends code to the AI endpoint and returns generated tests directly.
- Click "Generate Tests".
- For Pynguin: watch the live logs panel while the generator runs, and view the generated test code when finished.
- For AI: the generated test code appears when the API returns a response.


## API endpoints (backend)

- `POST /generate-tests` — starts a Pynguin generation task and returns a `task_id`.
- `GET /generate-tests/stream/<task_id>` — Server-Sent Events (SSE) stream for logs/results of a Pynguin task.
- `POST /generate-ai-tests` — synchronous endpoint that returns AI-generated test code (uses `HF_TOKEN`).


## Notes and Security

- `.env` may contain sensitive tokens. Do not commit `.env` to source control. A `.gitignore` is included to exclude common secrets and generated artifacts.
- The in-memory task store (`tasks` in `app.py`) is not persistent. If you restart the backend, in-progress tasks are lost.
- The AI generation uses the HuggingFace router via an OpenAI-compatible client — usage may incur costs and requires a valid token.


## Troubleshooting

- If you see Unicode / encoding errors from subprocess output, ensure `PYTHONIOENCODING` is set to `utf-8` in the environment or in `app.py` the subprocess env is configured accordingly.
- If the frontend can't reach the backend, ensure CORS is enabled and both servers run on the expected ports.


## Contributing

- Make edits on feature branches and open PRs against `main`.
- Keep secrets out of commits — use `.env` and environment variables.


## License

This project does not include a license file by default. Add a `LICENSE` if you wish to distribute the code under a specific license.
