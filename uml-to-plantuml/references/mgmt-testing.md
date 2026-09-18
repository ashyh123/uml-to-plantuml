# 测试与项目管理视图：控制流图、甘特图、PERT 网络图

## 控制流图（flow）

**课件方法要点（基本路径测试 / McCabe）**
- 由流程图转换：结构化构件改为有向图，**谓词结点**（条件判断）出度 ≥2；复合条件必须先拆成等价简单条件。
- 节点形式：过程块、判定点、结合点；边代表控制流。
- 环形复杂度 `V(G) = E − N + 2 = 谓词结点数 + 1 = 区域数`（含外部区域），即独立基本路径数。

**PlantUML 模板（活动图新语法可精确表达控制流）**
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
title <系统名> · <对象名>状态图
start
while (nPosX > 0?) is (真)
  :int nSum = nPosX + nPosY;
  if (nSum > 1?) then (真)
    :nPosX减一;
    :nPosY减一;
  else (假)
    if (nSum < -1?) then (真)
      :nPosX -= 2;
    else (假)
      :nPosX减四;
    endif
  endif
endwhile (假)
stop
@enduml
```
提示：每个 `if`/`while` 判定即一个谓词结点；可顺带在回复中给出 V(G) 供基本路径测试使用。

## 甘特图（gantt）

**课件方法要点**：左部工作表（任务名称、起止日期），右部条形图；用于描述项目进度计划。

**PlantUML 模板（`@startgantt`，课件风格）**
```plantuml
@startgantt
skinparam backgroundColor #FFFFFF
title <项目名> · 进度计划
Project starts 2026-09-18
[需求分析] lasts 14 days
[软件设计] lasts 21 days
[软件实现] lasts 30 days
[软件测试] lasts 14 days
[部署交付] lasts 7 days

[需求分析] -> [软件设计]
[软件设计] -> [软件实现]
[软件实现] -> [软件测试]
[软件测试] -> [部署交付]

[设计评审里程碑] happens at [软件设计]'s end
@endgantt
```
常用语法：`lasts N days`、`starts D+offset`、`ends`、`->` 依赖、`happens at <日期>` 或 `happens at [任务]'s end` 里程碑、`is colored` 着色、`[任务] is 100% complete`。**注意：甘特图结束标签必须是 `@endgantt`，写成 `@enduml` 会报 HTTP 500**。

## PERT 网络图（network）

**课件方法要点**：PERT/CPM 用有向图描述任务网络——**箭头=任务（标注持续时间），结点=事件**（流入任务完成、流出任务可开始）；计算最早时刻 EFT（正向取 max）与最迟时刻 LET（反向取 min），差值为机动时间，机动时间为 0 的任务连成**关键路径**。

**PlantUML 原生无 PERT 语法**，两种替代：
1. 甘特图表达任务依赖与关键路径（推荐，纯 PlantUML）：
```plantuml
@startgantt
skinparam backgroundColor #FFFFFF
title <项目名> · PERT 任务网络（甘特表达）
Project starts 2026-09-18
[任务A:需求调研] lasts 5 days
[任务B:概要设计] lasts 8 days
[任务C:详细设计] lasts 10 days
[任务D:编码] lasts 15 days
[任务E:测试] lasts 6 days
[任务A:需求调研] -> [任务B:概要设计]
[任务B:概要设计] -> [任务C:详细设计]
[任务C:详细设计] -> [任务D:编码]
[任务D:编码] -> [任务E:测试]
@endgantt
```
2. 严格 PERT 网络（结点=事件、边=任务）用 Graphviz dot 更贴切：
```dot
digraph PERT {
  rankdir=LR;
  1 -> 2 [label="任务A 5天"];
  2 -> 3 [label="任务B 8天"];
  3 -> 4 [label="任务C 10天"];
  4 -> 5 [label="任务D 15天"];
  5 -> 6 [label="任务E 6天"];
}
```
生成时可主动计算各事件 EFT/LET 并标出关键路径。
