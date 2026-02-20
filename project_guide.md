# Project Guide: Credit Risk and Dollarization in Cambodia

## A Dual-Currency Analysis Using Interest Rate Spreads (2013–2025)

---

## 1. Project Overview

### 1.1 Working Title

**"Credit Risk and Dollarization in Cambodia: A Dual-Currency Analysis Using Interest Rate Spreads (2013–2025)"**

### 1.2 Research Questions

1. How do credit risk dynamics differ between USD and KHR lending in Cambodia's banking sector?
2. Which currency segment is more sensitive to financial shocks, particularly the COVID-19 pandemic?
3. Can a composite dual-currency Credit Risk Index serve as an effective early warning tool for monitoring financial stability?

### 1.3 The Big Idea

Cambodia's banking sector operates in two currencies simultaneously — roughly 80% of lending is in USD and 20% in KHR. Credit risk may behave very differently depending on which currency a loan is denominated in. By modeling the interest rate spread (loan rate minus deposit rate) separately for each currency using a mean-reverting Ornstein-Uhlenbeck stochastic process, we construct currency-specific Credit Risk Indices and a system-wide composite index. Comparing how these indices behave — especially during the COVID-19 shock — reveals whether dollarization amplifies or dampens credit risk, and which segment serves as a better early warning signal.

### 1.4 Why This Topic Is Strong

- **Original**: No existing study applies a dual-currency CRI framework to Cambodia
- **Policy-relevant**: Cambodia is actively pursuing de-dollarization — results speak directly to whether that changes the risk profile
- **Data-feasible**: Uses only publicly available NBC interest rate data (no loan-level data needed)
- **Technically impressive**: Stochastic modeling, MLE estimation, comparative analysis, stress testing, rolling windows
- **Interview-ready**: Demonstrates deep understanding of Cambodia's unique banking landscape
- **Excellent sample size**: 156 monthly observations (Jan 2013 – Dec 2025) spanning pre-COVID, COVID, and post-COVID periods

---

## 2. Your Data

### 2.1 Source and Coverage

| Item | Detail |
|------|--------|
| Source | National Bank of Cambodia (NBC) Statistical Reports |
| Period | January 2013 – December 2025 |
| Frequency | Monthly |
| Observations | 156 per currency |
| Currencies | KHR (Cambodian Riel) and USD (US Dollar) |
| Coverage | Deposit money banks (commercial + specialized banks) |

### 2.2 Rate Types in the NBC Data

The NBC reports two versions of each rate:

| Version | What It Measures | Speed of Response |
|---------|-----------------|-------------------|
| **New Amount** (primary) | Rates on newly issued loans/deposits that month | Fast — reflects banks' current risk pricing |
| **Outstanding Amount** (robustness) | Average rate across all existing loans/deposits | Slow — diluted by legacy rates |

**Decision: Use "New Amount" rates for primary analysis.** For an early warning indicator, you want the series that reacts fastest to changing risk conditions. Outstanding Amount rates are used only as a robustness check.

### 2.3 Product Selection

| Product | Use? | Rationale |
|---------|------|-----------|
| **Term Loans** | **Yes — primary** | Most representative of standard credit risk pricing |
| Overdraft | No | Priced for flexibility, not pure credit risk |
| Credit Card | No | Bundled convenience premiums distort the signal |
| Other Loans | No | Ambiguous composition |

| Product | Use? | Rationale |
|---------|------|-----------|
| **Term Deposits** | **Yes — primary** | Best maturity-match with term loans |
| Demand Deposits | No | Near-zero rates, priced for liquidity |
| Saving Deposits | No | Partially liquidity-driven |
| Other Deposits | No | Ambiguous |

### 2.4 Computed Spreads

$$S_t^{USD} = r_{\text{Term Loans},t}^{USD} - r_{\text{Term Deposits},t}^{USD}$$

$$S_t^{KHR} = r_{\text{Term Loans},t}^{KHR} - r_{\text{Term Deposits},t}^{KHR}$$

### 2.5 Key Data Characteristics (from Notebook 01)

| Statistic | USD Spread | KHR Spread |
|-----------|-----------|------------|
| Mean | 6.72% | 11.34% |
| Std. Dev. | 2.02% | 7.11% |
| Min | 2.88% | 4.24% |
| Max | 11.30% | 26.65% |
| Correlation | 0.84 (high but not perfect) |
| Observations | 156 | 156 |

