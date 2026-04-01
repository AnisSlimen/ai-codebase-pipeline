"""
qa_agent.py — Phase 5: Integration & QA

Input  : all 4 prior artifacts
Output : artifacts/qa_output.txt
"""

from .base_agent import (
    artifact_exists,
    load_artifact,
    load_prompt,
    logger,
    run_agent,
    save_artifact,
)

ARTIFACT = "qa_output.txt"


def run() -> str:
    if artifact_exists(ARTIFACT):
        logger.info("[AGENT-QA] Skipping — artifact already exists: %s", ARTIFACT)
        return load_artifact(ARTIFACT)

    logger.info("[AGENT-QA] Running Phase 5: Integration & QA")

    arch_output = load_artifact("arch_output.txt")
    cli_output = load_artifact("cli_output.txt")
    backend_output = load_artifact("backend_output.txt")
    ai_output = load_artifact("ai_output.txt")
    plugin_output = load_artifact("plugin_output.txt")

    system_prompt = load_prompt("qa_prompt.txt")

    user_message = (
        "Here are the artifacts produced by all previous agents:\n\n"
        f"<arch_document>\n{arch_output}\n</arch_document>\n\n"
        f"<cli_implementation>\n{cli_output}\n</cli_implementation>\n\n"
        f"<backend_implementation>\n{backend_output}\n</backend_implementation>\n\n"
        f"<ai_module>\n{ai_output}\n</ai_module>\n\n"
        f"<plugin_implementation>\n{plugin_output}\n</plugin_implementation>\n\n"
        "Produce the complete QA test suite and Definition of Done checklist as described in your instructions. "
        "Write all test files in full — no placeholders or TODO comments."
    )

    output = run_agent(
        agent_name="AGENT-QA",
        system_prompt=system_prompt,
        user_message=user_message,
    )

    save_artifact(ARTIFACT, output)
    return output
