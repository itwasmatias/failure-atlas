#!/usr/bin/env python3
"""Build only a public-safe three-incident dataset from frozen v0.2.
No inference or evaluation question/answer files are read.
"""
from pathlib import Path
import hashlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parent
FROZEN = Path("/home/matias/projects/failure-atlas-v0-2-20261102/corpus/cases.jsonl")
EXPECTED_SHA256 = "1062ef960c06698dbb02a0a74898b83719f5bd47b49ab891fb57bd1bcd5bc64c"
CHECKPOINT = "3f521c14d07242da2827e1fa452cd8603fff510c"
ALLOWED_FIELDS = ("case_id","symptoms","cause","resolution","url","resolution_status")
EXPECTED_IDS = ("cf-2019-07-02","github-2018-10-21","cf-2020-07-17")
ALLOWED_URLS = (
    "https://blog.cloudflare.com/cloudflare-outage/",
    "https://github.blog/news-insights/company-news/oct21-post-incident-analysis/",
    "https://blog.cloudflare.com/cloudflare-outage-on-july-17-2020/",
)

def data():
    source = FROZEN.read_bytes()
    actual = hashlib.sha256(source).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError("Frozen corpus hash mismatch; public export refused")
    cases = [json.loads(line) for line in source.decode("utf-8").splitlines()]
    if len(cases) != 3 or tuple(case.get("case_id") for case in cases) != EXPECTED_IDS:
        raise ValueError("Case identities/order changed; public export refused")
    for case, url in zip(cases, ALLOWED_URLS):
        if case.get("url") != url or any(not isinstance(case.get(key), str) for key in ALLOWED_FIELDS):
            raise ValueError("Case source or required field changed; public export refused")
    return [{key: case[key] for key in ALLOWED_FIELDS} for case in cases]

def generate():
    cases=data()
    js_payload = json.dumps(cases, ensure_ascii=False, separators=(",",":")).replace("<","\\u003c")
    contents = "/* Three public historical paraphrases; not evaluation secrets. */\n"+"globalThis.FAILURE_ATLAS_CASES = "+js_payload+";\n"
    target = ROOT/"public-cases.js"
    pending = target.with_name(target.name+".new")
    with open(pending,"x",encoding="utf-8") as output:
        output.write(contents)
    os.replace(pending,target)
    manifest = {
        "schema":"failure-atlas-showcase-provenance/1",
        "origin":"Failure Atlas v0.2 corrected public case paraphrases",
        "source_path":str(FROZEN),
        "source_git_checkpoint":CHECKPOINT,
        "source_sha256":EXPECTED_SHA256,
        "output_sha256":hashlib.sha256(contents.encode("utf-8")).hexdigest(),
        "selected_public_fields":list(ALLOWED_FIELDS),
        "case_count":len(cases),
        "public_question_text_exported":False,
        "answer_keys_exported":False,
        "real_model_inference_performed":False,
    }
    (ROOT/"PROVENANCE.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("PUBLIC_EXPORT_OK case_count=3 sha256="+manifest["output_sha256"])

if __name__ == "__main__":
    try:
        generate()
    except (ValueError, OSError) as error:
        print("STOP:",error,file=sys.stderr)
        sys.exit(1)
