# 设计决定与后续工作

当前：元素E3的30项卡面与机制方向已由用户确认并进入[正式素材](../game-design-workflow/idea-materials/M-2026-09-13-element-short-rule-card-pool.md)，剩余只补具体接口与参数，不重问整版选择。按用户要求完成[简易25项短规则候选](../game-design-workflow/idea-inbox/2026-09-13-simple-spell-short-rule-card-pool.md)，新简易卡面待用户筛选；旧连发／蓄势决定保留，不默认新提议已确认。

此前方向：[第三期短规则重设计](../game-design-workflow/idea-inbox/2026-09-13-element-spell-symbol-card-pool-03.md)为当前候选阅读入口。30项机制卡面，完整处理前两期78条；用户要求容易理解、允许规则修改、排除复杂规则句及单纯数值改动。先筛选易懂的规则，不用额外符号隐藏复杂账目；此前存储、延期、继承方案仅保留历史。

此前请求：重新设想一期元素法术，以动词／镶嵌为机制创新点。见[第二期30项描述](../game-design-workflow/idea-inbox/2026-09-13-element-spell-mechanism-card-pool-02.md)，含18项新机制。先筛选，暂不要求回答储量与事件细节；局部例外及所有新增效果均Raw。

此前2026-09-13进入[第二流派48项创意卡池](../game-design-workflow/idea-inbox/2026-09-13-element-spell-creative-card-pool.md)：先筛选名词、动词、形容词和镶嵌，不开展数值与成型。新增方向均Raw，冰冻增甲与消耗护甲命名沿已确认方向。以下机制缺项保留，不要求在创意发散前逐项回答。

最新三项已明确：环境有转化阈值，先形态变化，有相关释放才完成转元素，无释放停留末阶段；异种元素被抵消消散时，有释放新增对应元素，无释放不新增；草状态／法术第一阶段后置，仅保留草单位克制。见[元素规则EL04／06](../game-design-workflow/idea-materials/M-2026-09-12-element-spell-archetype.md)。阈值随各单位事先设置；异种元素替换的初始层数取经克制修正后抵消的余量，零余量不留下新元素。无相关释放法术仍不新增元素，环境转化仍继承对应状态层数。后续按需补阈值衡量判据、阶段条件、转化身份、补生位置与持续事件，不重问上述选择。

当前优先：[第二流派元素法术](../game-design-workflow/idea-materials/M-2026-09-12-element-spell-archetype.md)。已明确同种叠层／空格生成／满位施加、共享状态层数、固有火草冰克制及异种抵消顺序。下一步补环境转换与持续事件边界，成型后续讨论。简易期保留48项候选，点燃／冰冻动词已撤出；原50项描述为初设历史。

当前新增：[第一人称战场与环境草案](battlefield-and-environment.md)。用户明确2×5与单层火焰作用，BF-C01–15已补成具体推荐；[Draft Change](../game-design-workflow/draft-changes/D-2026-09-12-first-person-grid-battlefield.md)列出对核心场景／范围／传播文字的拟替换。整包待审阅，测试r9暂缓；下方原规则采纳记录仍为正式基线，不阻止本次候选设计。

## 当前新增：第一流派简易法术

2026-09-12已按用户要求进入流派与配套内容设计。[方向素材](../game-design-workflow/idea-materials/M-2026-09-12-simple-spell-archetype.md)已Qualified：基础牌组与混搭定位、连续完整法术每次参与共享槽、本杖简易法术成功积累并强化下一次伤害／护甲后清空。未修改核心。

用户最新调整：先进行创意发散，只给卡牌描述，暂不考虑平衡和数值；第一期最终候选四类各至少5项。已形成[50项Raw创意卡池](../game-design-workflow/idea-inbox/2026-09-12-simple-spell-creative-card-pool.md)：12名词、12动词、12形容词、14镶嵌，各6项建议优先保留。当前先筛创意，复诵版本与ER-Q13／14等规格问答延后；已登记FX-035–059，不形成测试输入。

日期：2026-09-12。状态：G002-CORE-012法术类型与G002-CORE-013类型扩展、G002-CORE-014疲劳方向与G002-CORE-015全局边界处理已采纳，对象范围继续按G002-CORE-011；Core Concept v0.6，证据Hypothesis。当前已完成[全局规则审查](global-rules-audit-2026-09-11.md)，已建立[效果登记](effect-registry/README.md)，按实际依赖补齐[修饰词与镶嵌](modifier-and-inlay-design.md)，再进入[卡牌与流派流程](card-design-review-workflow.md)，测试积累后合批；共用[四层数值框架](../game-design-workflow/idea-materials/M-2026-09-11-numerical-evaluation-framework.md)，继续按[类型入口](spell-type-index.md)组织。

