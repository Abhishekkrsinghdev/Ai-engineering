# Self-Consistency Improves Chain of Thought Reasoning in Language Models

**Authors:** Xuezhi Wang et al.  
**Published:** ICLR 2023

---

## 1. The Problem

Chain-of-Thought (CoT) prompting improves reasoning by asking a language model to generate intermediate reasoning before producing the final answer.

However, traditional CoT generally uses **greedy decoding**:

```text
Question
   ↓
Language Model
   ↓
One reasoning path
   ↓
Final answer
```

The problem is that the model commits to a single reasoning trajectory.

If that trajectory contains an early mistake, the model can continue reasoning from the incorrect assumption and eventually produce a wrong answer.

The paper asks:

> **Why trust one reasoning path when a problem may have multiple valid ways of being solved?**

---

# 2. Core Idea — Self-Consistency

The paper replaces greedy CoT decoding with a **sample-and-marginalize** strategy.

Instead of generating one reasoning path:

```text
Question
   ↓
Path
   ↓
Answer
```

generate multiple diverse reasoning paths:

```text
                    Question
                       ↓
                 Language Model
                       ↓
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Path 1       Path 2       Path 3
          ↓            ↓            ↓
        Ans A        Ans A        Ans B
          └────────────┼────────────┘
                       ↓
                  Aggregate
                       ↓
                  Final Answer
```

The final answer is selected based on **consistency across the sampled reasoning paths**.

The simplest implementation is majority voting.

---

# 3. The Central Hypothesis

The key intuition is:

> **A complex reasoning problem can have multiple different reasoning paths that arrive at the same correct answer.**

Therefore:

```text
Correct reasoning paths
        ↓
Different approaches
        ↓
Same final answer
        ↓
High consistency
```

Whereas incorrect reasoning processes are more likely to disagree:

```text
Incorrect paths
     ↓
Different mistakes
     ↓
Different final answers
     ↓
Lower consistency
```

So answer agreement becomes a useful signal of correctness.

The paper explicitly describes correct reasoning processes as tending to have greater agreement in their final answer than incorrect processes.

---

# 4. Three Steps of Self-Consistency

### Step 1 — Chain-of-Thought Prompting

Use few-shot CoT examples to encourage the model to reason before answering.

### Step 2 — Sample Diverse Reasoning Paths

Replace greedy decoding with stochastic sampling.

The paper evaluates temperature sampling, top-k sampling and nucleus sampling.

Each sampled output contains:

```text
Reasoning path (rᵢ)
        ↓
Final answer (aᵢ)
```

The reasoning path is treated as a latent variable that leads to the final answer.

### Step 3 — Aggregate Final Answers

Extract the final answer from every generated path and select the answer with the highest consistency.

For majority voting:

```text
a* = most frequently occurring answer
```

The reasoning paths themselves don't need to be compared directly.

---

# 5. Example

Suppose the model generates five solutions:

```text
Path 1 → $18
Path 2 → $18
Path 3 → $26
Path 4 → $18
Path 5 → $18
```

Aggregation:

```text
$18 → 4 votes
$26 → 1 vote

Final answer → $18
```

The important point is that the paths don't have to be identical.

For example:

```text
Path A:
16 - 3 = 13
13 - 4 = 9
9 × 2 = 18

Path B:
3 + 4 = 7
16 - 7 = 9
9 × 2 = 18
```

Different reasoning expressions can still converge to the same answer.

---

# 6. Why Sampling Instead of Beam Search?

Self-consistency depends heavily on **diversity**.

Beam search attempts to retain high-probability sequences, so the resulting paths can be very similar.

Sampling intentionally explores different possible continuations.

```text
Beam Search

Path 1 ──────────────┐
Path 2 ──────────────┤
Path 3 ──────────────┤ → Similar reasoning
Path 4 ──────────────┤
Path 5 ──────────────┘


Self-Consistency

Path 1 → Approach A
Path 2 → Approach B
Path 3 → Approach C
Path 4 → Approach D
Path 5 → Approach E
             ↓
        More diversity
```

