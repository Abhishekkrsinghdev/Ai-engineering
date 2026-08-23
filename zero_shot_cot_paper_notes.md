# Large Language Models are Zero-Shot Reasoners

**Paper:** *Large Language Models are Zero-Shot Reasoners*\
**Authors:** Takeshi Kojima et al.\
**Venue:** NeurIPS 2022

------------------------------------------------------------------------

## 1. Paper in One Sentence

Large language models can perform surprisingly strong **zero-shot
multi-step reasoning** when prompted with a generic trigger such as:

> **"Let's think step by step."**

The key idea is to first generate an explicit **reasoning path**, then
use that generated reasoning as context for a second stage that extracts
the final answer.

------------------------------------------------------------------------

# 2. Why This Paper?

Before this work, Chain-of-Thought (CoT) prompting had shown that LLMs
can perform difficult multi-step reasoning much better when given
**few-shot examples containing step-by-step reasoning**.

For example:

``` text
Question → reasoning steps → answer
```

instead of:

``` text
Question → answer
```

Few-shot CoT was powerful, but it required **task-specific
demonstrations**.

That creates a natural question:

> **Do we actually need to provide reasoning examples?**

The paper's answer is:

> **Not necessarily.**

A sufficiently large LLM can often generate useful reasoning simply when
prompted to **think step by step**.

------------------------------------------------------------------------

# 3. Prior Work: Chain-of-Thought

CoT prompting provides demonstrations such as:

``` text
Question
↓
Step 1
↓
Step 2
↓
Step 3
↓
Answer
```

rather than ordinary:

``` text
Question
↓
Answer
```

This gives the model a pattern for producing an intermediate reasoning
path.

The paper highlights the large improvement obtained by Few-shot-CoT, for
example:

**PaLM 540B on GSM8K**

``` text
Few-shot      → 17.9%
Few-shot-CoT  → 58.1%
```

The important observation is that **multi-step reasoning benefits
strongly from generating intermediate reasoning**.

------------------------------------------------------------------------

# 4. The Core Hypothesis

The paper asks:

> If few-shot examples can elicit reasoning, perhaps the model already
> possesses a general reasoning capability and the examples are not
> strictly necessary.

So instead of:

``` text
Example 1
Question → reasoning → answer

Example 2
Question → reasoning → answer

New Question
```

try:

``` text
New Question

"Let's think step by step."
```

The model is then encouraged to generate its own reasoning path.

------------------------------------------------------------------------

# 5. Zero-shot-CoT

The central trigger is:

> **"Let's think step by step."**

This is called **Zero-shot Chain-of-Thought (Zero-shot-CoT)**.

The important distinction:

### Ordinary Zero-shot

``` text
Question
↓
Answer
```

### Few-shot-CoT

``` text
Examples with reasoning
↓
New Question
↓
Reasoning
↓
Answer
```

### Zero-shot-CoT

``` text
New Question
↓
"Let's think step by step."
↓
Reasoning
↓
Answer
```

No task-specific reasoning examples are required.

------------------------------------------------------------------------

# 6. The Two-Stage Inference Pipeline

This is one of the most important parts of the paper.

Zero-shot-CoT is not simply:

``` text
Question
↓
"Let's think step by step"
↓
Final answer
```

The paper explicitly separates the process into **reasoning extraction**
and **answer extraction**.

## Stage 1 --- Reasoning Extraction

Given question `X`, add a reasoning trigger:

``` text
Q: [question]

A: Let's think step by step.
```

The model generates a reasoning path:

``` text
Z = generated reasoning
```

For example:

``` text
There are 16 balls.
Half are golf balls, so there are 8 golf balls.
Half of those are blue, so there are 4 blue golf balls.
```

`Z` is the **intermediate reasoning text**, not the final answer.

------------------------------------------------------------------------

## Stage 2 --- Answer Extraction

The generated reasoning is appended to the original context.

Conceptually:

``` text
Question
+
Reasoning Z
+
Answer-extraction trigger
```

For example:

``` text
Q: ...

A: Let's think step by step.

There are 16 balls.
Half are golf balls, so there are 8.
Half of those are blue, so there are 4.

Therefore, the answer (arabic numerals) is
```

