# TASKS.md — Cambodia Credit Risk Index Project

## Project Status Dashboard

| Component | Status | Notes |
|-----------|--------|-------|
| Data Preparation (NB 01) | ✅ Done | 156 obs, Jan 2013–Dec 2025, clean |
| Literature Review | ✅ Done | 5,900 words, 25 references |
| Exploratory Analysis (NB 02) | 🔲 Not started | |
| Parameter Estimation (NB 03) | 🔲 Not started | |
| CRI Computation (NB 04) | 🔲 Not started | |
| Stress Testing (NB 05) | 🔲 Not started | |
| COVID Analysis (NB 06) | 🔲 Not started | |
| Rolling Window (NB 07) | 🔲 Not started | |
| Robustness (NB 08) | 🔲 Not started | |
| Paper Writing | 🔲 Not started | |

---

## Phase 0: Setup & Environment

- [ ] Install Anaconda (includes Python, pandas, numpy, matplotlib, scipy, Jupyter)
- [ ] Create project folder: `cambodia-credit-risk/` with subdirectories: `data/raw/`, `data/processed/`, `notebooks/`, `figures/`, `paper/`
- [ ] Place your NBC raw CSV in `data/raw/`
- [ ] Open Jupyter Notebook and verify you can import pandas, numpy, matplotlib, scipy
- [ ] Copy `01_data_preparation.ipynb` into `notebooks/`
- [ ] Run Notebook 01 with your actual data — verify the 6 output CSVs are generated
- [ ] Verify spreads match expected values (e.g., USD spread ~5.11% in Dec 2021, KHR spread ~5.39% in Dec 2021)
- [ ] Copy `literature_review_full.md` into `paper/`

**Deliverable:** Working Python environment, Notebook 01 runs successfully, processed data files saved.

---

## Phase 1: Exploratory Analysis (Notebook 02)

### Statistics
- [ ] Compute full descriptive statistics for both spreads (mean, std, min, max, median, skewness, kurtosis, percentiles 5/25/50/75/95)
- [ ] Compute statistics by sub-period (pre-COVID: 2013–2019, COVID: 2020–2021, post-COVID: 2022–2025)
- [ ] Test for normality: Shapiro-Wilk test, Jarque-Bera test on both spread series
- [ ] Compute autocorrelation (ACF) and partial autocorrelation (PACF) for both spreads — this supports mean reversion
- [ ] Augmented Dickey-Fuller (ADF) test for stationarity on both spreads
- [ ] Compute correlation between USD and KHR spreads (full sample and by sub-period)

### Visualizations
- [ ] **Figure 1**: Dual time series plot — both spreads on same chart, shaded COVID region (Jan 2020–Dec 2021), annotated key events (Fed rate hikes 2022–2023, NBC policy changes)
- [ ] **Figure 2**: Histograms of each spread with normal distribution overlay
- [ ] **Figure 3**: Raw rates plot — all 4 underlying rates (term loan USD, term deposit USD, term loan KHR, term deposit KHR) to show what's driving the spreads
- [ ] **Figure 4**: Scatter plot of USD spread vs. KHR spread with correlation coefficient
- [ ] **Figure (optional)**: ACF/PACF plots for both spreads
- [ ] **Figure (optional)**: Box plots of spreads by year

### Save Outputs
- [ ] Save all figures as PNG to `figures/` folder (300 dpi for paper quality)
- [ ] Export descriptive statistics as a formatted table (for Section 4 of paper)

**Deliverable:** Notebook 02 complete with all figures and statistics. You now have a clear picture of your data's properties.

---

## Phase 2: Parameter Estimation (Notebook 03)

### MLE Estimation
- [ ] Write the negative log-likelihood function for the OU process:
  ```
  def neg_log_likelihood(params, data, dt):
      kappa, theta, sigma = params
      # ... (formula from roadmap)
  ```
- [ ] Estimate parameters for **USD spread**: $(\hat{\kappa}^{USD}, \hat{\theta}^{USD}, \hat{\sigma}^{USD})$
- [ ] Estimate parameters for **KHR spread**: $(\hat{\kappa}^{KHR}, \hat{\theta}^{KHR}, \hat{\sigma}^{KHR})$
- [ ] Compute standard errors using the Hessian (inverse of Fisher information matrix)
- [ ] Compute 95% confidence intervals for all 6 parameters
- [ ] Compute half-life of shocks: $t_{1/2} = \ln(2) / \kappa$ for each currency

