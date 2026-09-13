# game-002 领域词汇

当前核心：Core Concept v0.6 / Stable Design Baseline。本文只定义领域术语；证据状态为Hypothesis。

| 术语 | 定义 | 依据 |
| --- | --- | --- |
| 卡面短规则 | 使用固定对象符号，按一次转换、一个触发或一条替换表达效果；属于显示约定，不取代实体词卡与句法。“改为”只执行替换后的结果。 | [已确认元素卡面素材](game-design-workflow/idea-materials/M-2026-09-13-element-short-rule-card-pool.md) |
| 环境转化阈值 | 随各环境单位事先设置的转化阈值；单位先经历形态阶段，处于相关释放法术作用下才最终消失变为元素，无释放则停留末阶段。具体判据另行定义。 | [元素方向EL04](game-design-workflow/idea-materials/M-2026-09-12-element-spell-archetype.md) |
| 单位固有属性 | 单位自身携带的火／草／冰或无属性等身份性质，用于元素克制判断，区别于当前携带状态。 | [元素方向](game-design-workflow/idea-materials/M-2026-09-12-element-spell-archetype.md) |
| 元素状态 | 单位身上可积累与消耗的元素状态；当前方向规定每单位最多一种，异种施加先抵消再替换，不限制非元素状态共存。 | [元素方向](game-design-workflow/idea-materials/M-2026-09-12-element-spell-archetype.md) |
| 元素共享层数 | 元素本体与它携带的对应状态共用的一份层数；归零时元素消失，环境转化为元素时继承对应状态层数。 | [元素方向](game-design-workflow/idea-materials/M-2026-09-12-element-spell-archetype.md) |
| 战前构句 | 从完整战外库存分配实体词卡，依据词性、句式和语义形成完整法术；配置不推进战斗时间。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-grammar-and-semantic-compatibility.md) |
| 战外词卡库存 | 本局战斗外持有的普通词卡集合，供每场战前配置；同名普通词最多三张。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-word-inventory-and-copies.md) |
| 实体词卡分配 | 一张实体卡在本次配置中只归属一条法术且占一个位置；同名重复需要对应副本。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-word-inventory-and-copies.md) |
| 循环法术 | 一个组合定义的完整法术，按既定冷却与释放周期持续尝试。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-casting-time-and-interruption.md) |
| 首次冷却起点 | 战前为各法术选择的第0–10刻内开始第一次冷却的时刻。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-casting-time-and-interruption.md) |
| 循环周期 | 冷却时长加释放时长；冷却由实际词卡时间贡献合计形成，释放时长单独设计。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-casting-time-and-interruption.md) |
| 共享释放槽 | 所有法术在每刻竞争一次释放开始机会的共同约束；直接效果在开始时结算一次，持续作用由过程或状态承载。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-timeline-schedule-preview.md) |
| 法杖顺序与覆盖 | 战前设置的法杖前后顺序；同刻靠后法术覆盖靠前法术，被覆盖者本次无效果、无特效，后续周期保持。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-timeline-schedule-preview.md) |
| 生命伤害打断 | 玩家实际承受生命伤害时取消当时正在冷却的普通法术本次机会，后续周期保持，已结算结果不回退。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-damage-armor-and-interruption.md) |
| 对象引用 | 法术指向战斗对象的方式，支持固定实例身份和战前固定条件两种绑定；对象仍须满足当前作用条件。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-10-instance-and-conditional-binding.md) |
| 对象失效 | 对象不再具备该法术的作用条件；释放时跳过并继续其他合法对象，失效尝试仍保留释放特效。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-basic-sentence-targeting-and-locking.md) |
| 环境对象 | 长方形场景中有位置且可操作、没有生命值和攻击行为的对象，例如大树和溪流。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-basic-sentence-targeting-and-locking.md) |
| 法杖与镶嵌 | 每根法杖承载一条法术，自带固定镶嵌定义身份、基础范围与可选特效；活动槽及获取等见候选。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-07-wand-inlay-configuration.md) |
| 固定镶嵌 | 随法杖自带的身份组成，规定其基础范围与可选特殊效果。 | [镶嵌素材](game-design-workflow/idea-materials/M-2026-09-12-wand-inlay-system.md) |
| 范围被动 | 以法杖范围和明确作用事件为条件的效果；可对其他来源生效，区别于仅强化本杖。 | [镶嵌素材](game-design-workflow/idea-materials/M-2026-09-12-wand-inlay-system.md) |
| 词卡类别与句法角色 | 名词、动词、修饰词是词卡大类；形容词修饰名词，副词修饰动词。主语、谓语、宾语是位置职责，修饰词不独立占据这些角色。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-11-modifier-card-system.md) |
| 修饰词挂接 | 每张修饰词直接指向本句一个原词出现位置，多张可共同挂接，不递归修饰。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-11-modifier-card-system.md) |
| 通用／适配／不兼容 | 修饰词针对原词声明的三类关系；不兼容禁止组合，适配采用替代通用的特殊版本。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-11-modifier-card-system.md) |
| 本句数值修正 | 只改变当前法术计算采用的数值，不永久改写场上原值；实际产生的状态按自身规则存续。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-11-modifier-card-system.md) |
| 执行者、操作内容与受术目标 | 谁执行、直接处理什么以及结果落在谁身上三个语义关系，具体词义分别声明。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-flexible-sentences-and-subject-roles.md) |
| 法术类型 | 根据句子的明确特征得到的可扩展分类，简易、状态、元素、召唤为当前基础类型；一条法术保留全部命中类型，区别于词性、实际效果与本次成功。 | [类型素材](game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |
| 简易法术 | 省略显式主语的法术；默认玩家语义补全不取消简易特征。 | [类型素材](game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |
| 状态法术 | 参与句义的名词中出现状态的法术，例如护甲、燃烧、冰冻状态；产生状态的动词本身不满足此特征。 | [类型素材](game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |
| 元素法术 | 参与句义的名词中出现火焰、雷电、冰霜等元素的法术。 | [类型素材](game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |
| 召唤法术 | 参与句义的名词中出现召唤物的法术；类型不等于本次实际生成单位。 | [类型素材](game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |
| 多类型法术 | 同一条法术同时命中多个类型特征；多标签不增加效果、释放或实体词卡次数。 | [类型素材](game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |
| 流派 | 围绕具体法术组合形成的玩法方向，说明核心操作、收益、时间与词卡成本、弱点及混搭关系；类型提供分类依据，类型与流派不强制一一对应，标签本身不产生加成。 | [流派规则](game-design-workflow/idea-materials/M-2026-09-07-supporting-design-rules.md)、[类型素材](game-design-workflow/idea-materials/M-2026-09-11-spell-type-system.md) |
| 状态引用 | 配置对应词卡后操作战场状态的语义权限；引用本身不自动消耗状态。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-battle-state-persistence.md) |
| 护甲 | 按数量累积的防护状态，普通伤害先等量消耗护甲，溢出扣生命；无自然到期与自动周期。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-armor-identity-generation-and-persistence.md) |
| 状态重施 | 同目标同种合并，可累积数量相加、有限剩余时长相加，保留原周期和排序位置。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-status-reapplication-and-stacking.md) |
| 状态周期 | 自生效起经过完整正周期后首次触发，随后按周期推进；每次开始读取当前量。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-status-timing-and-expiration.md) |
| 状态内部顺序 | 按首次生效、产生效果先后及效果固定顺序逐状态处理，周期和到期后分别检查。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-status-values-and-resolution-order.md) |
| 源方修正 | 实际执行者自身适用的强度修正，每次法术开始结算时读取；不自动共享到其他单位。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-spell-effect-sources-and-modifiers.md) |
| 周期强化继承 | 适用增幅先计入新增状态量，周期使用当前合并量，不重复应用这份增幅。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-07-periodic-state-modifier-inheritance.md) |
| 召唤种类词与单位身份 | 种类词表达一类单位，身份引用只指具体单位；当前不新增专属引用词卡，战前占位的具体机制后置。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-summon-unit-and-reference.md) |
| 战斗胜负 | 完整事件后的结果检查：全部敌人击败且玩家存活则胜利，玩家生命耗尽则失败；同检查点失败优先。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-normal-combat-outcomes.md) |
| 整体收益包 | 战后金币与法术产生的卡牌共同组成的领取对象，玩家整体领取或放弃。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-normal-combat-word-rewards.md) |
| 战斗耗时奖金 | 按共用战斗时间从0到胜利的经过量及遭遇预设基准计算，有上限、最低0。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-07-combat-gold-and-efficiency-bonus.md) |
| 休整取舍 | 在独立休整节点选择一次有限恢复或可用的词卡三候选选一；选词后拒收不返还恢复机会。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-05-rest-recovery-and-word-choice.md) |
| 商店货架 | 到店后公开且本次固定的商品与标价，每条目一份，售出不补货，交易检查资格和余额。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-07-shop-shelves-and-transactions.md) |
| 单向分叉路线 | 本局开始按约束生成且保持稳定的路线；分叉可选，进入后不撤回，完成节点不回访。 | [对应素材](game-design-workflow/idea-materials/M-2026-09-06-branching-run-routes.md) |
| 生命支付 | 由效果明确声明的生命代价，不自动归类为伤害；默认支付后须存活，自毁需专门声明。 | [接口素材](game-design-workflow/idea-materials/M-2026-09-10-accepted-design-interfaces.md) |
| 法术成功事件 | 完整法术至少有一个对象合法结算时产生的一次事件；合法零值可满足，多个对象不重复计次。 | [接口素材](game-design-workflow/idea-materials/M-2026-09-10-accepted-design-interfaces.md) |
| 待领取产出 | 本场已经合法产生、尚未加入战外持有资源的收益；造卡资格计入其中同名副本。 | [接口素材](game-design-workflow/idea-materials/M-2026-09-10-accepted-design-interfaces.md) |
| 单位占位 | 用于战前明确未来单位身份与出生关系的后续设计方向；具体机制尚未形成。 | [接口素材](game-design-workflow/idea-materials/M-2026-09-10-accepted-design-interfaces.md) |

