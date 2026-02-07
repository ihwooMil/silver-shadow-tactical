# Skill: Compact Context

## Description
Safely captures the current volatile session context (active tasks, debugging states, immediate todos) and persists them to `MEMORY.md` so the session can be reset to save tokens.

## Procedure
1.  **Analyze Context**: Identify ongoing processes (e.g., "Waiting for deployment"), specific version numbers (e.g., "Version Blue 4"), and the immediate next step.
2.  **Update Memory**: Write a `## 🔄 Session Checkpoint [YYYY-MM-DD HH:MM]` section to `MEMORY.md`.
    - Replace/Update any outdated "Current Status" sections.
    - Be specific about what to check next.
3.  **Signal Readiness**: Inform the user that memory is secured and request a `/reset`.

## Example
User: "Compact this."
Agent: (Writes to MEMORY.md) -> "Context saved. Please run /reset."
