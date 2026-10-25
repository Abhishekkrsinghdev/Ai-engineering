# ReAct — Synergizing Reasoning and Acting in Language Models

**Paper:** Yao et al., ICLR 2023  
**Core topic:** LLM Agents / Reasoning / Tool Use

## 1. One-line idea

ReAct interleaves language reasoning with actions and observations:

Thought → Action → Observation → Thought → Action → Observation → ...

Reasoning helps the model decide what to do next.
Actions let it interact with an external environment.
Observations bring external evidence/state back into the model's context.

The model can therefore continually update its plan instead of producing
a complete reasoning chain using only its parametric knowledge.

---

## 2. The problem before ReAct

There were roughly two separate directions:

### Reasoning-only / Chain-of-Thought

Question
  ↓
Reason
  ↓
Reason
  ↓
Answer

Strength:
- Good at decomposition and multi-step reasoning.

Weakness:
- No external grounding.
- A hallucinated premise can propagate through an otherwise logical chain.

Example:

Wrong fact
  ↓
Correct reasoning over wrong fact
  ↓
Wrong answer


### Acting-only

Goal
  ↓
Action
  ↓
Observation
  ↓
Action
  ↓
Observation

Strength:
- Can interact with external information/environments.

Weakness:
- Poor high-level planning.
- Can lose track of subgoals/state.
- Can repeat useless actions.

ReAct combines the strengths of both.

---

## 3. Formal intuition

Traditional agent:

a_t ~ π(a_t | c_t)

The next action depends on the trajectory/context so far.

ReAct expands the action space:

Â = A ∪ L

A = external/environment actions
L = language/reasoning actions

Important distinction:

Thought:
- Does NOT change external environment.
- Adds useful information to the trajectory/context.

Action:
- Interacts with or changes the external environment.
- Produces an observation.

Therefore:

Reasoning → improves/organizes current context
Action → interacts with world
Observation → adds external evidence/state to context

The model parameters remain unchanged during inference.

---

## 4. Why the loop works

Reason → Act:
- What information is missing?
- What is the current subgoal?
- Which action/tool should be used?
- What should be searched?
- Is enough information available to finish?

Act → Reason:
- Tool/environment returns new evidence.
- Evidence enters context.
- Previous assumptions can be corrected.
- Plan can be updated.

Therefore:

Reason to Act ↔ Act to Reason

The external environment effectively provides a feedback mechanism for
the model's reasoning.

---

## 5. Standard vs CoT vs Act vs ReAct

| Method   | Explicit Reasoning | External Interaction |
|----------|--------------------|----------------------|
| Standard | No                 | No                   |
| CoT      | Yes                | No                   |
| Act      | No                 | Yes                  |
| ReAct    | Yes                | Yes                  |

ReAct is not simply "LLM + tools".

Its important idea is the feedback loop between reasoning and interaction.

---

## 6. Knowledge-intensive tasks

Benchmarks:
- HotpotQA
- FEVER

The model receives only the question/claim and must either use internal
knowledge or retrieve external information.

Wikipedia environment exposes only:

search[entity]
lookup[string]
finish[answer]

Typical trajectory:

Question
  ↓
Thought: What information do I need?
  ↓
search[X]
  ↓
Observation
  ↓
Thought: What does this establish? What is still missing?
  ↓
search[Y]
  ↓
Observation
  ↓
finish[answer]

The retrieval system was intentionally simple, forcing the LLM to reason
about what information to retrieve.

---

## 7. Few-shot ReAct

The original paper mainly induces ReAct using demonstrations.

Prompt contains examples such as:

Question
Thought
Action
Observation
Thought
Action
Observation
...
Answer

A frozen LLM continues this demonstrated pattern.

For the knowledge tasks the paper used:
- 6 HotpotQA examples
- 3 FEVER examples

No parameter update is required for the basic prompting setup.

---

## 8. What "Thought" provides

Thoughts can perform:

- goal decomposition
- planning
- observation interpretation
- commonsense reasoning
- arithmetic/logical reasoning
- progress tracking
- search reformulation
- error recovery
- final answer synthesis

Thought is therefore useful as temporary trajectory/working state.

---

