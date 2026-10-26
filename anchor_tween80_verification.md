# Tween 80 锚点复算与核查记录

> 本文档记录"用 Tween 80 作锚点"这一步的实际输入、计算与原文核查结果。
> 目标：确认同一化合物在不同 HLB 公式下确实得到不同数值，从而证明
> "必须按同一公式先算锚点、再做相对比较"的必要性。

## 1. 原文锚点值（已逐字核对）

| 来源 | 原文位置 | Tween 80 的描述 | HLB 值 |
|---|---|---|---|
| Griffin 1954, Table 1 | J. Soc. Cosmet. Chem. 5(4), p.255 | Polyoxyethylene sorbitan monooleate | **15.0** |
| Davies 1957, Table II | Proc. 2nd Int. Congr. Surface Activity, p.430 | sorbitan "mono-oleate" + 20 (CH2-CH2-O) | 实验 **15**；基团法 **15.8** |

- Griffin 原文在 Table 1 表头注明：HLB 值 "believed to be correct to ±1"（±1 误差）。
- Davies 原文 Table II 同时列出"HLB from expt"和"HLB from group numbers"两列；
  Tween 80 一行即 15 与 15.8。
- Davies 原文 Table II 脚注："Calculated values for 'mono-oleates' assume these are
  1.38 oleates"——即他的计算假定商业"单油酸酯"实际平均含 1.38 个油酸酯基团。

## 2. 公式与基团数（原文提取）

Griffin（1954, p.251）：
- 多元醇脂肪酸酯：`HLB = 20 (1 - S/A)`，S=皂化值，A=酸的酸值。
- 皂化数据不佳：`HLB = (E + P)/5`，E=环氧乙烷质量%，P=多元醇质量%。
- 仅 EO 为亲水部分：`HLB = E/5`。

Davies（1957, p.430 式 (9)；p.431 Table III）：
- `HLB = 7 + Σ(亲水基团数) - 0.475 × n`，n=亲油基团个数。
- 亲水：-SO4Na 38.7、-COOK 21.1、-COONa 19.1、叔胺 N 9.4、
  酯(失水山梨醇环) 6.8、酯(游离) 2.4、-COOH 2.1、-OH(游离) 1.9、
  -O- 1.3、-OH(失水山梨醇环) 0.5；派生基团 -(CH2CH2O)- = +0.33。
- 亲油（每个 -0.475）：-CH-、-CH2-、CH3-、=CH-。

## 3. 公式实现的自检（用简单分子核对 Davies Table II）

在 hlb.py 中用同一实现计算，并与 Davies 原文 Table II 的数值对照：

| 分子 | 本实现 | Davies Table II | 一致 |
|---|---|---|---|
| 正丁醇 CH3(CH2)3OH | 7.00 | 7.0 | ✓ |
| 乙醇 CH3CH2OH | 7.95 | 7.9 | ✓（四舍五入） |
| 油酸 C17H33COOH | 1.03 | 1.0 | ✓（四舍五入） |

结论：Davies 公式与 Table III 基团数的提取、实现无误。

## 4. Tween 80 锚点复算（多种口径并排）

结构模型：聚氧乙烯(20)失水山梨醇单油酸酯，理想单酯，C64H124O26。
分子量：失水山梨醇 C6H12O5=164.1565；EO C2H4O=44.0526；油酸 C18H34O2=282.4614；
Tween 80 总计 = 1309.6538。

| 口径 | 公式 | 结果 |
|---|---|---|
| Griffin 原文 Table 1 | — | **15.0**（±1） |
| Griffin 皂化值法 | 20(1-S/A)，S=50, A=198.6 | 14.97 |
| Griffin 质量分数（Mh=总-油酸） | 20×1027.19/1309.65 | 15.69 |
| Griffin 质量分数（Mh=多元醇+EO） | 20×1045.21/1309.65 | 15.96 |
| Davies 原文 Table II | 基团法（含"1.38 oleates"假设） | **15.8** |
| Davies 朴素单酯约定（本文代码默认） | 7+6.8+2×0.5+20×0.33−17×0.475 | 13.33 |

## 5. 结论（对方法论的支撑）

1. 同一个 Tween 80，从结构出发用不同公式/口径，数值落在 **13.3 ~ 16.0**；
   只有 Griffin 原文 Table 1 的 15.0 是"公认锚点"。
2. Davies 方法对简单分子能精确复现（第 3 节），但对 Tween 80 的原文 15.8
   无法用朴素单酯模型复现，差异指向原文脚注"1.38 oleates"等未完全写明的
   结构假设——这是"结论核查"中发现的关键点。
3. 因此本项目采用**锚点相对比较法**：对每个公式，先算 Tween 80（同一套
   基团计数约定），再算目标物，报告二者的绝对值和相对差/比值，而不是把
   不同公式的绝对值直接互比。
