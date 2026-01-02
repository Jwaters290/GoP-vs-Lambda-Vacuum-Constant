"""
GoP Void-CMB Toy Model (Interpretation 2 + sqrt(N) aggregation)

Single source of truth for:
- g(z,|δ|)
- wΓ(g) = g * exp(1 - g)  (bell-curve; peak at g=1, w=1)
- A_GoP(R,z,|δ|) = f_ent * wΓ(g) * sqrt(V(R)/Vc)
- ΔT_core(R) = k_ISW * R^2 * A_GoP(R,z,|δ|)
- Anchor preset calibration of Vc so that ΔT_core(R_cal,z_cal,|δ_cal|)=ΔT_cal
"""

import math
from dataclasses import dataclass

# -----------------------------
# Constants / defaults
# -----------------------------
C = 299792458.0                  # m/s
TCMB = 2.725                     # K
MPC = 3.085677581491367e22       # m
KELVIN_TO_uK = 1e6

# Default toy-model knobs
DEFAULT_H0 = 67.4                # km/s/Mpc (repo-consistent)
DEFAULT_OMEGA_M0 = 0.315
DEFAULT_D_DECAY = 0.1            # effective potential-decay factor (toy)
DEFAULT_F_ENT = 0.20             # entanglement fraction (toy)
DEFAULT_Z_REF = 0.5
DEFAULT_DELTA_REF = 0.3
DEFAULT_N_EXP = 3.0

# Anchor presets
ANCHORS = {
    "baseline":    dict(R_cal_Mpc=80.0, z_cal=0.5, DeltaT_cal_uK=10.0, delta_cal_abs=0.3),
    "A1_lowz":     dict(R_cal_Mpc=55.0, z_cal=0.3, DeltaT_cal_uK=10.0, delta_cal_abs=0.3),
    "A2_lowz_band":dict(R_cal_Mpc=55.0, z_cal=0.3, DeltaT_cal_uK=8.0,  delta_cal_abs=0.3),
}

DEFAULT_ANCHOR = "A1_lowz"

DEFINITION_CAVEAT = (
    "|δ| is an effective core underdensity depth used only for the local regime mapping "
    "g(z,|δ|) → wΓ(g). It is not assumed equal to a catalog-defined density contrast. "
    "Future overlays will substitute |δ| from the chosen void-finder / tracer-bias model."
)

# -----------------------------
# Helpers
# -----------------------------
def H0_SI(H0_km_s_Mpc: float) -> float:
    return (H0_km_s_Mpc * 1e3) / MPC

def V_sphere_m3(R_m: float) -> float:
    return (4.0/3.0) * math.pi * R_m**3

# -----------------------------
# Core model functions
# -----------------------------
def g_of_z_delta(z: float, delta_abs: float,
                 z_ref: float = DEFAULT_Z_REF,
                 delta_ref: float = DEFAULT_DELTA_REF,
                 n_exp: float = DEFAULT_N_EXP) -> float:
    """
    g(z,|δ|) = (|δ|/δ_ref) * ((1+z)/(1+z_ref))^n
    """
    return (delta_abs / delta_ref) * ((1.0 + z) / (1.0 + z_ref))**n_exp

def w_gamma_of_g(g: float) -> float:
    """
    Bell-curve weight: wΓ(g) = g * exp(1 - g)
    Peak at g=1 with w=1.
    """
    return g * math.exp(1.0 - g)

def k_isw_uK_per_Mpc2(H0_km_s_Mpc: float = DEFAULT_H0,
                      Omega_m0: float = DEFAULT_OMEGA_M0,
                      delta_ref_abs: float = DEFAULT_DELTA_REF,
                      D_decay: float = DEFAULT_D_DECAY) -> float:
    """
    Baseline coefficient for:
      ΔT_uK ≈ k * R_Mpc^2
    based on:
      |Φ0| ≈ 0.5 Ωm H0^2 |δ_ref| R^2
      ΔT ≈ 2 Tcmb (|Φ0|/c^2) D_decay
    """
    H0 = H0_SI(H0_km_s_Mpc)
    k_K_per_m2 = 2.0 * TCMB * (0.5 * Omega_m0 * H0**2 * delta_ref_abs) / (C**2) * D_decay
    return k_K_per_m2 * KELVIN_TO_uK * (MPC**2)

