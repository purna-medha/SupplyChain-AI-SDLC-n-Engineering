# B3 assessment

1. How does a fixed chain differ from a router? Give the route for missing, delayed and unknown status.
2. Why does card 02 with a two-step budget report exhaustion even though the draft exists? What does the loop `else` mean?
3. In card 03, what does `max_steps` bound? What happens if every model response contains tool calls? Is a terminal model answer proof of correctness?
4. Why retry a timeout but stop on an unknown container ID? Why do tool retries and model-loop budgets need separate limits?
5. Which state transitions may a pending draft take? What should happen on a repeated decision, and does saving/reloading a pending record approve it?

## Evidence and scoring

Answer with a short trace or causal explanation rather than only naming a pattern. Each question is worth 2 points, for 10 total. Award one point for the correct behavior and one for why the mechanism produces it. Question-specific criteria and reasoned answers are in the instructor guide. Use the scores diagnostically: revisit honest stopping and approval where explanations are missing.
