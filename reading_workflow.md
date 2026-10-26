# AI 文献阅读工作流（真实输入与核查记录）

> 本文档记录本次实践实际使用的检索、读取、公式提取与核查过程，供读者复现。
> 执行环境：SciMaster 科研 Agent（工具：web_search、web_fetch、grep、read、
> PowerShell 计算）。模型版本与 token/费用无法获知，如实说明。

## 1. 检索（输入）

实际使用的检索词：

```
Griffin 1954 calculation HLB non-ionic surfactants polysorbate 80 HLB 15
Davies 1957 HLB group numbers hydrophilic lipophilic surfactant calculation
HLB Griffin Davies method comparison polysorbate 80 calculated value disagreement
octenyl succinate beta-cyclodextrin OSA degree of substitution HLB hydrophilic
octenyl succinic anhydride beta-cyclodextrin DS NMR titration emulsifier HLB value
```

命中并采用的关键来源：Griffin 1954 原文（SCC 期刊馆藏/存档 PDF）、Davies 1957
原文（存档 PDF）、Smejkal 2024（MDPI 开放获取）、Ke 2020（MDPI 开放获取）。

## 2. 读取（输入 → 输出）

web_fetch 读取以下 URL 并保存全文：

```
https://web.archive.org/web/20140812062747/http://journal.scconline.org//pdf/cc1954/cc005n04/p00249-p00256.pdf
https://web.archive.org/web/20140810022005/http://www.firp.ula.ve/archivos/historicos/57_Chap_Davies.pdf
https://www.mdpi.com/2504-5377/8/2/21
https://www.mdpi.com/1420-3049/25/3/654
```

提取到的关键结论（AI 输出）：

- Griffin(1954) 三个公式：`20(1-S/A)`、`(E+P)/5`、`E/5`；Table 1 中
  "Tween 80, Polyoxyethylene sorbitan monooleate" HLB = **15**。
- Davies(1957) 式(9)：`HLB = Σ(亲水基团数) − n×0.475 + 7`；Table III 基团数；
  Table II 中 Tween 80 实验=15、基团法=**15.8**；脚注 "1.38 oleates"。

## 3. 核查（关键发现）

1. **正反向核对**：把 Davies 公式实现对正丁醇/乙醇/油酸计算，得 7.0/7.9/1.0，
   与 Davies 原文 Table II 一致 → 公式与基团数提取正确。
2. **发现无法复现处**：Davies 对 Tween 80 的 15.8 用"朴素单酯"模型只能算出
   13.3，差异指向原文脚注 "Calculated values for 'mono-oleates' assume these
   are 1.38 oleates"（未完全写明的结构假设）。已如实记录，未冒充已复现。
3. **锚点绑定方法**：Tween 80 在 Griffin 标尺=15.0、Davies 标尺=15.8，
   因此"和 15 比"必须先说明用的是哪个公式。

## 4. 应用（代码实现）

- `code/hlb.py`：两种方法 + Davies Table III 基团数（取自原文）。
- `code/osa_beta_cd_hlb.py`：OSA-β-CD 的结构约定、分子量、DS=1..7 计算。
- 数值已用 PowerShell 独立复核（Python 运行时在当前沙箱不可用，已如实说明）。

## 5. 与"AI 输出 / 我的判断"的区分

- 公式、基团数、Tween 80 锚点：来自原文（可定位页码），非 AI 生成。
- OSA-β-CD 的分子式/MW 拆分、DS 计算、适用边界判断：本次工作（我的判断）。
- 未做实验：HLB 均为结构式计算值，DS 为用户给定参数。