def A_GoP(R_Mpc: float, z: float, delta_abs: float,
          Vc_m3: float,
          f_ent: float = DEFAULT_F_ENT,
          z_ref: float = DEFAULT_Z_REF,
          delta_ref: float = DEFAULT_DELTA_REF,
          n_exp: float = DEFAULT_N_EXP) -> float:
    """
    A_GoP = f_ent * wΓ(g(z,|δ|)) * sqrt(V(R)/Vc)
    """
    R_m = R_Mpc * MPC
    V = V_sphere_m3(R_m)
    g = g_of_z_delta(z, delta_abs, z_ref=z_ref, delta_ref=delta_ref, n_exp=n_exp)
    w = w_gamma_of_g(g)
    return f_ent * w * math.sqrt(V / Vc_m3)

def DeltaT_core_uK(R_Mpc: float, z: float, delta_core_abs: float,
                   Vc_m3: float,
                   H0_km_s_Mpc: float = DEFAULT_H0,
                   Omega_m0: float = DEFAULT_OMEGA_M0,
                   D_decay: float = DEFAULT_D_DECAY,
                   f_ent: float = DEFAULT_F_ENT,
                   z_ref: float = DEFAULT_Z_REF,
                   delta_ref: float = DEFAULT_DELTA_REF,
                   n_exp: float = DEFAULT_N_EXP) -> float:
    """
    ΔT_core_uK(R) = k_ISW * R^2 * A_GoP(R,z,|δ|)
    """
    k = k_isw_uK_per_Mpc2(H0_km_s_Mpc, Omega_m0, delta_ref, D_decay)
    A = A_GoP(R_Mpc, z, delta_core_abs, Vc_m3, f_ent=f_ent, z_ref=z_ref, delta_ref=delta_ref, n_exp=n_exp)
    return k * (R_Mpc**2) * A

def calibrate_Vc(anchor_preset: str = DEFAULT_ANCHOR,
                 H0_km_s_Mpc: float = DEFAULT_H0,
                 Omega_m0: float = DEFAULT_OMEGA_M0,
                 D_decay: float = DEFAULT_D_DECAY,
                 f_ent: float = DEFAULT_F_ENT,
                 z_ref: float = DEFAULT_Z_REF,
                 delta_ref: float = DEFAULT_DELTA_REF,
                 n_exp: float = DEFAULT_N_EXP) -> float:
    """
    Solve Vc from anchor constraint:
      ΔT_cal = k * R_cal^2 * f_ent * wΓ(g_cal) * sqrt(V(R_cal)/Vc)
    """
    if anchor_preset not in ANCHORS:
        raise ValueError(f"Unknown anchor preset: {anchor_preset}")

    a = ANCHORS[anchor_preset]
    R_cal = a["R_cal_Mpc"]
    z_cal = a["z_cal"]
    delta_cal = a["delta_cal_abs"]
    DT_cal = a["DeltaT_cal_uK"]

    k = k_isw_uK_per_Mpc2(H0_km_s_Mpc, Omega_m0, delta_ref, D_decay)

    g_cal = g_of_z_delta(z_cal, delta_cal, z_ref=z_ref, delta_ref=delta_ref, n_exp=n_exp)
    w_cal = w_gamma_of_g(g_cal)

    R_m = R_cal * MPC
    V = V_sphere_m3(R_m)

    denom = (k * (R_cal**2) * f_ent * w_cal)
    ratio = DT_cal / denom
    Vc = V / (ratio**2)
    return Vc
