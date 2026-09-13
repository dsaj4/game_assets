# game-002 代码开发进度

日期：2026-09-13。设计依据：[Core Concept v0.6](../game-design-workflow/core-concept.md)。

| 里程碑 | 设计来源 | 状态与证据 | 阻塞与下一步 |
| --- | --- | --- | --- |
| 战前配置与完整自动战斗 | 当前核心及[正式素材](../game-design-workflow/idea-materials/README.md) | Planned；尚无符合当前全流程的实现验收证据 | [接口范围](design-decisions-needed.md)已确认；先建立当前规则所需参数，再登记实现与验证 |
| 时间、覆盖、打断与终止验证 | 当前核心及[攻防候选v0.1](../game-design-workflow/idea-materials/M-2026-09-11-simple-spell-parameter-candidates.md) | Limited Verified：TH-2026-09-11-001/r2的726组逐事件差分与10项规则边界通过；[报告](test-reports/TH-2026-09-11-001-r2-run-01.md) | 仅两句攻防、固定单敌；其他词义和完整流程未验收 |
| 超时疲劳 | [G002-CORE-014与FAT-C候选](../game-design-workflow/idea-materials/M-2026-09-11-overtime-fatigue.md) | Limited Experimental Evidence：TH-003/r1独立模型验证无恢复条件的有限终局与归因；[报告](test-reports/TH-2026-09-13-003-r1-run-01.md) | demo尚未接入；加入治疗、复活或生命上限变化须重新检查，不外推完整玩法 |
| 词义、数值与路线验证 | 当前合格素材及[数值重设计任务](numerical-redesign.md) | Planned；候选参数不等于已平衡 | 重新建立输入并完成资格确认，再验证完整规则关系 |

可用实现资源目录为 E:/Project/game-002-glyph-timeline；本次未检查或修改该目录，不能据目录存在推定当前设计已实现。[实现记录快照](../../../archive/2026-09-10-game-002-design-originals/workspaces/game-002/docs/code-development-index.md)保留已登记的提交、测试范围及原始证据。

## 关联demo数值测试注册

按用户2026-09-11指定的「时序施法原型」任务，另登记`E:/Project/yanzhou-pixel-lab`为本轮可玩数值测试实现；不替换上述资源身份，不视为完整v0.6实现。