### AR(1) Cross-Check
- [ ] Run OLS regression: $S_{t+1} = a + b \cdot S_t + \varepsilon_t$ for each currency
- [ ] Back out OU parameters from AR(1) coefficients:
  - $\hat{\kappa} = -\ln(\hat{b}) / \Delta t$
  - $\hat{\theta} = \hat{a} / (1 - \hat{b})$
  - $\hat{\sigma} = \text{std}(\varepsilon) \cdot \sqrt{2\hat{\kappa} / (1 - \hat{b}^2)}$
- [ ] Compare MLE and AR(1) parameter estimates — they should be very close

### Parameter Comparison Table
- [ ] Create Table 2 for the paper:

| Parameter | USD (MLE) | USD (AR1) | KHR (MLE) | KHR (AR1) |
|-----------|-----------|-----------|-----------|-----------|
| θ (long-run mean) | ? | ? | ? | ? |
| κ (mean reversion speed) | ? | ? | ? | ? |
| σ (volatility) | ? | ? | ? | ? |
| Half-life (months) | ? | — | ? | — |

### Key Questions to Answer
- [ ] Is $\theta^{KHR} > \theta^{USD}$? (Expected — KHR carries exchange rate risk premium)
- [ ] Is $\kappa^{KHR}$ higher or lower than $\kappa^{USD}$? (If lower → KHR shocks more persistent)
- [ ] Is $\sigma^{KHR} > \sigma^{USD}$? (If yes → KHR segment more volatile)
- [ ] Do MLE and AR(1) estimates agree? (Should be very close)

**Deliverable:** Notebook 03 complete. You have estimated OU parameters for both currencies with confidence intervals and cross-validation.

---

## Phase 3: CRI Computation (Notebook 04)

### Crisis Threshold
- [ ] Compute 95th percentile of historical spreads for each currency:
  - $S_c^{USD} = P_{95}(S_t^{USD})$
  - $S_c^{KHR} = P_{95}(S_t^{KHR})$
- [ ] Also compute 90th and 99th percentiles (for robustness later)

### Crisis Probability Time Series
- [ ] For each month $t$ and each currency, compute:
  - Conditional mean: $m^c(t) = \theta^c + (S_{t-1}^c - \theta^c)e^{-\kappa^c \Delta t}$
  - Conditional variance: $v^c(t) = \frac{(\sigma^c)^2}{2\kappa^c}(1 - e^{-2\kappa^c \Delta t})$
  - Crisis probability: $P(S_t^c > S_c^c) = 1 - \Phi\left(\frac{S_c^c - m^c(t)}{\sqrt{v^c(t)}}\right)$
- [ ] **Figure 6**: Plot crisis probability over time for both currencies on same chart, annotate COVID onset and key events

### Currency-Specific CRIs
- [ ] Compute $\text{CRI}^{USD}_t = 0.5 \cdot \hat{\sigma}^{USD} + 0.5 \cdot P_t^{USD}$ for each month
- [ ] Compute $\text{CRI}^{KHR}_t = 0.5 \cdot \hat{\sigma}^{KHR} + 0.5 \cdot P_t^{KHR}$ for each month
- [ ] **Figure 7**: Plot both currency CRIs over time

### System-Wide CRI
- [ ] Get USD/KHR lending shares from NBC annual reports (or use ~0.80/0.20 as default)
- [ ] Compute $\text{CRI}_{\text{Sys},t} = w_{USD} \cdot \text{CRI}^{USD}_t + w_{KHR} \cdot \text{CRI}^{KHR}_t$
- [ ] **Figure 8**: Plot system CRI alongside individual currency CRIs
- [ ] Determine appropriate CRI level interpretations (Low/Moderate/High thresholds based on your results)

**Deliverable:** Notebook 04 complete. You have CRI time series for USD, KHR, and System, with visualizations.

---

## Phase 4: Stress Testing (Notebook 05)

- [ ] Define stress scenarios: δ = 0.10 (mild), 0.30 (moderate), 0.50 (severe)
- [ ] For each scenario, compute stressed spreads: $S_t^{c,\text{stress}} = S_t^c(1 + \delta)$
- [ ] Re-estimate OU parameters on stressed data
- [ ] Recompute crisis probabilities and CRIs under each stress scenario
- [ ] Create Table 4:

