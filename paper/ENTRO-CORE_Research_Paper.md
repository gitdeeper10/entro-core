# ENTRO-CORE: A Closed-Loop Entropy-Based Control Architecture for Self-Regulated Intelligence Systems

**ENTROPY RESEARCH LAB --- E-LAB-03**

*Control Theory · Cybernetics · Adaptive Intelligence Systems*

---

## Author Information

**Samir Baladi**
- Interdisciplinary AI & Theoretical Physics Researcher
- Ronin Institute / Rite of Renaissance
- Email: gitdeeper@gmail.com
- ORCID: 0009-0003-8903-0029

---

## Project Information

| Field | Details |
|-------|---------|
| Project Code | E-LAB-03 v1.0.0 |
| Submitted To | arXiv / Zenodo |
| Manuscript Type | Original Research Article |
| Date | April 2026 |
| Builds on | ENTROPIA (E-LAB-01) + ENTRO-AI (E-LAB-02) |

---

## DOIs

| Project | DOI |
|---------|-----|
| ENTROPIA (E-LAB-01) | 10.5281/zenodo.19416737 |
| ENTRO-AI (E-LAB-02) | 10.5281/zenodo.19284086 |
| **ENTRO-CORE (E-LAB-03)** | **10.5281/zenodo.19431029** |

---

## Abstract

This paper introduces ENTRO-CORE, a closed-loop control architecture designed to regulate entropy dynamics in adaptive intelligence systems. The framework models system instability through a scalar entropy state Ψ(t) and its temporal derivatives. A nonlinear control law combining sigmoid and hyperbolic tangent functions is proposed to stabilize system behavior under feedback-driven conditions. Unlike traditional optimization-based approaches, ENTRO-CORE operates as a real-time regulatory mechanism rather than a predictive model. The proposed architecture is generalizable to AI systems exhibiting recursive feedback, context saturation, or distributional instability. ENTRO-CORE constitutes the third project of the EntropyLab research program (E-LAB-03), extending the thermodynamic framework established in ENTROPIA (E-LAB-01) and the inference monitoring system of ENTRO-AI (E-LAB-02) toward a fully internalized self-regulation mechanism.

**Index Terms:** Entropy control, cybernetics, nonlinear systems, adaptive AI, closed-loop feedback, stability analysis, information dynamics, self-regulated intelligence, control law, phase space.

---

## I. Introduction

Modern AI systems operate under high-dimensional feedback loops that can lead to instability, especially under long-context reasoning or recursive inference. These instabilities manifest as entropy accumulation in the system's internal state — a phenomenon formally characterized in ENTROPIA (E-LAB-01) through the Dissipation Coefficient Ψ and monitored externally in ENTRO-AI (E-LAB-02) via the Entropy-Driven Throttling (EDT) controller.

ENTRO-CORE advances this program by a conceptually significant step: rather than monitoring entropy from the outside and intervening after detection, ENTRO-CORE embeds the control mechanism within the system's core operational loop. The architecture is designed to self-regulate — not as an external patch, but as an intrinsic property of how the system processes information.

The distinction is analogous to the difference between a thermostat (reactive external control) and homeostasis (intrinsic biological self-regulation). ENTRO-CORE targets the latter: a system that maintains thermodynamic stability as a consequence of its own control law, without requiring external triggers or post-hoc interventions.

---

## II. System State Representation

The entropy state of the system is represented as a scalar time-varying quantity:

| Equation | Expression | Description |
|----------|------------|-------------|
| Eq. 1 | Ψ(t) ∈ ℝ | Entropy state variable |
| Eq. 2 | dΨ/dt | Entropy velocity (first derivative) |
| Eq. 3 | d²Ψ/dt² | Entropy acceleration (second derivative) |

The three-component state vector (Ψ, dΨ/dt, d²Ψ/dt²) constitutes a minimal but complete representation of the system's instantaneous thermodynamic condition. The state Ψ(t) encodes the cumulative information-theoretic dissipation; its first derivative captures the rate of departure from equilibrium; and its second derivative captures the momentum of that departure, enabling anticipatory control action before instability becomes irreversible.

### Normalization

For normalization purposes, the raw Ψ state is mapped to a bounded domain via a logistic function:

**Eq. 4:** `Ψ_norm = Ψ_c · (1 − 1 / (1 + Ψ_raw / ref))`

