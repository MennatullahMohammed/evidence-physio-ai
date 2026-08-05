# EvidencePhysio AI — Product Vision

## The Problem

Physiotherapists are expected to base treatment decisions on current, published evidence. In practice, that's hard to do consistently. Searching PubMed well takes training most clinicians never got, and reading through dozens of abstracts to find the handful relevant to a specific patient takes time most clinicians don't have. The result is that evidence-based practice often turns into evidence-informed guesswork: clinicians lean on what they remember from school, a handful of papers they read once, or something a colleague mentioned.

This isn't a knowledge problem. The evidence exists. It's a retrieval and synthesis problem.

## The Idea

EvidencePhysio AI does the evidence-gathering work a physiotherapist would otherwise do by hand, faster and more consistently. It takes a patient's clinical profile, searches the actual published literature, filters and ranks what it finds by quality and relevance, and returns a short, patient-specific summary with the studies behind it.

It does not diagnose. It does not recommend a specific treatment. It assumes a working diagnosis is already in place, and its only job is to answer: given this patient, what does the current evidence say, and how reliable is it?

The physiotherapist reads the summary, checks the sources, and makes the actual clinical decision. The tool's output is a starting point for that decision, not a replacement for it.

## Who This Is For

- Physiotherapists in clinical practice who want an evidence check on a treatment plan without spending an hour on PubMed
- Physiotherapy students learning to practice in an evidence-based way, who need a faster way to see what the literature actually supports for a given case
- Clinics and small practices without access to expensive, enterprise clinical-decision-support subscriptions

## Why This, Specifically

General clinical AI tools already do this well at a much larger scale, across all of medicine. EvidencePhysio AI isn't trying to compete with them. It's built around a narrower, physiotherapy-specific workflow: the fields that matter for a musculoskeletal diagnosis, the kind of evidence physiotherapists actually cite, and a search strategy built around physiotherapy-relevant terms rather than generic medical ones.

Narrower scope means it can go deeper on the specific case it's built for, instead of being a smaller, weaker version of a general tool.

## What "Good" Looks Like

- A physiotherapist enters a patient case and gets a report in under a minute they'd trust enough to read before deciding on treatment
- The evidence confidence rating is honest: it says "low confidence" when the literature is thin, instead of manufacturing false certainty
- Every claim in the report traces back to a real, cited study, not a hallucinated one
- The system is upfront about its own limitations, both to the clinician using it and in how it's built

## Current Stage

EvidencePhysio AI is an early-stage MVP, built as both a working tool and a learning project in AI system design. It connects to real data (PubMed) and produces real, structured output, but several components are still being verified, and the system hasn't been validated in a real clinical setting. It isn't yet suitable for unsupervised clinical use.

## Where This Could Go

- Expanding the diagnosis knowledge base beyond the current handful of conditions
- Validating the confidence-scoring rules against how experienced physiotherapists actually judge evidence quality
- Testing the tool with real physiotherapists on real (anonymized) cases, and adjusting based on what's actually useful to them in practice, not just what's technically correct