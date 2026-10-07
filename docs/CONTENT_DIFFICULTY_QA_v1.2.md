# Content & Difficulty QA Report — Final Rebuild v1.2

## Baseline generator audit
- 1,500 generated L1–L3 questions sampled
- 0 hard validity issues
- Structural repetition rate: 72.1% (expected for parametric templates)

## Advanced generator audit
- 1,080 generated L4/L5 questions sampled
- 0 hard validity issues
- 23 distinct advanced reasoning archetypes across 9 advanced skill families
- Every advanced skill family exposes at least 2 reasoning archetypes

Advanced families:
- Multi-step percentage
- Weighted average
- Data interpretation
- Rate change from table
- Constraint ordering
- Assignment constraints
- Verbal critical inference
- Only-if / conditional logic
- Figural matrix transform

## Difficulty ladder
- Foundation (L1)
- Standard (L2)
- Exam (L3)
- Hard (L4)
- Expert (L5, optional ceiling; not required for badge)

Hard difficulty is produced by deeper reasoning, information selection, combined constraints, less-obvious transformations, and stronger distractors—not merely larger numbers.

## Mastery challenge
Each TPA section challenge contains 15 items and at least 4 Hard L4 transfer items.

## Release gates
- Python test suite: 25/25 PASS
- Python compile: PASS
- Full npm dependency installation/build: not verified in builder environment because npm install timed out while fetching dependencies. Vercel/GitHub CI remains the deployment gate for the Next.js production build.
