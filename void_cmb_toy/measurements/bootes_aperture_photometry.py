"""
Minimal single-void aperture photometry on Planck CMB maps (HEALPix).

Purpose
- Compute a compensated aperture statistic for one void:
    ΔT = <T>_core - <T>_rim
  using a disc (core) and annulus (rim) scaled to an input angular radius θ_R.

What this minimal script includes
- HEALPix map + mask loading
- RA/Dec (ICRS) -> Galactic (l,b) conversion (astropy)
- Masking + NaN/UNSEEN exclusion
- JSON output (stdout + optional --out_json)

What this script intentionally does NOT include
- Bootstrap uncertainty
- Random-center null distribution
- Multi-map consistency sweeps

For those, use:
  measurements/bootes_aperture_photometry_plus.py
"""

import argparse
import json
import numpy as np
import healpy as hp
from astropy.coordinates import SkyCoord
import astropy.units as u


def load_healpix_map(map_path: str, field: int = 0) -> np.ndarray:
    m = hp.read_map(map_path, field=field, verbose=False)
    return np.array(m, dtype=np.float64)


def to_uK(m: np.ndarray, map_in_uK: bool) -> np.ndarray:
    return m if map_in_uK else (m * 1e6)


def load_keep_mask(mask_path: str, field: int = 0, threshold: float = 0.8) -> np.ndarray:
    """
    Load a HEALPix mask and return a boolean keep-mask.
    Assumes mask values are in [0,1] (confidence/apodized) or {0,1}.
    """
    mk = hp.read_map(mask_path, field=field, verbose=False)
    mk = np.array(mk, dtype=np.float64)
    return mk >= threshold


def radec_to_galactic(ra_deg: float, dec_deg: float) -> tuple[float, float]:
    c = SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg, frame="icrs")
    g = c.galactic
    return float(g.l.deg), float(g.b.deg)


def disc_mask(nside: int, vec_center: np.ndarray, radius_rad: float) -> np.ndarray:
    ipix = hp.query_disc(nside, vec_center, radius_rad, inclusive=False)
    m = np.zeros(hp.nside2npix(nside), dtype=bool)
    m[ipix] = True
    return m


def annulus_mask(nside: int, vec_center: np.ndarray, r_in_rad: float, r_out_rad: float) -> np.ndarray:
    outer = disc_mask(nside, vec_center, r_out_rad)
    inner = disc_mask(nside, vec_center, r_in_rad)
    return outer & (~inner)


def aperture_photometry_deltaT_uK(
    cmb_uK: np.ndarray,
    keep_mask: np.ndarray,
    lon_deg: float,
    lat_deg: float,
    theta_R_deg: float,
    core_frac: float = 0.6,
    rim_in_frac: float = 0.8,
    rim_out_frac: float = 1.2,
    min_pix: int = 50,
) -> dict:
    """
    Compute ΔT = <T>_core - <T>_rim (µK) for a single target.

    Coordinates are Galactic:
      lon_deg = l, lat_deg = b
    """
    nside_map = hp.get_nside(cmb_uK)
    nside_mask = hp.get_nside(keep_mask.astype(np.float64))
    if nside_map != nside_mask:
        raise ValueError(f"NSIDE mismatch: map nside={nside_map} vs mask nside={nside_mask}")

    # healpy angles: theta = colatitude, phi = longitude (radians)
    phi = np.deg2rad(lon_deg)
    theta = np.deg2rad(90.0 - lat_deg)
    vec = hp.ang2vec(theta, phi)

    theta_R = np.deg2rad(theta_R_deg)
    core_r = core_frac * theta_R
    rim_in = rim_in_frac * theta_R
    rim_out = rim_out_frac * theta_R

    core = disc_mask(nside_map, vec, core_r)
    rim = annulus_mask(nside_map, vec, rim_in, rim_out)

    good = np.isfinite(cmb_uK)  # also removes NaNs
    core_sel = core & keep_mask & good
    rim_sel = rim & keep_mask & good

    if core_sel.sum() < min_pix or rim_sel.sum() < min_pix:
        raise RuntimeError(
            "Too few unmasked pixels in core/rim. "
            "Try a different θ_R, loosen mask threshold, or use a less aggressive mask."
        )

    Tcore = float(np.mean(cmb_uK[core_sel]))
    Trim = float(np.mean(cmb_uK[rim_sel]))
    dT = Tcore - Trim

    return {
        "DeltaT_uK": dT,
        "Tcore_uK": Tcore,
        "Trim_uK": Trim,
        "n_core_pix": int(core_sel.sum()),
        "n_rim_pix": int(rim_sel.sum()),
        "theta_R_deg": float(theta_R_deg),
        "core_frac": float(core_frac),
        "rim_in_frac": float(rim_in_frac),
        "rim_out_frac": float(rim_out_frac),
        "gal_lon_deg": float(lon_deg),
        "gal_lat_deg": float(lat_deg),
    }


