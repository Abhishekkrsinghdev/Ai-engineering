# Fast Inference from Transformers via Speculative Decoding

**Authors:** Yaniv Leviathan, Matan Kalman, Yossi Matias  
**Venue:** ICML 2023  
**Paper:** https://proceedings.mlr.press/v202/leviathan23a.html  
**arXiv:** https://arxiv.org/abs/2211.17192

---

## 1. The Problem

Large language models are typically **autoregressive**.

To generate:

```text
x1 → x2 → x3 → x4
```

the model must generate `x1` before it can determine `x2`, then `x2` before `x3`, and so on.

Therefore, generating `K` tokens normally requires roughly `K` sequential target-model decoding steps.

The fundamental problem is:

- the target model is expensive;
- next-token generation is inherently serial;
- every new token requires another target-model decoding step;
- in important inference regimes, the workload can be **memory-bandwidth bound**, leaving some compute capacity underutilized.

The paper asks:

> **Can we use the available compute more effectively by verifying several future tokens together, without changing the target model's output distribution?**

---

# 2. The Core Idea: Speculative Decoding

Introduce a smaller and faster **draft model**.

Instead of asking the expensive target model for one token at a time:

```text
Target → x1
Target → x2
Target → x3
Target → x4
```

let the draft model speculate:

```text
Draft:
x1 → x2 → x3 → x4
```

Then give those speculative tokens to the target model.

The Transformer can evaluate the proposed positions **in parallel**.

So the expensive work changes conceptually from:

```text
4 serial target executions
```

toward:

```text
1 target execution
       ↓
verify x1 x2 x3 x4 together
```

The draft model therefore **does not replace the target model**.

It proposes.

The target remains the source of truth.

---

# 3. Why This Does Not Reduce Model Quality

A naive approach would be:

> "The small model is less capable, so just use its output."

That would trade latency for quality.

Speculative decoding does something different.

For every drafted token, the target model checks whether the token is compatible with its own probability distribution.

Conceptually:

```text
Draft:
x1  x2  x3  x4

Target:
✓   ✓   ✓   ✗
```

The accepted prefix is:

```text
x1 x2 x3
```

At the first mismatch, the algorithm corrects the generation using the target distribution.

The paper's speculative sampling procedure ensures that the resulting samples have the **same distribution as sampling directly from the target model**.

Therefore:

```text
Normal target decoding
        ↓
Target distribution

Speculative decoding
        ↓
Same target distribution
```

The objective is not "approximately the same answer."

It is:

> **Same target distribution, fewer serial target-model executions.**

---

# 4. Probability Intuition

Let:

- `q(x)` = probability assigned by the draft model
- `p(x)` = probability assigned by the target model

The draft proposes a token according to `q`.

The target then asks:

> **"How much probability did I, the target model, actually give this token?"**

If the proposed token is sufficiently supported by the target distribution, accept it.

If it is not, reject it and sample a correction from the target distribution.

The important intuition is:

> **The draft model is allowed to suggest; it is never allowed to change the target model's final probability distribution.**

This is the key reason speculative decoding can accelerate inference while preserving the target distribution.

---

# 5. What Is γ?

`γ` is simply:

> **The number of tokens the draft model speculates before the target model verifies them.**

For example:

### γ = 1

```text
Draft → x1
Target → verify
```

### γ = 4

```text
Draft → x1 → x2 → x3 → x4
Target → verify all four together
```

A natural question is:

> **Why not make γ extremely large?**

Because there is a trade-off.

### γ too small

```text
Less speculation
      ↓
Less parallelism
      ↓
Less potential speedup
```

### γ too large

```text
More speculation
      ↓
More positions to verify
      ↓
Higher chance that the draft diverges
      ↓
More potentially wasted verification work
```

So the useful quantity is not simply:

> "How many tokens did the draft model generate?"

It is:

> **"How many tokens did the target model accept per expensive target execution?"**

A stronger draft model generally allows a longer useful speculative sequence because it agrees with the target more often.

The paper uses a fixed `γ` in its experiments and notes that adapting `γ` during inference could potentially improve results.

---

# 6. The Rejection Walkthrough

Suppose:

```text
Draft:
A → B → C → D
```

The target verifies them together:

```text
A ✓
B ✓
C ✓
D ✗
```

Then:

1. `A`, `B`, and `C` are accepted.
2. The sequence does **not** have to restart from the beginning.
3. At the first rejection, the target distribution supplies the correction.
4. The next draft sequence starts from the newly accepted prefix.

So if the draft generated:

```text
A B C D
```

and `D` is rejected, we keep:

```text
A B C
```

and correct the next token using the target distribution.

This is why a rejection does not destroy all the useful work from the earlier accepted tokens.

---

