#!/usr/bin/env python3
"""Public safety and documentation checks. No network and no model calls."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
PREFIX="globalThis.FAILURE_ATLAS_CASES = "
FIELDS={"case_id","symptoms","cause","resolution","url","resolution_status"}

class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.assets=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag=="script" and "src" in a: self.assets.append(a["src"])
        if tag=="link" and a.get("rel")=="stylesheet": self.assets.append(a.get("href"))

class ShowcaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text=(ROOT/"public-cases.js").read_text(encoding="utf-8")
        cls.js_text=text
        cls.records=json.loads(text.split(PREFIX,1)[1].strip().removesuffix(";"))
        cls.manifest=json.loads((ROOT/"PROVENANCE.json").read_text(encoding="utf-8"))
    def test_exact_public_case_schema(self):
        self.assertEqual(len(self.records),3)
        self.assertEqual([x["case_id"] for x in self.records],
                         ["cf-2019-07-02","github-2018-10-21","cf-2020-07-17"])
        for row in self.records:
            self.assertEqual(set(row),FIELDS)
            self.assertTrue(row["url"].startswith("https://"))
            self.assertTrue(row["symptoms"] and row["cause"] and row["resolution"])
        self.assertEqual(self.manifest["case_count"],3)
        self.assertFalse(self.manifest["answer_keys_exported"])
        self.assertFalse(self.manifest["public_question_text_exported"])
    def test_export_provenance_hash(self):
        self.assertEqual(hashlib.sha256(self.js_text.encode()).hexdigest(),self.manifest["output_sha256"])
        source=Path(self.manifest["source_path"])
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),self.manifest["source_sha256"])
    def test_no_private_evaluation_data_or_model_claims(self):
        combined="\n".join((ROOT/p).read_text(encoding="utf-8") for p in
                           ["index.html","app.js","style.css","public-cases.js"])
        for phrase in ["FA02-001","expected_diagnosis","evaluation/private/","secret_token",
                       "private/schedule.json","scoring_rubric.json","answer_keys.jsonl",
                       "api_key","source_evidence_private"]:
            self.assertNotIn(phrase,combined)
        self.assertIn("0", (ROOT/"index.html").read_text())
        self.assertIn("not executed",combined.lower())
        self.assertIn("No AI model involved",combined)
    def test_portable_site_assets(self):
        doc=HTMLLinks()
        doc.feed((ROOT/"index.html").read_text(encoding="utf-8"))
        self.assertTrue({"top","query","case-grid","search-form","match-results","evidence"}.issubset(doc.ids))
        self.assertEqual(set(doc.assets),{"./style.css","./app.js","./public-cases.js"})
        self.assertTrue(all((ROOT/name.removeprefix("./")).is_file() for name in doc.assets))
    def test_javascript_has_no_network_calls(self):
        js=(ROOT/"app.js").read_text()
        for needle in ("fetch(","XMLHttpRequest","WebSocket(","eval("):
            self.assertNotIn(needle,js)
        self.assertIn("Matching terms:",js)
        self.assertIn("not proof",js.lower())

if __name__=="__main__":
    unittest.main()
