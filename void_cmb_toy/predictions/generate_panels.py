import argparse
import numpy as np
import matplotlib.pyplot as plt

from common.gop_void_toy import (
    calibrate_Vc, DeltaT_core_uK, g_of_z_delta, w_gamma_of_g, DEFAULT_Z_REF, DEFAULT_DELTA_REF
)

def delta_profile(r_frac, delta_core=0.30, delta_rim=0.10, sigma=0.35):
    """
    Simple radial interpolation:
      δ(r) = δ_rim + (δ_core - δ_rim) * exp(-(r/sigma)^2)
    where r is normalized to R (0..1).
    """
    return delta_rim + (delta_core - delta_rim) * np.exp(-(r_frac / sigma) ** 2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchor_preset", default="A1_lowz",
                    choices=["baseline", "A1_lowz", "A2_lowz_band"])
    ap.add_argument("--outA", default="figures/panelA_DeltaT_core_vs_R.png")
    ap.add_argument("--outB", default="figures/panelB_normalized_profile.png")
    ap.add_argument("--n_exp", type=float, default=3.0)

    args = ap.parse_args()

    # Calibrate once for the chosen anchor
    Vc = calibrate_Vc(anchor_preset=args.anchor_preset, n_exp=args.n_exp)

    # -------------------------
    # Panel A: ΔT_core(R)
    # -------------------------
    R_vals = np.linspace(20, 120, 220)
    z_for_panelA = 0.3
    delta_for_panelA = 0.30

    dT = [DeltaT_core_uK(R, z_for_panelA, delta_for_panelA, Vc_m3=Vc, n_exp=args.n_exp) for R in R_vals]

    plt.figure()
    plt.plot(R_vals, dT)
    plt.xlabel("Void radius R [Mpc]")
    plt.ylabel("ΔT_core [µK]")
    plt.title(f"Panel A — ΔT_core(R) (anchor={args.anchor_preset}, z={z_for_panelA}, |δ|={delta_for_panelA})")
    plt.tight_layout()
    plt.savefig(args.outA)
    plt.close()

    # -------------------------
    # Panel B: normalized ΔT(r/R) for representative void sizes
    # -------------------------
    r_frac = np.linspace(0.0, 1.2, 240)  # extend beyond R to include rim if desired
    void_sizes = [30, 60, 90]
    z_for_panelB = 0.5  # fixed illustrative z

    plt.figure()

    for R in void_sizes:
        # compute wΓ(g(r)) from δ(r)
        delta_r = delta_profile(r_frac, delta_core=0.30, delta_rim=0.10, sigma=0.35)

        # Map through g and wΓ. Use the same proxy form as the toy model.
        g_r = (delta_r / DEFAULT_DELTA_REF) * (((1.0 + z_for_panelB) / (1.0 + DEFAULT_Z_REF)) ** args.n_exp)
        w_r = g_r * np.exp(1.0 - g_r)

        # Normalize to core
        w_r_norm = w_r / w_r[0]

        plt.plot(r_frac, w_r_norm, label=f"R={R} Mpc")

    plt.xlabel("r / R")
    plt.ylabel("Normalized ΔT(r/R) (shape via δ(r)→g→wΓ)")
    plt.title("Panel B — Normalized radial profile (physics-mapped)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.outB)
    plt.close()

if __name__ == "__main__":
    main()
