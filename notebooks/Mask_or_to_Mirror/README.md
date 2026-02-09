# "To Mask or to Mirror: Human-AI Alignment in Collective Reasoning"  Research Paper
[Read](https://deepmind.google/research/publications/180362/)

LLMs are being deployed in group decision systems — hiring, project leadership, resource allocation. This project provides the statistical infrastructure to determine whether those systems replicate, suppress, or amplify human bias and under what conditions that behavior changes. It is the audit layer that should run before any such system ships.

The project originates from eight gaps explicitly listed in the limitations section of Qian et al. 2025. The paper studied whether LLMs replicate human gender bias in group leader elections but could not address passive-vs-active participation, cross-domain generalization, model scale, multilingual behavior, temporal dynamics, statistical structure of nested data, causal decomposition, or formal fairness criteria. Each gap maps to one or more extensions in this project.

The system simulates and analyzes thirteen extensions to a published study on LLM bias in group leader selection. It generates synthetic experimental data calibrated to the original paper's reported values, runs statistical, causal and fairness analyses on that data and produces comparison visualizations. It does not call any live LLM. It measures properties of the experimental design and the statistical claims in the original work.

## Technology Stack

**Languages:** Python 3

**Libraries:** NumPy, SciPy (stats, gaussian_kde, beta distribution), Matplotlib (pyplot, gridspec), Scikit-learn (PCA, cosine_similarity, silhouette_score), Seaborn

**Algorithms implemented (hand-rolled, no external package):** REML random-intercept estimation, Empirical Bayes shrinkage, Beta-Bernoulli posterior sampling, Highest Density Interval computation, Baron-Kenny OLS mediation with 10 000-iteration bootstrap, Cohen's kappa for categorical arrays, rule-based NLP feature extraction

**Environment:** Google Colab (Jupyter notebook format, .ipynb)

**Models referenced as subjects of analysis (not called live):** Gemini 3, GPT-4.1 Mini, Claude Haiku 3.5

**Data integrations:** None. All data is synthetic, generated within the notebooks. Simulated values are calibrated to the ranges reported in Qian et al. 2025 (alignment rates, OLG decomposition, self-nomination scores, male election rates, group counts).

**Datasets:** The source dataset is the set of baseline values extracted from Qian et al. 2025 (N=748 participants, 187 groups). All simulation inputs are derived from those values.

---

## Functionality

**(P1–P5):** Simulates five experimental extensions that each address a gap stated in the original paper's limitations section. 

-P1 simulates alignment and discourse dominance across three group compositions (all-human, mixed, all-LLM). 

-P2 simulates alignment and male election rate across three task domains with different stereotype directions. 

-P3 simulates alignment, OLG and self-nomination gap across three model size tiers. 

-P4 simulates alignment and OLG across four languages (English, French, German, Spanish). 

-P5 simulates alignment, OLG and male election rate across five repeated rounds. Each produces a 3-panel matplotlib figure and feeds into a master heatmap comparing all five projects against the baseline.

**(E1–E8):** Eight extensions that address statistical, mechanistic, causal, robustness and fairness gaps in the paper. 

-E1 fits a one-way random-intercept model to nested group data and computes ICC and design effect. 

-E2 extracts six linguistic features from simulated transcripts using rule-based pattern matching and computes Spearman correlations with self-nomination scores. 

-E3 computes Beta posteriors for alignment and OLG and derives pairwise posterior probabilities P(A > B). 

-E4 sweeps temperature from 0.1 to 1.8 across 30 values, computes alignment and OLG curves per model type, defines three prompt variants and identifies the joint stability region. 

-E5 generates 64-dimensional rationale embeddings, projects via PCA, computes per-group cosine similarity, runs silhouette scoring and classifies groups into outcome-aligned vs reasoning-aligned quadrants. 

-E6 runs Baron-Kenny mediation with OLS path coefficients and 10 000-iteration bootstrap confidence intervals on the indirect effect. 

-E7 computes three fairness metrics — demographic parity, equalized odds (TPR gap), counterfactual fairness gap — and flags violations against defined thresholds. 

-E8 simulates 10 independent runs per model, computes pairwise Cohen's kappa across all run pairs and measures the fraction of unanimous groups.

---

## Features with Usages

Baseline reference table: loads and displays alignment rate, OLG (total, self-exclusion, peer-exclusion) and male election rate from the paper.

Group composition simulation (P1): generates alignment, OLG and discourse dominance values for all-human, mixed and all-LLM group types.

Cross-domain simulation (P2): generates alignment and male election rate across technical, strategic and caregiving domains.

Model scale simulation (P3): generates alignment, OLG and self-nomination gap ratio across small, medium and large model tiers.

Cross-lingual simulation (P4): generates alignment, OLG and male election rate for English, French, German and Spanish.

Temporal drift simulation (P5): generates alignment, OLG and male election rate across five sequential rounds.

Master heatmap: places alignment rate and OLG for all five P-extensions and the baseline on a single color-mapped grid.

Random-intercept model (E1): estimates ICC, design effect, between-group and within-group variance and Empirical Bayes group effects.

Linguistic feature extraction (E2): computes assertion density, hedge ratio, question rate, agreement rate, disagreement rate and turn length from text. Computes Spearman correlation of each feature with self-nomination score.

Bayesian posterior analysis (E3): computes Beta posteriors for alignment and OLG. Derives HDI. Computes pairwise P(A > B) matrix.

Temperature sweep (E4): computes alignment and OLG as functions of temperature for mirror and mask model types. Identifies the joint stability region.

Prompt sensitivity (E4): computes alignment rate shift across three prompt variants.

Embedding space analysis (E5): generates rationale embeddings, projects via PCA, computes cosine similarity per group, scores cluster separation via silhouette, classifies groups into outcome/reasoning alignment quadrants.

Causal mediation (E6): computes total, direct and indirect effects with OLS. Runs 10 000-iteration bootstrap on all three paths. Reports proportion mediated.

Fairness audit (E7): computes demographic parity, TPR gap (equalized odds) and counterfactual fairness gap. Flags violations against defined thresholds.

Cross-run consistency (E8): simulates 10 runs per model. Computes pairwise Cohen's kappa. Measures unanimous group fraction and alignment variance across runs.

---

## Comprehensive Description

This project is a simulation and analysis framework built in two Google Colab notebooks. It extends the findings of Qian et al. 2025, which studied whether LLMs replicate human gender bias in group leader elections using the Lost at Sea task. The original paper identified eight methodological gaps. This project addresses those gaps through thirteen distinct extensions.

The first part contains five experimental extensions. Each simulates an experiment that the original paper could not run: active LLM discourse participation, cross-domain task variation, model scale variation, grammatically gendered languages and temporal drift across repeated rounds. All simulated values are calibrated to the baseline rates reported in the paper. Each extension produces a 3-panel comparison figure and feeds into a master heatmap that places all five extensions and the baseline on a single grid.

The second part contains eight extensions that address the statistical, mechanistic, causal, robustness and fairness layers of the analysis. These include a multilevel reanalysis that computes ICC and design effect for the nested group structure, a linguistic feature extraction pipeline that measures assertion density and hedge ratio in simulated transcripts, a Bayesian posterior analysis that replaces point estimates with full Beta distributions, a temperature and prompt sensitivity sweep, an embedding space analysis that separates outcome alignment from reasoning alignment, a causal mediation decomposition with bootstrap confidence intervals, a counterfactual fairness audit against three standard criteria and a cross-run consistency measurement using Cohen's kappa.

---

## Target Audience

Researchers studying LLM bias in group decision-making. AI fairness auditors evaluating deployed models. Teams building LLM-assisted decision tools who need pre-deployment bias characterization. The project operates as a self-contained analysis environment: open the notebook, run all cells sequentially, review figures and printed tables. No external data source or API key is required.


---

## Industrially Relevant

**Gender bias in group decision systems.** Organizations deploy LLMs in team-based decision tools (hiring committees, project leadership selection, resource allocation). This project measures whether LLMs replicate, suppress, or amplify the gender bias that humans exhibit in group leader selection — and under what conditions that behavior changes.

**AI fairness auditing.** E7 applies three standard fairness definitions (demographic parity, equalized odds, counterfactual fairness) to the election pipeline. Any organization deploying LLMs in decision roles needs this type of audit before deployment.

**Robustness of AI findings.** E4 and E8 address whether reported behavioral patterns in LLMs are stable across temperature, prompt wording and repeated runs. This is a prerequisite for treating any single-run LLM evaluation as a reliable finding.

**Causal attribution in AI systems.** E6 decomposes the causal pathway (identity cue → self-nomination → election outcome) into direct and indirect effects per model. This determines whether a model's bias operates through the same mechanism as human bias or through a different pathway.

**Multilingual AI deployment.** P4 tests whether grammatical gender structure in a language changes model behavior. This matters for any organization deploying LLMs in non-English contexts.
