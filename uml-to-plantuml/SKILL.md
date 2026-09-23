---
name: uml-to-plantuml
description: 依据软件工程建模方法（BCE 分析类、用例模型、详细设计类图等）生成 UML 及工程图，并渲染校验为 PNG/SVG。支持类图、用例图、顺序图/时序图、活动图、状态图、对象图、包图、构件图、部署图、通信图、控制流图、甘特图、PERT 网络图；支持从文字描述生成、从源码生成、修改已有图、Markdown 内嵌图渲染、图质量评审五种模式。使用时机：用户要求"画 UML 图"、"生成 PlantUML 代码"、按软件工程方法建模，或给出场景/源码要求绘制上述任一类图。
---

# UML 图生成与渲染（PlantUML）

## 快速开始

1. 按下方映射表确定图类型，打开对应 reference，按其**方法要点**建模要素。
2. 写 `.puml` 文件（结构化命名：`<场景>_<序号>_<类型>_<标题>.puml`）。
3. 渲染并校验：`python scripts/render_puml.py <file>.puml`（零本地依赖，Kroki → plantuml.com 自动兜底）。
4. 失败则按 [references/workflow.md](references/workflow.md) 的降级阶梯自纠（最多 3 轮），再读 PNG 做视觉自检。
5. **只交付两样：渲染后的 UML 图片 ＋ 完整 PlantUML 代码块**。不输出方法依据、设计说明、渲染提示、文件路径列表等任何其他内容；涉密内容禁止用公共渲染服务。

五种模式（Generate / From code / Embed / Refine / Review）的路由与完整闭环见 [references/workflow.md](references/workflow.md)。

## 图表类型映射表

| 用户说的图 | 类型 | 方法要点与语法参考 |
|---|---|---|
| 用例图 | usecase | [references/behavioral.md](references/behavioral.md) §用例图 |
| 顺序图 / 时序图 / 序列图 | sequence | [references/behavioral.md](references/behavioral.md) §顺序图 |
| 活动图 | activity | [references/behavioral.md](references/behavioral.md) §活动图 |
| 状态图 | state | [references/behavioral.md](references/behavioral.md) §状态图 |
| 通信图 / 协作图 | communication | [references/behavioral.md](references/behavioral.md) §通信图 |
| 类图（分析类图 / 设计类图 / 界面类图） | class | [references/structural.md](references/structural.md) §类图 |
| 对象图 | object | [references/structural.md](references/structural.md) §对象图 |
| 包图 | package | [references/structural.md](references/structural.md) §包图 |
| 构件图 / 组件图 | component | [references/structural.md](references/structural.md) §构件图 |
| 部署图 | deployment | [references/structural.md](references/structural.md) §部署图 |
| 架构图 / 体系结构图 | architecture | [references/structural.md](references/structural.md) §架构图（软件体系结构） |
| 控制流图 / 流图 / 程序流程图 | flow | [references/mgmt-testing.md](references/mgmt-testing.md) §控制流图 |
| 甘特图 | gantt | [references/mgmt-testing.md](references/mgmt-testing.md) §甘特图 |
| PERT 图 / 网络图 / 关键路径图 | network | [references/mgmt-testing.md](references/mgmt-testing.md) §PERT网络图 |

## 生成原则

- **先建模后翻译**：先按方法要点确定要素（如 BCE 三类分析类、消息命名动名词、决策边条件互斥），再写 PlantUML 语法。
- **默认课件风格**（与软件工程课件视觉统一，消除"AI 感"），规则见下节"课件风格约定"；用户明确要求其他风格时再切换。

## 课件风格约定（默认样式）

每张图统一以下元素（已与课件示例比对验证）：

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
title <系统名> · <图名>
' 顺序图额外加：hide footbox（去除底部参与者重复）
' 类图额外加：skinparam classAttributeIconSize 0 + CircledCharacterRadius 0 + CircledCharacterFontSize 0（去除工具图标）
```

- **顺序图**：参与者用 `participant "«boundary»\n__名称__" as X` 矩形框（不用 boundary/control/entity 关键字，避免圆圈图标；Creole `__` 为加粗名称）；**编号按业务逻辑顺序顺号标注**（1、2、3…，不用 1.1/1.1.1 层级）；**返回消息统一虚线 `-->` 且不编号**；**界面最终结果反馈**（错误提示并停留、禁止继续提交、跳转主界面、提示成功等）**统一实线 `->` 并顺号编号**；界面中间展示可用自消息（实线、顺号）；用例约束用黄色 `note` 批注；关键消息可用 `-[#red]>` 强调。
- **用例图**：执行者与用例之间用无向边 `--`（课件规定）；用例关系用 `..>` 虚线箭头＋«include»/«extend»；补充说明用黄色 note。
- **类图**：构造型写 `<<boundary>>`/`<<control>>`/`<<entity>>` 于类名上方；关系标多重性；可见性用 +/−/#。
- **部署图**：实例节点命名"节点名: 类型名"；节点内工件标 `<<artifact>>`/`<<deploymentSpec>>`（配置参数写名称串内逐行，勿用属性块）；通信边标协议构造型 `<<HTTP>>`/`<<JDBC>>`/`<<Web Services>>`；链条从左到右布局。
- **架构图**：分层体系结构用 package 作层（用户界面层/业务逻辑层/基础服务层），**总体自上而下**——`top to bottom direction`＋`skinparam linetype ortho`＋隐形边锁行压层（层内 `-[hidden]r-`，跨层 `-[hidden]d-`，详见 structural.md 分层模板），连线横平竖直、避免斜线，层间边标"请求/应答"与"事件"；课件式接口画 `rectangle "«Interface»\n名称"` 方框，不用棒棒糖。
- **禁用 `!theme sketchy`**：手绘主题在中文消息标签上会丢字（已实测，Kroki/plantuml.com 均复现）。
- 每个图独立 `.puml` 文件；结构图可混排构件/节点/包（不写 `allow_mixing`，Kroki 后端混合 node+component 时该指令会报 400，裸混排即可）；大图（>15 节点）拆多张。
- 公共渲染服务会收到图源码，涉密场景改用本地 plantuml.jar。
- 非 UML 需求的路由：ER 图用 `entity` 语法近似；DFD 用活动图近似；通信图无原生语法（见 behavioral.md 替代方案）。
- 若用户场景信息不足，先提问再生成；信息充分时直接产出。

## 资源

- `scripts/render_puml.py` — 渲染+校验（PNG/SVG，`--check` 仅校验），双后端自动兜底，退出码 0/2/3 区分成功/语法错/网络错。
- `references/workflow.md` — 模式路由、渲染闭环、降级阶梯、实测排错表。
- `references/behavioral.md` / `structural.md` / `mgmt-testing.md` — 各图型的课件方法要点 + 已验证模板。
