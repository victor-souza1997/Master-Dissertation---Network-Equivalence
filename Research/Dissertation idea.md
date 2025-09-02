
# Main Idea to my dissertation
# Big picture

1. **Synthesis (fast):**

   * Use **MILP** (backward preimage) to compute the safe sets $\mathcal P^{2i}$ at each affine layer $2i$ such that $x_{2i}\in\mathcal P^{2i}\Rightarrow$ the remaining suffix of the net lands in the desired output set $O$.
   * Use **CROWN/α,β-CROWN** (forward LiRPA bounds) to get tight **over-approximations** of the activations under a candidate quantization $(Q_i,F_i)$.
   * Pick $(Q_i,F_i)$ to (try to) make the **reachable set** at layer $2i$ lie **inside** $\mathcal P^{2i}$.

2. **Audit (exact, but local and parallel):**

   * For each layer $2i$, run an **SMT/ESBMC** check that “the quantized output of layer $2i$ is **always** inside $\mathcal P^{2i}$” under the inputs allowed at that layer.
   * Do these **per-layer checks in parallel**. If all pass, the global property follows from the preimage construction.

# Two workable variants for the SMT layer checks

### Variant A — **Single-layer check (fastest, most parallel)**

What you encode in SMT/C:

* **Inputs to layer $2i$**: use the CROWN/LiRPA **input region** $R^{2i-1}$ (a box or linear envelope) as `assume(...)` constraints.
* **Layer $2i$ itself**: its **quantized** affine computation (fixed-point bit-vectors or C with saturating fxp helpers).
* **Assertion**: for every neuron $j$, `lower_j <= a_{2i}[j] <= upper_j`, i.e., membership in $\mathcal P^{2i}$.

Pros: embarrassingly **parallel** across layers; very **light** encodings.
Con: conservative—if $R^{2i-1}$ is too wide, you may need more bits than strictly necessary (but it remains **sound**).

### Variant B — **Prefix check (more exact)**

* Encode the **prefix network up to $2i$** (quantized) with the **original input set** $X$; assert $x_{2i}\in\mathcal P^{2i}$.
* Still parallel across $i$, but each job is heavier (it includes all earlier layers).

Pros: fewer false alarms; Cons: more SMT time per layer.

> In both variants, if all layers pass their checks, you’ve proved the global property because the preimages $\mathcal P^{2i}$ were defined against the *suffix* network.

# Minimal C/ESBMC pattern (Variant A)

Assume Qm.n format with scale $S=2^{-F_i}$ at layer $2i$. Convert real bounds in $\mathcal P^{2i}$ to integers once:
$\texttt{L\_int}[j]=\lceil L_j/S \rceil,\quad \texttt{U\_int}[j]=\lfloor U_j/S \rfloor$.

```c
// Inputs to layer 2i (post-activation from layer 2i-1), int representation
int16_t x[k]; // size = n_{2i-1} in fixed-point units (scaled by 2^{F_{i-1}} or same scale if you align)

// Assume: LiRPA/CROWN box for the inputs to this layer
for (int j = 0; j < k; ++j) {
  x[j] = nondet_int16_t();
  __ESBMC_assume(Xmin_int[j] <= x[j] && x[j] <= Xmax_int[j]);
}

// Quantized affine: y = sat_round( W * x + b ) at this layer’s scale
int16_t y[m]; // size = n_{2i}
for (int r = 0; r < m; ++r) {
  int32_t acc = 0;
  for (int c = 0; c < k; ++c) {
    // fxp_mul handles scaling & saturation (e.g., (w* x) >> F_aligned)
    acc = fxp_add_sat(acc, fxp_mul_sat(W_int[r][c], x[c], /*F align*/));
  }
  acc = fxp_add_sat(acc, b_int[r]);
  y[r] = fxp_rescale_sat(acc, /*to F_i*/);
  __ESBMC_assert(L_int[r] <= y[r] && y[r] <= U_int[r], "layer 2i in P^{2i}");
}
```

* `fxp_*` implement **bit-exact** rounding/saturation (no undefined overflow).
* For **INT8 with scale/zero-point** (ONNX style), compare against bounds after **de-biasing** with the zero-point.

# How the pieces fit (soundness intuition)

* **Backward (MILP)** gave $\mathcal P^{2i}\subseteq N_{[2i+1:2d]}^{-1}(O)$.
* **Your SMT layer check** proves: for all allowed inputs to layer $2i$, the **quantized** output of layer $2i$ lies in $\mathcal P^{2i}$.
* Therefore, the suffix produces outputs in $O$. If this holds for each certified layer along the path, the whole network satisfies the property.

# Parallelization plan

* Spawn one job per certified affine layer $2i$ (and optionally per channel/neuron for coarse parallelism).
* Keep jobs **stateless**: each receives $(R^{2i-1}, W_i, b_i, (Q_i,F_i), \mathcal P^{2i})$ and runs independently.
* Use a pool (e.g., 16–64 workers). Most layers will solve quickly; focus time on those that fail and need bit tweaks.

# Where to use counterexamples

* If a layer SMT job returns **SAT**, it gives an input violating $\mathcal P^{2i}$.

  * Use it to **raise $F_i$** minimally (or $Q_i$ if overflow) using the gain/margin heuristic.
  * Optionally refine the LiRPA box $R^{2i-1}$ locally (region-split) and rerun.
* Keep a **pool of CEs** and ensure the new $(Q,F)$ kills **all** of them (hitting-set style), avoiding regressions.

# Gotchas (practical)

* **Scale alignment:** if adjacent layers use different $F$, be careful rescaling in C so bounds compare apples to apples.
* **Rounding mode & ties:** fix one (nearest-even vs away-from-zero) and use it **everywhere** (training export, MILP noise bounds, SMT/C).
* **Saturation vs wrap:** always saturate in C; set bounds accordingly.
* **LiRPA boxes too loose:** expect false failures → either increase bits or tighten with α,β-CROWN on the quantized model (include quantization noise as bounded perturbation).

# Verdict

* **Yes**, you can **find optimal bit-widths with MILP + CROWN** and **verify per-layer preimage with SMT/ESBMC**, compiling each layer to C.
* It **makes sense**, is **sound** (given the preimage construction), and is **highly parallelizable**.
* Keep an **end-to-end SMT check** on a small subset (or final model) as an optional “belt-and-suspenders” audit for complete confidence.
