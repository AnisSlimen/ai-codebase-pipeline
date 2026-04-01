# AI Codebase Architect Plugin - Multi-Agent Pipeline

## Project Overview
This is an automated multi-agent pipeline that builds the **AI Codebase Architect Plugin** — a VS Code extension that analyzes Java Spring Boot codebases, detects architectural violations, visualizes dependency graphs, and answers natural language questions about the code using RAG.

The pipeline uses the Anthropic Claude API to run 6 specialized agents sequentially/in parallel, each producing a large artifact that feeds into the next.

## Repository
https://github.com/AnisSlimen/ai-codebase-pipeline (branch: master)

## Project Structure
ai-codebase-pipeline/
├── orchestrator.py # Main entry point - runs the full pipeline
├── requirements.txt # anthropic>=0.25.0, python-dotenv>=1.0.0
├── .env.example # Copy to .env and add ANTHROPIC_API_KEY
├── agents/
│ ├── base_agent.py # Shared: get_client, run_agent, load/save artifacts
│ ├── arch_agent.py # Phase 1: Solution Architect
│ ├── cli_agent.py # Phase 2a: Static Analysis CLI (Java/Maven)
│ ├── backend_agent.py # Phase 2b: Spring Boot Backend
│ ├── ai_agent.py # Phase 3: AI/RAG module
│ ├── plugin_agent.py # Phase 4: VS Code TypeScript extension
│ └── qa_agent.py # Phase 5: Integration & QA
├── prompts/
│ ├── arch_prompt.txt # AGENT-ARCH system prompt (fill in)
│ ├── cli_prompt.txt # AGENT-CLI system prompt (fill in)
│ ├── backend_prompt.txt # AGENT-BACKEND system prompt (fill in)
│ ├── ai_prompt.txt # AGENT-AI system prompt (fill in)
│ ├── plugin_prompt.txt # AGENT-PLUGIN system prompt (fill in)
│ └── qa_prompt.txt # AGENT-QA system prompt (fill in)
├── artifacts/ # Pipeline outputs saved here (gitignored at runtime)
└── logs/ # pipeline.log written here


## Pipeline Phases
| Phase | Agent | Input | Output |
|-------|-------|-------|--------|
| 1 | AGENT-ARCH | none | `arch_output.txt` (OpenAPI spec, DB schema, ADRs) |
| 2 | AGENT-CLI + AGENT-BACKEND | arch_output.txt | `cli_output.txt`, `backend_output.txt` (run in parallel) |
| 3 | AGENT-AI | arch + cli + backend | `ai_output.txt` (RAG/embedding module) |
| 4 | AGENT-PLUGIN | arch + backend + ai | `plugin_output.txt` (VS Code extension) |
| 5 | AGENT-QA | all artifacts | `qa_output.txt` (tests, DoD checklist) |

## Setup & Running
```bash
cp .env.example .env          # Add your ANTHROPIC_API_KEY
pip install -r requirements.txt
python orchestrator.py

The pipeline is idempotent — re-running skips agents whose output already exists in artifacts/.

What Still Needs To Be Done
 Paste actual system prompts into each prompts/*.txt file (replace placeholder text)
 Run the pipeline end-to-end
 Review generated artifacts in artifacts/
Key Design Decisions
Model: claude-sonnet-4-5 (configurable per agent via model= param in run_agent)
Max tokens per agent: 8096
Phase 2 agents run in parallel via ThreadPoolExecutor
Artifacts are plain .txt files passed as context to downstream agents
Logs written to logs/pipeline.log