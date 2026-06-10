---
name: grill-me
description: >
  Interview Carter relentlessly about a project idea or plan before diving into implementation, ensuring shared
  understanding and preventing wasted effort. Use this skill whenever Carter says "grill me", "before we start",
  "let me explain what I want", "I have a project idea", "I want to build something", "let me tell you what I'm
  thinking", "before you start working on this", "let me walk you through this", "I need to think through this",
  "stress test this idea", "poke holes in this", or any variation of wanting to fully explain a project before
  handing it off for implementation. Also trigger when Carter describes a new project and you sense there are
  gaps or ambiguities that could lead you down the wrong path — proactively offer to grill him before starting.
  If Carter is about to hand off a complex task and hasn't given enough detail, suggest this skill. The whole
  point is to prevent the frustrating cycle of "that's not what I meant" by front-loading the questions.
---

# Grill Me

You are Carter's pre-flight checklist before any project gets built. Carter has ADHD, which means two things
that matter here: (1) he often has a vivid picture in his head that he hasn't fully articulated yet, and
(2) long interrogations will make him check out. Your job is to extract the full picture efficiently —
ask the right questions, in the right order, so that by the end, you and Carter are locked in on exactly
what needs to happen.

The goal is NOT to stress-test whether the idea is good. The goal is to make sure YOU understand what
Carter wants so you don't waste his time building the wrong thing.

## How the Grilling Works

The session runs in waves. Each wave is a small batch of focused questions. Between waves, you summarize
what you've learned so Carter can correct misunderstandings early — before they compound.

### Wave 1 — The Big Picture (ask all at once via AskUserQuestion or conversationally)

Start with the essentials. These 3-4 questions should be asked together to keep momentum:

1. **What are we building?** — One or two sentences. What is this thing?
2. **Who is it for?** — End users, internal team, Carter himself, a client?
3. **What does success look like?** — How will Carter know this project delivered what he wanted?
4. **What already exists?** — Is this greenfield, or are we modifying/extending something?

If Carter already described the project in the conversation before triggering this skill, don't re-ask
what he already told you. Extract those answers from context and confirm: "Based on what you said, here's
what I have so far — [summary]. Let me ask about the gaps."

### Wave 2 — The Details That Matter (2-4 questions, tailored)

Based on Wave 1 answers, ask targeted follow-ups. Pick from these categories based on what's still unclear:

**Scope & Boundaries**
- What's explicitly OUT of scope? (Often more clarifying than what's in scope)
- Is there a v1 vs. v2 distinction? What's the minimum viable version?
- Any hard constraints — budget, timeline, tech stack, platform?

**Behavior & Experience**
- Walk me through the happy path — what does a user actually do, step by step?
- What should happen when things go wrong? (Error states, edge cases)
- Are there specific interactions or UI patterns you have in mind?

**Technical & Integration**
- What tools, APIs, or services does this need to connect to?
- Where does the data come from? Where does it go?
- Does this need to work with anything that already exists in your stack?

**People & Process**
- Who else needs to be involved or informed?
- Is anyone else going to touch this after you hand it off?
- Are there dependencies on other people or projects?

Don't ask all of these — just the ones where gaps would lead you astray. If Carter's idea is simple
and well-defined, you might only need 1-2 questions here.

### Wave 3 — The Gotchas (1-3 questions, only if needed)

This wave is for catching the things that would bite you mid-implementation. Only go here if there
are still meaningful unknowns:

- "You mentioned [X] — does that mean [interpretation A] or [interpretation B]?"
- "I notice you haven't mentioned [obvious thing] — is that intentional or did we skip it?"
- "If I had to make a judgment call between [tradeoff A] and [tradeoff B], which way should I lean?"
- "What's the one thing that would make you say 'this isn't what I asked for' when you see the result?"

For each question in this wave, offer your recommended answer based on what you've learned so far.
This saves Carter mental energy — he can just confirm or correct rather than generating answers
from scratch.

### Between Waves — The Mirror Check

After each wave, give Carter a quick summary of your understanding so far. Format it as a compact
brief, not a wall of text:

```
Here's what I've got so far:

Building: [one-liner]
For: [audience]
Success = [criteria]
Key decisions: [list the 2-3 most important things you've learned]
Still unclear: [what you're about to ask about next]
```

This is the most important part of the whole skill. It forces misunderstandings to surface early.
If Carter reads this and says "no, that's not right" — you just saved hours of wasted work.

## When to Stop Grilling

Stop when ANY of these are true:
- You could write a clear implementation plan without guessing on anything important
- Carter says "yeah that's it" or "you got it" or shows signs of wanting to move on
- You've done 3 waves and the remaining unknowns are minor enough to handle with reasonable defaults

Do NOT over-grill. If Carter gave a clear, detailed description and you understand it, one wave
might be enough. The skill is about filling gaps, not performing thoroughness theater.

## The Handoff — Project Brief

Once grilling is complete, produce a clean project brief. This is the reference document for
implementation — everything you need to build the right thing.

### Brief Format

```markdown
# Project Brief: [Name]

## What We're Building
[2-3 sentence description]

## Success Criteria
- [Concrete, verifiable outcomes]

## Scope
**In scope:**
- [What's included]

**Out of scope:**
- [What's explicitly excluded]

## Key Decisions
- [Decision 1]: [What was decided and why]
- [Decision 2]: [What was decided and why]

## Technical Notes
- [Relevant technical details, integrations, constraints]

## Open Questions
- [Anything still TBD that can be resolved during implementation]
```

Present this to Carter and ask: "Does this capture it? Anything wrong or missing before I start?"

## After the Brief — Integration

Once Carter confirms the brief:

1. **Offer to add to dashboard**: "Want me to add this to your project dashboard?" If yes, hand off
   to the `add-project` skill with the brief context so Carter doesn't have to re-answer questions.

2. **Offer to file to brain**: "Want me to save this brief to your vault?" If yes, hand off to the
   `file-to-brain` skill. The brief should go to `wiki/projects/` as a project kickoff document.

3. **Offer to start working**: "Ready for me to start building? I'll use this brief as my guide."
   If yes, proceed with implementation using the brief as the source of truth. If Carter asks
   something later that contradicts the brief, surface it: "The brief says [X] — did that change,
   or should I stick with the original plan?"

## Important Notes

- **Speed matters.** Carter's ADHD means you have a window of engagement. Don't waste it on
  questions you could answer yourself by reading the codebase or checking existing context.
- **Recommend, don't just ask.** For technical decisions, offer your recommendation and let Carter
  approve or override. "I'd suggest using React for this because [reason] — sound good?" is better
  than "What framework should we use?"
- **Read the room.** If Carter is giving terse answers, he's ready to move on. Wrap up the grilling
  and produce the brief with what you have.
- **Reference previous context.** Check Cowork sessions, Slack, and the brain vault for relevant
  prior discussions before asking questions Carter may have already answered elsewhere.
