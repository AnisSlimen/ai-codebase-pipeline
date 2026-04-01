"""
plugin_agent.py — Phase 4: VS Code TypeScript Extension

Input  : artifacts/arch_output.txt, backend_output.txt, ai_output.txt
Output : artifacts/plugin_output.txt
"""

from .base_agent import (
    artifact_exists,
    load_artifact,
    load_prompt,
    logger,
    run_agent,
    save_artifact,
)

ARTIFACT = "plugin_output.txt"


def run() -> str:
    if artifact_exists(ARTIFACT):
        logger.info("[AGENT-PLUGIN] Skipping — artifact already exists: %s", ARTIFACT)
        return load_artifact(ARTIFACT)

    logger.info("[AGENT-PLUGIN] Running Phase 4: VS Code Extension")

    arch_output = load_artifact("arch_output.txt")
    backend_output = load_artifact("backend_output.txt")
    ai_output = load_artifact("ai_output.txt")

    system_prompt = load_prompt("plugin_prompt.txt")

    user_message = (
        "Here are the artifacts produced by previous agents:\n\n"
        f"<arch_document>\n{arch_output}\n</arch_document>\n\n"
        f"<backend_implementation>\n{backend_output}\n</backend_implementation>\n\n"
        f"<ai_module>\n{ai_output}\n</ai_module>\n\n"
        "Implement the complete VS Code extension as described in your instructions. "
        "Write all source files in full — no placeholders or TODO comments."
    )

    output = run_agent(
        agent_name="AGENT-PLUGIN",
        system_prompt=system_prompt,
        user_message=user_message,
    )

    save_artifact(ARTIFACT, output)
    return output
