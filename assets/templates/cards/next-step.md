# Next-Step Card Template

This template defines the Markdown display hierarchy for next-step cards.

## Display Hierarchy

When rendering a next-step card to the user, follow this order:

1. **Current stage and status**
2. **Recommended next move** — stable role plus concrete Skill or fallback
3. **Why this is the next move**
4. **Copyable prompt** or manual instruction
5. **Expected output**
6. **Confirmation question**
7. **Fallback if missing**
8. **State updates and short routing trace**
9. **Not-now Skills**

The card should feel like guidance, not a schema dump.

## Markdown Rendering

Use this format when rendering in Markdown:

```markdown
## Next Step: {recommended_role}

**Stage:** {current_stage} → {target_stage_after_completion}
**Confidence:** {confidence}

### Why
{why}

### What to do
{prompt}

### Expected output
{expected_output list}

### Confirm?
Does this look right? (yes / no / skip)

### Fallback
{fallback_if_missing list}

### State updates
- On confirm: status → in_progress, active_card → {id}
- After success: stage → {target_stage_after_completion}

### Routing
{routing_trace bullets}

### Not now
{not_now list}
```

## Fenced Block Format

For machine-readable card data, use the `next-step-card` fenced block. See `references/navigator/next-step-card.md` for complete canonical card examples for every lifecycle stage.

The fenced block uses `key: value` scalar fields, top-level lists with two-space-indented `- item` lines, and one-level nested maps with two-space-indented `nested_key: value` lines.
