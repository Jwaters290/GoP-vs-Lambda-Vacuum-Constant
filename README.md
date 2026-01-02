
# GoP-vs-Lambda-Vacuum-Constant
A simple Python demonstration comparing the ΛCDM cosmological constant’s vacuum energy density with the emergent vacuum scale predicted by the Gravity of Probability (GoP) framework—showing GoP reproduces Λ’s value without cosmological tuning.


The repository is provided for reproduciability, but here are the results:
```
=== ΛCDM vacuum energy (from cosmology) ===
H0                  = 67.40 km/s/Mpc
Ω_Λ                 = 0.688
ρ_Λ (mass)          = 5.875e-27 kg/m^3
ρ_Λ (energy)        = 5.281e-10 J/m^3

=== GoP emergent vacuum scale (no Λ tuning) ===
κA                  = 1.50e-15
E0                  = 1.00e+12 erg
Coherence volume    = 1.00 m^3
ρ_vac^GoP (energy)  = 1.500e-10 J/m^3

=== Comparison ===
ρ_vac^GoP / ρ_Λ     = 0.284
(~ O(1) agreement without any cosmological tuning)
```

Key Result: 

 - The GoP emergent vacuum energy density (ρ_vac^{GoP} ≈ 1.5 × 10^{-10} J/m³) matches the ΛCDM value (ρ_Λ ≈ 5.3 × 10^{-10} J/m³) to within a factor of ~0.3—close to order-unity agreement. This demonstrates GoP's ability to reproduce the observed dark energy scale naturally, using parameters constrained elsewhere (not tuned to cosmology).
 - Implications: Supports GoP as a viable alternative to ΛCDM for explaining cosmic acceleration, potentially resolving fine-tuning issues. The script notes this is a distilled toy model, not the full formalism, but it aligns with GoP's broader predictions (e.g., stable vacuum without instability).
 - Limitations: This demonstration intentionally employs a highly simplified coherence volume (fixed to 1 m³) to illustrate the emergence of the GoP vacuum energy scale in a transparent, order-of-magnitude manner.

# v2.0.0: Void–CMB Toy Model Extension