接口处理范围见[设计决定与后续工作](docs/design-decisions-needed.md)，具体参数按[数值任务](docs/numerical-redesign.md)重新设计。

## 语义世界对象范围

**语义世界**：具有明确对象结构、交互能力与执行规则的战斗世界，玩家构成的法术句子在其中产生结果。当前范围以单位、环境物体、法术生成物、属性状态与未完成过程为主，变化落在明示数量或状态。
_避免_：以画面出现的任何内容都能接受任意动词，代替明确的对象能力。

**过程对象**：战斗中发生或持续的一项作用及其进程，例如飞行物、敌方攻击与法术冷却；具体引用和可操作内容由对应机制定义。
_避免_：把一次真实过程、整个循环规则和释放演出视为同一个对象。

**世界基础规则**：战斗世界的共同约束，包括胜负判定和全局结算顺序；SW01范围中保持固定。
_避免_：把改变某次攻击或冷却等同于修改整个战斗的结算规则。

依据：[已确认的SW01范围](game-design-workflow/idea-materials/M-2026-09-10-semantic-world-object-scope.md)。

## 对象引用

**实例绑定**：战前明确所指对象身份、后续释放持续尝试该对象的引用方式；对象失效时跳过。
_避免_：将同名新对象视为原实例，或失效时隐式转为条件搜索。

