# Credit Risk and Dollarization in Cambodia

**A Dual-Currency Analysis Using Interest Rate Spreads (2013–2025)**

*Research Reda Lab – Business Club*  
**Members:** DUK Pagnarith, PHAL Menghak, Hoeurn Sreyka

## Project Overview

This research constructs currency-specific and system-wide **Credit Risk Indices (CRIs)** for Cambodia's dual-currency banking sector. Cambodia's economy is highly dollarized, with approximately 80% of bank lending denominated in US Dollars (USD) and the remaining 20% in Cambodian Riel (KHR). This structural feature uniquely exposes domestic credit conditions to US Federal Reserve policy decisions.

This project investigates:
1. Whether USD and KHR segments exhibit distinct credit risk dynamics.
2. If the COVID-19 pandemic triggered a structural decoupling between the two segments.
3. The extent to which US monetary policy shocks transmit to Cambodia's domestic credit market.

## Website

The complete methodology, detailed results, and interactive execution outputs are hosted on the companion Quarto website:
👉 **[View the Research Website](https://DUKPagnarith.github.io/research_reda/)**

## Methodology

This analysis follows a comprehensive 16-step methodological pipeline using National Bank of Cambodia (NBC) monthly interest rate data (Jan 2013 – Dec 2025). The approach includes:

- **Credit Risk Index Construction:** Using the spread between term loan and term deposit rates.
- **Stochastic Modeling:** Fitting an Ornstein-Uhlenbeck (OU) mean-reverting diffusion process using Maximum Likelihood Estimation (MLE).
- **Stress Testing:** Simulating severe shocks using 10%, 30%, and 50% spread shocks.
- **Structural Break Analysis:** Sub-period and rolling window analysis around the COVID-19 pandemic.
- **Advanced Extensions:** 2-State Markov Regime-Switching OU models, dynamic rolling thresholds, and implied default probability extractions using reduced-form pricing logic.
- **VAR Interdependence:** Vector Autoregression, Granger Causality, and Impulse Response Functions to test US policy transmission.

## Repository Contents

The repository contains 12 standalone Jupyter notebooks, run sequentially:

- `01_data_preparation.ipynb`: Sourcing, cleaning, and calculating raw credit spreads.
- `02_exploratory_analysis.ipynb`: Descriptive statistics, stationarity tests, and correlations.
- `03_parameter_estimation.ipynb`: MLE and AR(1) cross-check for the OU scale parameters.
- `04_cri_computation.ipynb`: Threshold mapping, crisis probabilities, and System CRI aggregation.
- `05_stress_testing.ipynb`: Simulating hypothetical adverse spread shocks.
- `06_covid_analysis.ipynb`: Analyzing the COVID shock as a structural break.
- `07_rolling_window.ipynb`: 36-month rolling estimation to track parameter evolution.
- `08_robustness.ipynb`: Checks using outstanding amount rates instead of new lending ratios.
- `09_regime_switching.ipynb`: Modeling unobserved "Calm" and "Stress" states.
- `10_dynamic_threshold.ipynb`: Replacing static definitions with rolling historical cutoffs.
- `11_implied_pd.ipynb`: Market-implied 1-year default probabilities and recovery rate sensitivity.
- `12_policy_divergence.ipynb`: Testing the "monetary decoupling" hypothesis using Vector Autoregression.

## Key Findings

1. **Structural Risk Asymmetry:** The KHR segment exhibits structurally higher and more volatile credit risk than the USD segment, reflecting the exchange rate risk premium.
2. **Permanent Regime Shift:** COVID-19 was not a transitory shock; it permanently shifted the equilibrium levels of risk in Cambodia's banking sector.
3. **Decoupling Confirmed:** Pre-COVID, the US Federal Reserve dictated borrowing costs across both currencies (p < 0.001). Post-COVID, the KHR segment successfully decoupled from US monetary policy (p = 0.159), while the USD segment remained highly anchored.
4. **Local Autonomy:** The National Bank of Cambodia's policy tools are gaining traction, increasingly influencing even the dollarized segment—a key indicator of advancing de-dollarization.

## License

This project is intended for research purposes as part of the Research Reda Lab – Business Club. All data rights belong to the National Bank of Cambodia (NBC) and the Federal Reserve Economic Data (FRED).
