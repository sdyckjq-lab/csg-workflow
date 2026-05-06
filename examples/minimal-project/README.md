# Minimal CSG Workflow Project

This example shows the smallest useful project handoff state.

Start from an empty project, then add:

- `docs/workflow/state.md`
- `docs/workflow/decisions.md`
- `docs/workflow/log.md`

When a new session starts, `csg-workflow` reads `state.md` first and continues from the recorded next action.

## Example Flow

1. User says: "I want to build a small AI coding helper."
2. `csg-workflow` sees no prior state and creates the workflow files.
3. Current stage becomes requirements.
4. Next action becomes `ce-brainstorm`.
5. Future sessions continue from this state instead of restarting.
