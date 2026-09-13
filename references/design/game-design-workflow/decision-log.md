# game-002 决策记录

当前对象范围以G002-CORE-011为准，类型特征与讨论组织按G002-CORE-012，类型扩展与主动建议按G002-CORE-013；下方保留各次决策发生时的文字与来源，早先开放的位移、结构、取材和指定端点权限不再作为当前工作范围。

修饰词基础模型与当前系统设计顺序按G002-CORE-016；涉及镶嵌的历史后置文字保留为当时决定，当前在修饰词之后补齐细则。

## 当前生效决定

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-ADMIN-001 | 2026-09-05 | 建立独立工作区，仅共享方法、结构与规范 | Accepted / Administration | 原始决策完整记录见下方 |
| G002-CORE-006 | 2026-09-09 | 战前完整库存构句、一组合一循环法术、一法术一法杖；配置顺序、0–10刻首次冷却与自动循环；同刻四阶段、生命伤害打断冷却、胜利终止、整体战后收益；目标引用适用G002-CORE-008 | Accepted：配置与循环依据；目标引用已按SW02完善；Hypothesis | [核心](core-concept.md)、[战前配置适用文本](draft-changes/D-2026-09-09-prebattle-spell-wand-assembly.md) |
| G002-DOC-001 | 2026-09-10 | 按用户授权逐份统一文档并保存原始快照；兼容部分保留，接口集中呈现；用户采纳范围按G002-CORE-007与G002-SCOPE-001执行 | Accepted / Documentation；Hypothesis | [文档统一](draft-changes/D-2026-09-10-current-design-alignment.md)、[决定清单](../docs/design-decisions-needed.md) |

## 决策证据索引

G002-ADMIN-001、G002-CORE-001至G002-CORE-006的完整原始决定、日期与状态均保存在[原始决策记录](../../../archive/2026-09-10-game-002-design-originals/workspaces/game-002/game-design-workflow/decision-log.md)。以下文件是当前适用范围说明，不能当作原始决定原文：

- G002-CORE-001：[施法设计支柱](draft-changes/D-2026-09-09-casting-design-pillars.md)。
- G002-CORE-002：[时间背包编排](draft-changes/D-2026-09-09-timeline-backpack-core.md)。
- G002-CORE-003、004：[自动战斗边界](draft-changes/D-2026-09-09-automatic-battle-boundaries.md)。
- G002-CORE-005：[稳定设计基线](draft-changes/D-2026-09-09-core-system-stable-baseline.md)。
- G002-CORE-006：[战前构句与法杖](draft-changes/D-2026-09-09-prebattle-spell-wand-assembly.md)。

C01–C08按用户批量确认全部处理，当前没有本轮遗留人工冲突。数值重新设计已确认，具体参数与体验证据仍为Unknown / Hypothesis。

## 接口采纳与数值任务

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-007 | 2026-09-10 | C01伤害/支付分类与独立反馈，C02逐对象材料、公开固定顺序和完整法术成功，C06产出资格前置与产金成本，C08词卡时间合计用于冷却；数值全部重新设计 | Accepted / Core Concept v0.6；Hypothesis | [拟修改与来源](draft-changes/D-2026-09-10-accept-design-decisions.md)、[数值任务](../docs/numerical-redesign.md) |
| G002-SCOPE-001 | 2026-09-10 | C03完整召唤后置，推进时设计战前单位占位与出生位置；C04当前不增加专属引用词卡；C05镶嵌细则与C07 BF1–BF3按推荐后置 | Accepted / Scope；具体机制Unknown | [决定清单](../docs/design-decisions-needed.md)、[合格范围素材](idea-materials/M-2026-09-10-accepted-design-interfaces.md) |

确认前推荐、数值来源与文档验收已封存于[决策输入快照](../../../archive/2026-09-10-game-002-decision-inputs/INDEX.md)，用于追溯，不作为参数基线。

## 语义世界对象范围

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-SCOPE-002 | 2026-09-10 | SW01：实体、部件、材料、属性状态、空间关系及飞行物、敌方攻击、法术冷却等过程纳入法术对象设计范围；各类按明确能力开放操作；胜负判定、全局结算顺序等基础规则保持固定 | Accepted / Scope；Hypothesis。具体引用与操作机制待定，Core Concept v0.6基础执行规则继续适用 | [用户确认](idea-inbox/2026-09-10-semantic-world-object-scope.md)、[范围素材](idea-materials/M-2026-09-10-semantic-world-object-scope.md)、[提案](idea-proposals/P-2026-09-10-semantic-world-object-scope.md)、[评估](evaluations/E-2026-09-10-semantic-world-object-scope.md)、[采纳文本](draft-changes/D-2026-09-10-semantic-world-object-scope.md) |

