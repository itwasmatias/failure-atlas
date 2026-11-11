# Failure Atlas showcase — verification record

Date: November 11, 2026 (America/Chicago)

## What a nontechnical viewer should understand

A past software outage can be a useful clue when investigating a new outage, but similarity is not proof of the same cause. The page demonstrates looking up three real postmortems by symptoms and cites the original publishers. Whether retrieval improves an AI's answers is still unknown.

## Directly observed tests

- Frozen v0.2 integrity: 54 delivery-file hashes match; 13 archived snapshot-file hashes match; 12 public evaluation questions present. No integrity failures.
- Frozen v0.2 offline harness: 11 unit tests passed.
- Existing private Research Console: 5 unit tests passed. Private Tailscale URL responded 200 after restoring the existing transient service.
- Public-safe showcase: 5 unit tests passed.
- JavaScript syntax: Node `--check` passed for app.js and public-cases.js.
- Real Firefox on HP14: 3 incident cards rendered, example symptom search returned matches, unmatched search handled correctly, 3 publisher links present, no horizontal overflow.
- Real Firefox on HP14: screenshot captured at 390 × 844 (mobile viewport); page displays project purpose and evidence totals clearly.
- Fedora headless Firefox and Chromium timed out during screenshot attempts; HP14 successfully completed the visual and interactive checks. Those Fedora attempts are not counted as passing.

## Frozen-source provenance

- Source path: /home/matias/projects/failure-atlas-v0-2-20261102/corpus/cases.jsonl
- Source checkpoint: 3f521c14d07242da2827e1fa452cd8603fff510c
- Expected source SHA-256: 1062ef960c06698dbb02a0a74898b83719f5bd47b49ab891fb57bd1bcd5bc64c
- Export: exactly three cases; only id, symptoms, cause, resolution, source URL, resolution status.
- No evaluation questions, answer keys, private arm maps, provider credentials or raw reports exported.

## Claims we cannot make

- No real-model accuracy or speed improvement measured.
- No real baseline-versus-retrieval inference or scoring.
- No evidence that matching words identifies a root cause.
- No general production security guarantee.
- iPhone Safari has not yet been personally checked with this **new** showcase.

The original v0.2 research and private console were not edited. This showcase was built in its own Fedora workspace. Publishing to GitHub or a public website remains a human approval boundary.