where Ψ_c = 2.0 is the critical entropy threshold inherited from the ENTROPIA framework (E-LAB-01, Eq. 9), and ref = 10.0 is the logistic reference scale. This normalization ensures that Ψ_norm ∈ [0, Ψ_c] for all finite raw inputs, providing a bounded domain for the control law.

---

## III. The ENTRO-CORE Control Law

The ENTRO-CORE control signal u(t) is defined as a weighted combination of three nonlinear functions acting on the three state components:

**Eq. 5:** `u(t) = w₁·σ(Ψ_norm − θ) + w₂·tanh(dΨ/dt) + w₃·tanh(d²Ψ/dt²)`

where σ(x) = 1/(1 + e⁻ˣ) is the sigmoid activation function, tanh(x) is the hyperbolic tangent, θ is the activation threshold, and the weights are:

| Weight | Value | Component | Interpretation |
|--------|-------|-----------|----------------|
| w₁ | 0.5 | Ψ_norm − θ | Global state awareness (perception) |
| w₂ | 0.3 | dΨ/dt | Reactive stabilization (reflex) |
| w₃ | 0.2 | d²Ψ/dt² | Anticipatory correction (intuition) |
| θ | 1.4 | Activation threshold | Onset of control response |

The naming of the three components — perception, reflex, and intuition — reflects their functional analogues in biological regulation: global state awareness activates the control system when the entropy state exceeds a critical level; reactive stabilization damps velocity-driven divergence; and anticipatory correction acts on the second derivative to counteract accelerating instability before it reaches critical levels.

---

## IV. Actuation Mapping

The scalar control output u(t) ∈ [0, 1] is translated into system-level actions through one of four actuation mapping strategies, selectable based on system characteristics and operational requirements:

| Strategy | Function | Behavior | Use Case |
|----------|----------|----------|----------|
| Linear | a(t) = u(t) | Proportional response | Direct, smooth control |
| Exponential | a(t) = 1 − exp(−5·u(t)) | Aggressive at high u | Rapid intervention under high load |
| Quadratic | a(t) = u(t)² | Gentle at low u, sharp at high u | Noise-tolerant, soft onset |
| Threshold | a(t) = 0 if u < 0.3, else u(t) | Dead-band below threshold | Filtering spurious activations |

The exponential strategy is recommended for AI inference systems where rapid load shedding is critical near the critical threshold Ψ_c = 2.0. The threshold strategy is recommended for systems with significant measurement noise in the Ψ estimation pipeline, where small spurious fluctuations should not trigger actuation.

---

## V. Closed-Loop Control Architecture

The complete ENTRO-CORE control loop is organized as a seven-stage pipeline operating at configurable resolution (default: 10 ms, inherited from the ENTRO-AI Ψ-Dashboard):

| Stage | Module | Function |
|-------|--------|----------|
| 1 | State Input | Receive raw system telemetry (utilization, token rate, memory pressure) |
| 2 | Ψ Estimation | Compute Ψ(t) from telemetry via ENTROPIA thermodynamic equations |
| 3 | Derivative Computation | Calculate dΨ/dt and d²Ψ/dt² via finite difference over rolling window |
| 4 | Normalization | Apply logistic normalization (Eq. 4) to produce Ψ_norm |
| 5 | Control Law | Evaluate u(t) = w₁·σ(Ψ_norm − θ) + w₂·tanh(dΨ/dt) + w₃·tanh(d²Ψ/dt²) |
| 6 | Actuation Mapping | Translate u(t) to system action a(t) via selected mapping strategy |
| 7 | Feedback | Apply a(t) to system; updated state feeds back to Stage 1 |

The key architectural distinction from ENTRO-AI is the placement of the control law: in ENTRO-AI, the EDT controller acts on the inference engine's resource scheduler from outside the model's computational graph. In ENTRO-CORE, the control signal is designed to be embedded within the system's operational core — conceptually equivalent to integrating the thermodynamic regulator into the processing unit itself rather than attaching it as a peripheral monitor.

---

## VI. Dynamical Behavior and Stability

### VI.A Boundedness

The nonlinear saturation functions σ and tanh ensure that u(t) ∈ (0, 1) for all finite state inputs, providing hard bounds on the control output. Combined with bounded actuation mappings, this prevents runaway feedback amplification under any finite perturbation.

### VI.B Equilibrium and Convergence

The system is designed to maintain bounded entropy dynamics:

**Eq. 6:** `Ψ(t) ≤ Ψ_max for all t ≥ 0`

and to converge toward a stable equilibrium:

**Eq. 7:** `lim_{t→∞} Ψ(t) = Ψ*`

where Ψ* is the system-specific steady-state entropy level, which depends on the operating load ρ/ρ_c. Under subcritical load (ρ < ρ_c), simulation results show convergence to Ψ* < 1.5 within 200–400 control steps for all tested actuation strategies.

### VI.C Stability Discussion (Qualitative)

A formal Lyapunov stability proof for the full nonlinear closed-loop system is outside the scope of this paper and is identified as primary future work. However, three structural properties of the control law provide qualitative stabilizing characteristics:

1. **Derivative feedback terms (w₂ and w₃)** implement a form of damping: positive entropy velocity and acceleration increase the control signal, which acts to reduce the system's load and therefore reduce both dΨ/dt and d²Ψ/dt² in subsequent timesteps. This is qualitatively equivalent to derivative control in classical PID theory.

2. **Sigmoid activation on the state term (w₁)** ensures that the control system is inactive when Ψ_norm << θ (normal operating conditions) and maximally active as Ψ_norm → Ψ_c, providing graduated rather than bang-bang control.

3. **Multi-timescale structure** — acting simultaneously on state, velocity, and acceleration — enables the controller to respond at three different prediction horizons, reducing the risk that rapid entropy acceleration overwhelms the control capacity before the system can respond.

---

## VII. Simulation Methodology

To characterize the dynamical behavior of ENTRO-CORE under controlled conditions, a synthetic entropy system was implemented as a damped oscillatory process governed by:

**Eq. 8:** `d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u(t) + ξ(t)`

where γ = 0.3 is a damping coefficient, k = 0.5 is a restoring force coefficient, u(t) is the ENTRO-CORE control signal defined by Eq. 5, and ξ(t) ~ N(0, 0.01) is a Gaussian noise term simulating measurement uncertainty in the Ψ estimation pipeline.

Simulations were initialized with Ψ(0) = 1.0 and dΨ/dt(0) = 0.2, representing a system starting above its equilibrium with positive entropy velocity — a scenario analogous to an LLM inference pipeline beginning to experience context pressure. The control loop was evaluated over T = 1,000 timesteps (Δt = 0.1 s) with all four actuation strategies applied independently.

---

## VIII. Simulation Results

| Actuation Strategy | Convergence Steps | Final Ψ* | Max |u(t)| | Overshoot |
|--------------------|-------------------|----------|-------------|-----------|
| Linear | ~320 | 0.41 | 0.73 | Minimal |
| Exponential | ~210 | 0.38 | 0.91 | None |
| Quadratic | ~380 | 0.44 | 0.61 | None |
| Threshold | ~290 | 0.42 | 0.68 | Minimal |

The exponential actuation strategy achieves the fastest convergence (210 steps) due to its aggressive response at high u values, at the cost of a higher peak control magnitude. The quadratic strategy provides the smoothest trajectory with no overshoot, at the cost of slower convergence. All four strategies successfully maintain Ψ(t) < Ψ_c = 2.0 throughout the simulation under the tested initial conditions.

---

## IX. Limitations

ENTRO-CORE is presented as a conceptual framework and simulation-validated architecture. Several limitations constrain the strength of claims made in this paper:

1. **Domain-Dependence of Ψ:** The entropy state Ψ(t) is defined abstractly. Operational deployment requires domain-specific instantiation of Ψ from measurable telemetry.

2. **Absence of Formal Stability Proof:** The stability discussion is qualitative. A rigorous Lyapunov function has not been derived.

3. **Synthetic Simulation Only:** Validation is based entirely on a synthetic damped oscillator model. Empirical validation on real AI inference systems is required.

4. **Weight Calibration:** The weights w₁, w₂, w₃ and threshold θ are set manually. An adaptive calibration mechanism would strengthen generalizability.

---

## X. Conclusions and Future Directions

### X.A Summary of Contributions

| Contribution | Description |
|--------------|-------------|
| Closed-loop architecture | Seven-stage feedback control pipeline for entropy regulation |
| Nonlinear control law | Hybrid sigmoid-tanh control signal combining state, velocity, and acceleration feedback (Eq. 5) |
| Actuation strategies | Four mapping strategies (Linear, Exponential, Quadratic, Threshold) with characterized trade-offs |
| Phase space validation | Simulation demonstrates spiral attractor convergence under all four strategies |
| EntropyLab integration | Extends ENTROPIA (E-LAB-01) and ENTRO-AI (E-LAB-02) toward intrinsic self-regulation (E-LAB-03) |