SW01范围的后续引用模型按G002-CORE-008确认，单次名单按G002-CORE-009确认；其余具体机制继续设计，数值重新设计继续执行。

## 两种引用并存

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-008 | 2026-09-10 | SW02：实例绑定保持所指身份，失效跳过、不自动改指向；条件绑定战前固定选择条件，每次释放自动匹配当前对象，符合条件的新生对象可参与。两种方式并存，战前配置与既有语义、范围和材料约束继续适用 | Accepted / Reference Model；Hypothesis。名单时点后续由G002-CORE-009明确，排序及表达框架随后按G002-CORE-010明确，具体条目待设计 | [用户确认](idea-inbox/2026-09-10-semantic-world-object-scope.md)、[素材](idea-materials/M-2026-09-10-instance-and-conditional-binding.md)、[采纳文本](draft-changes/D-2026-09-10-instance-and-conditional-binding.md) |

SW02采纳只包含引用模型；用户随后单独确认SW02-A，见下表。

## 2026-09-10：单次直接对象名单

| 编号 | 日期 | 决定 | 状态 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-009 | 2026-09-10 | SW02-A：完整法术开始处理时确定一次直接名单，本次不重选、追加或补位；逐对象仍检查当前合法性与材料，失效或固定消耗不足跳过且既有合法结果不回滚；本次新生或新符合条件对象留到后续释放 | Accepted / Target List；Hypothesis | [用户确认](idea-inbox/2026-09-10-semantic-world-object-scope.md)、[合格素材](idea-materials/M-2026-09-10-instance-and-conditional-binding.md)、[采纳文本](draft-changes/D-2026-09-10-single-release-target-list.md) |

用户同时要求一次性列出剩余决策。[R01–R32来源总表](idea-inbox/2026-09-10-semantic-world-remaining-decisions.md)保留批量建议；用户随后全部采纳，见G002-CORE-010。

## 2026-09-10：语义世界执行规则

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-010 | 2026-09-10 | 用户全部采用R01–R32推荐：明确对象与能力、条件与成本、位移与身份、复合对象短语、多端点、过程窗口及改期、释放开始仲裁、环境反应、配置资源与跨战权限 | Accepted / Semantic World Rules；Hypothesis。32项无遗留人工选择；内容、数值与体验待验证 | [用户确认](idea-inbox/2026-09-10-semantic-world-remaining-decisions.md)、[32条正式规则](idea-materials/M-2026-09-10-semantic-world-executable-rules.md)、[提案](idea-proposals/P-2026-09-10-semantic-world-executable-rules.md)、[评估](evaluations/E-2026-09-10-semantic-world-executable-rules.md)、[采纳文本](draft-changes/D-2026-09-10-semantic-world-executable-rules.md) |

R12允许明确法术位移与结构变化；R17允许明示独立遗体；R18允许名词位复合短语；R23允许改变当前剩余冷却；R24在释放开始仲裁共享槽。现用相关规则均按本决定同步，既有决定的采纳时文字从原始记录追溯。完整召唤、法杖起始资源与镶嵌、BF1–BF3仍后置；数值重新设计继续有效。

## 2026-09-10：简化对象交互与法术生成物

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-011 | 2026-09-10 | 以对象数量/状态变化为主；暂缓位移、连接、支撑、独立空间参照、定向/指定端点、环境份额/容器/配方/搬运加工；收集止于对象掉卡；增加火焰、雷电、冰霜等真实法术生成对象；允许继续设计不指定方向的抵挡/反弹及非指定接收者的作用转移 | Accepted / Scope and Flow；Hypothesis。具体效果与数值Unknown | [用户原话](idea-inbox/2026-09-10-simple-object-interactions.md)、[素材](idea-materials/M-2026-09-10-simple-object-interactions.md)、[提案](idea-proposals/P-2026-09-10-simple-object-interactions.md)、[评估](evaluations/E-2026-09-10-simple-object-interactions.md)、[采纳](draft-changes/D-2026-09-10-simple-object-interactions.md) |

这是对SW01及R01–R32当前操作范围的收束，已有身份、引用、单次名单、状态数量、时间与收益骨架继续有效。简单点燃/冰冻进入内容设计；燃料、传播、导电网络、坍塌及完整召唤/镶嵌仍后置。本轮未采纳首批候选的逻辑卡、路径/配方或介入额度。输入原文见[快照](../../../archive/2026-09-10-game-002-semantic-simplification-inputs/INDEX.md)。