**Key observations:**
- KHR spread compressed dramatically from ~24% (2013) to ~4–5% (2025) — major structural shift reflecting financial sector maturation and de-dollarization progress
- KHR volatility is 3.5x higher than USD — the riel segment carries substantially more risk instability
- No missing values, no negative spreads, no data gaps — pristine dataset
- 156 observations is excellent for the 3-parameter OU model
- 7 years of pre-COVID data (2013–2019) provides strong baseline for COVID sub-period analysis

---

## 3. Paper Structure (18–28 pages)

### Section 1: Introduction (2–3 pages)

**What to write:** Open with the significance of credit risk in banking, narrow to Cambodia's specific context. The key tension: Cambodia has a dual-currency banking system, and we don't know whether credit risk behaves the same way in both segments.

**Key arguments:**
- Cambodia's rapid credit growth (15–25% annually), banking assets over 180% of GDP
- One of the most dollarized economies in the world (~80% of lending in USD)
- NBC's gradual de-dollarization push (higher USD reserve requirements, riel promotion)
- Loan-level default data is scarce — interest rate spreads offer an indirect but powerful alternative
- First study to construct a dual-currency CRI for Cambodia using 13 years of NBC data
- COVID-19 serves as a natural stress event to validate the framework

**End with:** Three research questions clearly stated, followed by a brief roadmap of the paper.

### Section 2: Literature Review (8–10 pages)

**Already written** — see `literature_review_full.md` (5,900 words, 25 references).

Five subsections:
- 2.1 Credit Risk Measurement in Banking (PD/LGD/EAD framework, IFRS 9, data scarcity, portfolio segmentation)
- 2.2 Interest Rate Spreads as Credit Risk Indicators (Ho & Saunders 1981, Angbazo 1997, Maudos & Fernández de Guevara 2004, TED spread, limitations)
- 2.3 Mean-Reverting Stochastic Models (OU process, Vasicek 1977, CIR extension, parameter estimation)
- 2.4 Cambodia's Financial System and Dollarization (UNTAC origins, dual economy, financial stability, COVID-19 and NPLs, de-dollarization)
- 2.5 Research Gap (three specific gaps your study fills)

### Section 3: Methodology (5–6 pages)

This is the heart of the paper. You apply the same framework to each currency, then combine them.

**3.1 Data Selection Rationale** — Why New Amount, Term Loans, Term Deposits

**3.2 Spread Definition** — $S_t^c = r_{\text{loan},t}^c - r_{\text{deposit},t}^c$ for $c \in \{USD, KHR\}$

**3.3 The Ornstein-Uhlenbeck Model:**

$$dS_t^c = \kappa^c(\theta^c - S_t^c)\,dt + \sigma^c\,dW_t^c$$

| Parameter | Meaning | What to Compare |
|-----------|---------|-----------------|
| $\theta^c$ | Long-run equilibrium spread | Is "normal" spread higher for KHR or USD? |
| $\kappa^c$ | Speed of mean reversion | Which currency recovers faster from shocks? |
| $\sigma^c$ | Volatility | Which currency has more volatile spreads? |

**3.4 Parameter Estimation (MLE):**
- Exact transition density for discretely observed OU process
- Log-likelihood function (given in full in roadmap)
- Optimization via `scipy.optimize.minimize`
- AR(1) cross-check: $S_{t+1} = a + bS_t + \varepsilon$ with mapping to OU parameters

**3.5 Crisis Threshold:**
- Primary: 95th percentile of historical spreads (currency-specific)
- Sensitivity: 90th and 99th percentiles

**3.6 Crisis Probability:**

$$P(S_t^c > S_c^c) = 1 - \Phi\left(\frac{S_c^c - m^c(t)}{\sqrt{v^c(t)}}\right)$$

**3.7 Currency-Specific CRI:**

$$\text{CRI}^c = 0.5 \cdot \hat{\sigma}^c + 0.5 \cdot P(S_t^c > S_c^c)$$

**3.8 System-Wide Composite CRI:**

$$\text{CRI}_{\text{System}} = w_{USD} \cdot \text{CRI}^{USD} + w_{KHR} \cdot \text{CRI}^{KHR}$$

Three weighting schemes: loan-share (~0.80/0.20), equal (0.50/0.50), time-varying.

**3.9 Stress Testing:**

$$S_t^{c,\text{stress}} = S_t^c(1 + \delta), \quad \delta \in \{0.10, 0.30, 0.50\}$$

