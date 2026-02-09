# Architecture & System Design Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            SOURCE LAYER                                 │
│  Paper Baseline Values (Qian et al. 2025)                               │
│  - Alignment rates: Gemini 0.466, GPT 0.354, Claude 0.222               │
│  - OLG: total, self-exclusion, peer-exclusion per model                 │
│  - Male election rates, self-nomination scores                          │
│  - N=88 identified groups, N=99 pseudonymous groups                     │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         NOTEBOOK LAYER                                  │
│  ┌──────────────────────────┐    ┌─────────────────────────────────┐    │
│  │ extension_research.ipynb │    │ advanced_extensions.ipynb       │    │
│  │ Projects P1-P5           │    │ Extensions E1-E8                │    │
│  └──────────────────────────┘    └─────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      SIMULATION ENGINE                                  │
│  - Generate nested group data (groups × members × gender)               │
│  - Random intercept variance components                                 │
│  - Logistic outcome models                                              │
│  - Bootstrap resampling (10,000 iterations)                             │
│  - Monte Carlo posterior sampling (50,000 samples)                      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      ANALYSIS MODULES (13 total)                        │
│                                                                         │
│  EXPERIMENTAL (P1-P5)              ADVANCED (E1-E8)                     │
│  ┌─────────────────────┐           ┌────────────────────────────┐       │
│  │ P1: Active Discourse│           │ E1: Multilevel REML        │       │
│  │ P2: Cross-Domain    │           │ E2: Linguistic NLP         │       │
│  │ P3: Model Scale     │           │ E3: Bayesian Posteriors    │       │
│  │ P4: Gendered Lang   │           │ E4: Prompt/Temp Sweep      │       │
│  │ P5: Temporal Drift  │           │ E5: Embedding PCA          │       │
│  └─────────────────────┘           │ E6: Causal Mediation       │       │
│                                    │ E7: Fairness Audit         │       │
│                                    │ E8: Cross-Run Kappa        │       │
│                                    └────────────────────────────┘       │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    VISUALIZATION ENGINE                                 │
│  - Matplotlib 3-panel figures (13 total)                                │
│  - Master heatmap (alignment + OLG matrices)                            │
│  - Color-coded comparison plots                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          OUTPUT                                         │
│  - 13 PNG figure files                                                  │
│  - Printed summary tables (ICC, DEFF, kappa, violations)                │
│  - Master comparison matrix (6×3 grid: projects vs models)              │
└─────────────────────────────────────────────────────────────────────────┘


DATA FLOW:
Input → Simulation → Analysis Fork → Visualization → Output
         (calibrated    ├─ P1-P5 path   (matplotlib)   (PNG + tables)
          to baseline)  └─ E1-E8 path


EXECUTION ORDER:
1. Load baseline dict
2. Fork: left path (P1-P5) | right path (E1-E8)
3. Each module: simulate → compute → plot
4. Merge paths → master comparison
5. Print summary table (13 rows: ID, technique, finding)
```