## 2026-09-11：按特征识别法术类型

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-012 | 2026-09-11 | 简易看省略主语；状态、元素、召唤看参与句义的对应名词特征；一条法术保留全部命中类型。完成首批18词及例句归类，后续按四类讨论并交叉索引；上一批具体词效、参数及原定保护细则推进先搁置 | Accepted / Spell Classification；具体效果与数值Parked或按已有状态，证据Hypothesis | [用户原话](idea-inbox/2026-09-11-spell-type-system.md)、[素材](idea-materials/M-2026-09-11-spell-type-system.md)、[提案](idea-proposals/P-2026-09-11-spell-type-system.md)、[评估](evaluations/E-2026-09-11-spell-type-system.md)、[采纳文本](draft-changes/D-2026-09-11-spell-type-system.md) |

护甲按已有状态定义，“获得护甲”为简易＋状态；“火焰吞噬护甲”为元素＋状态；“恶魔释放火焰”为召唤＋元素。类型不由动词、输出效果、场上偶然存在的对象或本次成功与否决定。词义合法性与类型识别分别处理，状态主语简写例句不自动扩展通用语法或解锁复杂传播；完整召唤流程仍后置。

阶段调整保留18词作为分类对象，上一批6刻元素／一次使用、冰冻减伤、一次掉卡、参数及逐刻记录均为Parked。已有基础执行规则、对象范围和数值重设计约束继续有效。本次未恢复这些具体方案，后续按[类型入口](../docs/spell-type-index.md)展开。

## 2026-09-11：类型扩展与流派设计

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-013 | 2026-09-11 | 简易、状态、元素、召唤为可扩展的当前基础类型；类型关联后续流派设计。后续遇到未归类法术时主动检查可判定、可复用的新特征，适合时提出新类型及例句、与现有类型的关系、流派价值和待验证问题；用户采纳后同步分类与相关记录，保留所有命中类型 | Accepted / Extensible Classification；证据Hypothesis，具体新类型及流派内容待提出 | [用户补充](idea-inbox/2026-09-11-spell-type-system.md)、[素材](idea-materials/M-2026-09-11-spell-type-system.md)、[采纳文本](draft-changes/D-2026-09-11-extensible-spell-types.md) |

用户本轮明确要求类型可扩展，并授权后续适合时主动提出新类型。新类型按自身明确的特征定义；当前状态、元素、召唤三类仍按名词特征判定。流派需要具体组合、核心操作、收益、时间与词卡成本、弱点和混搭关系，类型标签本身不产生加成。本次没有新增第五类，首批18词与26项例句的现有分类保留；具体词效、数值与后置系统保持各自状态。

## 2026-09-11：超时疲劳

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-014 | 2026-09-11 | 超时进入疲劳，双方随时间扣生命，疲劳期间法术不能恢复生命；保留生命胜负与同检查点失败优先 | Accepted：FAT-A方向；FAT-C执行／数值Candidate，证据Hypothesis | [用户原话](idea-inbox/2026-09-11-overtime-fatigue.md)、[素材](idea-materials/M-2026-09-11-overtime-fatigue.md)、[提案](idea-proposals/P-2026-09-11-overtime-fatigue.md)、[评估](evaluations/E-2026-09-11-overtime-fatigue.md)、[采纳文本](draft-changes/D-2026-09-11-overtime-fatigue.md) |

NF-D01的方向已确定为疲劳；不采用“到验收截止即直接失败”的处理。具体触发刻、扣血曲线、护甲／打断及同刻细则仍为候选。既有报告仅对应其固定输入；本次没有新增其他词效或实现。

## 2026-09-11：全局规则边界与卡牌评测要求

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-015 | 2026-09-11 | 全部采用GR01–GR12推荐处理：参数归属／取整、冷却与取消、角色配对声明、状态归零、联合支付、存活资格与完整事件、事件声明、生成物与产出字段、候选合批、正常／极端评价范围及实际资源输入 | Accepted：处理方式／GR v1；证据Hypothesis。GR07-C01、FAT-C与数值目标仍Candidate，具体卡牌字段待设计 | [用户确认](idea-inbox/2026-09-11-global-rules-review.md)、[合格素材](idea-materials/M-2026-09-11-global-rule-boundaries.md)、[提案](idea-proposals/P-2026-09-11-global-rule-boundaries.md)、[评估](evaluations/E-2026-09-11-global-rule-boundaries.md)、[采纳文本](draft-changes/D-2026-09-11-global-rule-boundaries.md) |

本次逐项保留推荐的边界：GR07选择将同阶段派生延至下一刻作为待测候选，GR10选择保留完整FAT-C候选；不等于执行细则全部定稿。GR11评价范围已采纳，四层框架升至Candidate v0.3，数值不变。12项处理选择已结清；生成物、产出、死亡派生顺序与正式资源随相关内容补齐。测试交接TH-002/r4继续Draft／NotRun，用户下一次启动前不运行或分派，旧报告不改写。

