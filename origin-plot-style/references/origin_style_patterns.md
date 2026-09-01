# OriginPro style patterns

Read this reference when writing or repairing Python `originpro` or LabTalk graph-formatting code. Journal requirements and an existing validated project override these defaults.

## Keep style separate

Prefer small style functions that receive existing Origin objects. They should not load new data, refit a model, or choose scientific ranges.

```python
def apply_curve_style(plot, color: str, width: float = 2.2) -> None:
    plot.color = color
    plot.set_cmd(f'-c color("{color}")', f"-wp {width}", "-d 0", "-k 0")
```

Use line-only formatting only for data that should be represented as continuous curves. Preserve symbols and error bars when they carry scientific meaning.

## Four-sided frame

The following graph-level pattern has worked for recent Origin versions. Supply ranges and increments from the caller; do not embed scientific range decisions in the style helper.

```python
def apply_four_sided_frame(
    graph,
    *,
    x_min: float,
    x_max: float,
    x_step: float,
    y_min: float,
    y_max: float,
    y_step: float,
    x_title: str,
    y_title: str,
) -> None:
    graph.lt_exec(
        f"""
        layer.x.from = {x_min};
        layer.x.to = {x_max};
        layer.x.inc = {x_step};
        layer.x.rescale = 0;
        layer.y.from = {y_min};
        layer.y.to = {y_max};
        layer.y.inc = {y_step};
        layer.y.rescale = 0;

        layer.x.showAxes = 3;
        layer.y.showAxes = 3;
        layer.x.showLabels = 1;
        layer.y.showLabels = 1;
        layer.x2.showlabel = 0;
        layer.y2.showlabel = 0;
        layer.x2.ticks = 0;
        layer.y2.ticks = 0;

        layer.x.thickness = 2.0;
        layer.y.thickness = 2.0;
        layer.x2.thickness = 2.0;
        layer.y2.thickness = 2.0;
        layer.tickW = 2.0;
        layer.tickstyle = 1;

        layer.x.label.font = font(Arial);
        layer.y.label.font = font(Arial);
        layer.x.label.fsize = 22;
        layer.y.label.fsize = 22;
        layer.x.label.bold = 1;
        layer.y.label.bold = 1;
        layer.x.grid.show = 0;
        layer.y.grid.show = 0;

        xb.text$ = "{x_title}";
        yl.text$ = "{y_title}";
        xb.font = font(Arial);
        yl.font = font(Arial);
        xb.fsize = 28;
        yl.fsize = 28;
        xb.bold = 1;
        yl.bold = 1;
        layer.title = 0;
        label -r TITLE;
        """
    )
```

Useful Origin rich-text examples:

- Italic potential: `\\i(U) (V vs. SHE)`
- Delta G: `Δ\\i(G) (eV)`
- Subscripted grand energy: `\\i(E)\-(grand) (eV)`

Test rich text after PNG or PDF export. Fonts, Unicode, and title offsets can vary with Origin version and export format.

## Legends

For line-only graphs, stable explicit legend entries are often preferable:

```python
legend_lines.append(rf"\l({plot_index}) {label}")
```

Check the rendered legend for raw column names, substitution tokens, duplicated entries, or stale workbook labels. Do not change the scientific series order merely to simplify legend construction.

## Project inventory

Use the public project iterator and the graph layer's plot list:

```python
graphs = list(op.pages("g"))
workbooks = list(op.pages("w"))
for graph in graphs:
    plot_count = len(graph[0].plot_list())
```

Do not assume a `GLayer` is itself countable or iterable. For multiple layers, index layers explicitly and verify the layer count with the API available in the installed Origin version.

## Visual QA

- Four frame lines are visible and have consistent thickness.
- Top/right axes have no ticks, tick labels, or titles.
- Bottom/left ticks point outward and labels do not collide.
- Rich text renders as intended.
- Legends contain only intended entries.
- Lines, symbols, and error bars match the data semantics.
- Axis limits do not clip data, error bars, annotations, or legends.
- Exported dimensions and resolution match the requested final figure size.

## Official references

- [OriginPro Python project API](https://docs.originlab.com/originpro/namespaceoriginpro_1_1project.html)
- [OriginPro external Python](https://docs.originlab.com/externalpython/)
- [LabTalk Layer object](https://docs.originlab.com/labtalk/ref/layer-obj/)
- [LabTalk Layer.Axis object](https://docs.originlab.com/labtalk/ref/layer-axis-obj/)
- [LabTalk graphing and export tutorial](https://docs.originlab.com/labtalk/tutorials/tutorial-graphing-and-exporting-with-lt/)
