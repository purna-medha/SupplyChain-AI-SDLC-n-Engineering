# B6 standalone lab

Build an evidence inspection habit: check eligibility and retrieval coverage before judging an answer. All notes are synthetic. No capstone, database, notebook or shared helper is needed. The offline part uses supplied rankings to isolate the evaluation mechanism; it does not simulate semantic retrieval or inference.

## 1 · Worked example: explain a ranking

Read the supplied rankings below before running any endpoint. Explain each metric's numerator and denominator and what changing rank can affect. Then inspect card 02: identify where actual embeddings and retrieval replace supplied rankings. This worked calculation and the starter are catch-up baselines; no previous lab is required.

```python
relevant = {"gate-a"}
ranked = ["gate-b", "gate-a", "reefer-a"]
for k in (1, 2, 3):
    returned = ranked[:k]
    hits = len(set(returned) & relevant)
    precision = hits / k
    recall = hits / len(relevant)
    rr = next((1 / rank for rank, item in enumerate(returned, 1)
               if item in relevant), 0)
    print(k, precision, recall, rr)
```

At k=2 precision=0.5, recall=1.0 and reciprocal rank=0.5. At k=3 precision falls to 1/3 while recall and reciprocal rank stay unchanged because this worked example has one relevant ID. Explain why the guided example below, with two relevant IDs, has different recall.

## 2 · Guided practice: enforce scope and measure coverage

Save this as `b6_lab.py` anywhere. It requires only Python 3. Complete `eligible` and `metrics` without changing fixtures or assertions. The ranked ID list is a prepared observation, not model output. For this exercise the trusted application scope is Terminal A.

```python
notes = {
    "gate-a": {"terminal": "A", "text": "Terminal A gate opens at 06:00."},
    "gate-b": {"terminal": "B", "text": "Terminal B gate opens at 08:00."},
    "reefer-a": {"terminal": "A", "text": "Terminal A reefer desk is beside gate 2."},
}
trusted_terminal = "A"
ranked = ["gate-b", "gate-a", "reefer-a"]
relevant = {"gate-a", "reefer-a"}

def eligible(ids, terminal):
    # TODO: retain only IDs whose metadata matches trusted terminal.
    raise NotImplementedError

def metrics(ids, expected, k):
    # TODO: precision@k, recall@k and reciprocal rank among first k.
    # Precision denominator is k, even if fewer than k results exist.
    # Empty expected set: recall=0 by this exercise's convention.
    raise NotImplementedError

assert metrics(ranked, relevant, 2) == (0.5, 0.5, 0.5)
scoped = eligible(ranked, trusted_terminal)
assert scoped == ["gate-a", "reefer-a"]
assert metrics(scoped, relevant, 2) == (1.0, 1.0, 1.0)
assert metrics([], relevant, 2) == (0.0, 0.0, 0.0)
assert eligible(ranked, "C") == []
print("PASS: prepared ranking scope and metric contracts")
```

Run `python3 b6_lab.py`. Explain why filtering this complete prepared list before truncating to k succeeds, while fetching an unscoped top-1 and then filtering could leave no result. In a live system apply supported metadata filters inside the retriever before ranking; the exercise's list filter only makes the rule visible.

With a configured endpoint, copy card 02 to a new local script. Add terminal metadata to each node and the filter shown in the slides, then run it. Inspect the actual candidate IDs and terminal metadata. Change scope from A to B and repeat. Then copy card 03 and inspect actual answer claims against its returned source nodes. Keep unknown, missing-evidence questions in your observations. Do not turn a live failure into prepared success. If the endpoint is unavailable, record this stage as SKIPPED and complete the offline stage; the live learning outcome remains unverified.

## 3 · Independent transfer: repair a documented failure

Start from your completed script and a copy of the relevant live card. Add a new synthetic Terminal A note containing an exact identifier, a current/obsolete distinction, or a rule with an exception. Write two questions and relevant-ID labels before running retrieval. Make one question answerable and one deliberately unsupported by your corpus.

Capture a baseline's candidate IDs, metadata and answer claims. Diagnose the first failing boundary, choose one of metadata scope, hybrid retrieval, reranking or query rewriting, and justify its cost. Implement that change in your copy. Compare the same questions before and after, and test one changed question you did not use while tuning. If the baseline already succeeds, construct a controlled failure by removing a required candidate or splitting its exception and label that manipulation explicitly.

No implementation is supplied for this stage. Without endpoint access, perform a clearly labelled supplied-ranking experiment and state which semantic retrieval and generation claims remain untested. A missing-answer case must remain unavailable rather than acquire an invented answer. Advanced extension: inspect a live agent trace and explain a real observation-to-next-action decision and its stop condition.

## Evidence to submit

Submit the runnable script, original and changed fixtures, relevance labels, before/after observations, and one paragraph explaining the chosen repair and its limit. Include empty-scope behavior and one deliberately failing check followed by its repair. State whether live embedding, synthesis and agent execution were observed or skipped. Sources accompanying an answer do not replace claim-level checking.
