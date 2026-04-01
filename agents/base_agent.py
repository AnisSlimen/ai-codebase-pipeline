"""
base_agent.py — Shared utilities for all pipeline agents.

Provides:
  - get_client()        : returns a configured Anthropic client
  - run_agent()         : calls the API with streaming, returns full text
  - load_artifact()     : reads a text artifact from artifacts/
  - save_artifact()     : writes a text artifact to artifacts/
  - artifact_exists()   : returns True if an artifact already exists (idempotency)
"""

import logging
import os
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent.parent
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
LOGS_DIR = ROOT_DIR / "logs"

ARTIFACTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "pipeline.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("pipeline")


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------
def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client.  ANTHROPIC_API_KEY must be set in the env."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set.  Copy .env.example to .env and add your key."
        )
    return anthropic.Anthropic(api_key=api_key)


# ---------------------------------------------------------------------------
# Core runner
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_MAX_TOKENS = 8096


def run_agent(
    *,
    agent_name: str,
    system_prompt: str,
    user_message: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """
    Run a single agent call against the Claude API using streaming.

    Parameters
    ----------
    agent_name   : Human-readable label used in logs.
    system_prompt: The agent's role / instructions.
    user_message : The user turn (may include injected artifacts).
    model        : Claude model ID.
    max_tokens   : Hard ceiling on output tokens.

    Returns
    -------
    The full text response as a string.
    """
    client = get_client()
    logger.info("[%s] Starting — model=%s max_tokens=%d", agent_name, model, max_tokens)

    full_text = ""

    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text_chunk in stream.text_stream:
            full_text += text_chunk
            print(text_chunk, end="", flush=True)

        final = stream.get_final_message()

    print()  # newline after streamed output
    logger.info(
        "[%s] Done — input_tokens=%d output_tokens=%d",
        agent_name,
        final.usage.input_tokens,
        final.usage.output_tokens,
    )
    return full_text


# ---------------------------------------------------------------------------
# Artifact helpers
# ---------------------------------------------------------------------------
def artifact_path(filename: str) -> Path:
    return ARTIFACTS_DIR / filename


def artifact_exists(filename: str) -> bool:
    return artifact_path(filename).exists()


def save_artifact(filename: str, content: str) -> None:
    path = artifact_path(filename)
    path.write_text(content, encoding="utf-8")
    logger.info("Saved artifact: %s (%d chars)", path.name, len(content))


def load_artifact(filename: str) -> str:
    path = artifact_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Artifact not found: {path}")
    return path.read_text(encoding="utf-8")


def load_prompt(prompt_filename: str) -> str:
    """Load a system prompt from prompts/."""
    path = ROOT_DIR / "prompts" / prompt_filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")
