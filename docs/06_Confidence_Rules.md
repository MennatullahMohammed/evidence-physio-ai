# EvidencePhysio AI — Evidence Confidence Rules

## Purpose

This document explains how the Evidence Confidence Engine (Component 7) rates the overall reliability of the evidence returned for a patient case. The scoring is fully rule-based, and no language model is involved in producing the confidence rating. That keeps the result explainable and reproducible: the same evidence set always produces the same rating.

## Why Rule-Based, Not AI

An AI model could plausibly generate a confidence rating, but it would be hard to explain why it landed on a particular answer, and the same input might not reliably produce the same output twice. For a rating that affects a clinical decision, that unpredictability is a real cost. A fixed set of rules means the physiotherapist, or anyone reviewing the system, can trace exactly how a rating was reached.

## Step 1: Scoring an Individual Study

Each validated study gets a score based on two factors.

**Study design score**, based on the study design reported in the extracted data:

| Study Design | Points |
|---|---|
| Systematic review | 4 |
| Meta-analysis | 4 |
| Randomized controlled trial | 3 |
| Review | 2 |
| Case reports | 1 |
| Anything else / not recognized | 1 (default) |

**Sample size bonus**: studies reporting 50 or more participants get an extra point. Smaller or unreported sample sizes get no bonus.

A study's total score is the design score plus the sample size bonus. A randomized controlled trial with 60 participants, for instance, scores 3 + 1 = 4.

## Step 2: Comparing Across Studies

The engine averages the score across every validated study in the evidence set. That single number represents the overall quality of the evidence gathered, not just the strongest or weakest study in the set.

## Step 3: Classifying Overall Confidence

The average score is checked against fixed thresholds:

| Confidence Level | Average Score Threshold |
|---|---|
| High | ≥ 4.0 (and at least 3 studies) |
| Moderate | ≥ 2.5 |
| Low | ≥ 1.0 |
| Very Low | below 1.0 |

**Exception worth noting:** even if the average score clears the "High" threshold, the rating only reaches "High" with at least 3 validated studies behind it. One excellent study isn't enough to claim high confidence; however well-designed, a single study doesn't establish a reliable evidence base on its own. Short of that, the rating falls back to "Moderate."

## Step 4: Explaining the Rating

Alongside the confidence level, the engine writes a short explanation stating the number of studies used and the average score, so a physiotherapist isn't just handed a label like "Moderate" with nothing behind it.

## Design Principle

If the evidence is thin, the system says so. A "Low" or "Very Low" rating is a correct, useful output, not a failure of the system. Inflating a confidence rating to make a report look stronger would defeat the entire point of scoring it by fixed rules in the first place.

## Known Limitation

The scoring depends on the `study_design` and `sample_size` fields as extracted from each paper. If Component 6 (Claude Evidence Extraction Engine) misreads or misclassifies a paper's design, that study's confidence score will be affected downstream. Worth keeping in mind when interpreting results, and a candidate for future validation work (see the Project Roadmap).