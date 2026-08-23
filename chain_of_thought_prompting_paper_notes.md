# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

**Jason Wei et al. — Google Research — NeurIPS 2022**  
Paper: *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*

---

## 1. Core Idea

### Problem

Large language models can perform well with few-shot prompting, but **standard prompting often struggles with multi-step reasoning**, especially arithmetic, commonsense, and symbolic reasoning tasks.

Standard few-shot prompting gives demonstrations of:

```text
Question → Answer
```

The paper proposes **Chain-of-Thought (CoT) prompting**, where demonstrations instead contain:

```text
Question → Intermediate reasoning steps → Answer
```

A chain of thought is a series of intermediate natural-language reasoning steps that lead to the final output.

### Example

**Standard prompting**

```text
Q: Roger has 5 tennis balls. He buys 2 cans.
   Each can has 3 tennis balls. How many now?

A: 11
```

**Chain-of-thought prompting**

```text
Q: Roger has 5 tennis balls. He buys 2 cans.
   Each can has 3 tennis balls. How many now?

A: Roger started with 5 balls.
   2 cans × 3 balls = 6 balls.
   5 + 6 = 11.
   The answer is 11.
```

The model is therefore encouraged to generate a **sequence of intermediate steps** instead of making one direct jump from question to answer.

---

## 2. Why CoT Helps

The key intuition is that LLMs are **autoregressive**: generated tokens become part of the context used to predict subsequent tokens.

### Direct answer

```text
Problem
   ↓
Final answer
```

The model must perform a large reasoning transformation in one prediction process.

### Chain of thought

```text
Problem
   ↓
Reasoning step 1
   ↓
Reasoning step 2
   ↓
Reasoning step 3
   ↓
Final answer
```

Each intermediate step becomes part of the context for subsequent generation.

This allows a complex problem to be **decomposed into smaller sequential transformations**.

For a word problem:

```text
Natural-language problem
        ↓
Understand relationships
        ↓
Intermediate operation
        ↓
Intermediate result
        ↓
Next operation
        ↓
Final answer
```

The important idea is not simply that the model generates **more tokens**. The intermediate tokens need to represent useful reasoning steps.

---

## 3. Why Model Scale Matters

One of the paper's most important findings is that CoT is strongly dependent on **model scale**.

For smaller models, CoT often provides little benefit and can produce fluent but illogical reasoning chains.

At sufficiently large scales (roughly around 100B+ parameters in the experiments), CoT produces substantial improvements.

```text
Model scale ↑
     ↓
Stronger ability to execute reasoning patterns
     ↓
CoT becomes increasingly effective
     ↓
Performance rises sharply on difficult reasoning tasks
```

The authors describe this as an **emergent ability of model scale**.

### Error analysis

For LaMDA 137B:

- Nearly all examined correct answers had logically/mathematically correct chains of thought, apart from two cases that reached the answer coincidentally.
- Among incorrect answers, **46%** of chains were almost correct with relatively minor errors.
- The remaining **54%** contained major semantic-understanding or coherence errors.

Comparing PaLM 62B with PaLM 540B showed that scaling fixed a substantial portion of missing-step and semantic-understanding errors.

### Important qualification

The paper does **not** establish that the neural network is literally "reasoning" in the human sense. It demonstrates that CoT prompting elicits substantially better reasoning-like behavior on the evaluated tasks.

---

## 4. Experimental Setup

The authors compare:

### Standard prompting

Few-shot examples contain:

```text
Input → Output
```

### Chain-of-thought prompting

Few-shot examples contain:

```text
Input → Chain of thought → Output
```

For most arithmetic experiments, the authors manually created **eight CoT exemplars** and used the same set across benchmarks.

Models evaluated included:

- GPT-3
- LaMDA
- PaLM
- UL2
- Codex

The experiments use greedy decoding.

---

# 5. Arithmetic Reasoning

Benchmarks:

- GSM8K
- SVAMP
- ASDiv
- AQuA
- MAWPS

### Main result

CoT substantially improves arithmetic reasoning, especially on difficult multi-step problems.

The strongest result is **PaLM 540B on GSM8K**, where CoT achieved state-of-the-art performance and substantially outperformed standard prompting.

### Important observation

The harder the problem, the larger the benefit.

For example:

```text
Easy / one-step problem
        ↓
Small or negligible CoT gain

Complex multi-step problem
        ↓
Large CoT gain
```

This supports the idea that CoT is particularly useful when the task requires several reasoning steps.

---

# 6. Ablation Studies — Why Does CoT Work?

The paper tests alternative explanations for the improvement.

## A. Equation-only prompting

Instead of natural-language reasoning:

```text
Problem → Equation → Answer
```

For complex GSM8K problems, this does **not** help much.

Why?

The difficult part is often not merely performing arithmetic. The model must first interpret the natural-language semantics and determine which operations represent the relationships in the problem.

For simpler one- or two-step problems, equation-only prompting can improve performance.

**Takeaway:** directly translating a complex natural-language problem into an equation is itself difficult.

