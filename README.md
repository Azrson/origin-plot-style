# Origin Plot Style

一个面向 Codex 的 OriginPro 科研绘图 Skill：帮助智能体用 Python `originpro` 和 LabTalk 创建、统一并核验可投稿的 Origin 图，而不是只生成“能跑”的脚本。

> A Codex skill for reproducible, publication-ready OriginPro graph styling and verification.

## 能做什么

- 创建或修复 Origin `.opju` 自动化脚本
- 统一四边框坐标轴、字体、线宽、刻度和图例
- 正确处理 Origin 富文本中的斜体、上下标和希腊字母
- 严格分离数据处理与图形样式，避免“改格式时改了数据”
- 只读统计项目中的图页、工作簿和曲线数量
- 在交付前要求代码检查、项目结构检查和导出图目视检查

## 安装

将本仓库克隆到 Codex 的 skills 目录：

```powershell
git clone https://github.com/Azrson/origin-plot-style.git "$env:USERPROFILE\.codex\skills\origin-plot-style"
```

重新打开 Codex，或让 Codex 重新加载 skills。实际绘图自动化还需要 Windows、OriginPro，以及能够连接 Origin 的 `originpro` Python 包：

```powershell
python -m pip install originpro
```

## 使用示例

```text
Use $origin-plot-style to restyle this Origin script with a four-sided frame,
Arial labels, outward ticks, and no top/right tick labels. Do not change data logic.
```

```text
用 $origin-plot-style 检查这个 .opju：统计图页和曲线数，导出 PNG，
并检查图例、坐标轴标题和四边框是否符合论文格式。
```

## 项目结构

```text
origin-plot-style/
├── SKILL.md
├── agents/openai.yaml
├── references/origin_style_patterns.md
├── scripts/inspect_origin_project.py
└── assets/
```

`SKILL.md` 是 Codex 的入口；详细的 OriginPro/LabTalk 模式放在 `references/`；`scripts/inspect_origin_project.py` 用只读方式输出项目清单。

## 只读检查项目

请先关闭不希望被自动化连接的 Origin 会话，再运行：

```powershell
python scripts/inspect_origin_project.py path\to\figure.opju
```

脚本不会保存项目，但会启动或连接 Origin Automation Server，并在完成后退出该自动化会话。

## 设计原则

- 期刊模板或用户要求永远优先于默认样式。
- 仅改样式时，不改公式、拟合、数据范围、插值和科学标签。
- 不在公开脚本中写死私人路径或项目数据。
- 成功运行不等于图形正确；必须检查导出图。

## 官方资料

- [OriginPro Python API](https://docs.originlab.com/originpro/namespaceoriginpro_1_1project.html)
- [External Python with OriginPro](https://docs.originlab.com/externalpython/)
- [LabTalk Layer object](https://docs.originlab.com/labtalk/ref/layer-obj/)
- [LabTalk Layer.Axis object](https://docs.originlab.com/labtalk/ref/layer-axis-obj/)

## License

[MIT](LICENSE)
