import argparse
import json
from common.gop_void_toy import (
    DeltaT_core_uK, calibrate_Vc, ANCHORS, DEFINITION_CAVEAT
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchor_preset", default="A1_lowz",
                    choices=["baseline", "A1_lowz", "A2_lowz_band"])
    ap.add_argument("--out_json", default="")
    ap.add_argument("--delta_abs", type=float, default=0.85)
    ap.add_argument("--z", type=float, default=0.052)
    ap.add_argument("--R_Mpc", type=float, default=62.0)
    ap.add_argument("--delta_band", type=float, nargs=2, default=[0.75, 0.90],
                    help="Two values: low high for δ sensitivity band.")
    ap.add_argument("--n_exp", type=float, default=3.0)

    args = ap.parse_args()

    Vc = calibrate_Vc(anchor_preset=args.anchor_preset, n_exp=args.n_exp)

    def predict(delta_val: float) -> float:
        return DeltaT_core_uK(args.R_Mpc, args.z, delta_val, Vc_m3=Vc, n_exp=args.n_exp)

    dT_lock = predict(args.delta_abs)
    dT_low = predict(args.delta_band[0])
    dT_high = predict(args.delta_band[1])

    payload = {
        "object": "Bootes Void",
        "anchor_preset": args.anchor_preset,
        "anchor_values": ANCHORS[args.anchor_preset],
        "inputs": {
            "R_Mpc": args.R_Mpc,
            "z": args.z,
            "delta_lock_abs": args.delta_abs,
            "delta_band_abs": args.delta_band,
            "n_exp": args.n_exp
        },
        "calibration": {
            "Vc_m3": Vc
        },
        "prediction": {
            "DeltaT_core_uK": dT_lock,
            "delta_sensitivity": {
                "low_delta_abs": args.delta_band[0],
                "low_DeltaT_uK": dT_low,
                "high_delta_abs": args.delta_band[1],
                "high_DeltaT_uK": dT_high
            }
        },
        "definition_caveat": DEFINITION_CAVEAT
    }

    txt = json.dumps(payload, indent=2)
    print(txt)

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            f.write(txt)

if __name__ == "__main__":
    main()
