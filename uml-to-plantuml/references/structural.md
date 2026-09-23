# 结构视图：类图、对象图、包图、构件图、部署图

## 类图（class）

**课件方法要点**
- 分析类三分法：边界类 `<<boundary>>`（与执行者交互）、控制类 `<<control>>`（协调控制）、实体类 `<<entity>>`（持久信息）。
- 分析类图五步：①确定分析类（执行者＋各用例顺序图中出现的对象）→②确定职责（对象接收的消息 ↔ 职责一一对应）→③确定属性（需持久保存/消息参数涉及的数据）→④确定关系（A→B 有消息 ⇒ 关联/依赖/聚合/组合；一般特殊关系 ⇒ 继承）→⑤绘制类图（过大时按子系统拆分）。
- **分析 vs 设计的阶段约定（重要）**：分析类图只画 plain 直线表"有关系"，**不标关系名（如"拥有/发起"）、不标多重性**（SE6 示例即如此）；多重性（1:1/1:n/0:n/n:m）、关系语义强度（继承>组合>聚合>关联>依赖）、属性类型与可见性是 SE10 设计类图"精化类间的关系"阶段的内容。泛化层次（如"患者/医生"继承"用户"）在分析阶段即可标识。
- 设计类图构造：从分析类图、体系结构图、用例顺序图找候选类；职责来自对消息的响应；A 与 B 有消息 ⇒ 有关系；属性＝需保存的数据项；最后按模块化、职责单一化整合。
- 精化规则：属性可见范围默认 private（信息隐藏）；关系语义强度 继承 > 组合 > 聚合 > 关联 > 依赖，尽量采用语义强度较小的关系；多重性 1:1 / 1:n / 0:n / n:m 决定属性形态——1:1 关联/聚合用引用类型属性，1:n 用集合（List）属性，1:1 组合直接持有对象，1:n 组合持有对象集合。
- 详细设计类图可包含子系统 `<<Sub system>>` 和构件 `<<Component>>`。
- 界面设计：界面元素（动态元素、用户输入元素、命令元素）也可建模为类，界面跳转关系可用类图表示（界面类间建立关联）。

**PlantUML 模板（课件风格）**
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam classAttributeIconSize 0
skinparam CircledCharacterRadius 0
skinparam CircledCharacterFontSize 0
title <系统名> · 分析类图

class LoginUI <<boundary>> {
  -account: String = ""
  -password: String = ""
  +login(account, password): int
}
class LoginManager <<control>> {
  +verifyUserValidity(account, password): int
}
class UserLibrary <<entity>> {
  -account: String
  -password: String
  +isUserValid(account, password): boolean
}
class GuidingUI <<screen>>

GuidingUI --> LoginUI : 跳转
LoginUI --> LoginManager
LoginManager --> UserLibrary
UserLibrary "1" o-- "0..*" LoginRecord : 登录日志

interface IMonitor {
  +monitorElder()
}
MonitoringUI ..|> IMonitor
@enduml
```
关系速查：`A <|-- B`（B 继承 A）、`A *-- B`（B 组合于 A，实心菱形在 A 端写作 `A *-- "1" B`）、`A o-- B`（聚合）、`A --> B`（关联/导航）、`A ..> B`（依赖）、`A ..|> B`（实现接口）。可见性 `+ public` `- private` `# protected` `~ package`。多重性 `"1" o-- "0..*"`。

## 对象图（object）

**课件方法要点**：类图的实例层快照，描述某时刻对象及其链接关系，用于示例复杂类图。

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
title <系统名> · 对象图
object "loginUI : LoginUI" as ui
object "loginManager : LoginManager" as cm
object "userLibrary : UserLibrary" as ul
ui --> cm
cm --> ul
@enduml
```

## 包图（package）

**课件方法要点**：从包层面描述系统静态结构；类仅被本包使用则私有，否则公开，尽量缩小可见性。

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
title <系统名> · 包图
package "用户界面层" {
  class LoginUI
  class GuidingUI
}
package "业务控制层" {
  class LoginManager
}
package "数据层" {
  class UserLibrary
}
用户界面层 ..> 业务控制层
业务控制层 ..> 数据层
@enduml
```

## 构件图（component）

**课件方法要点**：描述构件及其依赖关系、对外接口；构件是粗粒度、可独立部署、可替换的二进制单元。

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
title <系统名> · 构件图
allow_mixing
component "RobotController" as RC {
  component "RemindNotifier"
  component "Timer"
}
component "OLVTI-SDK" as SDK
interface "IText2Voice" as T2V
RC --> T2V : 使用
T2V - SDK : 提供
database "UserLibrary" as DB
RC --> DB
@enduml
```

## 部署图（deployment）

**课件方法要点**：描述工件（artifact）在物理运行环境中的部署。①实例性节点命名"节点名: 类型名"（如 `1#服务器: Web服务器`、`客户端: Web客户端`）；②节点内驻留工件以 `<<artifact>>` 标识，部署规格 `<<deploymentSpec>>` 工件内写配置参数（键=值逐行列出）；③持久数据用数据库符号（圆柱）；④节点间通信边标注协议构造型（`<<HTTP>>`、`<<JDBC>>`、`<<Web Services>>`）；⑤按"客户端→Web服务器→应用服务器→数据库/外部服务器"链条**从左到右**布局，节点行列对齐、避免斜线。

**PlantUML 模板（课件风格，含实例节点/协议构造型/部署规格）**
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam linetype ortho
left to right direction
title <系统名> · 部署图