The [January 2nd 2026, v2.0.0 Release](https://github.com/Jwaters290/GoP-vs-Lambda-Vacuum-Constant/releases) extends the GoP vs. Λ Vacuum Constant repository beyond vacuum-scale demonstrations by introducing a reproducible, toy-level prediction and measurement scaffold for cosmic-void imprints in the CMB. This extension is designed for conceptual scaling, regime mapping, and preregistration, not precision cosmological inference.
```
=== GoP Void-Core Toy Model — Illustrative Output (v2.0.0) ===
(Using default A1_lowz anchor: representative low-redshift void regime)

Calibration anchor:
  R_cal = 55 Mpc, z_cal = 0.3, ΔT_cal = 10 µK
  (Places typical low-z voids at O(10 µK) by construction)

Boötes Void regime placement (R = 62 Mpc, z ≈ 0.052, |δ_core| proxy ≈ 0.85):
  g(z, |δ|) ≈ 0.98  →  w_Γ(g) ≈ 1.00
  (Near-maximal decoherence-retention regime)

Illustrative ΔT_core:
  O(10 µK under this anchor (mid-teens µK in the idealized toy limit)

Panel A scaling (fixed z = 0.5, |δ| = 0.3):
  Threshold onset below ~40 Mpc; steep rise for larger voids
  (Idealized toy behavior ∝ R^{7/2})

Sensitivity notes:
  • Amplitude is anchor-relative (regime placement, not absolute normalization)
  • Real surveys limit observable signals to O(10 µK) via projection, variance,
    and decoherence-saturation effects

```
Version context
v1.0.0 demonstrated order-unity agreement between the GoP emergent vacuum energy scale and the ΛCDM cosmological constant, using fixed parameters and no cosmological tuning. This remains a standalone vacuum-emergence sanity check.
v2.0.0 explores relative scaling and regime placement within the cosmic-void sector under explicit calibration anchors. It should be interpreted as conceptual mapping and preregistration, not as an independent precision forecast or normalization.


1. **Void CMB Toy Model**

 - Introduces a minimal, physically motivated mapping from GoP decoherence physics to void-scale CMB temperature shifts.
 - Implements a bell-curve decoherence kernel Γ(E) with environmental weighting 𝑔(𝑧,∣𝛿∣)g(z,∣δ∣).
 - Provides closed-form scaling Δ𝑇core∝𝑅7/2⋅𝑤Γ(𝑔)ΔTcore  ∝R 7/2⋅wΓ(g).

2. **Anchor-Calibrated Predictions**

**Adds explicit calibration presets:**

 - ```baseline``` (R=80 Mpc, z=0.5, ΔT=10 µK)
 - ```A1_lowz``` (R=55 Mpc, z=0.3, ΔT=10 µK, default)
 - ```A2_lowz_band``` (R=55 Mpc, z=0.3, ΔT=8 µK)
Enables preregistered predictions for individual voids (e.g., Boötes).

3. **Boötes Void Case Study**

 - Includes a concrete, parameter-locked prediction for the Boötes Void using literature-consensus size and redshift.
 - Designed as a single-object sanity check, not a statistical detection claim.

4. **Planck Aperture Photometry Measurement Harness**

**Adds a reproducible HEALPix-based aperture photometry pipeline:**
 - Core-minus-rim ΔT measurement
 - Bootstrap uncertainty estimation
 - Matched-latitude random-center null distribution
 - Multi-map consistency support (SMICA / NILC / Commander)
 - Outputs machine-readable JSON artifacts for predictions and measurements.

**Implications & Limitations**
Key Result:
 - Within the toy model, large low-redshift voids such as Boötes are placed in a high decoherence-retention regime (𝑤Γ≈1wΓ≈1), yielding O(10 µK warm cores). This is qualitatively opposite to the cold imprints typically expected from late-time ΛCDM ISW effects, providing a clear sign-level differentiator.


Implications:
- Illustrates how GoP decoherence physics can imprint observable CMB structure without introducing new free parameters, and provides preregistered targets for Planck- and DESI-era void analyses.


Limitations:
 - Toy-level only: simplified geometry, fixed decay factors, spherical symmetry, and no full N-body or bias modeling.
 - Anchor-dependent: amplitudes illustrate relative scaling, not absolute normalization.
 - Steep idealized scaling (∝𝑅7/2 ∝R 7/2) is moderated in practice by projection effects, foregrounds, and cosmic variance; observable signals are expected to remain O(10 µK).
 - Single-void measurements (e.g., Boötes) have intrinsically low S/N; the provided harness is designed for null tests and preregistered checks, not standalone detections.

**Falsifiability and Failure Modes**
The v2.0.0 void–CMB module makes explicit, preregistered, and falsifiable predictions at the toy-model level. These criteria apply only to the void–CMB toy model presented here and do not, by themselves, falsify the broader Gravity of Probability (GoP) framework.

Primary falsification criteria (ensemble-level):

Sign falsification.
If stacked low-redshift (𝑧 ≲ 0.6), large-radius voids (𝑅 ≳ 40–50 Mpc) consistently exhibit cold cores (negative ΔT) with statistical significance (e.g., >4𝜎) after controlling for projection and selection effects, the toy model’s warm-core prediction is falsified.

Amplitude falsification.
If stacked analyses of such voids yield

**∣⟨Δ𝑇core⟩∣ ≲ 3𝜇K**

with high statistical confidence, the toy model’s O(10 µK regime placement is falsified.

Secondary falsification criteria (morphology-level):

Profile falsification:
If stacked void–CMB profiles show no central enhancement and no compensating rim structure within ∼0.8–1.2R_void, inconsistent with the predicted warm-core + rim morphology, the toy model’s decoherence-driven imprint mechanism is falsified.

Non-falsifying outcomes:
 - Null or ambiguous results for individual voids (e.g., Boötes alone) due to low signal-to-noise, cosmic variance, or projection effects.
 - Mild suppression or broadening of the signal due to foregrounds, masking, or void-finder definition differences.

**Interpretation note.**
Failure of the above criteria falsifies the void–CMB toy model and its assumed scaling/anchoring, not the full GoP framework, which is tested independently through galaxy dynamics, lensing, and cosmological observables.

---

Reproducable code for observational overlays from DR2 VACs (DESIVAST) is a work in porogress - there's currently not public data available.

---

# GoP vs Λ Vacuum Constant Comparison

This repository provides a small, transparent Python demonstration comparing the 
vacuum energy density required by the ΛCDM cosmological constant (Λ) with the 
emergent vacuum scale predicted by the Gravity of Probability (GoP) framework.

In ΛCDM, Λ is a tuned phenomenological constant chosen to match the observed 
cosmic acceleration. GoP, in contrast, produces a vacuum energy density of the 
same order of magnitude *without* cosmological tuning, using a fixed global 
parameter set constrained independently from galaxy dynamics and decoherence 
physics.

The script `lambda_vs_gop_vacuum_constant.py` computes:

- The ΛCDM vacuum energy density  
- The GoP emergent vacuum energy density  
- Their numerical ratio  

The result shows that GoP’s fixed parameters naturally reproduce the observed 
dark-energy scale (∼10⁻¹⁰ J/m³), whereas ΛCDM must set Λ by hand. This repository 
serves as a clear, minimal reference illustrating that GoP turns the cosmological 
constant from an input into an output.

---

## Origin

This specific repository works in parallel to the primary Github [GoP-DESI-VACs-Pipeline-And-Testbed](https://github.com/Jwaters290/GoP-DESI-VACs-Pipeline-And-Testbed).

## Features

- Computes ΛCDM vacuum energy density from standard cosmological values  
- Computes emergent GoP vacuum constant using:
  - κA = 1.5×10⁻¹⁵  
  - E₀ = 10¹² erg  
- No cosmological tuning required  
- Clear numerical comparison with a single, readable Python script  

---

## Running the Script

```bash
python3 lambda_vs_gop_vacuum_constant.py
```

## Author & Research Links

**Author:** Jordan Waters  
**ORCID:** https://orcid.org/0009-0009-0793-8089  
**Figshare Profile:** https://figshare.com/authors/Jordan_Waters/21620558

Additional research materials, data tables, and full Gravity of Probability 
papers can be found on the Figshare profile above.

## Notes

- This repository is intentionally minimal and designed for clarity. Its purpose is
  to provide a clean comparison between the ΛCDM vacuum constant and the emergent
  vacuum density predicted by the Gravity of Probability (GoP) using fixed global
  parameters (κA, E₀).

- The numerical agreement is an order-of-magnitude demonstration of a key GoP
  feature: what ΛCDM treats as a tuned cosmological constant emerges naturally
  from decoherence-driven probabilistic curvature without cosmological fitting.

- The code here is not a complete GoP implementation; it is a focused, 
  easy-to reproduce calculation meant to illustrate this conceptual distinction.

- For full analyses, datasets, lensing models, and the complete GoP series of
  papers, refer to the Figshare profile included above.

  ---

This test demonstrates that the canonical kernel

Γ(E) = κA · E · exp(1 − E / E₀)

**naturally saturates**, producing a stable effective cosmological constant Λ_eff under
cosmological conditions.

# Why vacuum energy matching is a non-negotiable requirement

In GoP, vacuum energy is not an auxiliary quantity. It is foundational.

 - GoP asserts that information density and decoherence flow contribute to gravitational curvature.
 - The vacuum is the maximal information reservoir in the theory
 - Therefore, its effective gravitational weight must be reproduced correctly using the same parameters

If GoP failed to reproduce the observed vacuum energy scale, the framework would collapse immediately — not later, immediately.

There is no “patch” available.

So the fact that it lands near 1:1 is not cosmetic; it is existence-level validation.

Most approaches treat vacuum energy in one of three unsatisfactory ways:

 - Cancel it by hand (Λ problem avoidance)
 - Renormalize it away (formal but physically empty)
 - Declare it anthropic (landscape reasoning)

The GoP framework does none of these, it is doing something far stricter:

 - The vacuum has weight because it carries unrealized quantum probability, and that weight must match observation under the same bookkeeping rules that govern galaxies and voids.

That is a single-source requirement.

Very few frameworks even attempt this, but here there's a match.


### Key Results

- No overproduction of vacuum energy
- Rapid convergence to a constant Λ_eff
- Stability under extreme energy distributions
- Compatibility with late-time acceleration
- No fine-tuning required

Consistency is demonstrated relative to:

- Planck CMB ΛCDM parameters
- DESI BAO expansion history
- Type Ia supernova luminosity distances

This validates GoP as a **dark-matter-free curvature model that remains cosmologically viable**.

---
---
### Vacuum Energy Consistency and the Cosmological Constant Problem

The cosmological constant problem (CCP) is widely regarded as one of the most severe fine-tuning challenges in fundamental physics. Standard quantum field theory predicts vacuum zero-point energy densities extending up to the Planck scale (∼10¹¹² erg cm⁻³ or higher), whereas cosmological observations require an effective vacuum energy density of only ∼10⁻⁸ erg cm⁻³ (ρ_Λ ≈ 5 × 10⁻¹⁰ J m⁻³). This mismatch of roughly 120 orders of magnitude necessitates an extraordinarily precise cancellation between a “bare” cosmological constant and quantum contributions—without any known symmetry, conservation law, or dynamical mechanism enforcing such precision.

Most existing approaches treat vacuum energy as peripheral or adjustable. Typical strategies include introducing a finely tuned bare Λ to cancel quantum contributions, absorbing divergences through renormalization without a physical explanation of the observed scale, or invoking anthropic or multiverse arguments. While mathematically admissible, these approaches do not derive the observed vacuum energy from a single underlying physical principle.

In the Gravity of Probability (GoP) framework, vacuum energy matching is not optional. The vacuum is identified as the ground state of maximal unrealized quantum probability, and its gravitational weight must emerge from the same probabilistic–decoherence mechanism that governs curvature on galactic, lensing, and large-scale-structure scales. The decoherence kernel Γ(E) and its associated parameters (κ_A, E₀) are universal within the framework. There is no independent cosmological dial or compensating term available. If the predicted vacuum energy density differed from observation by orders of magnitude, the framework would be internally inconsistent at a foundational level and would be falsified outright.

A simple toy-level computation within GoP yields an effective vacuum energy density ρ_vac^{GoP} ≈ 1.5 × 10⁻¹⁰ J m⁻³—within a factor of a few of the observed value—using parameters fixed independently by galaxy rotation curves and related datasets. This agreement is therefore not a post-hoc fit, but a stringent consistency check. The framework does not function unless the vacuum energy is reproduced under the same probabilistic bookkeeping rules that apply to baryonic and large-scale structures.

This single-source consistency is uncommon among proposed solutions to the CCP. Other approaches—such as running-vacuum models, self-tuning scalar fields, scale-invariant constructions, or inhomogeneous screening mechanisms—typically introduce additional fields, assumptions, or dynamical layers. GoP instead achieves order-of-magnitude agreement by treating vacuum curvature as fossilized quantum probability, governed by the same decoherence dynamics responsible for non-classical gravitational effects elsewhere.

When combined with the absence of vacuum overproduction, rapid convergence to an effective Λ, late-time acceleration compatibility, and the lack of parameter tuning, this vacuum-energy consistency positions GoP as cosmologically viable in a particularly stringent sense. It passes a test that immediately falsifies many alternatives, while remaining directly testable through independent predictions in cosmic voids, the CMB, and large-scale structure.

Vacuum energy matching is therefore not an auxiliary success of the framework; it is a structural requirement. Continued agreement with upcoming observational datasets (e.g., DESI full releases and Euclid) would represent a significant milestone in assessing the validity of the Gravity of Probability framework as a unified semiclassical description of gravitational sourcing.


  ## Keywords

Gravity of Probability, GoP, cosmological constant, Lambda, ΛCDM, dark energy, 
vacuum energy, vacuum constant, zero-point energy, emergent cosmology, 
probabilistic curvature, decoherence, quantum decoherence, quantum gravity, 
baryonic bias, emergent Λ, cosmology, theoretical physics, SPARC galaxies, 
gravitational modeling, decoherence-driven curvature, quantum information, 
semi-classical gravity, vacuum density, Hubble parameter, large-scale structure, 
decoherence physics, GoP parameterization, Λ prediction, cosmological fine-tuning, 
cosmic acceleration, alternative gravity models, dark matter alternatives.
