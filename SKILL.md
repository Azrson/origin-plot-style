---
name: origin-plot-style
description: Create, restyle, and verify publication-ready OriginPro graphs through Python originpro and LabTalk. Use for Origin .opju automation, four-sided axes, curve and symbol formatting, rich-text titles, legends, graph export, or graph/plot-count validation; do not use for non-Origin plotting libraries.
---

# Origin Plot Style

Create reproducible OriginPro figures while keeping data processing and visual formatting separate.

## Workflow

1. Inspect the source workbook, plotting script, existing `.opju`, and any reference figure that the user actually supplied.
2. Record the requested journal or template requirements. They override this skill's defaults.
3. Identify the boundary between data logic and style logic. A style-only request must not change formulas, source ranges, fitted parameters, interpolation, curve ordering, or scientific labels.
4. Before implementing Origin properties, read [references/origin_style_patterns.md](references/origin_style_patterns.md). Reuse a proven script from the current repository when one exists.
5. Centralize formatting in functions such as `apply_axis_style`, `apply_curve_style`, and `apply_legend_style`. Do not scatter unexplained LabTalk fragments through data-processing code.
6. Compile changed Python files. If an Origin deliverable is requested and Origin is available, regenerate it, enumerate graph pages with `op.pages("g")`, enumerate plots with `graph[0].plot_list()`, and visually inspect representative exports.
7. Report exact output paths, what was verified, and any Origin-version-dependent property that still needs a local visual check.

## Preservation Rules

- Treat source workbooks, reference projects, and raw data as read-only unless the user explicitly authorizes changes.
- Preserve the user's units, potential reference, notation, colors, data-point semantics, and requested output format.
- Do not silently replace scatter/error-bar data with lines. The line-only profile is a default for continuous calculated curves, not a universal rule.
- Do not hardcode local application, project, or data paths in reusable code. Accept paths through arguments, configuration, or environment variables.
- When modifying an existing project, save to a new destination unless overwriting was explicitly requested.

## Publication Default

Use these only when the user or journal template does not specify another style:

- Four-sided black frame; ticks and tick labels on bottom/left only.
- Top/right frame visible with their ticks, labels, and titles hidden.
- Outward ticks, no grid, consistent axis and tick thickness.
- Arial typography; 22 pt bold tick labels and 28 pt bold axis titles as a starting point.
- Calculated continuous curves: solid line, 2.2 pt, no symbols.
- Use Origin rich text for italic variables, subscripts, superscripts, and Greek symbols.

Scale fonts and stroke widths to the final physical figure size rather than applying the defaults mechanically.

## Verification

- Run `python -m py_compile <changed-script.py>`.
- Use `scripts/inspect_origin_project.py <project.opju>` for a read-only inventory when external Python and OriginPro are available.
- Check graph and workbook counts, per-layer plot counts, axis ranges, titles, legend text, and exported page dimensions.
- Inspect at least one representative exported image. For multi-graph projects, inspect one combined graph and one individual graph when both types exist.
- Never claim visual fidelity based only on a successful Python run.