| Scenario | CRI^USD | CRI^KHR | CRI_System | Δ from Baseline |
|----------|---------|---------|------------|-----------------|
| Baseline | ? | ? | ? | — |
| Mild (δ=0.1) | ? | ? | ? | ? |
| Moderate (δ=0.3) | ? | ? | ? | ? |
| Severe (δ=0.5) | ? | ? | ? | ? |

- [ ] **Figure 11**: Bar chart or grouped comparison of CRI values across stress scenarios
- [ ] Answer key question: Which currency is more fragile under stress?

**Deliverable:** Notebook 05 complete. Stress test results table and chart.

---

## Phase 5: COVID Sub-Period Analysis (Notebook 06)

- [ ] Split data into three periods:
  - Pre-COVID: Jan 2013 – Dec 2019 (84 observations)
  - COVID: Jan 2020 – Dec 2021 (24 observations)
  - Post-COVID: Jan 2022 – Dec 2025 (48 observations)
- [ ] Estimate OU parameters separately for each sub-period, each currency (6 sets of parameters)
- [ ] Compute CRI for each sub-period, each currency
- [ ] Create Table 5:

| Period | θ_USD | κ_USD | σ_USD | CRI_USD | θ_KHR | κ_KHR | σ_KHR | CRI_KHR |
|--------|-------|-------|-------|---------|-------|-------|-------|---------|
| Pre-COVID | ? | ? | ? | ? | ? | ? | ? | ? |
| COVID | ? | ? | ? | ? | ? | ? | ? | ? |
| Post-COVID | ? | ? | ? | ? | ? | ? | ? | ? |

- [ ] **Figure 9**: Side-by-side parameter comparison across periods (bar charts)
- [ ] Answer key questions:
  - [ ] Did volatility (σ) spike during COVID for both currencies?
  - [ ] Which currency was hit harder?
  - [ ] Did post-COVID parameters return to pre-COVID levels?
  - [ ] Did mean reversion speed (κ) change — did shocks become more or less persistent?

**Deliverable:** Notebook 06 complete. COVID impact analysis with parameter shift table.

---

## Phase 6: Rolling Window (Notebook 07)

- [ ] Choose window size: 24 months (provides enough observations per window for 3-parameter estimation)
- [ ] For each month $t$ from month 25 to month 156:
  - Take the 24 observations from $t-23$ to $t$
  - Estimate $(\kappa_t, \theta_t, \sigma_t)$ for each currency
  - Compute crisis probability and CRI at time $t$
- [ ] **Figure 10**: Three-panel plot showing rolling $\hat{\kappa}_t$, $\hat{\theta}_t$, $\hat{\sigma}_t$ over time for both currencies
  - Annotate with COVID, Fed rate hikes, NBC policy changes
- [ ] Discuss: Are USD and KHR risk dynamics converging or diverging over time?

**Deliverable:** Notebook 07 complete. Rolling parameter evolution plots.

---

## Phase 7: Robustness Checks (Notebook 08)

- [ ] **Check 1 — Outstanding Amount rates**: Repeat full analysis (NB 03 + 04) using Outstanding Amount spreads instead of New Amount
  - Compare parameter estimates with New Amount results
  - Does CRI ranking (USD vs. KHR) hold?
  - Does New Amount CRI give earlier/sharper signals? (It should)
- [ ] **Check 2 — Alternative crisis thresholds**: Recompute CRI using 90th and 99th percentiles
  - Are CRI patterns qualitatively similar?
- [ ] **Check 3 — Alternative CRI weights**: Test α=0.3/β=0.7 and α=0.7/β=0.3
  - Does the relative ranking of USD vs. KHR change?
- [ ] **Check 4 — Equal system weights**: Compute system CRI with w=0.50/0.50
  - How different from loan-share weighted?
- [ ] Create Table 6 (robustness summary):

| Check | Main Finding Holds? | Notes |
|-------|-------------------|-------|
| Outstanding Amount rates | ? | |
| 90th percentile threshold | ? | |
| 99th percentile threshold | ? | |
| Equal system weights | ? | |
| CRI weights (0.3/0.7) | ? | |
| CRI weights (0.7/0.3) | ? | |

**Deliverable:** Notebook 08 complete. Robustness summary table.

---

## Phase 8: Paper Writing

### Draft 1 — Structure
- [ ] Set up paper.qmd with all section headers, empty tables, figure placeholders
- [ ] Insert all table shells with "?" values ready to fill

