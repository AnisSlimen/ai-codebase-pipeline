"""
orchestrator.py — Main entry point for the AI Codebase Architect Pipeline.

Pipeline phases:
  Phase 1  : AGENT-ARCH  (sequential)
  Phase 2  : AGENT-CLI + AGENT-BACKEND  (parallel via ThreadPoolExecutor)
  Phase 3  : AGENT-AI    (sequential, needs Phase 2 outputs)
  Phase 4  : AGENT-PLUGIN (sequential, needs Phase 3 output)
  Phase 5  : AGENT-QA    (sequential, needs all prior outputs)

The pipeline is idempotent: if an artifact already exists in artifacts/,
the corresponding agent is skipped.

Usage:
    python orchestrator.py
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Load .env file if present (sets ANTHROPIC_API_KEY)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on shell env

# Add project root to path so `agents` package is importable
sys.path.insert(0, str(Path(__file__).parent))

from agents.base_agent import logger
from agents import arch_agent, cli_agent, backend_agent, ai_agent, plugin_agent, qa_agent


def run_phase_1() -> None:
    """Phase 1: Solution Architect (sequential)."""
    print("\n" + "=" * 70)
    print("PHASE 1 — AGENT-ARCH: Solution Architect")
    print("=" * 70)
    arch_agent.run()


def run_phase_2() -> None:
    """Phase 2: CLI + Backend in parallel."""
    print("\n" + "=" * 70)
    print("PHASE 2 — AGENT-CLI + AGENT-BACKEND (parallel)")
    print("=" * 70)

    tasks = {
        "AGENT-CLI": cli_agent.run,
        "AGENT-BACKEND": backend_agent.run,
    }

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(fn): name for name, fn in tasks.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                future.result()
                logger.info("[%s] Completed successfully", name)
            except Exception as exc:
                logger.error("[%s] Failed: %s", name, exc)
                raise


def run_phase_3() -> None:
    """Phase 3: AI/RAG module (sequential)."""
    print("\n" + "=" * 70)
    print("PHASE 3 — AGENT-AI: RAG Module")
    print("=" * 70)
    ai_agent.run()


def run_phase_4() -> None:
    """Phase 4: VS Code Extension (sequential)."""
    print("\n" + "=" * 70)
    print("PHASE 4 — AGENT-PLUGIN: VS Code Extension")
    print("=" * 70)
    plugin_agent.run()


def run_phase_5() -> None:
    """Phase 5: Integration & QA (sequential)."""
    print("\n" + "=" * 70)
    print("PHASE 5 — AGENT-QA: Integration & QA")
    print("=" * 70)
    qa_agent.run()


def main() -> None:
    start = time.time()
    logger.info("Pipeline starting")

    try:
        run_phase_1()
        run_phase_2()
        run_phase_3()
        run_phase_4()
        run_phase_5()
    except Exception as exc:
        logger.error("Pipeline failed: %s", exc)
        sys.exit(1)

    elapsed = time.time() - start
    logger.info("Pipeline complete in %.1f seconds", elapsed)

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print(f"Elapsed: {elapsed:.1f}s")
    print("Artifacts saved to: artifacts/")
    print("=" * 70)


if __name__ == "__main__":
    main()
