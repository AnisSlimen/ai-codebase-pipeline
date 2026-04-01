"""
cli_agent.py — Phase 2a: Static Analysis CLI (runs in parallel with backend_agent)

Input  : artifacts/arch_output.txt
Output : artifacts/cli_output.txt
"""

from .base_agent import (
    artifact_exists,
    load_artifact,
    load_prompt,
    logger,
    run_agent,
    save_artifact,
)

ARTIFACT = "cli_output.txt"


def run() -> str:
    if artifact_exists(ARTIFACT):
        logger.info("[AGENT-CLI] Skipping — artifact already exists: %s", ARTIFACT)
        return load_artifact(ARTIFACT)

    logger.info("[AGENT-CLI] Running Phase 2a: Static Analysis CLI")

    arch_output = load_artifact("arch_output.txt")
    system_prompt = load_prompt("cli_prompt.txt")

    user_message = (
        "Here is the architecture document produced by AGENT-ARCH:\n\n"
        f"<arch_document>\n{arch_output}\n</arch_document>\n\n"
        "Implement the complete static analysis CLI as described in your instructions. "
        "Write all source files in full — no placeholders or TODO comments."
    )

    output = run_agent(
        agent_name="AGENT-CLI",
        system_prompt=system_prompt,
        user_message=user_message,
    )

    save_artifact(ARTIFACT, output)
    return output