## 9. Dense vs sparse reasoning

Knowledge QA uses relatively dense:

Thought → Action → Observation
Thought → Action → Observation

Long-running decision tasks can use sparse reasoning:

Thought: establish subgoal
Action
Observation
Action
Observation
Action
Observation
Thought: subgoal complete; establish next subgoal

Important lesson:

Reasoning does NOT need to precede every trivial action.

Reason strategically when planning/state/subgoal decisions matter.

---

## 10. ALFWorld

Text-based household environment.

Example goal:

"Put the pepper shaker in the drawer."

Agent may need to:

1. determine likely pepper-shaker locations
2. search locations
3. find it
4. pick it up
5. find drawer
6. open drawer
7. place shaker inside

This demonstrates why reasoning matters for:
- high-level planning
- commonsense
- tracking state
- tracking completed subgoals

ReAct best success: 71%
Act-only best: 45%

---

## 11. WebShop

Agent navigates a shopping environment and must satisfy user constraints.

Example:

"Nightstand with drawers, nickel finish, below $140."

The agent must connect noisy observations back to the original constraints.

ReAct success rate: 40.0%
Act-only: 30.1%

Reasoning helps bridge observations and actions.

---

## 12. Failure modes

ReAct is NOT universally superior to CoT.

On HotpotQA:
CoT: 29.4
ReAct: 27.4

On FEVER:
CoT: 56.3
ReAct: 60.9

Why?

CoT:
- flexible reasoning
- but susceptible to hallucinated facts

ReAct:
- better factual grounding
- but introduces new failure modes:
  - bad searches
  - uninformative observations
  - repetitive action/reasoning loops
  - reasoning errors

Key trade-off:

External grounding reduces hallucination
but introduces interaction/retrieval failures.

---

## 13. ReAct + Self-Consistency

The paper therefore combines ReAct with CoT-SC.

Idea:

If internal reasoning appears uncertain:
CoT-SC → ReAct

If ReAct gets stuck:
ReAct → CoT-SC

This demonstrates a broader principle:

Internal model knowledge and external knowledge are complementary.

---

# Modern Agent Interpretation

IMPORTANT:
The following is a modern architectural mapping, NOT the architecture
specified by the original ReAct paper.

A modern agent can be viewed as:

User Goal
   ↓
Agent Harness
   ├── instructions
   ├── goal/constraints
   ├── planning
   ├── context management
   └── tool definitions
           ↓
          LLM
           ↓
      decide next step
       /          \
    answer        action
                    ↓
                tool/world
                    ↓
               observation
                    ↓
             update context
                    ↓
                   LLM

The ReAct loop remains underneath:

Reason → Act → Observe → Reason

---

## 14. Memory vs Context

Do not conflate them.

### Parametric knowledge
Knowledge encoded in model weights.

Normally frozen during inference.

### Context
Tokens currently available to a model invocation:
- instructions
- user request
- conversation
- tool descriptions
- observations
- retrieved memory
- relevant task state

### KV cache
Inference optimization storing previous attention key/value
representations.

It is not long-term semantic memory.

### External memory/state
Information persisted outside the model.

Can include:

Short-term:
- current goal
- current plan
- completed subgoals
- recent observations
- intermediate results

Long-term:
- durable project knowledge
- reusable decisions
- preferences
- previous experiences

Storage implementation depends on the use case:
- database
- files
- object store
- vector database
- graph database
- Redis
- etc.

Critical distinction:

Memory → retrieval/selection → Context → LLM

Memory may be huge.
Only relevant information needs to enter the current context window.

---

## 15. Tools and MCP

ReAct requires actions/environment interaction but does NOT define MCP.

Modern tools may be:

1. Native/custom tools
2. MCP-exposed tools

MCP standardizes how capabilities can be exposed to an agent.

An MCP server may expose tools/resources/etc. and communicate using
supported transports such as stdio or Streamable HTTP.

Conceptually:

Agent Harness
   ↓
MCP Client
   ↓
stdio / Streamable HTTP
   ↓
MCP Server
   ↓
Tool
   ↓
External System

The resulting observation can then be returned to the agent's context.

---

## 16. Long-running agents

A context window should not be treated as durable workflow storage.

