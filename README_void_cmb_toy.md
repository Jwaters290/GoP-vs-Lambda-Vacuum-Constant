# GoP Void–CMB Toy Model (v2.0.0)

## Overview

This module extends the **Gravity of Probability (GoP)** framework to **void–scale CMB signatures**, providing:

- A **toy-model mapping** from GoP decoherence physics to void-induced CMB temperature signals
- **Pre-registered predictions** for individual cosmic voids (currently Boötes)
- **Minimal and extended measurement pipelines** for aperture photometry on Planck CMB maps
- Transparent, order-of-magnitude scaling intended for falsifiable comparison — *not* a full cosmological analysis

This release is designed to bridge **intuition → prediction → measurement**, prior to stacked or survey-scale analyses.

---

## What This Release Is

- A **toy-model implementation** connecting GoP decoherence kernels to void-scale CMB temperature behavior
- A **prediction-first pipeline** (predictions are generated before any measurements)
- A **single-void testbed** for exploring detectability, scaling, and sign (warm vs cold)
- A reproducible, modular codebase suitable for extension to stacking or survey analyses

---

## What this release is not

- Not a Boltzmann solver
- Not a ΛCDM replacement pipeline
- Not a full ISW analysis
- Not a survey-optimized estimator
- Not statistically conclusive on its own

Single-void CMB measurements are **noise-dominated by construction**.  
This repository is about **structure, scaling, and falsifiable calls**, not detection claims.

---

## Scientific Motivation

In the GoP framework, **quantum decoherence contributes an effective curvature term** that can act as a vacuum-like energy density.  
On large, underdense scales (cosmic voids), this contribution may manifest as a **temperature imprint on the CMB**.

This module explores that possibility via:

- A **proxy mapping** from void properties → decoherence weight
- A **bell-shaped decoherence kernel** consistent with prior GoP Γ(E) formulations
- A √N aggregation argument + geometric scaling for void size
- Explicit calibration anchors tied to observed stacked ISW amplitudes

---

## Repository Structure

```
GoP-vs-Lambda-Vacuum-Constant/
├── vacuum_scale/                      # existing scripts (unchanged)
├── void_cmb_toy/                      # new module 
│   ├── common/
│   ├── predictions/
|     |       ├──/generate_panels
│   ├── measurements/
│   │      ├──bootes_aperture_photometry.py
│   │      ├──bootes_aperture_photometry_plus.py
│   ├── runs/
│   ├── figures/
│   └── data/                          
├── requirements-void.txt              
├── README.md
└── README_void_cmb_toy.md 
```
---

## Core Physics (Toy Model)

All physics lives in:

common/gop_void_toy.py

markdown
Copy code

### Key Components

- **Void proxy**
g(z, |δ|) = (|δ| / δ_ref) × ((1 + z) / (1 + z_ref))^n

markdown
Copy code
- **Decoherence weight (bell curve)**
wΓ(g) = g · exp(1 − g)

yaml
Copy code
Peaks at `g = 1`, consistent with Γ(E) motivation in GoP.

- **Amplitude scaling**
- √N aggregation of coherence domains
- Geometric scaling ∝ R²
- Combined → ΔT ∝ R^(7/2) × wΓ(g)

- **Calibration anchors**
Used to fix the absolute scale without tuning per void.

---

## Anchor Presets (Pre-Registered)

| Preset | R_cal (Mpc) | z_cal | ΔT_cal | Motivation |
|------|------------|------|--------|-----------|
| baseline | 80 | 0.5 | 10 µK | Original GoP scaling reference |
| **A1_lowz (default)** | 55 | 0.3 | 10 µK | Typical observed voids |
| A2_lowz_band | 55 | 0.3 | 8 µK | Conservative ISW-aligned band |

The default for this release is **A1_lowz**.

---

## Boötes Void Prediction

Using literature-consensus values:

- Radius: **~62 Mpc**
- Redshift: **z ≈ 0.052**
- Underdensity (effective): **|δ| ≈ 0.8–0.9**

### Predicted ΔT_core (toy model)

| Anchor | ΔT_core (µK) |
|-----|-------------|
| baseline | ~4 µK |
| **A1_lowz** | **~20 µK** |
| A2_lowz_band | ~16 µK |

These values are **toy-level predictions**, intended to be checked against aperture photometry with explicit uncertainty.

---

## Generating Predictions & Figures

### Install dependencies
```bash
pip install -r requirements.txt```

Run predictions + figures

``` ./run_all.sh ```
Outputs:

runs/predictions_bootes_A1.json

figures/panelA_DeltaT_core_vs_R.png

figures/panelB_normalized_profile.png
