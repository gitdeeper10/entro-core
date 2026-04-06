# 🔴 ENTRO-CORE — Regime-Dependent Entropy-Augmented Control

> *"Intelligence by Design, Stability by Physics"*

**ENTRO-CORE** is the third project of the **EntropyLab** research program (E-LAB-03). It investigates entropy-based control architectures for dynamical systems, introducing a hybrid regime-switching controller that combines PID with nonlinear entropy feedback.

**Project Code:** `E-LAB-03` | **Lab:** Entropy Research Lab | **Submitted:** April 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-darkred.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-pip_install_entro--core-red.svg)](https://pypi.org/project/entro-core/)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.19431029-blue.svg)](https://doi.org/10.5281/zenodo.19431029)
[![Builds on](https://img.shields.io/badge/Builds_on-ENTROPIA_E--LAB--01-darkred.svg)](https://doi.org/10.5281/zenodo.19416737)
[![Web](https://img.shields.io/badge/Web-entropia--lab.netlify.app-red.svg)](https://entropia-lab.netlify.app/entro-core)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Finding](#-key-finding)
- [Control Laws](#-control-laws)
- [Experimental Results](#-experimental-results)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Validation](#-validation)
- [EntropyLab Roadmap](#-entropylab-research-roadmap)
- [Documentation](#-documentation)
- [Citation](#-citation)
- [Author](#-author)
- [License](#-license)

---

## 🔭 Overview

Modern AI systems operate under high-dimensional feedback loops that can lead to instability, especially under long-context reasoning or recursive inference. ENTRO-CORE moves entropy control from an external monitoring layer (ENTRO-AI) into the **core control architecture itself**.

**Instead of:** Monitor → Detect → Intervene (reactive)  
**ENTRO-CORE does:** Self-regulate internally (proactive)

| Metric | Value |
|--------|-------|
| PID Final Ψ (stable regime) | **0.017** |
| ENTRO-CORE Final Ψ | -0.239 |
| Hybrid Final Ψ | -0.012 |
| Validation Runs | 5 runs per controller |
| Noise Robustness | σ = 0.00 → 0.15 |

---

## 🔬 Key Finding

> Entropy-based control is **regime-dependent**, not universally superior.  
> PID remains optimal in stable linear systems, while entropy-based control provides benefits in near-critical regimes.

| Regime | Optimal Controller |
|--------|-------------------|
| Stable linear | **PID** |
| Near-critical / nonlinear | ENTRO-CORE / Hybrid |

---

## 📐 Control Laws

### PID Controller
```

u_PID(t) = K_p·e(t) + K_i·∫e(τ)dτ + K_d·ė(t)

```
with e(t) = -Ψ(t), K_p=0.8, K_i=0.2, K_d=0.3

### Entropy-Based Controller (ENTRO-CORE v1)
```

u_ENTRO(t) = w₁·σ(Ψ_norm - θ) + w₂·tanh(Ψ̇) + w₃·tanh(Ψ̈)

```
with w₁=0.5, w₂=0.3, w₃=0.2, θ=1.4

### Hybrid Regime-Switching Controller
```

u(t) = { u_PID(t)      if Ψ(t) < Ψ_th
{ u_ENTRO(t)    if Ψ(t) ≥ Ψ_th

```
with switching threshold Ψ_th = 1.7

---

## 📊 Experimental Results

Under near-critical initial conditions (Ψ(0)=1.8, Ψ̇(0)=0.3):

| Controller | Final Ψ (t=20s) | Outcome |
|------------|-----------------|---------|
| Uncontrolled | 0.053 | Naturally stable |
| **PID** | **0.017** | **Optimal convergence** |
| ENTRO-CORE v1 | -0.239 | Mild overshoot |
| Hybrid (threshold=1.7) | -0.012 | Robust performance |

### Noise Sensitivity (Hybrid Controller)

| Noise σ | Final Ψ | Outcome |
|---------|---------|---------|
| 0.00 | 0.339 | Stabilized |
| 0.02 | 0.341 | Stabilized |
| 0.05 | 0.355 | Stabilized |
| 0.10 | 0.412 | Stabilized |
| 0.15 | 0.523 | Stabilized |

---

## 🗂️ Project Structure

```

entro-core/
│
├── 📄 README.md                            # This file
├── 📄 LICENSE                              # MIT License
├── 📄 CHANGELOG.md                         # Version history
├── 📄 CONTRIBUTING.md                      # Contribution guidelines
├── 📄 CITATION.cff                         # Academic citation metadata
├── 📄 pyproject.toml                       # Build configuration
├── 📄 requirements.txt                     # Runtime dependencies
├── 📄 requirements-dev.txt                 # Development dependencies
│
├── 📁 entro_core/                          # Core Python package
│   ├── 📄 init.py                      # Package entry point
│   ├── 📄 controller.py                    # ENTRO-CORE v1 (original)
│   ├── 📄 controller_v2.py                 # ENTRO-CORE v2 (negative feedback)
│   ├── 📄 hybrid_controller.py             # Regime-switching controller
│   ├── 📄 actuator.py                      # Actuation strategies
│   ├── 📄 normalize.py                     # Logistic normalization (Eq. 4)
│   ├── 📄 state.py                         # State tracker (Ψ, Ψ̇, Ψ̈)
│   └── 📄 control_law.py                   # Control law u(t) (Eq. 5)
│
├── 📁 simulation/                          # Validation simulations
│   ├── 📄 generate_figures_fixed.py        # Trajectory generation
│   ├── 📄 validation_experiment.py         # Full validation suite
│   ├── 📄 hybrid_test.py                   # Hybrid controller test
│   └── 📁 results/
│       └── 📄 trajectories_fixed.csv       # Comparison data
│
├── 📁 tests/                               # Unit tests
│   ├── 📄 test_controller.py               # Controller tests (21 tests)
│   └── 📄 init.py
│
├── 📁 paper/                               # Research paper assets
│   └── 📁 arxiv/
│       └── 📄 entro_core_paper_revised.tex # LaTeX manuscript
│
└── 📁 docs/                                # Documentation
├── 📄 index.md
├── 📄 control_theory.md
└── 📄 api_reference.md

```

---

## ⚙️ Installation

### Requirements

- Python 3.11+
- No external dependencies required (pure Python)

### Via PyPI

```bash
pip install entro-core
```

From Source

```bash
git clone https://github.com/gitdeeper10/entro-core.git
cd entro-core
pip install -e ".[dev]"
```

---

🚀 Quick Start

1. Import and Use Hybrid Controller

```python
from entro_core.hybrid_controller import HybridController

# Create controller with threshold
controller = HybridController(threshold=1.7)

# Simulate a near-critical state
result = controller.step(psi=1.8)

print(f"u(t) = {result.u:.3f}")
print(f"Mode: {result.mode}")  # 'PID' or 'ENTRO-CORE'
print(f"Active: {result.is_active}")
```

```
u(t) = 0.423
Mode: ENTRO-CORE
Active: True
```

2. Run Validation Experiment

```bash
python simulation/validation_experiment.py
```

3. Generate Comparison Trajectories

```bash
python simulation/generate_figures_fixed.py
```

---

📊 Validation Results

Test Suite (21 tests)

Category Passed
Normalization 4/4 ✅
Sigmoid 3/3 ✅
Tanh 3/3 ✅
Control Law 3/3 ✅
Actuation 4/4 ✅
Controller 4/4 ✅
Total 21/21

---

🗺️ EntropyLab Research Roadmap

```
E-LAB-01  ✅  ENTROPIA          — Thermodynamic unification
E-LAB-02  ✅  ENTRO-AI          — Entropy-resistant AI inference
E-LAB-03  ✅  ENTRO-CORE        — Regime-dependent control (this repository)
E-LAB-04  📅  ENTRO-ENGINE      — Generalized entropy control framework
E-LAB-05  📅  ENTRO-FIN         — Financial entropic dynamics
E-LAB-06  📅  ENTRO-SOCIAL      — Information cascades in networks
E-LAB-07  📅  ENTRO-QUANTUM     — Quantum entropy extension
E-LAB-08  📅  ENTRO-BIO         — Biological neural entropy systems
E-LAB-09  📅  ENTRO-CLIMATE     — Climate entropy modeling
E-LAB-10  📅  ENTRO-META        — Unified entropy control theory
```

✅ Complete | 🔄 In Progress | 📅 Planned

---

📚 Documentation

Resource Link
Full Documentation entropia-lab.netlify.app/entro-core/docs
Research Paper (PDF) entropia-lab.netlify.app/entro-core/paper
API Reference entropia-lab.netlify.app/entro-core/api
Parent Project (ENTRO-AI) entro-ai.netlify.app
Foundation (ENTROPIA) doi.org/10.5281/zenodo.19416737

---

🤝 Contributing

```bash
git clone https://github.com/gitdeeper10/entro-core.git
cd entro-core
pip install -e ".[dev]"
pytest tests/
```

Priority contribution areas:

· Smooth switching (sigmoidal interpolation)
· Additional system dynamics models
· Real-world validation datasets

---

📖 Citation

```bibtex
@software{baladi2026entrocore,
  author       = {Samir Baladi},
  title        = {ENTRO-CORE: Regime-Dependent Entropy-Augmented Control},
  year         = {2026},
  version      = {0.1.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.19431029},
  url          = {https://doi.org/10.5281/zenodo.19431029},
  note         = {E-LAB-03. Builds on E-LAB-01 and E-LAB-02}
}
```

Parent frameworks:

```bibtex
@article{baladi2026entropia,
  title        = {ENTROPIA: Statistical Dynamics of Information Dissipation},
  author       = {Samir Baladi},
  year         = {2026},
  doi          = {10.5281/zenodo.19416737},
  note         = {E-LAB-01}
}

@software{baladi2026entroai,
  author       = {Samir Baladi},
  title        = {ENTRO-AI: Entropy-Resistant Inference Architecture},
  year         = {2026},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.19284086},
  note         = {E-LAB-02}
}
```

---

👤 Author

Samir Baladi

· Role: Principal Investigator, Interdisciplinary AI Researcher
· Affiliation: Ronin Institute / Rite of Renaissance
· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· GitHub: github.com/gitdeeper10
· GitLab: gitlab.com/gitdeeper10

---

📜 License

MIT License — see LICENSE for details.

---

<div align="center">

ENTRO-CORE — Entropy Research Lab — E-LAB-03

Regime-Dependent Entropy-Augmented Control

https://img.shields.io/badge/PyPI-pip_install_entro--core-red.svg
https://img.shields.io/badge/DOI-10.5281/zenodo.19431029-blue.svg

entropia-lab.netlify.app · pip install entro-core

Builds on ENTROPIA (E-LAB-01) and ENTRO-AI (E-LAB-02)

</div>