The paper found that Self-Consistency using sampling outperformed versions using beam search because beam search produces less diverse reasoning paths.

**Key takeaway:**

> Self-consistency doesn't need the most probable paths; it needs **diverse plausible paths**.

---

# 7. Why Not Sample and Pick the Highest-Probability Answer?

Another alternative is **sample-and-rank**:

```text
Generate many sequences
       ↓
Rank them by probability
       ↓
Pick highest-probability sequence
```

Self-consistency instead does:

```text
Generate many sequences
       ↓
Extract final answers
       ↓
Count/aggregate answers
       ↓
Pick most consistent answer
```

The paper shows that Self-Consistency substantially outperforms sample-and-rank using the same number of samples.

Why?

Because the model's probability for a generated sequence is not necessarily a reliable indicator that its reasoning is correct.

---

# 8. Why Does It Work?

The model already contains a distribution over possible continuations.

Sampling allows us to explore that distribution:

```text
                    Question
                       ↓
              Model's distribution
                       ↓
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
   Reasoning A      Reasoning B     Reasoning C
       ↓               ↓               ↓
      18              18              26
```

Self-consistency effectively asks:

> **Across different plausible reasoning trajectories, which final answer remains stable?**

This converts additional inference compute into a form of **statistical evidence**.

Important:

**The paper does NOT establish that the same neurons or internal circuits are activated across consistent reasoning paths.**

The "reasoning path" in this paper refers to the generated sequence of reasoning tokens, not a physical neural pathway.

---

# 9. Number of Sampled Paths

The authors evaluate different numbers of paths:

```text
1 → 5 → 10 → 20 → 40
```

Accuracy generally improves as more diverse paths are sampled.

The effect is visible across arithmetic and commonsense benchmarks.

However, gains eventually saturate.

Therefore:

> **More paths improve the estimate, but the marginal benefit decreases.**

The authors suggest starting with around **5–10 paths** in practice rather than automatically using a very large number.

---

# 10. Major Experimental Results

Self-consistency improves CoT across multiple models and reasoning tasks.

Some reported absolute gains include:

| Benchmark | Gain |
|---|---:|
| GSM8K | **+17.9%** |
| SVAMP | **+11.0%** |
| AQuA | **+12.2%** |
| StrategyQA | **+6.4%** |
| ARC-Challenge | **+3.9%** |

The paper evaluates UL2-20B, LaMDA-137B, GPT-3 and PaLM-540B.

A particularly important example:

```text
PaLM-540B on GSM8K

CoT + Greedy          → 56.5%
CoT + Self-Consistency → 74.4%

Improvement            → +17.9 percentage points
```

This is achieved **without changing the model parameters**.

---

# 11. It Is an Inference-Time Technique

Self-consistency requires:

- No fine-tuning
- No additional training
- No additional verifier
- No additional model
- No human annotations

It operates on top of an existing language model as an inference/decoding strategy.

This makes it similar to a **self-ensemble**:

```text
                SAME MODEL
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
    Sample        Sample       Sample
       ↓            ↓            ↓
    Answer        Answer       Answer
       └────────────┼────────────┘
                    ↓
                Aggregate
```

Unlike a conventional model ensemble, we don't train multiple models.

---

# 12. Consistency as an Uncertainty Signal

A particularly interesting observation:

```text
40 sampled paths

Answer A → 36
Answer B → 3
Answer C → 1
```

High consistency → likely higher confidence.

Compared with:

```text
Answer A → 12
Answer B → 11
Answer C → 9
Answer D → 8
```

Low consistency → likely lower confidence.

The paper finds that consistency is highly correlated with accuracy and suggests using it as an uncertainty estimate.

Therefore:

```text
High consistency
       ↓
Higher confidence

Low consistency
       ↓
Potential uncertainty
```

