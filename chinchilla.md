# Chinchilla: Training Compute-Optimal Large Language Models

## Why This Paper Exists

After the Kaplan Scaling Laws paper, the AI community believed that additional compute should mostly be spent on increasing model parameters.

Most large language models followed this trend:

- GPT-3: 175B parameters, ~300B tokens
- Gopher: 280B parameters, ~300B tokens
- MT-NLG: 530B parameters, ~270B tokens

DeepMind questioned whether these models were actually trained optimally.

---

# Core Idea

The paper argues that many large language models are **undertrained**, not too small.

Instead of always increasing model size, compute should be balanced between:

- Model Parameters
- Training Tokens
- Total Compute

There exists a compute-optimal combination.

---

# Kaplan vs Chinchilla

### Kaplan Scaling Laws

- Spend more compute on larger models.
- Token count grows relatively slowly.

### Chinchilla

- Balance model size and training tokens.
- Smaller models trained on significantly more data can outperform much larger undertrained models using the same compute budget.

---

# Key Concepts

## Compute Budget

Training compute is limited.

More parameters increase the cost per training step.

More training tokens increase the number of training steps.

Choosing one limits the other.

---

## Undertraining vs Overfitting

Undertraining:
- Model has unused capacity.
- Has not seen enough training data.

Overfitting:
- Model memorizes the training data.
- Performs poorly on unseen data.

Chinchilla mainly addresses **undertraining**.

---

## Learning Rate

Learning rate controls how much weights change after each gradient update.

- Too high → unstable training.
- Too low → slow learning.

Learning rate schedules usually decrease over time to allow fine adjustments.

---

# Important Experiments

## IsoFLOP

Compare models trained with the **same compute budget**.

Goal:
Find the parameter/token combination with the lowest loss.

---

## Parametric Curve Fitting

Fit mathematical equations to hundreds of experiments.

Purpose:
Predict optimal model size and training tokens without training every possible combination.

---

## Downstream Benchmarks

Verify that lower training loss also improves real NLP tasks.

Result:
Compute-optimal models outperform much larger undertrained models.

---

# Engineering Takeaways

- Bigger models are not automatically better.
- More parameters require more training data.
- Compute should be allocated optimally between model size and training duration.
- Lower training loss is meaningful only if it also improves downstream benchmarks.
- Always think in terms of **compute efficiency**, not just parameter count.

---

# One-Line Summary

Chinchilla showed that, for a fixed compute budget, training a somewhat smaller model on substantially more data is often a better strategy than training the largest possible model on relatively little data.