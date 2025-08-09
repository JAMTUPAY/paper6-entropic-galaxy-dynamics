import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.edg import predict

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="Input CSV with columns: R_kpc,V_obs_kms,V_err_kms,V_gas_kms,V_disk_kms,V_bul_kms")
    ap.add_argument("--model", default="edg1", choices=["newtonian","edg1","rar"])
    ap.add_argument("--ml-disk", type=float, default=0.5)
    ap.add_argument("--ml-bulge", type=float, default=0.7)
    ap.add_argument("--H0", type=float, default=70.0, help="Hubble constant [km/s/Mpc]")
    ap.add_argument("--deltaS", type=float, default=9.81, help="ΔS_RG in k_B units")
    ap.add_argument("--out", default="outputs")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    df = pd.read_csv(args.csv)
    required = ["R_kpc","V_obs_kms","V_err_kms","V_gas_kms","V_disk_kms","V_bul_kms"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing columns: {missing}")

    V_pred = predict(
        df["R_kpc"].values,
        df["V_gas_kms"].values,
        df["V_disk_kms"].values,
        df["V_bul_kms"].values,
        model=args.model,
        ml_disk=args.ml_disk,
        ml_bulge=args.ml_bulge,
        H0=args.H0,
        deltaS_kB=args.deltaS
    )

    out_df = df.copy()
    out_df["V_pred_kms"] = V_pred
    out_csv = os.path.join(args.out, "results.csv")
    out_df.to_csv(out_csv, index=False)

    # χ^2 with provided errors (if present)
    if "V_err_kms" in df.columns:
        chi2 = np.sum(((df["V_obs_kms"].values - V_pred) / np.maximum(df["V_err_kms"].values, 1e-6))**2)
        dof = max(len(df) - 2, 1)
        redchi2 = chi2 / dof
    else:
        chi2 = np.nan
        redchi2 = np.nan

    # Plot
    plt.figure()
    plt.errorbar(df["R_kpc"], df["V_obs_kms"], yerr=df["V_err_kms"], fmt="o", label="Observed")
    plt.plot(df["R_kpc"], V_pred, label=f"Predicted ({args.model})")
    plt.xlabel("R [kpc]")
    plt.ylabel("V [km/s]")
    plt.title(f"Rotation curve — model={args.model}, H0={args.H0}, M/Ld={args.ml_disk}, M/Lb={args.ml_bulge}")
    plt.legend()
    figpath = os.path.join(args.out, "rotation_curve.png")
    plt.savefig(figpath, dpi=150, bbox_inches="tight")

    with open(os.path.join(args.out, "fit_report.txt"), "w") as f:
        f.write(f"Model      : {args.model}\n")
        f.write(f"H0         : {args.H0} km/s/Mpc\n")
        f.write(f"ΔS_RG (kB) : {args.deltaS}\n")
        f.write(f"M/L (disk) : {args.ml_disk}\n")
        f.write(f"M/L (bulge): {args.ml_bulge}\n")
        f.write(f"N points   : {len(df)}\n")
        f.write(f"chi^2      : {chi2:.3f}\n")
        f.write(f"red. chi^2 : {redchi2:.3f}\n")
        f.write(f"Outputs    : {out_csv}, {figpath}\n")

    print(f"Done. Results: {out_csv}\nPlot: {figpath}")

if __name__ == "__main__":
    main()