| 项目 | 当前记录 |
| --- | --- |
| 设计与参数 | 固定提交1d4bb7faff715f787cba31794829fc8c6527a1c1；Candidate v0.1，未Accepted |
| 实现提交 | 8347088f5e56d46bdc39793cfeb2b59ef01dba33；分支codex/test-agent-candidate-v01，本地已提交，无远端 |
| 测试协作 | [固定交接](test-handoff.md)，TH-2026-09-11-001 / r2，Codex测试agent任务01a08e19-0acb-7cb2-a022-1f54ec6c308d |
| 可玩入口 | [本地demo](http://127.0.0.1:5199/)；根目录已有启动言咒.cmd |
| 已覆盖 | 四种攻防配置、8/10/12刻敌人节奏、六张实体卡、两根法杖、单敌、时间编排、自动战斗、记录导出入口；页面共用引擎726组与独立模型一致，构建与包装检查通过 |
| 实现边界 | 原v0.5视觉资产复用，旧火焰/雷电/回响与金币参数不参与本包；每次重试还原输入生命。范围恒定许可、无跨战成长；浏览器交互和玩家体验未验收 |
| 技术细节与证据 | [代码仓库测试维护说明](E:/Project/yanzhou-pixel-lab/docs/numerical-testing.md)、[实现哈希与事件清单](E:/Project/yanzhou-pixel-lab/docs/test-evidence/TH-2026-09-11-001-r2-run-01/verification.json) |
| 下一步 | 当前先审查数值框架与疲劳候选；后续实现疲劳须登记新设计／实现版本并独立验证。T01/T02玩家可读性测试仍未执行 |

技术细节与测试结果写在对应代码仓库；本索引只记录里程碑、证据、阻塞和下一步。代码完成度不能提升核心或素材的证据状态。

## 2026-09-13 两流派独立数值实验

用户要求自行设初值，明确允许补临时实验规则，并要求本轮无需注册demo。已完成[TH-2026-09-13-003/r1/run-01](test-reports/TH-2026-09-13-003-r1-run-01.md)，状态为Completed / Limited Experimental Evidence；正式规则、S2素材资格与旧demo配置保持原状态。

| 项目 | 当前记录 |
| --- | --- |
| 设计输入 | 16231ee77e389864b10dd4de15d328cccf071d0a；简易方向、EL01–07及选定E3子集；S2新卡仅Raw实验 |
| 实现位置 | [独立实验仓库](E:/Project/game-002-numerical-lab/README.md)，非可玩实现，无demo依赖 |
| 实现与结果 | codex/archetype-tests-2026-09-13；2d783252999f7de703a9e6938d9840c4b408b847，本地已提交、无远端；输入冻结83b3f3c |
| 完成证据 | 17424场主矩阵、6534场数值敏感性、484场临时规则对照、4962场连续生命账本，共29404场；14项规则检查及数据完整性检查通过 |
| 覆盖界限 | 16构筑、9场景、两杖起点0–10；固定单敌与单目标邻近关系，尚非完整2×5环境／全卡池／真实经济／玩家试玩 |
| 主要发现 | 简易复诵较快；元素普通场景可持续，但快攻弱、冰冻结算分支敏感；空心＋自噬与衰减取整需设计裁决 |
| 下一步 | 先决定冰冻增甲及小数衰减接口，再复核脉冲3层候选的压力场景；扩展未测E3组合与空间过滤 |

完整技术输入、实现、复现步骤与逐场证据保留在独立代码仓库。此批不证明当前两流派已能在demo游玩。

## 2026-09-13 自动平衡校准

用户要求先定标准／硬规则、再定任务／临时规则，最后模拟与自动调整。已实现[自动校准流程](automatic-balance-calibration.md)，[CAL-2026-09-13-001/r3报告](test-reports/CAL-2026-09-13-001-r3-run-01.md)为限定任务达标证据，未接入demo。

| 项目 | 当前记录 |
| --- | --- |
| 实现 | [独立数值校准器](E:/Project/game-002-numerical-lab/CALIBRATION.md)；codex/archetype-tests-2026-09-13，9657353e09ed168f9d576617ce8b81ccdaf7d847；本地已提交，无远端 |
| 输入与范围 | 保留TH-003引擎；H01–H08、四代表、四训练场景、允许数值域与临时结算先冻结；机制与标准不进入搜索 |
| 执行 | r1共720点无解，r2共192点无解，r3共60点中18点训练可行；三轮合计975659场，选定候选后一次留出验证 |
| 验证 | r3新敌人1452场、全16配置×9场景×121起点回归17424场、三连战实际5260场；24项检查及三轮版本／选优／统计审计通过 |
| 交付 | [独立候选参数包](E:/Project/game-002-numerical-lab/calibrated-candidate-r3.json)，状态CalibratedCandidate；原TH-003参数和所有失败记录保留 |
| 限制与下一步 | 普通防御损耗中位为0，须为战斗压力和防御机会成本另立任务；全卡池、真实经济、战场与体验未验收 |

修订内自动调参已运行；外层参数域扩大由agent明确制定后重新冻结。当前没有自动改机制、改验收标准或发布参数的权限流程。数值满足本任务不能升级为核心玩法Accepted。

## 2026-09-13 外部技术选型调研

用户要求调研Astra游戏开发案例，并明确目标为持续开发可发布的独立游戏。[案例与选型研究](../research/03-product-case-studies/2026-09-13-astra-game-development-stack.md)推荐Godot、带类型标注的GDScript与Blender，状态为Research / Recommendation / Proposed。尚未确定为本项目技术栈，未审查或迁移既有代码，未运行游戏测试；现有实现里程碑保持原状态。下一步在启动实现时结合首发平台、目标设备与既有代码审查决定是否采用。

同日补充[生成工作流与Blender MCP比较](../research/03-product-case-studies/2026-09-13-godot-blender-workflow-comparison.md)：推荐原生Godot主项目、Blender脚本生产与单一Blender MCP交互桥接；Godogen／GodotMaker用于独立实验或方法参考。状态仍为Research / Recommendation，未安装、运行或采纳工具链。