## 2026-09-11：修饰词与系统设计顺序

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-016 | 2026-09-11 | 增加修饰词卡：形容词修饰名词，副词修饰动词；可多张直接挂原词，支付实体／时间成本；不兼容→适配→通用，特殊替代通用；数值仅修正本句，真实状态正常存续；适配看原词，同值按现有规则合并，不同附加效果从左到右。先补修饰词与镶嵌，再设计流派成套物品 | Accepted：Modifier v0.1基础模型；Hypothesis。具体词效、参数、获取及镶嵌细则仍待设计 | [四项确认](idea-inbox/2026-09-11-modifier-card-system.md)、[素材](idea-materials/M-2026-09-11-modifier-card-system.md)、[提案](idea-proposals/P-2026-09-11-modifier-card-system.md)、[评估](evaluations/E-2026-09-11-modifier-card-system.md)、[采纳文本](draft-changes/D-2026-09-11-modifier-card-system.md) |

休整第三候选沿剩余合格词范围接纳有资格的修饰词，不改变前两位和三选一结构。词卡新大类不等于新法术类型。镶嵌进入当前设计顺序，取代此前排期上的后置安排；既有槽位、获取和事件候选未自动采纳。TH-002/r5只积累MDT01–MDT09，未运行或分派测试。

## 2026-09-12：固定镶嵌、类型强化与范围被动

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-CORE-017 | 2026-09-12 | 每杖自带一个固定镶嵌，象征身份并规定基础范围及可选特殊效果；强化整条法术并关联类型／特征。简易加速按第2、4、6……周期各减1刻冷却，覆盖／打断也计，不永久累积；燃烧强化为范围内各来源施加增层，周期伤害不重加层 | Accepted：IN-A及两项例子含义；Hypothesis。IN-C01–IN-C14补充、具体物品与数值仍Candidate／Unknown | [用户定义和确认](idea-inbox/2026-09-12-wand-inlay-system.md)、[素材](idea-materials/M-2026-09-12-wand-inlay-system.md)、[提案](idea-proposals/P-2026-09-12-wand-inlay-system.md)、[评估](evaluations/E-2026-09-12-wand-inlay-system.md)、[采纳文本](draft-changes/D-2026-09-12-wand-inlay-system.md) |

用户授权agent先补获取、装配等规则，已形成固定身份＋可换槽位、商店渠道、同种／叠加、跨战及事件的完整候选，未将建议当作用户采纳。初始固定镶嵌的存在已明确；起始法杖数、范围参数和价格仍待设计。测试交接TH-002/r6增加IN-T01–IN-T10，未启动或分派测试。

## 效果登记工作流

| ID | 日期 | 决定 | 状态与证据 | 来源 |
| --- | --- | --- | --- | --- |
| G002-DOC-002 | 2026-09-12 | 建立跨系统效果注册、分类与边界理清；后续主动登记用户提出的效果，检查未来实现输入完整性，不做代码或具体架构 | Accepted / Documentation；效果与参数状态各自保留，价值Hypothesis | [用户原话](idea-inbox/2026-09-12-effect-registry.md)、[工作流素材](idea-materials/M-2026-09-12-effect-registry.md)、[系统入口](../docs/effect-registry/README.md) |

本轮建立32项登记、67项显式案例关系及未决审查，接入项目AGENTS、设计流程与测试交接r7。没有修改Core Concept v0.6或采纳新的具体效果；IN-C、GR07-C01、FAT-C与Parked词效保持各自状态。本轮只做文档一致性及设计可落地审查，未运行／分派玩法测试。

## 第一人称格子战场设计记录

| ID | 日期 | 记录 | 状态 | 来源 |
| --- | --- | --- | --- | --- |
| G002-BF-001 | 2026-09-12 | 用户要求第一人称2×5、敌人居中、地面／环境物性、生成物占位及火焰导致树草燃烧／烧焦；明确树草不继续传播 | 用户方向与单项确认；完整规则Draft Change，未改核心 | [素材](idea-materials/M-2026-09-12-first-person-grid-battlefield.md)、[GDD](gdd/GDD-2026-09-12-first-person-grid-battlefield.md)、[拟修改](draft-changes/D-2026-09-12-first-person-grid-battlefield.md) |

BF-C01–15为本次补全的推荐方案，未将用户对单层传播的回答扩为全部采纳。局部范围变化已列具体替换文本；原正式基线与Parked内容保持。新增FX-060–062、FX-003／010 r2候选，测试交接r9仅积累。