**3.10 COVID-19 Sub-Period Analysis:**

| Period | Dates | Label | Observations |
|--------|-------|-------|-------------|
| Pre-COVID | Jan 2013 – Dec 2019 | Baseline | 84 |
| COVID | Jan 2020 – Dec 2021 | Shock | 24 |
| Post-COVID | Jan 2022 – Dec 2025 | Recovery | 48 |

Estimate OU parameters and CRI separately for each sub-period, for each currency.

**3.11 Rolling Window Analysis:**
- 24-month rolling window to re-estimate parameters monthly
- Produces time series of $\hat{\kappa}_t$, $\hat{\theta}_t$, $\hat{\sigma}_t$ for each currency

**3.12 Robustness Checks:**

| Check | What You Vary | Purpose |
|-------|--------------|---------|
| Outstanding Amount rates | Data source | Confirm results hold with alternative rate measure |
| 90th / 99th percentile thresholds | Crisis threshold | Show CRI is not sensitive to threshold choice |
| Alternative CRI weights (α=0.3, β=0.7) | Component weights | Show CRI ranking is stable |
| Equal vs. loan-share system weights | System weights | Show system CRI is robust to weighting |

### Section 4: Data Description (2–3 pages)

- Full description of NBC dataset, products, frequencies
- Descriptive statistics table (mean, std, min, max, skewness, percentiles)
- Four key visualizations: dual time series (with COVID shading), histograms, correlation plot, raw rates plot
- Discussion of KHR spread compression trend and what it means

### Section 5: Results (5–6 pages)

Present in this order — building from components to big picture:
- 5.1 Estimated OU Parameters (USD vs. KHR comparison)
- 5.2 Crisis Probability Over Time (annotated with COVID, Fed hikes, NBC policies)
- 5.3 Currency-Specific CRIs
- 5.4 System-Wide Composite CRI
- 5.5 COVID-19 Case Study (sub-period parameter shifts)
- 5.6 Rolling Window Parameter Evolution
- 5.7 Stress Test Results
- 5.8 Robustness Check Summary

### Section 6: Discussion (2–3 pages)

- Dollarization and risk: Does USD segment stabilize or amplify?
- COVID-19 impact: Temporary or structural?
- Early warning value: Did CRI signal risk before it was obvious?
- Policy implications for NBC, de-dollarization, and banks
- Limitations (honest assessment)
- Future research directions

### Section 7: Conclusion (1 page)

---

## 4. Complete Model Summary

| Step | Formula | Each Currency? |
|------|---------|---------------|
| 1. Compute spread | $S_t^c = r_{\text{loan},t}^c - r_{\text{deposit},t}^c$ | Yes (USD + KHR) |
| 2. Fit OU model | $dS_t^c = \kappa^c(\theta^c - S_t^c)dt + \sigma^c dW_t^c$ | Yes |
| 3. MLE estimation | Maximize log-likelihood for $(\kappa^c, \theta^c, \sigma^c)$ | Yes |
| 4. AR(1) cross-check | Regress $S_{t+1}$ on $S_t$, back out OU parameters | Yes |
| 5. Crisis threshold | $S_c^c = P_{95}(S_t^c)$ | Yes |
| 6. Crisis probability | $P(S_t^c > S_c^c) = 1 - \Phi\left(\frac{S_c^c - m^c(t)}{\sqrt{v^c(t)}}\right)$ | Yes |
| 7. Currency CRI | $\text{CRI}^c = 0.5\hat{\sigma}^c + 0.5 P(S_t^c > S_c^c)$ | Yes |
| 8. System CRI | $\text{CRI}_{\text{Sys}} = w_{USD}\text{CRI}^{USD} + w_{KHR}\text{CRI}^{KHR}$ | Once |
| 9. Stress test | $S_t^{c,\text{stress}} = S_t^c(1+\delta)$, recompute CRIs | Yes |
| 10. Sub-period analysis | Re-estimate steps 2–7 for pre/during/post COVID | Yes |
| 11. Rolling window | Re-estimate steps 2–7 on 24-month rolling window | Yes |
| 12. Robustness | Repeat with Outstanding Amount rates + alternatives | Yes |

---

## 5. Python Project Structure