### Section-by-Section Writing
- [ ] **Section 1: Introduction** (2–3 pages)
  - [ ] Opening: significance of credit risk in banking
  - [ ] Cambodia context: rapid growth, dollarization, data gap
  - [ ] Your contribution: dual-currency CRI, first for Cambodia
  - [ ] Three research questions
  - [ ] Paper roadmap
- [ ] **Section 2: Literature Review** (8–10 pages)
  - [ ] Revise `literature_review_full.md` based on any new sources found
  - [ ] Ensure all 25 references are properly cited
  - [ ] Add any additional Cambodia-specific references found during research
- [ ] **Section 3: Methodology** (5–6 pages)
  - [ ] Data selection rationale (New Amount, Term Loans/Deposits)
  - [ ] Spread definition with equations
  - [ ] OU model specification with full SDE
  - [ ] MLE estimation procedure with log-likelihood
  - [ ] Crisis threshold and probability formulas
  - [ ] CRI construction (currency-specific and system)
  - [ ] Stress testing methodology
  - [ ] Sub-period and rolling window approach
  - [ ] Robustness check descriptions
- [ ] **Section 4: Data Description** (2–3 pages)
  - [ ] Fill in descriptive statistics table with actual values from NB 02
  - [ ] Insert figures 1–4
  - [ ] Discuss KHR spread compression and structural shift
  - [ ] Discuss correlation between USD and KHR spreads
- [ ] **Section 5: Results** (5–6 pages)
  - [ ] Fill in all parameter tables with actual values from NB 03
  - [ ] Insert CRI figures from NB 04
  - [ ] COVID sub-period comparison from NB 06
  - [ ] Rolling window results from NB 07
  - [ ] Stress test results from NB 05
  - [ ] Robustness summary from NB 08
- [ ] **Section 6: Discussion** (2–3 pages)
  - [ ] Interpret findings re: dollarization and risk
  - [ ] COVID-19 impact discussion
  - [ ] Early warning value assessment
  - [ ] Policy implications (NBC, de-dollarization, banks)
  - [ ] Limitations (be honest)
  - [ ] Future research directions
- [ ] **Section 7: Conclusion** (1 page)
- [ ] **References** — ensure all in-text citations match reference list

### Polish
- [ ] Ensure consistent notation throughout paper
- [ ] Number all tables and figures sequentially
- [ ] Cross-reference tables and figures in text ("as shown in Table 2", "Figure 5 illustrates")
- [ ] Proofread for grammar and clarity
- [ ] Check page count (target: 18–28 pages)
- [ ] Format references consistently (author-date style)

**Deliverable:** Complete paper draft ready for review.

---

## Phase 9: Final Review & Interview Prep

- [ ] Re-read entire paper from start to finish for flow and consistency
- [ ] Verify all numbers in tables match notebook outputs
- [ ] Ensure all figures are high-resolution and properly labeled
- [ ] Practice the 60-second pitch (see Project Guide Section 8)
- [ ] Prepare answers for likely follow-up questions
- [ ] Read abstracts of 5 key papers: Ho & Saunders (1981), Vasicek (1977), Duma (2011), Menon (2008), Drehmann & Juselius (2014)
- [ ] Be ready to explain: What is mean reversion? What is MLE? What is the OU process? Why dual-currency?

**Deliverable:** Finished paper + interview confidence.

---

## Files Completed So Far

| File | Location | Status |
|------|----------|--------|
| `01_data_preparation.ipynb` | `/mnt/user-data/outputs/` | ✅ Complete |
| `literature_review_full.md` | `/mnt/user-data/outputs/` | ✅ Complete |
| `literature_review_guide.qmd` | `/mnt/user-data/outputs/` | ✅ Complete |
| `roadmap_v3_dual_currency_final.qmd` | `/mnt/user-data/outputs/` | ✅ Complete |
| `project_guide.md` | This file | ✅ Complete |
| `tasks.md` | This file | ✅ Complete |

---

## Quick Reference: Key Dates for Chart Annotations

| Date | Event | Impact on Spreads |
|------|-------|-------------------|
| Jan 2013 | Sample start | — |
| Mar 2020 | Cambodia's first COVID case, NBC restructuring begins | Spreads may widen |
| Jun 2022 | NBC restructuring program expires | NPLs begin revealing true quality |
| Mar 2022 | Fed begins rate hiking cycle (0% → 5.25%) | USD spreads affected |
| Jul 2023 | Fed reaches peak rate (5.25–5.50%) | USD funding costs peak |
| Sep 2024 | Fed begins rate cuts | USD funding pressure eases |
| Dec 2025 | Sample end | — |