---

## B. Variable-compute-only

The authors test whether CoT works simply because it gives the model more intermediate tokens / computation.

The model is prompted to produce a sequence of meaningless dots corresponding to the required amount of computation.

Result:

```text
Variable compute only ≈ Standard prompting
```

**Takeaway:**

> More tokens alone are not sufficient.

The intermediate tokens need to contain meaningful reasoning information.

---

## C. Reasoning after the answer

Another possibility is that CoT simply helps the model access knowledge from pretraining.

So the authors put the reasoning **after** the answer:

```text
Question → Answer → Reasoning
```

This performs roughly like the baseline.

The normal CoT ordering:

```text
Question → Reasoning → Answer
```

performs much better.

**Takeaway:**

The sequential reasoning steps appear to be useful for producing the final answer, rather than merely serving as an explanation appended afterward.

---

# 7. Commonsense Reasoning

The paper tests whether CoT is a math-specific trick.

Benchmarks include:

- CommonsenseQA (CSQA)
- StrategyQA
- Date Understanding
- Sports Understanding
- SayCan

CoT improves performance across a range of commonsense reasoning tasks, with particularly strong results at larger model scales.

For example, PaLM 540B with CoT:

- outperformed the prior state of the art on StrategyQA
- substantially outperformed an unaided sports enthusiast on Sports Understanding

The gain on CSQA was comparatively small.

**Takeaway:** the language-based nature of CoT makes it applicable beyond mathematical calculation.

---

# 8. Symbolic Reasoning & Length Generalization

The paper studies two toy symbolic tasks:

### Last-letter concatenation

Example:

```text
Amy Brown → yn
```

The model must take the last letter of each word and concatenate them.

### Coin flip

Example:

```text
Coin starts heads.
Person A flips it.
Person B does not.
→ tails
```

The authors test both:

- **In-domain:** same reasoning length as demonstrations
- **Out-of-domain:** longer reasoning sequences than demonstrations

### Key result

With sufficiently large models, CoT enables much stronger performance on longer sequences.

```text
Few-shot examples
      ↓
Learn reasoning procedure
      ↓
Apply procedure
      ↓
Longer unseen sequence
```

Standard prompting fails much more severely on these OOD tasks.

**Takeaway:** CoT can facilitate **length generalization** of reasoning procedures.

---

# 9. Robustness

Because few-shot prompting can be sensitive to the demonstrations, the authors test:

- different annotators
- different reasoning styles
- different exemplar sets
- different exemplar orders
- different numbers of exemplars

Performance varies, as expected for few-shot prompting, but the different CoT prompts consistently outperform standard prompting.

Therefore, the improvement is **not dependent on one particular linguistic style or one magical set of examples**.

---

# 10. Overall Paper Argument

The paper's argument can be summarized as:

```text
Standard few-shot prompting
          ↓
Often struggles with multi-step reasoning
          ↓
Add reasoning traces to demonstrations
          ↓
Chain-of-thought prompting
          ↓
Model generates intermediate reasoning steps
          ↓
Intermediate tokens become future context
          ↓
Complex problems can be decomposed
          ↓
Large models can execute these reasoning patterns
          ↓
Improved arithmetic + commonsense + symbolic reasoning
          ↓
Can generalize to longer reasoning sequences
```

### The central contribution

> **Chain-of-thought prompting demonstrates that sufficiently large language models can be prompted to perform substantially better on complex reasoning tasks by providing few-shot examples containing intermediate reasoning steps rather than only final answers.**

---

# 11. Limitations

The authors identify several limitations:

1. **CoT does not prove genuine human-like reasoning.** Whether the neural network is actually "reasoning" remains an open question.

2. **Reasoning chains can be incorrect.** A generated chain is not guaranteed to faithfully represent a correct reasoning process.

3. **Annotation cost can become significant.** Manually creating reasoning traces is inexpensive for a few-shot prompt but can become expensive for large-scale fine-tuning datasets.

4. **Large models are required for strong CoT behavior.** This increases inference cost and makes real-world serving more expensive.

5. **Further scaling and prompting methods remain open questions.** The paper suggests that CoT may expand the set of tasks that large language models can successfully perform.

---

# 12. Paper in One Mental Model

```text
                 CHAIN-OF-THOUGHT PROMPTING

                    Few-shot examples
                           │
                           ▼
              Question + reasoning + answer
                           │
                           ▼
                 Model learns the pattern
                           │
                           ▼
                  New complex problem
                           │
                           ▼
                 Step-by-step generation
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
     Intermediate tokens          Intermediate state
       become context             guides next token
             │                           │
             └─────────────┬─────────────┘
                           ▼
                  Sequential reasoning
                           │
                           ▼
                       Answer

             Works especially well at
                  sufficient scale
```

### One-line takeaway

**CoT turns a difficult direct prediction problem into a sequence of intermediate predictions, and sufficiently large language models can exploit those intermediate steps to perform substantially better reasoning.**