# 7. Why Memory Bandwidth Matters

One of the important systems insights behind the paper is that large-model inference can be **memory-bandwidth bound**.

The target model's weights are already resident in accelerator memory in the relevant inference setting.

The issue is not:

```text
SSD → load entire model → every token
```

Instead, think:

```text
Accelerator memory
       ↓
memory subsystem
       ↓
compute units
```

The accelerator repeatedly needs to access model state and KV-cache information while decoding.

If the compute units are capable of more arithmetic than the memory system can feed them, the workload becomes memory-bandwidth bound.

In that regime, speculative decoding can trade some additional arithmetic for fewer **serial target-model executions** and better utilization of available compute.

---

# 8. Why Speculative Decoding Is Not Always Helpful

Speculative decoding is particularly attractive when:

```text
Memory bandwidth is limiting
        +
Compute capacity is available
```

But if the target model is already **compute-bound**:

```text
Compute units already saturated
        ↓
Speculative verification adds arithmetic
        ↓
Benefit can shrink or disappear
```

So speculative decoding is not universally beneficial.

Its value depends on the hardware utilization regime.

---

# 9. KV Cache and Speculative Decoding

KV caching and speculative decoding solve different problems.

### KV cache

Avoids recomputing attention information for tokens that have already been processed.

```text
Previous tokens
      ↓
Cached K/V
      ↓
Reuse during future decoding
```

### Speculative decoding

Reduces the number of **serial target-model decoding steps**.

```text
Draft several tokens
        ↓
Target verifies together
        ↓
Fewer serial target executions
```

Therefore they are complementary rather than competing ideas.

---

# 10. The Draft Model Trade-off

The draft model has to satisfy two competing requirements.

### Too weak

```text
Very cheap
   ↓
Poor predictions
   ↓
Low acceptance rate
   ↓
Little useful speculation
```

### Too large

```text
Better predictions
   ↓
Higher acceptance rate
   ↓
But expensive drafting
   ↓
Speedup is reduced
```

The useful region is:

```text
                Draft quality
                     ↑
                     │
             sweet spot
                     │
Draft cost ──────────┼─────────→
```

The ideal draft model is therefore:

> **Much cheaper than the target, but accurate enough to produce a high proportion of acceptable tokens.**

---

# 11. The Entire Algorithm

```text
                Current context
                       │
                       ▼
                Small draft model
                       │
                       ▼
             x1 → x2 → x3 → x4
                       │
                       ▼
              Large target model
            verifies positions together
                       │
                 ┌─────┴─────┐
                 ▼           ▼
              Accept       Reject
                 │           │
                 │      Target correction
                 │           │
                 └─────┬─────┘
                       ▼
                 Continue decoding
```

The crucial property is:

> **The draft model proposes; the target model decides.**

---

# 12. What the Paper Demonstrated

The paper evaluates speculative decoding with Transformer models including T5 configurations.

Its experiments demonstrate substantial decoding acceleration, with reported speedups reaching roughly **2×–3×** in the tested settings.

The experiments also show the importance of the draft model:

```text
Better draft
     ↓
Higher acceptance rate
     ↓
More useful tokens per target execution
     ↓
Greater potential speedup
```

The paper therefore establishes that speculative decoding can reduce inference latency **without modifying the target model or changing its output distribution**.

---

# 13. The Paper in One Mental Model

```text
AUTOREGRESSIVE DECODING

Target
  ↓
token
  ↓
Target
  ↓
token
  ↓
Target
  ↓
token

        SERIAL
          │
          ▼
     Latency problem
          │
          ▼
SPECULATIVE DECODING
          │
          ▼
Small model drafts γ tokens
          │
          ▼
Large model verifies them together
          │
     ┌────┴────┐
     ▼         ▼
  Accept     Reject
     │         │
     └────┬────┘
          ▼
   Continue decoding
          │
          ▼
Same target distribution
+ fewer serial executions
```

---

# 14. Final Takeaway

> **Speculative decoding does not make the large model smaller. It makes the large model do less serial work.**

The draft model supplies **cheap guesses**.

The target model supplies **correctness**.

Parallel verification converts some of the expensive serial dependency into parallel work.

The technique is especially attractive when:

- the target model is expensive;
- decoding is memory-bandwidth bound;
- spare compute capacity exists;
- a sufficiently capable but much cheaper draft model is available.

The central trade-off is:

```text
Draft cost
    ↕
Draft quality / acceptance rate
    ↕
Number of speculative tokens γ
    ↕
Target verification cost
```

**The goal is to maximize useful accepted tokens per expensive target-model execution.**

---

## Paper links

- ICML/PMLR: https://proceedings.mlr.press/v202/leviathan23a.html
- arXiv: https://arxiv.org/abs/2211.17192