def main():
    p = argparse.ArgumentParser()

    # Inputs
    p.add_argument("--cmb_map", required=True, help="Path to Planck CMB HEALPix FITS (e.g., SMICA).")
    p.add_argument("--cmb_field", type=int, default=0, help="FITS field index for temperature (default 0).")
    p.add_argument("--map_in_uK", action="store_true", help="Set if the CMB map is already in µK.")

    p.add_argument("--mask", required=True, help="Path to a HEALPix mask FITS.")
    p.add_argument("--mask_field", type=int, default=0, help="Mask field index (default 0).")
    p.add_argument("--mask_threshold", type=float, default=0.8, help="Keep pixels with mask >= threshold.")

    # Target center (ICRS). Defaults match the Boötes example you’ve been using.
    p.add_argument("--ra_deg", type=float, default=222.5, help="Target center RA (deg, ICRS).")
    p.add_argument("--dec_deg", type=float, default=46.0, help="Target center Dec (deg, ICRS).")

    # Aperture geometry
    p.add_argument("--theta_R_deg", type=float, default=14.0, help="Void angular radius θ_R (deg).")
    p.add_argument("--core_frac", type=float, default=0.6, help="Core radius fraction of θ_R.")
    p.add_argument("--rim_in_frac", type=float, default=0.8, help="Rim inner radius fraction of θ_R.")
    p.add_argument("--rim_out_frac", type=float, default=1.2, help="Rim outer radius fraction of θ_R.")
    p.add_argument("--min_pix", type=int, default=50, help="Minimum unmasked pixels required per region.")

    # Output
    p.add_argument("--out_json", default="", help="If set, write JSON output to this path.")

    args = p.parse_args()

    cmb = load_healpix_map(args.cmb_map, field=args.cmb_field)
    cmb_uK = to_uK(cmb, map_in_uK=args.map_in_uK)

    keep = load_keep_mask(args.mask, field=args.mask_field, threshold=args.mask_threshold)

    l_deg, b_deg = radec_to_galactic(args.ra_deg, args.dec_deg)

    measurement = aperture_photometry_deltaT_uK(
        cmb_uK=cmb_uK,
        keep_mask=keep,
        lon_deg=l_deg,
        lat_deg=b_deg,
        theta_R_deg=args.theta_R_deg,
        core_frac=args.core_frac,
        rim_in_frac=args.rim_in_frac,
        rim_out_frac=args.rim_out_frac,
        min_pix=args.min_pix,
    )

    payload = {
        "script": "measurements/bootes_aperture_photometry.py",
        "inputs": {
            "cmb_map": args.cmb_map,
            "cmb_field": args.cmb_field,
            "map_in_uK": bool(args.map_in_uK),
            "mask": args.mask,
            "mask_field": args.mask_field,
            "mask_threshold": args.mask_threshold,
            "ra_deg": args.ra_deg,
            "dec_deg": args.dec_deg,
            "theta_R_deg": args.theta_R_deg,
            "core_frac": args.core_frac,
            "rim_in_frac": args.rim_in_frac,
            "rim_out_frac": args.rim_out_frac,
            "min_pix": args.min_pix,
        },
        "measurement": measurement,
        "notes": {
            "statistic": "DeltaT_uK = mean(core) - mean(rim)",
            "scope": "Single-void quick-look. For bootstrap + null distribution + multi-map support, use bootes_aperture_photometry_plus.py.",
        },
    }

    txt = json.dumps(payload, indent=2)
    print(txt)

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            f.write(txt)


if __name__ == "__main__":
    main()
