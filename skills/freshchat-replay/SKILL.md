---
name: freshchat-replay
description: >
  Evaluation harness for the Freshchat bot. Replays historical resolved conversations against the
  freshchat-autoreply decision logic and scores how the bot would have performed versus what the
  human actually did. Use this skill when the user wants to "test the bot", "evaluate the bot",
  "see how the bot would do", "run a backtest", "check accuracy before going live", or after tuning
  the knowledge base / confidence rules. Produces a scorecard, not customer-facing output.
---

# Freshchat Bot Replay / Eval

Before the bot ever touches a live customer, this skill tells you how good it is — by replaying conversations your team already solved and grading the bot against the known-good human resolution.

It is **Phase 3** (validation) of the build. Run it whenever you change the knowledge base or the confidence rules, so you can see whether a change actually helped.

## How It Works

### 1. Build the test set

Pull a sample of **resolved** conversations the bot has NOT been trained to memorize (hold these out, or sample fresh from a recent window via `freshchat-mine`'s extract). Aim for coverage across `cf_topic`s, not just the easy ones. A few hundred is plenty; weight toward topics you expect the bot to handle.

For each, you know the ground truth: the human's actual resolution and whether it stuck (not reopened).

### 2. Replay

For each conversation, feed **only the customer side up to the point the agent first responded** into `freshchat-autoreply`, and capture its decision object (confidence, action, reply_text, kb_sources). The bot must not see the human's answer — that's the answer key.

### 3. Grade each decision

Compare the bot's decision to the human outcome:

| Bot did | Human outcome | Verdict |
|---------|---------------|---------|
| Responded (HIGH) | Same resolution as human, issue stayed resolved | ✅ **Correct auto-answer** |
| Responded (HIGH) | Different / wrong resolution | ❌ **False confident** (worst case — count these loudly) |
| Escalated | Human handled it with a simple KB answer | ⚠️ **Over-escalation** (missed automation opportunity) |
| Escalated | Human also needed backend/remote/billing | ✅ **Correct escalation** |
| Responded (MEDIUM) | — | 🟡 Would have gone to human approval — judge the draft quality |

Grade reply quality by semantic match to the human resolution (same fix, same steps), not literal text. A reply that's differently worded but correct is correct.

### 4. Score and report

Produce a scorecard:

- **Auto-answer accuracy** — of HIGH-confidence responses, what % were correct. This is the headline number; it must be high (target ≥95%) before any auto-send goes live.
- **False-confident rate** — % of HIGH responses that were wrong. The number that must be near-zero.
- **Coverage** — % of conversations the bot would have auto-answered at all (vs escalated). Low coverage = safe but not useful yet.
- **Over-escalation rate** — escalations that a documented KB answer would have solved.
- **Per-topic breakdown** — accuracy and coverage by `cf_topic`, so you see exactly which topics are bot-ready and which aren't.
- **Failure gallery** — the specific false-confident and bad-draft cases, with conversation IDs, so you can fix the underlying KB pattern.

### 5. Recommend

Close with a go/no-go read per topic: which `cf_topic`s are safe to enable for auto-send, which should stay human-approval, and which need more KB work before the bot touches them at all. This is the dial you turn as confidence grows.

## Guardrails

- This skill is **read-only against customers** — it never sends anything. It only scores.
- Don't let the bot peek at the answer. If the test conversation's transcript already contains the agent's resolution, truncate it before replay or the scores are meaningless.
- A high accuracy on a tiny coverage % is not "the bot works" — report both, always, and never bury low coverage.
- Stale ground truth: if a resolution relied on a since-fixed bug or old POS version, flag it rather than scoring the bot as wrong.

## Related

- `freshchat-autoreply` skill — the logic under test
- `freshchat-mine` skill — source of both the KB and the held-out test set
- `freshchat-learn` skill — turns the failure gallery into KB fixes
