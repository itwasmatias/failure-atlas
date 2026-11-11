# Failure Atlas — evidence-based troubleshooting (public-safe showcase)

A **small, portable, open-source demonstration** for a self-taught Python/AI developer portfolio.

## What a visitor can do

1. Open `index.html` in a normal browser; **no server, API key, package install, or internet connection is required** for the page to render.
2. Search a symptom description or click one of three examples.
3. See which words match short paraphrases from three real incident reports.
4. Read the original engineering postmortem at the public publisher URL when online.
5. See which research claims are verified and which are **not** proven.

This demo performs keyword overlap **only**. It is **not** an AI-powered diagnosis, semantic search, accuracy score, model evaluation, or live autonomous agent. Identifying similar incidents does not establish equal root causes.

## The research it explains

The independent frozen Failure Atlas v0.2 experiment compares a generic baseline solver with a solver given retrieved past incidents. It has 12 prepared questions and 24 **fixture** responses. As of this demonstration, **no real model A/B inference, measured effectiveness, paid calls or training** have occurred. The newer v0.3.2 security design is on HOLD for real execution.

Important: The 12 public evaluation questions, all private scoring keys, randomization and arm maps, and individual solver outputs are **not copied into this repo**. This site includes only three public historical case paraphrases and publisher URLs. Do not publish the original experimental workspace.

## How data provenance is protected

`build_public_data.py` reads **one** source file from frozen v0.2:

`/home/matias/projects/failure-atlas-v0-2-20261102/corpus/cases.jsonl`

It checks the pinned SHA-256 and expected three case IDs and three source URLs. It exports an allowlist of six public fields and fails if the frozen source changes. `PROVENANCE.json` contains the original checkpoint and SHA-256 of both source and export.

This source path is local to the owner's Fedora machine. A published clone can run the **prebuilt static website** and unit tests that don't require the original frozen corpus. Rebuilding the export requires access to that verified source file.

## Run / test on Fedora

```bash
cd /home/matias/projects/failure-atlas-showcase-v0-1-20261111
python3 -B -m unittest -v test_showcase
node --check app.js
node --check public-cases.js
firefox index.html
```

No credentials are required. There is no Python or JavaScript backend or telemetry. All source links use HTTPS and are informational; the page never fetches remote content automatically.

## Ethical / publication boundary

The supplied code and page design are original and offered under the MIT License. Original publisher incident reports remain under their respective publishers' rights; this repository provides original short paraphrases and attribution links, not copied reports.

**Publishing to GitHub or enabling a public website is a separate decision.** The demo is only prepared locally until the owner approves publishing. No performance claims, unreviewed confidential files or experimental answer keys should be added.

## What a person should understand in 30 seconds

When a service fails, engineers often consult past postmortems to find possible explanations and verification steps. This tool helps find relevant historical reports. The research asks whether giving such evidence to an AI helps it troubleshoot better — but that claim **has not yet been tested on real model responses**.

The project's value today is in transparent research preparation, provenance, honest limitations, and reproducible testing. Commercial effectiveness is not established.