node "客户端\n: Web客户端" as client {
  artifact "由WebUI生成的HTML页面\n(含JavaScript代码)" as html <<artifact>>
}
node "1#服务器\n: Web服务器" as websrv {
  artifact "WebUI\n(JSP+JavaScript)" as webui <<artifact>>
}
node "3#小型机\n: 应用服务器" as appsrv {
  artifact "customer.jar" as custjar <<artifact>>
  artifact "customerDeploy.xml\npointPerHundred=10\nsilverMinPoint=1000\ngoldenMinPoint=5000" as depxml <<deploymentSpec>>
  artifact "order&ticket.jar" as otjar <<artifact>>
}
node "6#服务器\n: 数据库服务器" as dbsrv {
  database "持久数据" as pdata
}
node "A航空公司\n票务服务器" as airlineA {
  [AirlineCompany] as compA
}

client --> websrv : <<HTTP>>
websrv --> appsrv
appsrv --> dbsrv : <<JDBC>>
appsrv --> airlineA : <<Web Services>>
depxml ..> custjar
@enduml
```
实测技巧：①`<<deploymentSpec>>` 的配置参数**不要写属性块**（`{ k=v }` 渲染成乱码圆圈），写在名称字符串里用 `\n` 逐行排；②实例节点名"名称: 类型"用 `\n` 折行；③协议构造型直接作边的标签（`: <<HTTP>>`）。

## 架构图（软件体系结构）

**课件方法要点（SE8）**
- 体系结构四视图：**逻辑视图**（要素及关系，结构视点，用**包图**表示）、**运行视图**（运行时进程/线程划分及并发同步，用活动图/对象图）、**开发视图**（源代码分包与目录结构、类库/中间件/框架/子系统与逻辑视图的映射）、**物理视图**（构件部署及连接交互，用**部署图**）。
- 描述体系结构的三类 UML 图：**包图、构件图、部署图**。
- 构件图：结点=构件（具有对外接口、可分离、独立功能的物理模块），边=依赖关系；**供给接口画在构件左侧，需求接口画在构件右侧**。
- 部署图：节点=计算资源（Web/应用/数据库服务器），工件以 `<<artifact>>` 标识驻留于节点内；边=通信关联＋依赖（工件间依赖尽量表现为接口上的依赖）；分描述性（逻辑布局）与实例性（具体运行环境，节点命名"节点名: 类型名"）两种。
- 部署图建模原则：节点按行列对齐，边用水平/垂直折线、避免斜线；依赖方向尽量从左至右。

**PlantUML 模板（架构图=包图+构件图+部署图，按视图组合）**
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
title <系统名> · 软件体系结构（构件图）

package "预约子系统" {
  [预约界面] as UI
  [预约管理器] as AM
}
package "数据子系统" {
  [预约记录库] as ApptDB
}

interface "I预约服务" as ISvc
UI ..> ISvc : 需求接口
AM - ISvc : 供给接口
AM --> ApptDB : 依赖

node "应用服务器" as srv {
  artifact "appointment.jar" as jar
}
jar ..> AM : 实现
note bottom of jar #FFF7CC
  供给接口在构件左侧，需求接口在右侧；
  依赖方向从左至右；部署图节点行列对齐、避免斜线
end note
@enduml
```

**分层体系结构图（layered）**——课件常见画法：纵向分层（用户界面层/业务逻辑层/基础服务层等），每层一个 package（自带标签页），层内放构件；层间交互边标注"请求/应答"（双向请求）与"事件"（上行通知）；对外服务可声明《Interface》接口，由本层构件实现。

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam linetype ortho
top to bottom direction
title <系统名> · 分层体系结构图

package "用户界面层" {
  [接收用户命令] as UICmd
  [Linphone4Android] as UILin
  [显示老人状况] as UIDisp
}
package "业务逻辑层" {
  [分析和处理老人信息] as Biz
  [控制机器人运行] as Ctrl
  rectangle "«Interface»\nDataService" as IDataService
  [DataService] as Impl
}
package "基础服务层" {
  [ROS] as ROS
  database "MySQL" as MySQL
}

' 层内行序 + 底层整体压到最底行（隐形边布局法）
UICmd -[hidden]r- UILin
UILin -[hidden]r- UIDisp
Biz -[hidden]r- Ctrl
ROS -[hidden]r- MySQL
IDataService -[hidden]d- ROS
IDataService -[hidden]d- MySQL

UICmd --> Biz : 请求/应答
UIDisp <-- Biz : 事件
Biz --> Impl
Impl --> IDataService
Biz --> ROS : 请求/应答
Impl --> MySQL : 事件
@enduml
```
实测技巧：①**总体自上而下布局（隐形边布局法）**：`top to bottom direction`＋`skinparam linetype ortho` 只保证大方向，要让每层严格横成行、层层竖直堆叠，需加隐形边——层内构件用 `X -[hidden]r- Y` 锁成同一行，用本层最底构件（如接口）`X -[hidden]d- 底层构件` 把下一层整体压到最底行；②渲染左右顺序与声明顺序镜像，层内顺序不对时**反转该层声明顺序**即可；③课件式接口是**方框**（《Interface》在上、名称在下），不是棒棒糖——用 `rectangle "«Interface»\n名称" as X` 画方框接口，构件与接口连线表示实现；棒棒糖（`interface` 关键字）只用于构件图的供给/需求接口；④`allow_mixing` 在 Kroki 后端混合 node+component 时会报 400，混排构件/节点/包时**不写** `allow_mixing`（实测裸混排即可正常渲染）。