## 当前已确定

| 范围 | 当前规则 | 依据 |
| --- | --- | --- |
| 战前与自动循环 | 完整库存构句，一卡一位置且同场一法术，一法术一法杖；首次冷却起点0–10刻 | [核心](../game-design-workflow/core-concept.md) |
| 引用与名单 | 实例保持身份，条件战前固定；每次开始确定一次直接名单，不追加、不重选、不补位 | [引用素材](../game-design-workflow/idea-materials/M-2026-09-10-instance-and-conditional-binding.md) |
| 时间与结果 | 释放开始仲裁，当前冷却改期最早下一刻；生命伤害打断、四阶段、整句成功与胜利终止 | [执行规则](../game-design-workflow/idea-materials/M-2026-09-10-semantic-world-executable-rules.md) |
| 对象交互 | 以数量、强度、剩余时间或状态改变为主；点燃/冰冻等简单变化进入当前内容设计 | [简化素材](../game-design-workflow/idea-materials/M-2026-09-10-simple-object-interactions.md) |
| 法术生成物 | 增加真实火焰、雷电、冰霜对象；身份/来源/窗口与宿主状态、演出分开 | 同上 |
| 资源收集 | 法术作用于合格对象后对象掉卡；资格与同名额度先检查，合法卡进入待领取整体收益 | [收益素材](../game-design-workflow/idea-materials/M-2026-09-06-normal-combat-word-rewards.md) |
| 超时疲劳 | 双方随时间扣减生命，法术不能恢复生命；沿用生命胜负，执行细则与数值候选 | [疲劳素材](../game-design-workflow/idea-materials/M-2026-09-11-overtime-fatigue.md) |
| 数值 | 全部重新设计；不使用示例默认值 | [数值任务](numerical-redesign.md) |
| 法术类型 | 简易看省略主语，状态/元素/召唤看名词特征；一条法术可同时命中多类；当前四类可以扩展，并为流派设计提供依据 | [类型素材](../game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |

## 当前暂缓

- 位移、连接、支撑、独立空间参照、指定飞行方向与玩家指定新受术端点。场景位置与范围判定仍保留。
- 环境材料份额、容器供材/收材、配方/合成、材料转移加工与物体复制。
- 完整召唤/指挥；法杖起始资源仍待明确。每杖固定镶嵌已明确，可换装配／获取等已有候选，见下方。
- 燃料、自动传播、导电网络和坍塌等复杂环境机制；简单点燃/冰冻已进入当前设计。

## 已处理的接口

C01伤害/生命支付与反馈、C02逐对象数量/成本及整句成功、C06产出资格、C08词卡时间用于冷却继续适用。C03/C04完整召唤及未来单位占位仍后置；C05固定镶嵌模型及两个示例已明确，其余规则见IN-C01–14候选。C07保留变化的发生/发展/结果表达，其复杂BF机制后置范围依上表；不再把简单点燃/冰冻一并阻挡。

R01–R32保留编号追踪，[现行规则表](../game-design-workflow/idea-materials/M-2026-09-10-semantic-world-executable-rules.md)直接陈述收束后的权限。G002-CORE-010是框架采纳记录，G002-CORE-011是当前范围修订；不要求重新回答这32项。

## 当前类型工作

已按用户明确指令采纳四类标准，完成首批18词归类及26项例句记录，包含全部用户例句；后续按[类型入口](spell-type-index.md)逐类讨论。护甲属于状态，因此“获得护甲”为简易＋状态；“恶魔释放火焰”为召唤＋元素。

上一批元素载体、冰冻减伤、对象一次掉卡、具体数值和逐刻方案先Parked，原定普通攻击保护/反弹/转移细则也暂停。基础执行规则与已采纳对象范围保持；数值重设计任务并未取消，但不把搁置方案作为默认值。

类型体系已确认可扩展，并关联后续流派设计。后续遇到未归类法术时主动检查可明确判定、可复用的新特征；适合时提出新类型的名称、特征、正反例、与现有类型的关系、流派价值和待验证问题，用户采纳后同步。当前没有新增类型或遗留人工选择，不需为扩展规则重复确认；TC23“我伤害敌人”保留现有结果，纳入后续扩展检查。

分类无需再确认四类标准。后续具体内容缺口按类记录：状态主语例句的完整语法/词义；元素的具体作用；召唤词义与完整流程边界；各类与交叉类型的收益。类型识别不替代句法和语义合法性，本次不据“燃烧蔓延／燃烧加倍”解锁新通用句式或复杂传播。

## 当前参数设计

用户已明确本轮同时给出参数定义和首轮测试数值，见[启动记录](../game-design-workflow/idea-inbox/2026-09-11-parameter-design-start.md)。现有[攻防Candidate v0.1](../game-design-workflow/idea-materials/M-2026-09-11-simple-spell-parameter-candidates.md)完成局部资格确认：通用参数、4种测试词、伤害敌人／获得护甲两句、共同敌人、4个代表配置及节奏敏感性。具体参数尚未Accepted；没有恢复被搁置的元素、冰冻或掉卡方案。

本轮结果供设计评议：以12刻敌方节奏作为入门测试候选，8、10刻作为压力样本。两种方案在快慢与损伤上有区别；护甲被击穿时会连带失去冷却机会，需要后续内容提供可解释的应对。限定计算与实现已独立复核；用户随后明确先建立四层框架，其他词效暂不展开。正式资源、经济和整局平衡仍待设计。

## 当前框架与待决问题

[四层框架Candidate v0.3](../game-design-workflow/idea-materials/M-2026-09-11-numerical-evaluation-framework.md)已经给出收益／时间方法、五个进度点的双方预算、跨战账本与EX01–EX09体验门槛。用户明确设计范围；具体指标目标仍为候选，不写成已通过结论。

| 编号 | 问题 | 推荐与当前状态 |
| --- | --- | --- |
| NF-D01 | 超时采用何种终局压力 | 已处理：G002-CORE-014采纳疲劳，双方随时间扣血且法术禁疗；不直接超时判负 |
| NF-D01-C | 疲劳执行细则与具体参数 | FAT-C01–08为候选：触发／周期／曲线、护甲与打断、同刻及禁疗；已加入下次批测积累，未作为正式默认值。EX02计入完整疲劳阶段 |
| NF-I01 | 阶段资源、获取分布、路线／恢复／价格尚未形成完整输入 | 按框架分层补齐；成长2.30／1.60等是目标预算，不是假定已获得属性 |
| NF-I02 | 卡池策略宽度、1倍速秒数与玩家理解证据不足 | 标NotEvaluable；不能从两句与自动检查证明无唯一最优或体验通过 |

## 全局规则审查与卡牌设计入口

四处表述修正已完成；用户已全部采用GR01–GR12推荐处理，见[GR v1素材](../game-design-workflow/idea-materials/M-2026-09-11-global-rule-boundaries.md)与[采纳文本](../game-design-workflow/draft-changes/D-2026-09-11-global-rule-boundaries.md)。12项处理选择已结清，不重复询问；卡牌进入可评测候选前补齐它实际涉及的具体声明或参数。

| 范围 | 当前处理 | 剩余工作 |
| --- | --- | --- |
| GR01–06 | 数值归属／截断、冷却取消、配对声明、归零、联合支付与存活资格已采纳 | 逐卡填参数域、角色／费用和死亡派生顺序 |
| GR07 | 事件声明与有限响应已采纳；同阶段派生延至下一刻为GR07-C01 Candidate | 相关事件卡按候选版本合批 |
| GR08–09 | 生成物和产出卡必填项已采纳 | 填当前卡的窗口、次数、空池、费用等 |
| GR10 | 保留完整FAT-C候选合批的处理已采纳 | 复用F06–F08，执行／数值尚未定稿 |
| GR11–12 | 正常／极端／玩家样本范围、固定实际资源输入已采纳 | 框架v0.3阈值仍候选，实际资源与体验证据按批补齐 |

用户要求暂不验证，积累到下一次一起测试；新增效果均先进入[登记与边界审查](effect-registry/README.md)，[修饰词与镶嵌](modifier-and-inlay-design.md)按实际依赖补齐，再按[设计—评测—采纳流程](card-design-review-workflow.md)处理流派成套物品。

## 修饰词与镶嵌

G002-CORE-016已采纳[Modifier v0.1](../game-design-workflow/idea-materials/M-2026-09-11-modifier-card-system.md)。形容词／副词、三类适配、直接多挂接、本句数值范围与固定结算顺序均明确，四项选择已结清。具体寒冷增幅、冰冻词义、寒冰／冰霜身份、吞噬语义和获取资格随内容补齐。

G002-CORE-017已明确每杖固定镶嵌定义身份、基础范围及可选特殊效果；两个例子的周期计数和范围含义已确认。获取／活动槽／替换、同种、叠加、激活、触发、跨战及收益边界已形成[IN-C01–IN-C14完整推荐候选](../game-design-workflow/idea-materials/M-2026-09-12-wand-inlay-system.md)，供本轮审阅，未全部采纳。具体法杖数、范围和价格等仍随内容设计；当前不启动测试。

## 测试交接

[固定测试交接](test-handoff.md)持续维护。上一批TH-2026-09-11-001已完成限定计算与demo验证，历史报告保留；TH-2026-09-11-002现为r7 Draft积累稿，保留r1／r2固定输入与待测项，追加全局边界、修饰词、镶嵌与后续物品候选；按用户指令暂不运行或分派测试。旧证据复评与新情境分开，合批启动前重新固定输入。执行状态以交接页为准，不重新执行已经通过且输入未变的完整726组，仅在发现差异或扩大范围时追加必要验证。

## 来源

- [本次用户原话与资格确认](../game-design-workflow/idea-inbox/2026-09-10-simple-object-interactions.md)。
- [本次采纳文本](../game-design-workflow/draft-changes/D-2026-09-10-simple-object-interactions.md)与[决策记录](../game-design-workflow/decision-log.md)。
- [C01–C08来源](../game-design-workflow/idea-inbox/2026-09-10-design-interface-questions.md)、[SW01/SW02来源](../game-design-workflow/idea-inbox/2026-09-10-semantic-world-object-scope.md)、[R01–R32来源](../game-design-workflow/idea-inbox/2026-09-10-semantic-world-remaining-decisions.md)。
- [本轮交付](semantic-world-simplification.md)及[修改前快照](../../../archive/2026-09-10-game-002-semantic-simplification-inputs/INDEX.md)。

当前分类来源：[2026-09-11用户原话](../game-design-workflow/idea-inbox/2026-09-11-spell-type-system.md)及[采纳文本](../game-design-workflow/draft-changes/D-2026-09-11-spell-type-system.md)。

类型扩展来源：[用户补充](../game-design-workflow/idea-inbox/2026-09-11-spell-type-system.md)及[G002-CORE-013采纳](../game-design-workflow/draft-changes/D-2026-09-11-extensible-spell-types.md)。

当前阶段来源：[本轮用户原话](../game-design-workflow/idea-inbox/2026-09-11-numerical-evaluation-framework.md)。

疲劳来源：[用户原话](../game-design-workflow/idea-inbox/2026-09-11-overtime-fatigue.md)、[G002-CORE-014](../game-design-workflow/draft-changes/D-2026-09-11-overtime-fatigue.md)。

全局边界来源：[用户批量确认](../game-design-workflow/idea-inbox/2026-09-11-global-rules-review.md)、[G002-CORE-015](../game-design-workflow/draft-changes/D-2026-09-11-global-rule-boundaries.md)。

## 效果登记后的内容缺项

用户已授权建立效果注册与理清工作流（G002-DOC-002），现有59项效果／方向与67项案例已登记，后续效果主动维护。具体缺项集中在[ER-Q01–12](effect-registry/readiness-review.md)：燃烧／冰冻词义、寒冰身份、吞噬关系、寒冷两个分支、元素窗口、镶嵌候选依赖、保护／转移细则及有限产出等。它们是逐效补齐任务，不是重新选择已采纳框架；当前没有因本轮工作流而产生的新即时审批项。

## 战场补充方案的集中审阅

不重问第一人称、2×5、环境／生成物占位及树草不传播。需审阅的补充为：每格地面＋单占位、正交邻近、敌人和火焰确定落点、独立火焰有限脉冲、燃烧量驱动两级环境阈值、烧焦保留身份／树占位、无隐含资源产出。完整推荐与理由在GDD的BF-C01–15；不是15个必须逐条重问的阻塞问题。参数以后按用户节奏补齐。
