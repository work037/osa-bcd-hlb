# 计算运行记录（实际输出）

Python 运行时在当前沙箱不可用（"managed runtime fallback … only node-poppler"），
因此本次数值用 PowerShell 独立复核；`code/osa_beta_cd_hlb.py` 为等效 Python 实现，
供读者在本地复现。

## 实际计算输出（PowerShell，已核对）

```
beta-CD MW = 1134.9842
OSA anhydride = 210.2695

=== Griffin 20*Mh/M ===
DS | 酸型 HLB | 钠盐型 HLB
1  | 17.543   | 17.583
2  | 15.751   | 15.867
3  | 14.385   | 14.587
4  | 13.310   | 13.595
5  | 12.442   | 12.803
6  | 11.726   | 12.157
7  | 11.125   | 11.620

=== Davies 7+sumH-0.475n ===
base beta-CD HLB = 45.150
dAcid/DS = -2.150   dSalt/DS = +14.850
DS | 酸型 HLB | 钠盐型 HLB
1  | 43.00    | 60.00
2  | 40.85    | 74.85
3  | 38.70    | 89.70
4  | 36.55    | 104.55
5  | 34.40    | 119.40
6  | 32.25    | 134.25
7  | 30.10    | 149.10
```

## 关键常量

- β-CD C42H70O35 = 1134.9842 g/mol（文献 1134.99）
- OSA（酸型净加）C12H18O3 = 210.2695 g/mol（文献 210.27）
- OSA（钠盐型净加）C12H17O3Na = 232.2513 g/mol
- -COOH = 45.0174；-COONa = 66.9993

## 与锚点对照

- Griffin 标尺：Tween 80 = 15.0（原文 Table 1）
- Davies 标尺：Tween 80 = 15.8（原文 Table II）
