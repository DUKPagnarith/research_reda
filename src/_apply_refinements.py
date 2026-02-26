#!/usr/bin/env python3
"""
Apply technical refinements to the Research_Reda notebooks.
This script modifies JSON cells in-place for three notebooks:
  1. 07_rolling_window.ipynb  — window 24 → 36
  2. 03_parameter_estimation.ipynb — OU vs CIR defense, exact discretization, FX risk premium
"""

import json
import copy
import os

NOTEBOOK_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────
def load_nb(name):
    path = os.path.join(NOTEBOOK_DIR, name)
    with open(path, 'r') as f:
        return json.load(f), path

def save_nb(nb, path):
    with open(path, 'w') as f:
        json.dump(nb, f, indent=4, ensure_ascii=False)
    print(f"  ✅ Saved: {path}")

def make_md_cell(lines):
    """Create a markdown cell from a list of raw lines (each ending with \\n except the last)."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    }

# ─────────────────────────────────────────────────────────────────────────────
# 1. Notebook 07 — Rolling Window 24 → 36
# ─────────────────────────────────────────────────────────────────────────────
def patch_07():
    nb, path = load_nb("07_rolling_window.ipynb")
    cells = nb["cells"]
    changed = 0

    for cell in cells:
        src = cell.get("source", [])
        new_src = []
        for line in src:
            # Change window = 24 → window = 36
            if "window = 24" in line:
                line = line.replace("window = 24", "window = 36")
                changed += 1
            # Update title text
            if "24-Month" in line:
                line = line.replace("24-Month", "36-Month")
                changed += 1
            if "24-month" in line:
                line = line.replace("24-month", "36-month")
                changed += 1
            if "24 months" in line and "only 24 observations" not in line:
                line = line.replace("24 months", "36 months")
                changed += 1
            if "24 observations" in line:
                line = line.replace("24 observations", "36 observations")
                changed += 1
            new_src.append(line)
        cell["source"] = new_src

    # Update the intro markdown cell to explain why 36
    intro_cell = cells[0]
    intro_cell["source"] = [
        "# Notebook 07 — Rolling Window Analysis\n",
        "\n",
        "## Time-Varying OU Parameters (36-Month Rolling Window)\n",
        "\n",
        "Notebook 03 estimated a single set of OU parameters for each currency over the entire 13-year sample. But the KHR spread compressed from ~24% to ~5%, meaning the \"true\" parameters changed dramatically over time. This notebook tracks parameter evolution by re-estimating the OU model on a **rolling 36-month window**.\n",
        "\n",
        "**Why 36 months (not 24)?** With 3 parameters to estimate (κ, θ, σ), the MLE requires enough transitions for the log-likelihood surface to be well-defined. A 24-month window provides only 23 transitions, which often leads to a flat likelihood surface and unreliable κ estimates. A 36-month window (35 transitions) provides substantially more statistical stability while still being short enough to capture structural shifts like the KHR compression."
    ]

    # Update interpretation cell about κ noise (the cell starting with "### Interpretation — Figure 10")
    for cell in cells:
        src = cell.get("source", [])
        if any("### Interpretation — Figure 10" in l for l in src):
            new_src = []
            for line in src:
                if "only 24 observations" in line:
                    line = line.replace(
                        "mean reversion speed is the hardest OU parameter to estimate precisely with only 24 observations",
                        "mean reversion speed is the hardest OU parameter to estimate precisely, though the 36-month window provides more stability than shorter alternatives"
                    )
                new_src.append(line)
            cell["source"] = new_src

    save_nb(nb, path)
    print(f"  → {changed} text replacements in 07_rolling_window.ipynb")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Notebook 03 — Three new/modified cells
# ─────────────────────────────────────────────────────────────────────────────
def patch_03():
    nb, path = load_nb("03_parameter_estimation.ipynb")
    cells = nb["cells"]

    # ── A. Find the MLE interpretation cell and expand the θ discussion (FX risk premium) ──
    for i, cell in enumerate(cells):
        src = cell.get("source", [])
        if any("### Interpretation — MLE Results" in l for l in src):
            new_src = []
            for line in src:
                if "reflecting the **exchange rate risk premium**" in line:
                    line = "The KHR equilibrium spread (8.07%) exceeds the USD (6.44%) by 1.6 pp. This gap reflects an **exchange rate risk premium** — banks demand a higher margin on riel loans to compensate for potential KHR depreciation against the USD. Importantly, the massive KHR spread compression from ~24% to ~5% is **not purely a reduction in credit risk**; it also captures the evaporation of this FX risk premium as public confidence in the riel grew and the NBC stabilized the exchange rate through reserve management and de-dollarization incentives. Note that the KHR SE for θ (4.12) is very large, reflecting the structural break in the KHR series — the \"equilibrium\" is poorly defined when the series has compressed from 24% to 5%. This motivates the rolling window analysis in Notebook 07.\n"
                new_src.append(line)
            cell["source"] = new_src
            mle_interp_idx = i
            break

    # ── B. Insert OU vs CIR defense cell right after the MLE interpretation cell ──
    cir_defense_cell = make_md_cell([
        "### Why Ornstein-Uhlenbeck Instead of Cox-Ingersoll-Ross?\n",
        "\n",
        "An interviewer may ask why we chose the OU process over the **Cox-Ingersoll-Ross (CIR)** model, which scales volatility with the spread level and prevents negative values:\n",
        "\n",
        "$$dS_t = \\kappa(\\theta - S_t)\\,dt + \\sigma\\sqrt{S_t}\\,dW_t \\quad \\text{(CIR)}$$\n",
        "\n",
        "**Our defense for choosing OU:**\n",
        "\n",
        "1. **Tractable MLE:** The OU process has an exact Gaussian transition density, giving a clean, globally convex log-likelihood that `scipy.optimize.minimize` handles reliably. The CIR exact transition density is a **non-central chi-squared** distribution, whose log-likelihood involves Bessel functions and is numerically unstable near certain parameter boundaries — convergence failures and local optima are common.\n",
        "\n",
        "2. **Negative values are not a practical concern:** The OU model theoretically permits negative spreads, but our data never approaches zero (USD minimum = 2.88%, KHR minimum = 4.24%). Over the 156-month sample, the OU model places negligible probability mass on negative spreads given the estimated parameters.\n",
        "\n",
        "3. **Diagnostics support the choice:** The standardized residuals from the OU fit (Figure 5) are approximately standard normal for USD and reasonable for KHR. If CIR's $\\sqrt{S_t}$ scaling were essential, we would see systematic residual patterns correlated with the spread level — our diagnostics do not show this for USD (though KHR shows some heteroskedasticity related to the structural break, not the level).\n",
        "\n",
        "4. **Precedent:** The OU/Vasicek (1977) framework is the standard in the interest rate modeling literature for mean-reverting processes. The CIR extension is typically motivated for short-rate models where rates can approach zero, which is not the case for lending-deposit spreads.\n",
        "\n",
        "**Bottom line:** We chose analytical tractability over theoretical elegance. The CIR model's additional complexity does not provide meaningful benefit for this dataset."
    ])
    cells.insert(mle_interp_idx + 1, cir_defense_cell)

    # ── C. Find the AR(1) section header and insert exact discretization cell before it ──
    for i, cell in enumerate(cells):
        src = cell.get("source", [])
        if any("## 2. AR(1) Cross-Check" in l for l in src):
            exact_disc_cell = make_md_cell([
                "### Exact Discrete-Time Solution (Not Euler-Maruyama)\n",
                "\n",
                "**Important technical note:** Throughout this project, all discrete-time representations use the **exact solution** to the OU SDE, not the Euler-Maruyama approximation. The exact solution is:\n",
                "\n",
                "$$S_{t+\\Delta t} = S_t e^{-\\kappa \\Delta t} + \\theta(1 - e^{-\\kappa \\Delta t}) + \\sigma \\sqrt{\\frac{1 - e^{-2\\kappa \\Delta t}}{2\\kappa}}\\, Z$$\n",
                "\n",
                "where $Z \\sim \\mathcal{N}(0,1)$ and $\\Delta t = 1/12$ for monthly data.\n",
                "\n",
                "This means:\n",
                "- **Conditional mean:** $\\mathbb{E}[S_{t+\\Delta t} | S_t] = \\theta + (S_t - \\theta)e^{-\\kappa\\Delta t}$ — used in our MLE and for the AR(1) mapping below\n",
                "- **Conditional variance:** $\\text{Var}(S_{t+\\Delta t} | S_t) = \\frac{\\sigma^2}{2\\kappa}(1 - e^{-2\\kappa\\Delta t})$ — used in our MLE log-likelihood\n",
                "\n",
                "The simpler Euler-Maruyama discretization ($S_{t+\\Delta t} \\approx S_t + \\kappa(\\theta - S_t)\\Delta t + \\sigma\\sqrt{\\Delta t}\\, Z$) introduces $O(\\Delta t)$ bias in parameter estimates. With monthly data ($\\Delta t = 1/12$), this bias can be non-negligible — the exact solution eliminates it entirely.\n",
                "\n",
                "The AR(1) cross-check below maps $S_{t+1} = a + bS_t + \\varepsilon_t$ back to OU parameters using the exact relationships: $b = e^{-\\kappa\\Delta t}$, $a = \\theta(1-b)$, confirming consistency with the MLE estimates."
            ])
            cells.insert(i, exact_disc_cell)
            break

    save_nb(nb, path)
    print("  → Patched 03_parameter_estimation.ipynb (CIR defense + exact discretization + FX premium)")

# ─────────────────────────────────────────────────────────────────────────────
# Run all patches
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Applying technical refinements...\n")
    print("── Notebook 07 ──")
    patch_07()
    print("\n── Notebook 03 ──")
    patch_03()
    print("\n✅ All refinements applied successfully.")