The model then generates the final answer:

``` text
4
```

### Mental model

``` text
                 QUESTION
                    │
                    ▼
        "Let's think step by step"
                    │
                    ▼
          REASONING GENERATION
                    │
                    ▼
          Reasoning path Z
                    │
                    ▼
       Add Z back into the context
                    │
                    ▼
          ANSWER EXTRACTION
                    │
                    ▼
             FINAL ANSWER
```

------------------------------------------------------------------------

# 7. Why the Intermediate Reasoning Matters

The central inference-time transformation is:

``` text
Question
   ↓
Answer
```

becomes:

``` text
Question
   ↓
Intermediate reasoning
   ↓
Answer
```

The generated reasoning becomes **additional context** for subsequent
token generation.

This is particularly useful for problems where the answer depends on
multiple intermediate operations.

For example:

``` text
Understand the quantities
        ↓
Identify relationships
        ↓
Perform operation 1
        ↓
Use result in operation 2
        ↓
Reach final answer
```

The paper therefore treats the generated reasoning as an intermediate
reasoning path rather than merely extra output text.

------------------------------------------------------------------------

# 8. Answer Cleansing

The second generation can still produce text that is not perfectly
formatted.

The paper therefore applies an answer-cleansing step.

For arithmetic:

``` text
"probably 375 and 376"
```

is parsed as:

``` text
375
```

For multiple-choice tasks, the first valid large letter is selected.

So the full pipeline is:

``` text
Reasoning generation
        ↓
Answer generation
        ↓
Deterministic answer cleansing
        ↓
Benchmark prediction
```

This is important because the LLM remains probabilistic, while the
benchmark requires a deterministic answer format.

------------------------------------------------------------------------

# 9. Main Experimental Result

Zero-shot-CoT substantially improves over ordinary zero-shot prompting
on difficult reasoning tasks.

### Important results

  Dataset        Zero-shot   Zero-shot-CoT
  ------------ ----------- ---------------
  MultiArith         17.7%       **78.7%**
  GSM8K              10.4%       **40.7%**
  AQUA               22.4%       **33.5%**
  SVAMP              58.8%       **62.1%**

The improvement is especially large on tasks requiring more explicit
multi-step reasoning.

------------------------------------------------------------------------

# 10. Zero-shot-CoT vs Few-shot-CoT

Zero-shot-CoT does **not** universally beat carefully engineered
Few-shot-CoT.

For example:

### MultiArith

``` text
Zero-shot          17.7%
Few-shot            33.8%
Zero-shot-CoT       78.7%
Few-shot-CoT        93.0%
```

### GSM8K

``` text
Zero-shot          10.4%
Few-shot            15.6%
Zero-shot-CoT       40.7%
Few-shot-CoT        48.7%
```

So the contribution is not:

> "Zero-shot-CoT is better than Few-shot-CoT."

The stronger and more accurate claim is:

> **Zero-shot-CoT achieves surprisingly strong reasoning performance
> without task-specific reasoning demonstrations.**

Few-shot-CoT can still be better when the examples are carefully
engineered for the task.

------------------------------------------------------------------------

# 11. Why Few-shot Examples Are Still Useful

Few-shot examples provide the model with information about:

-   expected task structure
-   answer format
-   reasoning style
-   examples of the desired behavior

But examples are finite.

You cannot enumerate every possible reasoning path that a new problem
may require.

Zero-shot-CoT instead asks the model to construct the reasoning path for
the **current problem**.

``` text
Few-shot-CoT

Human-designed examples
        ↓
Model conditions on examples
        ↓
New problem
        ↓
Answer


Zero-shot-CoT

New problem
        ↓
Generic reasoning trigger
        ↓
Model constructs reasoning
        ↓
Answer
```

This is why Zero-shot-CoT can be surprisingly strong despite having no
task-specific demonstrations.

------------------------------------------------------------------------

# 12. Broad vs Narrow Generalization

This is one of the paper's broader claims.

### Narrow / task-specific prompting

``` text
Task
↓
Task-specific examples / templates
↓
Reasoning
↓
Answer
```

The prompt is engineered around a particular task.

### Broad generalization

``` text
Different reasoning tasks
        ↓
Same generic trigger
        ↓
Reasoning
        ↓
Answer
```

