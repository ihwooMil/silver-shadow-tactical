# SKILL: Sub-Agent Management & Notification

## Overview
This skill allows the main agent to delegate complex tasks (like coding, data analysis, or world-building) to specialized sub-agents and ensure the user is notified via Telegram upon completion.

## Instructions
1. **Spawn Sub-Agent**: Use `sessions_spawn` with a clear task description, the model `google/gemini-3-pro-preview` for coding tasks, and a label.
2. **Monitor**: The sub-agent will operate in an isolated session.
3. **Notify**: Once the sub-agent task is complete, the main agent must send a direct message to the user via Telegram using the `message` tool to report the result.

## Usage Example
- Task: "Develop a complex wall and stat system in Godot."
- Sub-Agent: Spawned with the task.
- Notification: `message(action="send", target="telegram:8511385056", message="Sub-agent task complete: ...")`
