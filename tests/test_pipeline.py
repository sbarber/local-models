"""Offline regression tests for ranking, score detection and report integrity."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import aa  # noqa: E402
import change_detection  # noqa: E402
import ranking  # noqa: E402
import report  # noqa: E402


class RankingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fleet, cls.candidates = ranking.load_data()

    def test_every_machine_has_one_existing_tier(self):
        used = set()
        for machine in self.fleet["machines"]:
            for memory in machine["memory_gb"]:
                tier = machine["tiers"][memory]
                self.assertIn(tier, self.fleet["tiers"])
                entry = (machine["name"], memory)
                self.assertNotIn(entry, used)
                used.add(entry)
        for tier in self.fleet["tiers"]:
            self.assertTrue(ranking.machines_for_tier(self.fleet, tier))

    def test_registry_snapshot_has_explicit_tags(self):
        for model in self.candidates:
            self.assertTrue(model["tags"])
            for tag, info in model["tags"].items():
                self.assertIn(":", tag)
                self.assertGreater(info["size_gb"], 0)
                self.assertIn(info["format"], ("gguf", "mlx"))

    def test_near_tie_prefers_mlx_but_faster_build_determines_rank(self):
        m = {"name": "sample", "total": 4, "active": None, "gs": 25.0, "tb": 30.0,
             "score_source": "AA", "tag_tb": {}, "flag": False,
             "tags": {"sample:gguf": {"format": "gguf", "size_gb": 4, "kv64k_gb": 0},
                      "sample:nvfp4": {"format": "mlx", "size_gb": 4.3, "kv64k_gb": 0}}}
        machine = ({"bandwidth_gbs": 200}, 16)
        chosen, fastest = ranking.choose_tag(m, "Mac 16 GB", [machine], "general")
        self.assertEqual(chosen[0], "sample:nvfp4")
        self.assertEqual(fastest, 30)

    def test_keep_gguf_if_mlx_loses_usable_speed(self):
        model = {"name": "sample", "total": 4, "active": None, "gs": 25.0, "tb": 30.0,
                 "score_source": "AA", "tag_tb": {}, "flag": False,
                 "tags": {"sample:gguf": {"format": "gguf", "size_gb": 4, "kv64k_gb": 0},
                          "sample:nvfp4": {"format": "mlx", "size_gb": 4.3, "kv64k_gb": 0}}}
        chosen, _ = ranking.choose_tag(model, "Mac 16 GB", [({"bandwidth_gbs": 100}, 16)], "general")
        self.assertEqual(chosen[0], "sample:gguf")

    def test_vendor_score_is_specific_to_tag(self):
        model = {"name": "sample", "total": 4, "active": None, "gs": 25.0, "tb": 67.0,
                 "score_source": "vendor", "tag_tb": {"sample:nvfp4": 60.0}, "flag": False,
                 "tags": {"sample:gguf": {"format": "gguf", "size_gb": 4.2, "kv64k_gb": 0},
                          "sample:nvfp4": {"format": "mlx", "size_gb": 4.0, "kv64k_gb": 0}}}
        chosen, _ = ranking.choose_tag(model, "Mac 16 GB", [({"bandwidth_gbs": 200}, 16)], "coding")
        self.assertEqual(chosen[0], "sample:gguf")

    def test_tool_call_flag_follows_chosen_tag(self):
        machines = [{"name": "mac", "memory_gb": [16], "bandwidth_gbs": 200, "tiers": {16: "Mac 16 GB"}}]
        fleet = {"tiers": {"Mac 16 GB": {}}, "machines": machines}
        model = {"name": "sample", "total": 4, "active": None, "gs": 25.0, "tb": 30.0,
                 "score_source": "AA", "tag_tb": {}, "flag": False,
                 "tag_flag": {"sample:nvfp4": True},
                 "tags": {"sample:gguf": {"format": "gguf", "size_gb": 4, "kv64k_gb": 0},
                          "sample:nvfp4": {"format": "mlx", "size_gb": 4.3, "kv64k_gb": 0}}}
        row = ranking.rank(fleet, [model], "Mac 16 GB", "coding")[0]
        self.assertEqual((row["tag"], row["flag"]), ("sample:nvfp4", True))
        model["tags"]["sample:nvfp4"]["size_gb"] = 6
        row = ranking.rank(fleet, [model], "Mac 16 GB", "coding")[0]
        self.assertEqual((row["tag"], row["flag"]), ("sample:gguf", False))

    def test_coding_floor_and_fast_fallback(self):
        machines = [{"name": "low", "memory_gb": [16], "bandwidth_gbs": 100,
                     "tiers": {16: "Mac 16 GB"}}]
        fleet = {"tiers": {"Mac 16 GB": {}}, "machines": machines}
        models = []
        for i in range(6):
            models.append({"name": str(i), "total": 4, "active": None, "gs": 30 - i,
                           "tb": 30 - i, "score_source": "AA", "tag_tb": {}, "flag": False,
                           "tags": {f"sample:{i}": {"format": "gguf", "size_gb": 5 if i < 5 else 3, "kv64k_gb": 0}}})
        self.assertEqual(ranking.rank(fleet, models, "Mac 16 GB", "coding")[-1]["tag"], "sample:5")
        models[5]["tb"] = 19
        self.assertTrue(all(row["tag"] != "sample:5" for row in ranking.rank(fleet, models, "Mac 16 GB", "coding")))


class ContextTests(unittest.TestCase):
    MODEL = {"name": "dense", "total": 4, "active": None, "gs": 20.0, "tb": 30.0,
             "score_source": "AA", "tag_tb": {}, "flag": False,
             "tags": {"dense:q4": {"format": "gguf", "size_gb": 2.5, "kv64k_gb": 9.66}}}

    def fleet(self, memory):
        machines = [{"name": "mac", "memory_gb": [memory], "bandwidth_gbs": 400,
                     "tiers": {memory: "Mac test"}}]
        return {"tiers": {"Mac test": {}}, "machines": machines}

    def test_coding_counts_64k_context_with_raised_mac_limit(self):
        # 2.5 GB weights fit 60% of 8 GB, but weights + 64k context (12.2 GB) don't fit 80%.
        fleet = self.fleet(8)
        self.assertTrue(ranking.rank(fleet, [self.MODEL], "Mac test", "general"))
        self.assertFalse(ranking.rank(fleet, [self.MODEL], "Mac test", "coding"))
        self.assertTrue(ranking.rank(self.fleet(16), [self.MODEL], "Mac test", "coding"))

    def test_general_reports_largest_context_that_fits(self):
        row = ranking.rank(self.fleet(8), [self.MODEL], "Mac test", "general")[0]
        self.assertEqual(row["max_context"], 16384)

    def test_general_needs_room_for_default_context(self):
        model = {**self.MODEL, "tags": {"dense:q4": {"format": "gguf", "size_gb": 4.8, "kv64k_gb": 60}}}
        self.assertFalse(ranking.rank(self.fleet(8), [model], "Mac test", "general"))

    def test_vram_speed_requires_context_in_vram_for_coding(self):
        machine = {"gpu_vram_gb": 24, "gpu_bandwidth_gbs": 896, "bandwidth_gbs": 100}
        tag = {"kv64k_gb": 8}
        self.assertEqual(ranking.bandwidth(machine, 17, tag, "general"), 896)
        self.assertEqual(ranking.bandwidth(machine, 17, tag, "coding"), 100)


class FactCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import verify_facts
        cls.vf = verify_facts
        cls.source = (ROOT / "report.md").read_text()
        cls.models = json.loads((ROOT / "tests/fixtures/aa_models.json").read_text())

    def test_reads_every_table_row(self):
        rows = self.vf.table_rows(self.source)
        state = self.source.split("[picks]\n", 1)[1].split("\nEND STATE", 1)[0].splitlines()
        self.assertEqual(len(rows), len(state))

    def test_sizes_from_tags_page(self):
        self.assertEqual(self.vf.size_gb("17GB"), 17)
        self.assertAlmostEqual(self.vf.size_gb("366MB"), 0.366)

    def test_wrong_equivalent_is_reported(self):
        paid = [{"name": "Paid A", "isOpenWeights": False, "modelCreatorName": "OpenAI",
                 "hle": .2, "critpt": .1, "omniscienceAccuracy": .2, "omniscience": 0, "lcr": .3},
                {"name": "Paid B", "isOpenWeights": False, "modelCreatorName": "OpenAI",
                 "hle": .9, "critpt": .9, "omniscienceAccuracy": .9, "omniscience": 80, "lcr": .9}]
        score = aa.row(paid[0])["gs"]
        self.assertEqual(self.vf.check_equivalents([("x:y", "GS", score, "Paid A, low confidence")], paid), [])
        self.assertTrue(self.vf.check_equivalents([("x:y", "GS", score, "Paid B")], paid))

    def test_closed_issue_must_be_described_as_closed(self):
        line = "- watch [\\#1](https://github.com/ollama/ollama/issues/1) on Macs\n"
        self.assertTrue(self.vf.issue_line_problems(line, {"1": "closed"}))
        fixed = "- [\\#1](https://github.com/ollama/ollama/issues/1) was fixed in 0.40.4\n"
        self.assertEqual(self.vf.issue_line_problems(fixed, {"1": "closed"}), [])
        watched = "<!-- STATE\nopen_watched_issues: 2\nEND STATE -->"
        self.assertTrue(self.vf.issue_line_problems(watched, {"2": "closed"}))


class ReportTests(unittest.TestCase):
    def test_existing_source_matches_html_and_state_picks(self):
        source = (ROOT / "report.md").read_text()
        self.assertEqual(report.validate(source), source)
        self.assertEqual(report.render(source), (ROOT / "local-models-report.html").read_text())
        state_picks = source.split("[picks]\n", 1)[1].split("\nEND STATE", 1)[0].splitlines()
        self.assertEqual(sum(len(use) for tier in report.tables(source).values() for use in tier.values()), len(state_picks))

    def test_rank_error_is_caught(self):
        source = (ROOT / "report.md").read_text()
        tampered = source.replace("| 1 | `granite4.2:3b-q4_K_M`", "| 1 | `not-a-real-tag`", 1)
        with self.assertRaisesRegex(ValueError, "table differs from ranking"):
            report.validate(tampered)

    def test_broken_citation_is_caught(self):
        source = (ROOT / "report.md").read_text()
        with self.assertRaisesRegex(ValueError, "Broken citation"):
            report.validate(source.replace("(#ref-1)", "(#ref-999)", 1))


class ChangeDetectionTests(unittest.TestCase):
    def test_score_change_even_if_index_version_is_unchanged(self):
        candidates = json.loads((ROOT / "candidates.json").read_text())["models"]
        models = json.loads((ROOT / "tests/fixtures/aa_models.json").read_text())
        self.assertEqual(change_detection.score_changes(models, candidates), [])
        model = next(m for m in models if m["name"] == "Granite 4.2 3B")
        model["hle"] = (model["hle"] or 0) + 0.05
        self.assertTrue(any("Granite 4.2 3B gs" in c for c in change_detection.score_changes(models, candidates)))

    def test_library_update_without_tools_badge(self):
        models = [{"name": "no-badge", "capabilities": ["thinking"],
                   "updated": "Oct 16, 2026 2:00 PM UTC"},
                  {"name": "also-local", "capabilities": ["cloud", "tools"],
                   "updated": "Oct 16, 2026 2:00 PM UTC"}]
        self.assertEqual(change_detection.updated_models(models, "2026-10-15"), ["no-badge", "also-local"])

    def test_hash_ignores_file_timestamp_but_detects_same_day_edit(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "fleet"
            p.write_text("old")
            before = change_detection.content_hash(p)
            self.assertEqual(before, change_detection.content_hash(p))
            p.write_text("new")
            self.assertNotEqual(before, change_detection.content_hash(p))

    def test_zero_score_prints_as_zero(self):
        entry = {"name": "Zero", "gs": 0.0, "ii": 0, "ii_est": False, "tb21": 0.0,
                 "tbh": 0.0, "gpqa": 0.0, "price": (None, None), "deprecated": False}
        self.assertIn("TB2.1=  0.0", aa.fmt(entry))
        self.assertIn("GS=  0.0", aa.fmt(entry))


if __name__ == "__main__":
    unittest.main()