**条件绑定**：战前固定选择条件、每次释放匹配当前符合条件对象的引用方式；符合条件的新生对象可以参与。
_避免_：把绑定条件固定等同于匹配结果整场固定。

依据：[SW02引用模型](game-design-workflow/idea-materials/M-2026-09-10-instance-and-conditional-binding.md)。SW02-A名单时点及R05–R11引用、排序与成本规则均已确认。

**单次直接对象名单**：每次完整法术开始处理时确定的直接作用对象。本次不重选、追加或补位；逐对象仍读取当前合法性与状态数量/成本，新符合条件对象留到后续释放。名单不冻结世界状态，也不预留状态量/成本。依据：[SW02-A采纳](game-design-workflow/draft-changes/D-2026-09-10-single-release-target-list.md)。

## 对象交互与执行

以下术语依据[已采纳R01–R32](game-design-workflow/idea-materials/M-2026-09-10-semantic-world-executable-rules.md)。

| 术语 | 定义 |
| --- | --- |
| 语义身份 | 区分具体对象及延续关系的身份；同名不代表同一对象。 |
| 对象粒度 | 内容明示的可引用层级；当前以单位、环境物体、真实生成物、属性状态与过程为主。 |
| 交互能力 | 由对象类别、当前数量/状态与明示词义决定的作用资格；不隐含空间、结构或环境供材能力。 |
| 复合对象短语 | 在基础句式名词位置表达宿主状态、条件或来源关系的组合；新增词义由实际实体词卡承担。 |
| 选择优先级 | 在符合条件的对象中选择单个或限量对象的明示方式，与处理已选对象的顺序分别定义。 |
| 公开对象顺序 | 初始对象的公开顺序及新生对象按确定生成先后获得的位置；不意味着本次直接名单持续追加。 |
| 一次性成本 | 一次法术只支付一次的费用，与首个可执行对象固定费用联合检查后提交；无合法对象不付，与逐对象费用分开。 |
| 范围锚点 | 战前指定、用于确定法杖范围实际覆盖的位置参照；用于范围判定；当前不提供改变位置或编辑空间的操作。 |
| 独立遗体或残留物 | 内容明确在单位死亡后生成的环境对象，具备自己的身份与能力；不等于原单位继续存活。 |
| 当前剩余冷却 | 某次尚未完成冷却还需要经过的时间，可被适用法术修改；区别于词卡贡献决定的基础冷却。 |
| 可介入窗口 | 尚未完成的过程允许指定操作生效的阶段或时段；演出与已完成记录不提供回滚权限。 |
| 反应根因 | 后置复杂传播设计中的来源追踪概念；当前不展开传播链。 |
| 运行状态与配置 | 运行状态是当前对象与过程情况；配置是战前词卡分配、绑定条件、法杖顺序和镶嵌安排。 |

## 简单对象交互

