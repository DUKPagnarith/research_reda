# Cambodia Credit Risk Index — Dual-Currency Analysis

## Project Structure

```
Research_Reda/
├── data/
│   ├── raw/                          # Original NBC data
│   │   └── combined_interest_rates_long.csv
│   └── processed/                    # Computed spreads & model outputs
│       ├── spreads_usd_new_amount.csv
│       ├── spreads_khr_new_amount.csv
│       ├── spreads_usd_outstanding.csv
│       ├── spreads_khr_outstanding.csv
│       ├── all_rates_wide_new_amount.csv
│       ├── ou_parameters_mle.csv
│       ├── cri_results.csv
│       └── rolling_ou_parameters.csv
├── notebooks/                        # Analysis notebooks (run in order)
│   ├── 01_data_preparation.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_parameter_estimation.ipynb
│   ├── 04_cri_computation.ipynb
│   ├── 05_stress_testing.ipynb
│   ├── 06_covid_analysis.ipynb
│   ├── 07_rolling_window.ipynb
│   └── 08_robustness.ipynb
├── figures/                          # Publication-quality figures (300 dpi)
├── paper/                            # Literature review, roadmaps, drafts
├── project_guide.md
├── tasks.md
└── README.md
```

## Quick Start

```bash
cd notebooks
jupyter notebook
```

Run notebooks in order: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08

## Data

- **Source**: National Bank of Cambodia (NBC) Statistical Reports
- **Period**: January 2013 – December 2025 (156 monthly observations)
- **Currencies**: USD and KHR (Cambodian Riel)