```
cambodia-credit-risk/
├── data/
│   ├── raw/
│   │   └── nbc_interest_rates.csv          # Your NBC data
│   └── processed/
│       ├── spreads_usd_new_amount.csv      # Primary USD spread
│       ├── spreads_khr_new_amount.csv      # Primary KHR spread
│       ├── spreads_usd_outstanding.csv     # Robustness USD spread
│       ├── spreads_khr_outstanding.csv     # Robustness KHR spread
│       └── all_rates_wide_new_amount.csv   # Reference: all rates
├── notebooks/
│   ├── 01_data_preparation.ipynb           # ✅ DONE
│   ├── 02_exploratory_analysis.ipynb       # Deeper stats, figures
│   ├── 03_parameter_estimation.ipynb       # MLE + AR(1) both currencies
│   ├── 04_cri_computation.ipynb            # Crisis prob + CRI
│   ├── 05_stress_testing.ipynb             # Stress scenarios
│   ├── 06_covid_analysis.ipynb             # Sub-period comparison
│   ├── 07_rolling_window.ipynb             # 24-month rolling evolution
│   └── 08_robustness.ipynb                 # Outstanding Amount + checks
├── figures/
│   ├── fig1_spread_timeseries.png
│   ├── fig2_spread_histograms.png
│   ├── fig3_raw_rates.png
│   ├── fig4_correlation.png
│   ├── fig5_ou_parameters.png
│   ├── fig6_crisis_probability.png
│   ├── fig7_cri_timeseries.png
│   ├── fig8_system_cri.png
│   ├── fig9_covid_comparison.png
│   ├── fig10_rolling_parameters.png
│   ├── fig11_stress_test.png
│   └── fig12_robustness.png
├── paper/
│   ├── paper.qmd                            # Final paper
│   ├── literature_review.md                 # ✅ DONE
│   └── references.bib                       # BibTeX references
└── README.md
```

### Notebook Details

| # | Notebook | What It Does | Key Output |
|---|----------|-------------|------------|
| 01 | Data Preparation ✅ | Load NBC CSV, filter Term Loans/Deposits New Amount, compute spreads, quality checks | 6 processed CSVs, comparison plots |
| 02 | Exploratory Analysis | Descriptive stats, distributions, normality tests, autocorrelation, structural break tests | Figures 1–4, Table 1 |
| 03 | Parameter Estimation | MLE for $(\kappa, \theta, \sigma)$ per currency, AR(1) OLS cross-check, confidence intervals, half-life | Table 2 (parameters) |
| 04 | CRI Computation | $m(t)$, $v(t)$, crisis probability, CRI for USD/KHR/System over time | Figures 6–8, Table 3 |
| 05 | Stress Testing | Apply δ = 0.1, 0.3, 0.5 shocks, recompute CRIs, comparison charts | Figure 11, Table 4 |
| 06 | COVID Analysis | Split into pre/during/post COVID, re-estimate per period, compare parameters | Figure 9, Table 5 |
| 07 | Rolling Window | 24-month rolling re-estimation, parameter evolution plots | Figure 10 |
| 08 | Robustness | Outstanding Amount rates, alternative thresholds/weights | Table 6 |

---

## 6. Timeline (7–9 Weeks)

| Week | Task | Deliverable |
|------|------|-------------|
| 1 | Learn Python basics (pandas, matplotlib, numpy). Install Anaconda. Run Notebook 01 with your data | Notebook 01 verified with actual output |
| 2 | Deeper exploratory analysis: distributions, normality, correlation, autocorrelation plots | Notebook 02 complete |
| 3 | Study OU model math (YouTube videos). Implement MLE + AR(1) cross-check | Notebook 03 complete |
| 4 | Compute crisis probability and CRI for both currencies + system-wide composite | Notebook 04 complete |
| 5 | Stress tests + COVID sub-period analysis + rolling window | Notebooks 05 + 06 + 07 complete |
| 6 | Robustness checks. Start writing: Introduction, review Literature Review draft | Notebook 08 complete. Draft Sections 1–2 |
| 7 | Write: Methodology, Data Description, Results | Draft Sections 3–5 |
| 8 | Write: Discussion, Conclusion. Polish all charts. Ensure consistency | Complete draft |
| 9 | Final review, formatting, prepare interview talking points | Finished paper |

---

## 7. Supplementary Data to Find

| Data | Where to Find | Purpose |
|------|--------------|---------|
| USD/KHR lending shares over time | NBC Annual Supervision Reports (Tables section) | System CRI weights ($w_{USD}$, $w_{KHR}$) |
| NPL ratios (2013–2025) | NBC Financial Stability Reports, IMF Article IV | Cross-validate CRI against actual defaults |
| GDP growth (quarterly/annual) | World Bank, NBC, AMRO | Annotate charts with economic context |
| USD/KHR exchange rate | NBC statistical tables | Context for KHR spread movements |
| Fed Funds Rate (2013–2025) | FRED (St. Louis Fed) | Annotate USD spread with Fed policy |