依据：[G002-CORE-011](game-design-workflow/idea-materials/M-2026-09-10-simple-object-interactions.md)。

| 术语 | 定义 |
| --- | --- |
| 简单对象变化 | 明示法术使对象数量、强度、剩余时间或状态改变，不要求空间/结构或材料加工步骤。 |
| 法术生成物 | 法术产生、真实存在且能受到后续合法作用的新对象，例如火焰、雷电、冰霜；有独立身份、来源和实际窗口。 |
| 燃烧/冰冻状态 | 附着在宿主上的状态，区别于真实火焰/冰霜生成物；燃烧对应伤害，冰冻按2026-09-13方向增加护甲；具体获得时点、持续及结束效果由词义声明。 |
| 对象掉卡 | 收集法术合法作用于对象后，按资格与额度产生卡牌并记录待领取的结果，不包含材料提取、加工、运输或手动拾取。 |
| 抵挡 | 按词义减少或抵消尚未交付的作用，不指定飞行方向，不回滚已发生结果。 |
| 非定向反弹 | 玩家不指定方向的作用处理类别；自动归宿、失效与限制由具体词义确定。 |
| 非指定转移 | 玩家不指定新接收者，由词义固定规则处理当前作用的接收；不是材料或资源搬运。 |

## 超时疲劳

**疲劳**：战斗超时后双方持续扣减生命、法术不能恢复生命的全局战斗规则。
_避免_：将疲劳当成新增名词词卡、可驱散状态或直接超时判负。

依据：[G002-CORE-014疲劳方向](game-design-workflow/idea-materials/M-2026-09-11-overtime-fatigue.md)。具体执行与数值候选不作为术语默认参数。

## 卡牌共用边界

以下术语依据[GR v1](game-design-workflow/idea-materials/M-2026-09-11-global-rule-boundaries.md)，不包含候选参数。

**名义释放段**：当前机会计划占用的释放时段，即使被取消也保留其结束时点作为续排基础冷却的依据。
_避免_：把取消理解为立即重启周期，或通过改期恢复取消机会。

**存活操作资格**：单位作为存活执行者或受术对象的资格，生命归零即失去；区别于完整事件结束后完成的离场与胜负检查。
_避免_：把尚未处理离场视为仍能作为存活单位行动。

**数量状态耗尽**：数量型状态消耗至0的情形，默认结束该状态身份、计时与排序；有无型及特殊零值由状态独立声明。
_避免_：用合法零值成功证明场上仍存在零量状态。

**正常体验样本**：评测前登记正常资源、生命与遭遇条件的配置群体，区别于合法极端配置和真实玩家选择分布。
_避免_：依据测试结果事后剔除失败或残血样本。

## 效果登记术语

| 术语 | 含义 |
| --- | --- |
| 效果ID | FX稳定编号，供词卡、修饰词、镶嵌、流派及案例复用；不等于实体卡或法术类型 |
| 效果行为分类 | 按改变的数量、状态、对象、过程、条件修饰或产出分类，可多选；与法术类型分别判断 |
| 语义闭合 | 适用字段和依赖完整，给定输入能唯一裁定；不代表数值已验证或已实现 |
| 批次就绪 | 明确本批规则／候选版本、参数、资源、场景、预期与输入提交；还须用户启动才执行 |
| 登记与来源 | 框架负责通用约束，登记维护效果摘要、依赖和缺口；来源采纳及参数状态分别保留 |

完整入口：[效果注册与理清](docs/effect-registry/README.md)。后续讨论主动登记；未定或Parked案例不能因获得FX编号进入正式实现规格。

## 格子战场草案术语

本节描述[战场GDD候选](game-design-workflow/gdd/GDD-2026-09-12-first-person-grid-battlefield.md)，未替换上方正式基线术语。用户明确方向与推荐细则按BF-A／BF-C区分。

| 术语 | 本轮定义 |
| --- | --- |
| 第一人称战场 | 玩家位于战场近端，正面观察敌人与环境；不是自由移动或战中瞄准 |
| 前后两排 | 近排F、远排B，各5列；不是敌我两方阵营行 |
| 格子地面 | 具有独立地表属性与状态的格子对象；无占位物时仍存在 |
| 环境占位体 | 树、石块等占格物体；不自动拥有战斗单位生命或自主攻击 |
| 点燃／燃烧 | 点燃为动作；燃烧为宿主数量状态，不新增同义“点燃状态” |
| 燃烧形态／烧焦形态 | 环境对象依自身阈值改变的形态与资格，不等于换身份 |
| 邻近脉冲 | 火焰的明示后续环境作用；候选为本格地面及正交邻格，树草不派生同类作用 |

当前动作名称：消耗护甲（原名“吞噬护甲”）。2026-09-13用户要求仅改名，原消耗护甲转执行元素层数的推荐效果保持不变，具体规格以FX-023及来源素材为准。
