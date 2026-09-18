# 工作流：模式路由、渲染校验闭环、降级阶梯、排错表

## 五种模式路由

| 模式 | 用户想要什么 | 动作 |
|---|---|---|
| Generate（默认） | 从文字描述生成图 | 按"生成闭环"执行 |
| From code | 从现有源代码生成图 | 读代码，提取真实存在的类/构件/调用，只画有的；类图用 class 语法，架构用 component/deployment |
| Embed | Markdown 内 ```plantuml 代码块渲染成图片 | 逐块提取为 .puml，渲染后把代码块替换为图片链接 |
| Refine | 修改已有图 | 读现有 .puml，做最小修改，重新渲染 |
| Review | 评审已有图质量 | 渲染 PNG 后用视觉检查（读图）：标签截断、节点重叠、方向、连线混乱、对比度 |

## 生成闭环（Generate 核心流程）

1. **识别图类型**：用 SKILL.md 的映射表定位 reference 文件，按其"方法要点"组织要素（先建模、后翻译语法）。
2. **写 .puml 文件**：结构化命名 `<场景>_<序号>_<类型>_<标题>.puml`（如 `hospital_001_sequence_booking.puml`）；中文内容直接写，UTF-8 无问题；样式默认遵循 SKILL.md"课件风格约定"（标题、白底、矩形构造型、编号、去模板印记）。
3. **渲染校验**：运行 `python scripts/render_puml.py <file>.puml`
   - 退出码 0 且输出 PNG/SVG → 成功；
   - 退出码 2 → 语法错误，stderr 里有后端错误信息（Kroki 400 时 body 即 PlantUML 错误原文），据此修正；
   - 退出码 3 → 网络问题（Kroki 403/超时等），脚本已自动兜底 plantuml.com，均失败时检查网络后重试。
4. **自纠重试（最多 3 轮）**：修正后重新渲染。按"降级阶梯"逐步简化：去掉 skinparam/theme/注释 → 缩短标签 → 减少连线 → 拆分多张小图。
5. **视觉自检（Review 步）**：读取渲染出的 PNG，检查可读性（最多 2 轮）：标签截断、重叠、方向错误、连线交叉过多。
6. **交付**：只输出渲染后的 UML 图片和完整 PlantUML 代码块，不附方法说明、过程描述等任何其他内容；仅在用户要求嵌入文档时，才把代码块替换为图片链接并保留 .puml 源文件。

## 排错表（经实测验证的错误模式）

| 症状 | 真实原因 | 修正 |
|---|---|---|
| HTTP 400（plantuml.com） | 语法错误。实测例：在连线行上用 `as` 定义未声明别名（`Doctor --> UC6 as "名"`） | 先声明再引用：`usecase "名" as UC6`，然后 `Doctor --> UC6` |
| HTTP 500（plantuml.com） | 开始/结束标签不匹配。实测例：`@startgantt` 配 `@enduml` | 甘特图用 `@endgantt`，时序/类图等用 `@enduml` |
| Kroki HTTP 403 / 超时 | 网络或代理拦截（源码外传被禁） | 脚本自动兜底 plantuml.com；含敏感内容的图禁止用公共渲染服务，改本地 jar |
| 甘特任务依赖不生效 | 任务名两侧不一致 | 依赖行任务名必须与定义行逐字一致 |
| 中文字体方框 | 本地 jar 缺中文字体 | 公共服务器无此问题；本地渲染需装中文字体或指定 `skinparam defaultFontName` |
| 活动图分支语义看着不对 | 带泳道切换的 if/else 分支内多个 stop，自动布局可能混乱（实测） | 收敛为单出口：if 只装差异活动，公共活动放 endif 之后，末尾一个 stop |
| 手绘主题下文标签消失 | `!theme sketchy` 的箭头标签字体不含 CJK，中文消息标签整行丢失（Kroki/plantuml.com 实测均复现，与字体设置无关） | 不要用 sketchy；课件风格靠矩形构造型＋编号＋批注实现，见 SKILL.md"课件风格约定" |
| Kroki 渲染的类图带圆圈 C 图标 | Kroki 的 PlantUML 新版默认开启类图标（plantuml.com 无此问题） | 类图加 `skinparam CircledCharacterRadius 0` 和 `skinparam CircledCharacterFontSize 0` |

## 其他规则

- 公共渲染服务（kroki.io / plantuml.com）会收到图源码：涉密代码/内部系统名不得使用，改本地 plantuml.jar。
- 结构图之间可用 `allow_mixing` 混合（类图+构件图、部署图+构件图）。
- 大图优先拆分：单图超过约 15 个节点时按子系统/泳道拆多张。
- 渲染后端优先级：Kroki（POST，失败信息详尽）→ plantuml.com（GET，hex 编码）。两者都无需本地安装。
