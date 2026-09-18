# uml-to-plantuml

依据软件工程建模方法（BCE 分析类、用例模型、详细设计类图等）生成 UML 及工程图，并渲染校验为 PNG/SVG 的 Agent Skill。默认"课件风格"产出，消除模板感。

## 支持图型

| 类别 | 图型 |
|---|---|
| 行为 | 用例图、顺序图/时序图、活动图、状态图、通信图 |
| 结构 | 类图（分析/设计/界面类图）、对象图、包图、构件图、部署图 |
| 测试/管理 | 控制流图（McCabe 流图）、甘特图、PERT 网络图 |

## 特性

- **先建模后翻译**：每种图附课件方法要点（BCE 三步、分析类图五步、活动图决策边互斥等），再产出 PlantUML 语法
- **默认课件风格**：白底标题、矩形构造型参与者、课件式消息编号、黄色批注、去模板印记
- **渲染校验闭环**：`scripts/render_puml.py` 双后端（Kroki → plantuml.com 自动兜底），退出码区分语法错/网络错，含实测排错表
- **阶段约定**：分析类图（plain 直线）与设计类图（多重性/关系精化）按 SE6/SE10 区分

## 安装

```bash
# 方式一：直接下载 .skill 安装包
curl -L -o uml-to-plantuml.skill https://raw.githubusercontent.com/ashyh123/uml-to-plantuml/main/uml-to-plantuml.skill

# 方式二：git clone 整个仓库
git clone https://github.com/ashyh123/uml-to-plantuml.git

# 方式三：skills CLI（Claude Code / Cursor 等）
npx skills add ashyh123/uml-to-plantuml
```

下载后将 `uml-to-plantuml/` 目录复制到你的 agent skills 目录（如 `~/.config/agents/skills/` 或 Kimi Work 的 `daimon/skills/`），或用 `.skill` 包通过包管理器安装。

## 使用

```text
画一张医院挂号系统的预约医生顺序图（BCE 分析）
```

Skill 会：识别图型 → 按方法要点建模 → 生成 .puml → 渲染校验 → 视觉自检 → 交付代码与图片。

## 致谢

- 建模方法整理自《软件工程》课程课件（用例模型、BCE 分析类、详细设计等章节）
- 工作流设计参考开源社区 plantuml skill（Kroki 渲染、校验-自纠闭环）
- 渲染服务：Kroki / PlantUML 公共服务器

## License

MIT
