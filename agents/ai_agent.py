"""
ai_agent.py — Phase 3: AI/RAG Module

Input  : artifacts/arch_output.txt, cli_output.txt, backend_output.txt
Output : artifacts/ai_output.txt
"""

from .base_agent import (
    artifact_exists,
    load_artifact,
    load_prompt,
    logger,
    run_agent,
    save_artifact,
)

ARTIFACT = "ai_output.txt"


def run() -> str:
    if artifact_exists(ARTIFACT):
        logger.info("[AGENT-AI] Skipping — artifact already exists: %s", ARTIFACT)
        return load_artifact(ARTIFACT)

    logger.info("[AGENT-AI] Running Phase 3: AI/RAG Module")

    arch_output = load_artifact("arch_output.txt")
    cli_output = load_artifact("cli_output.txt")
    backend_output = load_artifact("backend_output.txt")

    system_prompt = load_prompt("ai_prompt.txt")

    user_message = (
        "Here are the artifacts produced by previous agents:\n\n"
        f"<arch_document>\n{arch_output}\n</arch_document>\n\n"
        f"<cli_implementation>\n{cli_output}\n</cli_implementation>\n\n"
        f"<backend_implementation>\n{backend_output}\n</backend_implementation>\n\n"
        "Implement the complete AI/RAG module as described in your instructions. "
        "Write all source files in full — no placeholders or TODO comments."
    )

    output = run_agent(
        agent_name="AGENT-AI",
        system_prompt=system_prompt,
        user_message=user_message,
    )

    save_artifact(ARTIFACT, output)
    return output