This gives Self-Consistency a second benefit beyond improving accuracy.

---

# 13. Robustness

Self-consistency remains useful even with imperfect prompts.

Example from the paper:

```text
Correct CoT prompt              → 17.1%
Imperfect CoT prompt            → 14.9%
Imperfect prompt + SC (40 paths) → 23.4%
```

It also works with:

- imperfect CoT demonstrations
- equation-based reasoning
- zero-shot CoT

For PaLM-540B, the reported zero-shot CoT experiment improved from **43.0% to 69.2%** with Self-Consistency.

---

# 14. Important Limitation

Self-consistency is **not a correctness proof**.

Agreement can still be wrong.

For example:

```text
Systematic model misconception
            ↓
       Path 1 → WRONG
       Path 2 → WRONG
       Path 3 → WRONG
       ...
       Path 40 → WRONG
            ↓
      40/40 agreement
```

Therefore:

> **Consistency is evidence, not verification.**

The paper acknowledges that models can still produce incorrect or nonsensical reasoning paths and highlights grounding of rationales as an area for future work.

---

# 15. The Cost

The main downside is inference cost.

```text
Greedy CoT

1 reasoning path
       ↓
1 generation


Self-Consistency

N reasoning paths
       ↓
N generations
       ↓
higher compute + latency
```

The paper explicitly identifies additional computation as the main limitation.

The practical observation is that accuracy often saturates relatively quickly, making a small number of paths a reasonable trade-off.

---

# 16. The Most Important Conceptual Distinction

### Greedy CoT

> **Trust one reasoning trajectory.**

```text
Question
   ↓
One path
   ↓
Answer
```

### Self-Consistency

> **Explore multiple reasoning trajectories and trust the answer they converge on.**

```text
Question
   ↓
Many diverse paths
   ↓
Many answers
   ↓
Consistency / aggregation
   ↓
Final answer
```

---

# 17. Connection to Inference-Time Compute

The deeper idea behind the paper is:

> **Inference-time computation can be exchanged for reasoning reliability.**

Instead of changing the model:

```text
More training
     ↓
Better model
```

Self-consistency says:

```text
Same model
     +
More inference compute
     ↓
Explore more reasoning possibilities
     ↓
Aggregate
     ↓
Better answer
```

This is why Self-Consistency is fundamentally an **inference-time decoding strategy**, not a new model architecture.

---

# 18. Paper in 30 Seconds

If you had to explain the paper in an interview:

> Chain-of-thought prompting traditionally uses greedy decoding, so the model commits to a single reasoning path. Self-Consistency replaces this with stochastic sampling of multiple diverse reasoning paths and then aggregates their final answers, typically using majority voting. The intuition is that correct solutions can be reached through multiple different reasoning paths and therefore tend to produce consistent final answers, while incorrect paths are more likely to disagree. The method requires no training or additional model, but trades additional inference compute for improved reasoning accuracy. The paper demonstrates substantial gains across arithmetic, commonsense and symbolic reasoning tasks and also finds that answer consistency can serve as an uncertainty signal.

---

# 19. Final Mental Model

```text
             ┌─────────────────────┐
             │      QUESTION       │
             └──────────┬──────────┘
                        ↓
             ┌─────────────────────┐
             │    CoT Prompting    │
             └──────────┬──────────┘
                        ↓
             ┌─────────────────────┐
             │   Language Model    │
             └──────────┬──────────┘
                        ↓
                Stochastic Sampling
                        ↓
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
   Reasoning 1      Reasoning 2      Reasoning N
       ↓                ↓                ↓
    Answer A         Answer A         Answer B
       └────────────────┼────────────────┘
                        ↓
                 Aggregate Answers
                        ↓
                 Most Consistent
                        ↓
                  FINAL ANSWER
```

### The one-line takeaway

> **Don't ask the model to find the single best reasoning path; let it explore several plausible paths and use their agreement to identify the most reliable answer.**