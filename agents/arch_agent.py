"""
arch_agent.py — Phase 1: Solution Architect

Input  : none
Output : artifacts/arch_output.txt
"""

from .base_agent import (
    artifact_exists,
    load_prompt,
    logger,
    run_agent,
    save_artifact,
)

ARTIFACT = "arch_output.txt"


def run() -> str:
    if artifact_exists(ARTIFACT):
        logger.info("[AGENT-ARCH] Skipping — artifact already exists: %s", ARTIFACT)
        from .base_agent import load_artifact
        return load_artifact(ARTIFACT)

    logger.info("[AGENT-ARCH] Running Phase 1: Solution Architect")

    system_prompt = load_prompt("arch_prompt.txt")

    user_message = (
        "Design the complete architecture for the AI Codebase Architect Plugin. "
        "Produce the full document as described in your instructions. "
        "Be thorough and complete — downstream agents depend on every section."
    )

    output = run_agent(
        agent_name="AGENT-ARCH",
        system_prompt=system_prompt,
        user_message=user_message,
    )

    save_artifact(ARTIFACT, output)
    return output
