#!/usr/bin/env python3
"""Print a read-only inventory of an Origin project.

Run this only on a machine with OriginPro and the `originpro` Python package.
The project is opened read-only and the script does not save it.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect graph, workbook, and plot counts in an Origin project."
    )
    parser.add_argument("project", type=Path, help="Path to an .opj or .opju file")
    parser.add_argument(
        "--show-origin",
        action="store_true",
        help="Show the Origin window while inspecting the project.",
    )
    return parser.parse_args()


def inspect_project(project: Path, show_origin: bool) -> dict[str, Any]:
    try:
        import originpro as op  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "The 'originpro' package is required. Install it in a Python "
            "environment that can automate your OriginPro installation."
        ) from exc

    project = project.expanduser().resolve()
    if not project.is_file():
        raise SystemExit(f"Project not found: {project}")
    if project.suffix.lower() not in {".opj", ".opju"}:
        raise SystemExit(f"Expected an .opj or .opju file: {project}")

    op.set_show(show_origin)
    try:
        if not op.open(str(project), readonly=True, asksave=False):
            raise SystemExit(f"Origin could not open: {project}")
        graphs = list(op.pages("g"))
        workbooks = list(op.pages("w"))
        graph_rows: list[dict[str, Any]] = []
        for graph in graphs:
            graph_rows.append(
                {
                    "name": graph.lname,
                    "first_layer_plot_count": len(graph[0].plot_list()),
                }
            )
        return {
            "project": str(project),
            "graph_count": len(graphs),
            "workbook_count": len(workbooks),
            "graphs": graph_rows,
            "workbooks": [book.lname for book in workbooks],
        }
    finally:
        try:
            op.exit()
        except Exception:
            op.detach()


def main() -> int:
    args = parse_args()
    report = inspect_project(args.project, args.show_origin)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