For long tasks, externalize important state:

Goal
Plan
Completed work
Current subgoal
Decisions
Artifacts
Failures
Next actions

Then reconstruct an appropriate context for subsequent model calls.

This prevents needing the complete raw trajectory forever.

---

## 17. ReAct vs Durable Execution

ReAct answers:

"What should I do next given what I currently know?"

Durable workflow/orchestration systems solve another problem:

"How do I reliably execute and resume this work across failures,
retries, waiting and process restarts?"

Example modern architecture:

LLM / Agent
   ↓
reason + choose next action
   ↓
Durable orchestration
   ↓
execute activity/tool
   ↓
external world
   ↓
observation/state
   ↓
LLM reasons again

A system such as Temporal can therefore complement an agent,
but Temporal itself is not ReAct and ReAct does not require Temporal.

---

## 18. Limitations from the paper

- Large action spaces can require more demonstrations.
- Demonstrations consume context-window capacity.
- Search/tool results can be uninformative.
- Agents can become stuck in repetitive loops.
- ReAct still makes reasoning errors.
- Connecting LLMs to real environments introduces safety concerns.
- Fine-tuning and higher-quality trajectories may improve performance.

---

# Final Mental Model

ReAct is not:

"Give an LLM tools."

ReAct is:

Reasoning determines useful actions.
Actions generate new external information/state.
Observations update the context.
The updated context changes subsequent reasoning.

Therefore:

        ┌─────────────────────────────┐
        │                             │
        ▼                             │
     REASON                           │
        │                             │
        ▼                             │
      ACTION                          │
        │                             │
        ▼                             │
   ENVIRONMENT                        │
        │                             │
        ▼                             │
   OBSERVATION ───────────────────────┘

The model's parameters remain frozen during ordinary inference;
the trajectory/context evolves.

Modern agent systems build infrastructure around this basic loop:
planning, context management, external memory, tools/MCP,
permissions, retries, checkpoints and durable execution.

## One sentence to remember

**ReAct turns an LLM from a model that reasons about what it already
knows into a loop that can reason about what to do, interact with the
world, learn from the resulting observation within context, and
continue reasoning toward the goal.**

## 19. ReAct Limitations → Modern Agent Architecture

A useful way to understand today's agent stack is that much of its
infrastructure addresses limitations that become apparent around the
ReAct loop.

| ReAct-era limitation | Modern architectural response |
|---|---|
| Limited context window | Context engineering, compaction, retrieval, external memory |
| Large action/tool space | Tool discovery, routing, MCP/tool registries |
| Poor/uninformative retrieval | Better search/RAG, reranking, query reformulation |
| Repetitive action/reasoning loops | Step limits, loop detection, evaluators |
| Long tasks lose state | External task state, checkpoints, short/long-term memory |
| Execution interrupted by failures | Durable execution/workflows such as Temporal |
| Hallucinated internal knowledge | Retrieval/tool grounding and verification |
| Tool/action failures | Retries, fallbacks, typed errors, idempotency |
| Dangerous external actions | Permissions, sandboxing, approval gates |
| Initial plan becomes stale | Re-planning from new observations |
| Difficult to understand agent behavior | Tracing, observability, tool/action histories |
| Demonstrations consume context | Fine-tuning and trained tool-use/reasoning behavior |

Important distinction:

The ReAct paper itself identifies limitations such as context-length
pressure, reasoning/search failures, repetitive trajectories, large
action spaces, and risks from external actions.

Technologies such as MCP, external memory architectures, modern context
engineering, and Temporal are later architectural responses/mappings;
they were NOT components proposed by the ReAct paper.

### Architectural takeaway

ReAct established the minimal cognitive loop:

Reason → Act → Observe → Reason

Modern agent engineering can be viewed as infrastructure that makes
this loop:

- scalable
- stateful
- reliable
- recoverable
- observable
- secure
- durable

Therefore, when encountering a new agent technology, ask:

> Which failure mode or missing capability around the
> Reason → Act → Observe loop is this component solving?

This provides a simpler mental model for understanding technologies
such as RAG, memory, MCP, planners, evaluators, checkpoints,
guardrails, and durable workflow systems.