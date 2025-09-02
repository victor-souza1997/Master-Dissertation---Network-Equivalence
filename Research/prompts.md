# Prompt

Prompt to ask neural network to resume a paper
```
“Explain the paper [title/authors/year] in very didactic detail. Please cover:

What problem does the paper try to solve (motivation)?

What is the core idea or contribution?

What methodology or encoding does it use (step by step, in simple words)?

What experiments or case studies were done, and what were the results?

What are the main strengths and limitations?

How does it compare to previous work (e.g., Reluplex, CROWN, MILP, ESBMC, etc.)?

How could these ideas inspire my own research in QNN/ANN verification?

Please use analogies and simple examples when possible (e.g., like a toy NN or fixed-point number).

If possible, draw or describe a diagram of the workflow.”
```


# Ask GTP to generate diagram

1. **Synthesis (fast):**

   * Use **MILP** (backward preimage) to compute the safe sets $\mathcal P^{2i}$ at each affine layer $2i$ such that $x_{2i}\in\mathcal P^{2i}\Rightarrow$ the remaining suffix of the net lands in the desired output set $O$.
   * Use **CROWN/α,β-CROWN** (forward LiRPA bounds) to get tight **over-approximations** of the activations under a candidate quantization $(Q_i,F_i)$.
   * Pick $(Q_i,F_i)$ to (try to) make the **reachable set** at layer $2i$ lie **inside** $\mathcal P^{2i}$.

2. **Audit (exact, but local and parallel):**

   * For each layer $2i$, run an **SMT/ESBMC** check that “the quantized output of layer $2i$ is **always** inside $\mathcal P^{2i}$” under the inputs allowed at that layer.
   * Do these **per-layer checks in parallel**. If all pass, the global property follows from the preimage construction.


### Variant B — **Prefix check (more exact)**

* Encode the **prefix network up to $2i$** (quantized) with the **original input set** $X$; assert $x_{2i}\in\mathcal P^{2i}$.
* Still parallel across $i$, but each job is heavier (it includes all earlier layers).

Pros: fewer false alarms; Cons: more SMT time per layer.

> In both variants, if all layers pass their checks, you’ve proved the global property because the preimages $\mathcal P^{2i}$ were defined against the *suffix* network.
>
> 
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


can you generate a diagram file with this instructions. It's for my master degree dissertation. I want it very well drawn and detailed. Flowchart format. Use graphviz dot format. The diagram should be in a file named diagram.dot```dot
digraph G {
    rankdir=LR;
    node [shape=box, style=filled, color=lightgrey];    
    subgraph cluster_synthesis {
        label="Synthesis (fast)";
        style=dashed;
        color=blue;
        
        milp [label="MILP: Compute Safe Sets P^{2i}"];
        crown [label="CROWN/α,β-CROWN: Over-approximate Activations"];
        pick [label="Pick (Q_i, F_i) to fit Reachable Set in P^{2i}"];
        
        milp -> crown -> pick;
    }

    subgraph cluster_audit {
        label="Audit (exact, but local and parallel)";
        style=dashed;
        color=red;
        smt [label="SMT/ESBMC Check: Quantized Output in P^{2i}"];
    }
    synthesis_to_audit [label="For each layer 2i", shape=ellipse, style=filled, color=lightblue];
    pick -> synthesis_to_audit -> smt;
    smt -> result [label="All Pass?"];
    result -> end [label="Yes: Global Property Proven", shape=ellipse, style=

filled, color=lightgreen];
    result -> counterexample [label="No: Get Counterexample", shape=ellipse, style=filled, color=lightcoral];
    counterexample -> refine [label="Refine (Q_i, F_i) or R^{2i-1}"];
    refine -> pick [label="Rerun Synthesis"];       
    end [label="End", shape=ellipse, style=filled, color=lightgrey];
}```

