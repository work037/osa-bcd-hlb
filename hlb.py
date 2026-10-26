# -*- coding: utf-8 -*-
"""
HLB (亲水亲油平衡值, Hydrophilic-Lipophilic Balance) 计算器。

实现两种经典方法，数据严格取自原始文献：

1. Griffin, W. C. (1954). "Calculation of HLB Values of Non-Ionic
   Surfactants", J. Soc. Cosmetic Chemists 5(4): 249-256.
   - 对多元醇脂肪酸酯:      HLB = 20 * (1 - S/A)
     S = 酯的皂化值 (saponification number), A = 脂肪酸的酸值 (acid number)
   - 对皂化数据不佳的酯:    HLB = (E + P) / 5
     E = 环氧乙烷质量百分数, P = 多元醇质量百分数
   - 仅以环氧乙烷为亲水部分: HLB = E / 5
   - (现代常见的等价/推广形式) HLB = 20 * Mh / M
     Mh = 亲水部分分子量, M = 全分子分子量

2. Davies, J. T. (1957). "A quantitative kinetic theory of emulsion type,
   I. Physical chemistry of the emulsifying agent",
   Proc. 2nd Int. Congr. Surface Activity, 426-438.
   - HLB = 7 + sum(亲水基团数) - 0.475 * n
     n = 亲油基团(-CH-, -CH2-, CH3-, =CH-)个数
   - 表 III 给出各基团数；派生基团 -(CH2-CH2-O)- = +0.33、
     -(CH2-CH2-CH2-O)- = -0.15。

注意：两种方法尺度不同，绝对值不可直接互比。本工具同时计算目标物与
锚点物(Tween 80, 公认 HLB≈15)，用"同一公式的相对差值/比值"做比较。
"""

# Davies (1957) Table III 基团数（亲水基团）
DAVIES_HYDROPHILIC = {
    "-SO4Na": 38.7,
    "-COOK": 21.1,
    "-COONa": 19.1,
    "N(tertiary amine)": 9.4,
    "ester(sorbitan ring)": 6.8,
    "ester(free)": 2.4,
    "-COOH": 2.1,
    "OH(free)": 1.9,
    "-O-": 1.3,
    "OH(sorbitan ring)": 0.5,
    # 派生基团 (Davies Table III "Derived groups")
    "EO(-CH2CH2O-)": 0.33,
    "PO(-CH2CH2CH2O-)": -0.15,
}

# Davies (1957) Table III 基团数（亲油基团，均计入 -0.475*n）
DAVIES_LIPOPHILIC = {
    "-CH-": -0.475,
    "-CH2-": -0.475,
    "CH3-": -0.475,
    "=CH-": -0.475,
}

# 常用原子量（用于 Griffin 质量分数法 20*Mh/M 的分子量拆分）
ATOMIC_MASS = {
    "H": 1.00794,
    "C": 12.0107,
    "N": 14.0067,
    "O": 15.9994,
    "Na": 22.98977,
    "K": 39.0983,
    "S": 32.065,
}


def griffin_saponification(S, A):
    """Griffin(1954) 多元醇脂肪酸酯公式：HLB = 20*(1 - S/A)。"""
    return 20.0 * (1.0 - S / A)


def griffin_EP(E, P):
    """Griffin(1954) 皂化数据不佳时：(E + P)/5（E、P 均为质量百分数）。"""
    return (E + P) / 5.0


def griffin_E(E):
    """Griffin(1954) 仅 EO 为亲水部分：E/5（E 为质量百分数）。"""
    return E / 5.0


def griffin_mass(Mh, M):
    """Griffin 质量分数形式：HLB = 20 * Mh / M。"""
    return 20.0 * Mh / M


def davies(hydrophilic_counts, lipophilic_counts):
    """
    Davies(1957) 基团贡献法。

    参数:
      hydrophilic_counts: dict, 亲水基团名 -> 个数
      lipophilic_counts:   dict, 亲油基团名(-CH-/-CH2-/CH3-/=CH-) -> 个数
    返回:
      HLB 值 (float)
    """
    hlb = 7.0
    for name, count in hydrophilic_counts.items():
        if name not in DAVIES_HYDROPHILIC:
            raise KeyError("未知亲水基团: %s" % name)
        hlb += DAVIES_HYDROPHILIC[name] * count
    for name, count in lipophilic_counts.items():
        if name not in DAVIES_LIPOPHILIC:
            raise KeyError("未知亲油基团: %s" % name)
        hlb += DAVIES_LIPOPHILIC[name] * count
    return hlb


def mw_from_formula(atom_counts):
    """由 {元素: 个数} 计算分子量。"""
    return sum(ATOMIC_MASS[el] * n for el, n in atom_counts.items())


if __name__ == "__main__":
    # 自检：Davies 原文 Table II 的简单分子复核
    # n-丁醇 CH3CH2CH2CH2OH -> 7.0；乙醇 CH3CH2OH -> 7.9
    butanol = davies({"OH(free)": 1}, {"CH3-": 1, "-CH2-": 3})
    ethanol = davies({"OH(free)": 1}, {"CH3-": 1, "-CH2-": 1})
    print("n-butanol HLB = %.2f (Davies Table II: 7.0)" % butanol)
    print("ethanol   HLB = %.2f (Davies Table II: 7.9)" % ethanol)
