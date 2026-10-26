# -*- coding: utf-8 -*-
"""
OSA-beta-CD（辛烯基琥珀酸 beta-环糊精）HLB 计算。

化合物: 2-octen-1-ylsuccinic anhydride 改性的 beta-环糊精，
        酸型(游离 -COOH) 与钠盐型(-COONa) 两种形式。
        DS = 取代度 = 每个 beta-CD 上平均接入的 OSA 基团数，取 1..7。

结构事实:
  - beta-CD: C42H70O35, 7 个葡萄糖单元, 21 个游离 OH。
  - OSA 半酯取代: CD-OH 开环 OSA 形成半酯，每取代净加 C12H18O3，
    并引入 1 个游离羧基；钠盐型为 -COONa (净加 C12H17O3Na)。
  - 因此 DS=n 时:
      酸型   C(42+12n) H(70+18n) O(35+3n)
      钠盐型 C(42+12n) H(70+17n) O(35+3n) Na(n)

方法（数据取自原始文献，见 README/核查记录）:
  - Griffin(1954) 质量分数: HLB = 20 * Mh / M
      Mh = 亲水部分 = beta-CD 核心 + n * M(游离羧基/羧酸钠)
      M  = 全分子量
  - Davies(1957) 基团贡献: HLB = 7 + sum(H_i) - 0.475 * n_lipo

锚点: Tween 80, 公认 HLB≈15 (Griffin 1954 Table 1 = 15.0;
      Davies 1957 Table II 实验 15 / 基团法 15.8)。
"""

import os
import sys

# 允许在任意工作目录下运行本脚本（同目录的 hlb.py 作为模块导入）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hlb import davies, mw_from_formula

# ---- 原子量（与 hlb.py 一致） ----
C = 12.0107
H = 1.00794
O = 15.9994
Na = 22.98977

# ---- 结构常数 ----
BCD = mw_from_formula({"C": 42, "H": 70, "O": 35})   # beta-CD C42H70O35
OSA_ACID = mw_from_formula({"C": 12, "H": 18, "O": 3})  # 每取代净加 C12H18O3
# 钠盐型: COOH -> COONa, 即 -H +Na
OSA_SALT = OSA_ACID - H + Na                        # 净加 C12H17O3Na
COO_H = mw_from_formula({"C": 1, "H": 1, "O": 2})   # -COOH 亲水部分
COO_Na = COO_H - H + Na                             # -COONa 亲水部分


def molecular_mass(ds, salt=False):
    """OSA-beta-CD 的分子量。"""
    base = BCD
    group = OSA_SALT if salt else OSA_ACID
    return base + ds * group


def griffin_hlb(ds, salt=False):
    """Griffin 质量分数法。

    约定: 亲水部分 = beta-CD 核心 + n 个游离羧基(-COOH 或 -COONa)；
          亲油部分 = OSA 的辛烯基链 + 琥珀酰骨架 + 酯键。
    """
    Mh = BCD + ds * (COO_Na if salt else COO_H)
    M = molecular_mass(ds, salt)
    return 20.0 * Mh / M


def davies_hlb(ds, salt=False):
    """
    Davies 基团贡献法（对整个分子做原子计数）。

    beta-CD 核心:
      亲水: OH(free) x21, -O-(环醚+糖苷键) x14
      亲油: 42 个碳 (35 CH + 7 CH2), 各 -0.475
    每个 OSA 取代(替换 1 个 OH):
      亲水: -1 OH(free), +1 酯(free), +1 -COOH 或 -COONa
      亲油: +10 个碳 (1 CH + 6 CH2 + 2 =CH + 1 CH3), 各 -0.475
    """
    hydro = {"OH(free)": 21 - ds, "-O-": 14, "ester(free)": ds}
    hydro["-COOH" if not salt else "-COONa"] = ds
    lipo = {"-CH-": 35 + ds * 1, "-CH2-": 7 + ds * 6,
            "=CH-": ds * 2, "CH3-": ds * 1}
    return davies(hydro, lipo)


if __name__ == "__main__":
    print("分子量: beta-CD = %.4f; OSA(酸) = %.4f; OSA(钠盐) = %.4f"
          % (BCD, OSA_ACID, OSA_SALT))
    print("锚点 Tween 80: Griffin=15.0; Davies(原文)=15.8\n")

    print("=" * 78)
    print("Griffin 20*Mh/M")
    print("%-4s %12s %12s   %12s %12s" %
          ("DS", "酸型 HLB", "钠盐型 HLB", "酸型 MW", "钠盐型 MW"))
    for ds in range(1, 8):
        ga = griffin_hlb(ds, salt=False)
        gs = griffin_hlb(ds, salt=True)
        print("%-4d %12.3f %12.3f   %12.2f %12.2f"
              % (ds, ga, gs, molecular_mass(ds, False), molecular_mass(ds, True)))

    print("=" * 78)
    print("Davies 7 + sum(H_i) - 0.475*n")
    print("%-4s %12s %12s" % ("DS", "酸型 HLB", "钠盐型 HLB"))
    for ds in range(1, 8):
        da = davies_hlb(ds, salt=False)
        ds_ = davies_hlb(ds, salt=True)
        print("%-4d %12.2f %12.2f" % (ds, da, ds_))

    print("=" * 78)
    print("注: Davies 法对高取代/多羟基大分子会超出 0-20 标尺(见正文讨论)。")