---

## 8. Interview Preparation

### The 60-Second Pitch

> "I built a dual-currency Credit Risk Index for Cambodia's banking sector. Cambodia is heavily dollarized — about 80% of lending is in US dollars — so I wanted to understand whether credit risk behaves differently in the dollar segment versus the riel segment. I used 13 years of monthly interest rate data from the National Bank of Cambodia, specifically weighted average rates on new term loans and term deposits. I chose new amount rates over outstanding amount rates because they respond faster to changes in risk perception, which is critical for an early warning tool. I modeled the lending-deposit spread for each currency using an Ornstein-Uhlenbeck stochastic process, estimated crisis probabilities, and constructed three indices: a USD-specific CRI, a KHR-specific CRI, and a loan-share-weighted system composite. I also ran stress tests, used COVID-19 as a natural case study with pre/during/post analysis, and tracked parameter evolution using rolling windows. The framework gives regulators and banks a practical monitoring tool that works without needing loan-level default data."

### Likely Follow-Up Questions

**"Why did you use interest rate spreads instead of default data?"**
> Cambodia doesn't have widely available loan-level default data. The spread approach captures how banks price risk in real time — when banks perceive higher credit risk, they widen spreads on new loans. It's well-established in the literature: Ho and Saunders (1981) showed that bank margins compensate for credit risk, and the TED spread is used by central banks worldwide as a systemic risk indicator.

**"Why new amount rates specifically?"**
> Outstanding amount rates average across all existing loans, including ones issued years ago. They're slow to react. New amount rates reflect what banks are charging right now — if risk perception changes today, it shows up in today's new loan rates. For an early warning tool, responsiveness is essential.

**"Why term loans and term deposits?"**
> Term loans are the most standard lending product — their pricing most directly reflects credit risk assessment. Overdrafts are priced for flexibility, credit cards bundle convenience premiums. Term deposits are the best maturity match, avoiding the liquidity-driven pricing of demand deposits.

**"What's the Ornstein-Uhlenbeck model and why did you choose it?"**
> It's a mean-reverting stochastic process — it captures the idea that spreads don't wander randomly, they tend to return to a normal level over time driven by competition and monetary policy. It has three intuitive parameters: the long-run average spread, the speed of reversion, and volatility. I chose it because interest rate spreads have this natural mean-reverting property, and it was first applied to finance by Vasicek in 1977. The model also has a closed-form solution, which means I can compute crisis probabilities analytically without needing Monte Carlo simulation.

**"What were your main findings?"**
> [Frame as a story about USD vs. KHR risk dynamics — depends on actual results. Example: "The KHR spread compressed dramatically from 24% to 4% over the sample, reflecting financial sector maturation. The USD segment is more stable day-to-day but both segments responded to COVID. The rolling window revealed..."]

**"What are the limitations?"**
> Three main ones. First, spreads capture operating costs and profit margins alongside credit risk, so I can't decompose exactly how much is pure credit risk. Second, I'm working with aggregate market rates — individual banks may behave differently. Third, the OU model assumes normally distributed shocks and constant parameters within each window, whereas reality may include jumps and regime changes.

---

## 9. Learning Resources

### Python (Start Here)
- **Kaggle's Python Course** (free, ~5 hours) — enough to get started
- **pandas**: Official "10 Minutes to pandas" tutorial
- **matplotlib**: Official pyplot tutorial
- **scipy.optimize.minimize**: For MLE — learn how this function works

### The Math
- **OU process**: YouTube "Ornstein-Uhlenbeck process explained" — watch 2–3 videos
- **MLE basics**: Khan Academy Maximum Likelihood Estimation video
- **Normal CDF**: You just need `scipy.stats.norm.cdf()` — understand what it returns

### Cambodia Context (Read Abstracts Only)
- Ho & Saunders (1981) — the theoretical foundation for your spread approach
- Vasicek (1977) — the model you're using
- Duma (2011) — IMF working paper on Cambodia's dollarization
- Menon (2008) — ADB study on Cambodia's persistent dollarization
- NBC Annual Supervision Reports
- IMF Cambodia Article IV Consultation Reports