The authors demonstrate Zero-shot-CoT across:

-   Arithmetic reasoning
-   Symbolic reasoning
-   Commonsense reasoning
-   Logical reasoning
-   Date understanding
-   Tracking shuffled objects

The same generic reasoning trigger can facilitate reasoning across these
different task categories.

The paper therefore argues that sufficiently capable LLMs may possess
**broader reasoning capabilities** than ordinary zero-shot evaluation
reveals.

------------------------------------------------------------------------

# 13. Prompt Sensitivity

The paper tests 16 different triggers on MultiArith.

The best-performing trigger was:

> **"Let's think step by step." → 78.7%**

Other instructive prompts also helped:

``` text
First,                                      → 77.3%
Let's think about this logically.           → 74.5%
Let's solve this problem by splitting it
into steps.                                 → 72.2%
Let's think                                 → 57.5%
```

But misleading or irrelevant prompts performed much worse.

Examples:

``` text
Don't think. Just feel.                     → 18.8%
Let's think step by step but reach
an incorrect answer.                       → 18.7%
It's a beautiful day.                       → 13.1%
```

The ordinary zero-shot baseline was:

``` text
17.7%
```

### Important conclusion

It is **not simply the presence of additional prompt tokens** that
helps.

The prompt needs to encourage an appropriate reasoning trajectory.

The paper establishes this empirically, but does not completely explain
the internal mechanism behind why the exact wording works.

------------------------------------------------------------------------

# 14. Scaling Behavior

Zero-shot-CoT becomes more effective as model size increases.

This connects directly to the earlier CoT observation:

``` text
Small model
    ↓
Reasoning trigger
    ↓
Limited / weak reasoning


Large model
    ↓
Reasoning trigger
    ↓
Much stronger reasoning behavior
```

The paper observes that ordinary zero-shot performance is comparatively
flat with scale, while Zero-shot-CoT performance improves substantially
as model size increases.

### Interpretation

The trigger does not create a new capability.

It is useful because sufficiently large models have richer learned
capabilities that can be **elicited through the reasoning prompt**.

------------------------------------------------------------------------

# 15. Error Analysis

One of the most important lessons from the paper:

> **Generating a chain of thought does not guarantee a correct answer.**

The authors observe several failure modes.

## Failure 1 --- Reasonable reasoning, wrong answer

The model can produce a flexible and reasonable chain of thought but
still make the wrong final prediction.

This is particularly visible in commonsense reasoning.

``` text
Reasoning
   ↓
looks reasonable
   ↓
wrong final prediction
```

------------------------------------------------------------------------

## Failure 2 --- Failure to reason

Sometimes the model does not actually generate a reasoning path.

Instead it simply rephrases the question.

``` text
Question
   ↓
"Reasoning"
   ↓
essentially a paraphrase
```

The reasoning trigger is therefore an **elicitation mechanism**, not a
guarantee.

------------------------------------------------------------------------

## Failure 3 --- Correct answer → unnecessary reasoning → wrong answer

This is one of the most interesting failure modes.

The model can:

``` text
reach correct answer
        ↓
continue generating
        ↓
produce unnecessary reasoning
        ↓
change its prediction
        ↓
wrong final answer
```

This is a direct consequence of allowing autoregressive generation to
continue after the model has already reached a useful conclusion.

------------------------------------------------------------------------

## Failure 4 --- Multiple answers

In multiple-choice reasoning, the model can identify several plausible
answers but fail to commit to one.

Example:

``` text
A could work
B could work
C could work
D could work
E could work

Therefore: A, B, C, D, or E
```

The reasoning may be plausible, but the model fails at the final
decision/selection step.

------------------------------------------------------------------------

# 16. Important Conceptual Distinction

The paper demonstrates three things that should not be conflated:

``` text
Reasoning capability
        ≠
Reasoning generation
        ≠
Correct final answer
```

A model may:

``` text
generate reasoning ✓
but reasoning is wrong ✗
```

or:

``` text
generate reasonable reasoning ✓
but fail to select the correct answer ✗
```

or:

``` text
reach correct answer ✓
then continue reasoning
and change it ✗
```

Therefore:

> **CoT is a powerful way to elicit reasoning, but it is not a
> correctness guarantee.**

------------------------------------------------------------------------

# 17. What the Paper Actually Discovered

The paper's central discovery can be summarized as:

``` text
Previously:

Multi-step reasoning
        ↓
Few-shot CoT examples
        ↓
Strong performance


This paper:

Multi-step reasoning
        ↓
Generic trigger
"Let's think step by step"
        ↓
Reasoning generation
        ↓
Strong zero-shot performance
```

This demonstrates that large LLMs can exhibit useful **zero-shot
reasoning behavior** without task-specific reasoning demonstrations.

------------------------------------------------------------------------

# 18. What Is New Compared With Few-shot CoT?

### Few-shot-CoT

Requires:

``` text
Human
 ↓
construct task-specific examples
 ↓
reasoning demonstrations
 ↓
model
```

### Zero-shot-CoT

Requires:

``` text
Human
 ↓
generic reasoning trigger
 ↓
model constructs reasoning itself
```

The second approach is therefore much more **task-agnostic**.

The paper's broader suggestion is to investigate generic prompts that
can uncover broad capabilities rather than manually engineering
demonstrations for every task.

------------------------------------------------------------------------

# 19. What NOT to Claim

These distinctions are important when discussing the paper.

### Don't say:

> Zero-shot-CoT always beats Few-shot-CoT.

**Correct:** Carefully engineered Few-shot-CoT generally performs
better.

### Don't say:

> The second stage verifies the reasoning.

**Correct:** The second stage performs **answer extraction conditioned
on the generated reasoning**. It is not an independent verifier.

### Don't say:

> Generating CoT guarantees correct reasoning.

**Correct:** The paper explicitly observes reasonable-but-wrong
reasoning and several other failure modes.

### Don't say:

> "Let's think step by step" adds factual knowledge.

**Correct:** It changes the prompting condition and encourages a
reasoning trajectory.

### Don't say:

> The paper proves that LLMs genuinely reason.

**Correct:** The paper demonstrates strong zero-shot reasoning behavior
and argues that large LLMs possess broad reasoning capabilities, but it
does not settle the philosophical question of what constitutes "real
reasoning."

------------------------------------------------------------------------

# 20. The Entire Paper in One Diagram

``` text
                 LARGE LANGUAGE MODEL
                         │
                         │
              Existing learned capability
                         │
                         ▼
                Generic prompt trigger
             "Let's think step by step"
                         │
                         ▼
              ┌─────────────────────┐
              │ Reasoning generation│
              │         Z           │
              └──────────┬──────────┘
                         │
                         │ Z becomes context
                         ▼
              ┌─────────────────────┐
              │ Answer extraction   │
              └──────────┬──────────┘
                         │
                         ▼
                  Final prediction
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
        Strong improvement       Failure modes
        on reasoning tasks       still remain
```

------------------------------------------------------------------------

# 21. The 5 Things to Remember

### ① The problem

Few-shot CoT works well but requires **task-specific reasoning
demonstrations**.

### ② The insight

A sufficiently large LLM may already possess useful reasoning behavior
that can be elicited without examples.

### ③ The technique

> **"Let's think step by step."**

followed by a second answer-extraction stage.

### ④ The result

Huge improvements over ordinary zero-shot prompting, especially on
multi-step reasoning tasks.

### ⑤ The limitation

**Reasoning generation ≠ guaranteed correctness.**

The model can reason incorrectly, fail to reason, fail to commit, or
even reason correctly and subsequently change the answer.

------------------------------------------------------------------------

# 22. Final Mental Model

If you remember only one thing from this paper:

> **Zero-shot-CoT turns a direct answer-generation problem into an
> intermediate-reasoning-generation problem followed by answer
> extraction.**

``` text
              Before

        Question ───────→ Answer


              After

        Question
            │
            ▼
   "Let's think step by step"
            │
            ▼
      Reasoning path
            │
            ▼
   Reasoning becomes context
            │
            ▼
      Answer extraction
            │
            ▼
         Answer
```

**The paper's big idea is not that the prompt teaches the model how to
reason. It shows that a generic inference-time trigger can expose
reasoning behavior that is already available in sufficiently capable
language models.**
