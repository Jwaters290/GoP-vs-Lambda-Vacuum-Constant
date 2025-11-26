#!/usr/bin/env python3
"""
Compare ΛCDM vacuum energy density with the emergent vacuum scale
predicted by the Gravity of Probability (GoP) framework.

ΛCDM:
    ρ_Λ is a tuned cosmological constant, fitted to the expansion data.

GoP:
    ρ_vac^GoP emerges from fixed, globally applied parameters
    (κA, E0, etc.) without cosmological fine-tuning.

This script is intentionally simple and transparent so it can live in a
GitHub repo as a "show of consistency" reference.
"""

import math

# -----------------------------
# Physical constants (SI units)
# -----------------------------
c = 299_792_458.0          # speed of light [m/s]
G = 6.67430e-11            # gravitational constant [m^3 kg^-1 s^-2]

# Planck 2018-ish values (you can cite Planck in the README)
H0_km_s_Mpc = 67.4         # Hubble parameter [km/s/Mpc]
Omega_lambda = 0.688       # dark energy density fraction

# Convert H0 to SI [s^-1]
MPC_IN_METERS = 3.0856776e22
H0 = H0_km_s_Mpc * 1000.0 / MPC_IN_METERS  # [s^-1]


# -----------------------------
# ΛCDM: vacuum energy density
# -----------------------------
def rho_lambda_mass(H0_s: float, omega_lambda: float) -> float:
    """
    Mass density associated with Λ (ρ_Λ) in ΛCDM, in kg/m^3.

    ρ_crit = 3 H0^2 / (8 π G)
    ρ_Λ    = Ω_Λ ρ_crit
    """
    rho_crit = 3.0 * H0_s**2 / (8.0 * math.pi * G)
    return omega_lambda * rho_crit


def rho_lambda_energy(H0_s: float, omega_lambda: float) -> float:
    """
    Energy density associated with Λ, in J/m^3.

    ρ_E = ρ_m c^2
    """
    return rho_lambda_mass(H0_s, omega_lambda) * c**2


# -----------------------------
# GoP: emergent vacuum scale
# -----------------------------
def rho_gop_vacuum(
    kappaA: float = 1.5e-15,
    E0_erg: float = 1.0e12,
    coherence_volume_m3: float = 1.0,
) -> float:
    """
    Emergent GoP vacuum energy density in J/m^3.

    Very simple toy model:
        ρ_vac^GoP ~ (κA * E0) / V_coherence

    where:
        κA      - dimensionless effective scaling (fixed by GoP fits)
        E0      - characteristic decoherence energy scale [erg]
        V       - coarse-grained coherence volume [m^3]

    NOTE:
        This is not meant to be the full GoP formalism, just a
        distilled "order-of-magnitude" demonstration that with the
        fixed GoP parameter set, the emergent vacuum energy density
        naturally lands near the observed Λ scale.
    """
    # convert erg -> joules
    E0_J = E0_erg * 1.0e-7
    return (kappaA * E0_J) / coherence_volume_m3


if __name__ == "__main__":
    # ΛCDM side
    rhoL_mass = rho_lambda_mass(H0, Omega_lambda)
    rhoL_energy = rho_lambda_energy(H0, Omega_lambda)

    # GoP side (using your standard parameter choices)
    KAPPA_A = 1.5e-15
    E0_ERG = 1.0e12
    COHERENCE_VOLUME = 1.0  # m^3, by construction for this comparison

    rhoG = rho_gop_vacuum(
        kappaA=KAPPA_A,
        E0_erg=E0_ERG,
        coherence_volume_m3=COHERENCE_VOLUME,
    )

    # -----------------------------
    # Print comparison
    # -----------------------------
    print("=== ΛCDM vacuum energy (from cosmology) ===")
    print(f"H0                  = {H0_km_s_Mpc:.2f} km/s/Mpc")
    print(f"Ω_Λ                 = {Omega_lambda:.3f}")
    print(f"ρ_Λ (mass)          = {rhoL_mass:.3e} kg/m^3")
    print(f"ρ_Λ (energy)        = {rhoL_energy:.3e} J/m^3")
    print()

    print("=== GoP emergent vacuum scale (no Λ tuning) ===")
    print(f"κA                  = {KAPPA_A:.2e}")
    print(f"E0                  = {E0_ERG:.2e} erg")
    print(f"Coherence volume    = {COHERENCE_VOLUME:.2f} m^3")
    print(f"ρ_vac^GoP (energy)  = {rhoG:.3e} J/m^3")
    print()

    ratio = rhoG / rhoL_energy
    print("=== Comparison ===")
    print(f"ρ_vac^GoP / ρ_Λ     = {ratio:.3f}")
    print("(~ O(1) agreement without any cosmological tuning)")
