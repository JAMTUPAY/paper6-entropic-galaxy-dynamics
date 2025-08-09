# Entropic Dynamics of Galaxies (EDG) — No Dark Matter

**Goal.** Test whether a single entropic acceleration scale, fixed by a universal QCD constant, can reproduce galaxy rotation curves from baryons alone (no dark matter).

**Key idea.** Use the QCD RG-entropy constant, \(|\Delta S_{\rm RG}|\approx 9.81\,k_B\) (Paper 1), to set an acceleration scale
\[
a_0 \;=\; \frac{\Delta S_{\rm RG}}{3\pi}\cdot\frac{c\,H_0}{2\pi}\,,
\]
then compare three models against rotation-curve data:
- `newtonian`  : \(g=g_b\)
- `edg1`       : MOND-like “simple” form with the **entropy-fixed** \(a_0\)
- `rar`        : Radial-acceleration-relation (RAR) form with the **entropy-fixed** \(a_0\)

The mapping is a **hypothesis** we are testing. The constant itself is established independently in Paper 1.  [oai_citation:2‡Universal_Entropy_Mass_Relation_in_QCD.pdf](file-service://file-AgPfRtTfqZqHT9dxHGQaGe)  For a cross‑scale application of the same constant to neutron stars, see Paper 4.  [oai_citation:3‡Entropy_Constrained_Neutron_Stars_from_a_Universal_QCD_Bound.pdf](file-service://file-6Uk6jGG9RhKSaasGG7Bj2E)

---

## Quick start (macOS)

```bash
# 1) clone your repo, then inside the repo:
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2) run on the included synthetic example
python scripts/run_one.py data/example.csv --model edg1

# Outputs:
# - outputs/results.csv
# - outputs/rotation_curve.png
# - outputs/fit_report.txt