### X.B Future Directions

1. **Formal Lyapunov proof:** Deriving a candidate Lyapunov function for the closed-loop system to establish conditions for global asymptotic stability.

2. **Empirical validation:** Integrating ENTRO-CORE into a live LLM inference pipeline and running comparative stress tests against the ENTRO-AI EDT baseline.

3. **Adaptive weight learning:** Replacing fixed weights with a meta-learning loop that adapts calibration parameters from operational entropy trajectories.

4. **ENTRO-ENGINE (E-LAB-04):** Extension to multi-domain control, where independent ENTRO-CORE instances coordinate across heterogeneous subsystems.

---

## Acknowledgments

This research was conducted independently through the Ronin Institute / Rite of Renaissance framework for scholar-driven science, as the third project (E-LAB-03) of the EntropyLab research program. No external funding was received.

---

## References

[1] C. E. Shannon, "A Mathematical Theory of Communication," Bell System Technical Journal, vol. 27, no. 3, pp. 379–423, 1948.

[2] N. Wiener, Cybernetics: Or Control and Communication in the Animal and the Machine. MIT Press, 1948.

[3] R. E. Kalman, "A New Approach to Linear Filtering and Prediction Problems," Journal of Basic Engineering, vol. 82, no. 1, pp. 35–45, 1960.

[4] S. Baladi, "ENTROPIA: Statistical Dynamics of Information Dissipation in Complex Non-Linear Digital Systems," EntropyLab E-LAB-01, Zenodo, 2026. DOI: 10.5281/zenodo.19416737

[5] S. Baladi, "ENTRO-AI: Entropy-Resistant Inference Architecture for Large Language Models & Neural Computing Systems," EntropyLab E-LAB-02, Zenodo, 2026. DOI: 10.5281/zenodo.19284086

[6] G. Nicolis and I. Prigogine, Self-Organization in Non-Equilibrium Systems. Wiley, 1977.

[7] T. M. Cover and J. A. Thomas, Elements of Information Theory, 2nd ed. Wiley-Interscience, 2006.

[8] R. Landauer, "Irreversibility and Heat Generation in the Computing Process," IBM Journal of Research and Development, vol. 5, no. 3, pp. 183–191, 1961.

---

## Appendix A — ENTRO-CORE Equation Reference

| Eq. | Expression | Description |
|-----|------------|-------------|
| 1 | Ψ(t) ∈ ℝ | Entropy state variable |
| 2 | dΨ/dt | Entropy velocity |
| 3 | d²Ψ/dt² | Entropy acceleration |
| 4 | Ψ_norm = Ψ_c·(1 − 1/(1 + Ψ/ref)) | Logistic normalization (Ψ_c=2.0, ref=10.0) |
| 5 | u(t) = w₁·σ(Ψ_norm−θ) + w₂·tanh(dΨ/dt) + w₃·tanh(d²Ψ/dt²) | ENTRO-CORE control law |
| 6 | Ψ(t) ≤ Ψ_max ∀t | Boundedness condition |
| 7 | lim Ψ(t) = Ψ* as t→∞ | Convergence to equilibrium |
| 8 | d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u(t) + ξ(t) | Simulation model (γ=0.3, k=0.5) |

---

## Appendix B — Digital Infrastructure & Data Availability

All ENTRO-CORE code, simulation notebooks, and phase space datasets are open-access:

| Resource | URL / Identifier |
|----------|------------------|
| GitHub | https://github.com/gitdeeper10/entro-core |
| GitLab (Primary) | https://gitlab.com/gitdeeper10/entro-core |
| PyPI | pip install entro-core · https://pypi.org/project/entro-core |
| Zenodo DOI | https://doi.org/10.5281/zenodo.19431029 |
| Parent (ENTRO-AI) | https://entro-ai.netlify.app · DOI: 10.5281/zenodo.19284086 |
| Foundation (ENTROPIA) | https://entropia-lab.netlify.app · DOI: 10.5281/zenodo.19416737 |

---

*"Intelligence that understands its own thermodynamic limits is not weaker. It is, for the first time, physically honest. ENTRO-CORE is the mechanism through which that honesty becomes intrinsic."*

**— Samir Baladi, April 2026**

---

*Part of the EntropyLab nine-project research program*

**ENTRO-CORE 🔴 | E-LAB-03 | April 5, 2026**
