#!/usr/bin/env python3
"""Evals for resolve-spec-paths.py — the living-spec path resolver.

Run: python3 lib/scripts/test_resolve_spec_paths.py
Covers: centralized vs colocated resolution, missing specPath, pattern/include/
exclude membership, most-specific ordering, union discovery, orphan detection
(and that .arch/.coverage siblings are not orphans), and tier paths.
"""
import json
import os
import tempfile
import unittest

import importlib.util

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "rsp", os.path.join(_here, "resolve-spec-paths.py"))
rsp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rsp)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def write(self, rel, content=""):
        p = os.path.join(self.tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(content)
        return p

    def cfg(self, domains, **extra):
        data = {"domains": domains}
        data.update(extra)
        self.write(".sdd.json", json.dumps(data))
        return rsp.load_config(self.tmp)


class TestResolution(Base):
    def test_centralized_default(self):
        cfg = self.cfg({"auth": {"pattern": "^src/auth/"}})
        dom = cfg["domains"]["auth"]
        self.assertEqual(rsp.resolve_spec_path("auth", dom, cfg), ".specs/auth/spec.md")

    def test_colocated_uses_specpath(self):
        cfg = self.cfg({"ui": {"pattern": r"\.tsx$", "location": "colocated",
                               "specPath": "src/ui/ui.spec.md"}})
        dom = cfg["domains"]["ui"]
        self.assertEqual(rsp.resolve_spec_path("ui", dom, cfg), "src/ui/ui.spec.md")

    def test_colocated_missing_specpath_raises(self):
        cfg = self.cfg({"ui": {"pattern": r"\.tsx$", "location": "colocated"}})
        with self.assertRaises(ValueError):
            rsp.resolve_spec_path("ui", cfg["domains"]["ui"], cfg)

    def test_custom_specdir(self):
        cfg = self.cfg({"auth": {"pattern": "^src/auth/"}}, specDir="docs/specs")
        self.assertEqual(
            rsp.resolve_spec_path("auth", cfg["domains"]["auth"], cfg),
            "docs/specs/auth/spec.md")


class TestMembership(Base):
    def test_pattern(self):
        self.assertTrue(rsp.matches({"pattern": "^src/auth/"}, "src/auth/login.ts"))
        self.assertFalse(rsp.matches({"pattern": "^src/auth/"}, "src/ui/x.ts"))

    def test_include_glob(self):
        dom = {"pattern": "^src/checkout/", "include": ["src/services/cart-*.ts"]}
        self.assertTrue(rsp.matches(dom, "src/services/cart-service.ts"))

    def test_exclude_wins(self):
        dom = {"pattern": "^src/checkout/", "exclude": ["**/*.test.*"]}
        self.assertTrue(rsp.matches(dom, "src/checkout/cart.ts"))
        self.assertFalse(rsp.matches(dom, "src/checkout/cart.test.ts"))

    def test_union_pattern_or_include(self):
        dom = {"include": ["src/legacy/order*.js"]}  # no pattern
        self.assertTrue(rsp.matches(dom, "src/legacy/orderUtils.js"))
        self.assertFalse(rsp.matches(dom, "src/legacy/cart.js"))


class TestOrdering(Base):
    def test_most_specific_first(self):
        cfg = self.cfg({
            "checkout": {"pattern": "^src/checkout/"},
            "checkout-cart": {"pattern": "^src/checkout/cart/"},
        })
        out = rsp.match_changed(["src/checkout/cart/item.ts"], cfg, self.tmp)
        self.assertEqual([e["domain"] for e in out], ["checkout-cart", "checkout"])
        self.assertGreater(out[0]["specificity"], out[1]["specificity"])

    def test_colocated_scope_depth(self):
        cfg = self.cfg({
            "checkout": {"location": "colocated", "specPath": "src/checkout/checkout.spec.md",
                         "pattern": "^src/checkout/"},
            "cart": {"location": "colocated", "specPath": "src/checkout/cart/cart.spec.md",
                     "pattern": "^src/checkout/cart/"},
        })
        out = rsp.match_changed(["src/checkout/cart/x.ts"], cfg, self.tmp)
        self.assertEqual(out[0]["domain"], "cart")


class TestFallback(Base):
    def test_parent_basename_fallback_zero_config(self):
        # no `domains` configured, but .specs/<dir>/spec.md exists
        self.write(".specs/specify/spec.md", "# specify")
        self.write(".sdd.json", json.dumps({}))
        cfg = rsp.load_config(self.tmp)
        out = rsp.match_changed(["skills/specify/SKILL.md"], cfg, self.tmp)
        self.assertEqual([e["domain"] for e in out], ["specify"])

    def test_no_fallback_when_no_living_spec(self):
        self.write(".sdd.json", json.dumps({}))
        cfg = rsp.load_config(self.tmp)
        out = rsp.match_changed(["skills/drift/SKILL.md"], cfg, self.tmp)
        self.assertEqual(out, [])


class TestDiscovery(Base):
    def test_union_config_and_glob(self):
        self.write(".specs/billing/spec.md", "# billing")
        cfg = self.cfg({"auth": {"pattern": "^src/auth/"}})
        names = {e["domain"] for e in rsp.discover_all(cfg, self.tmp)}
        self.assertEqual(names, {"auth", "billing"})

    def test_no_double_count(self):
        self.write(".specs/auth/spec.md", "# auth")
        cfg = self.cfg({"auth": {"pattern": "^src/auth/"}})  # centralized -> .specs/auth/spec.md
        out = rsp.discover_all(cfg, self.tmp)
        self.assertEqual([e["domain"] for e in out].count("auth"), 1)


class TestOrphans(Base):
    def test_orphan_flagged(self):
        self.write("src/legacy/legacy.spec.md", "# stray")
        cfg = self.cfg({"auth": {"pattern": "^src/auth/"}})
        self.assertIn("src/legacy/legacy.spec.md", rsp.find_orphans(cfg, self.tmp))

    def test_configured_colocated_not_orphan(self):
        self.write("src/ui/ui.spec.md", "# ui")
        cfg = self.cfg({"ui": {"pattern": r"\.tsx$", "location": "colocated",
                               "specPath": "src/ui/ui.spec.md"}})
        self.assertEqual(rsp.find_orphans(cfg, self.tmp), [])

    def test_arch_and_coverage_not_orphans(self):
        self.write("src/ui/ui.spec.md", "# ui")
        self.write("src/ui/ui.arch.md", "# arch")
        self.write("src/ui/ui.coverage.md", "# cov")
        cfg = self.cfg({"ui": {"location": "colocated", "specPath": "src/ui/ui.spec.md",
                               "pattern": r"\.tsx$"}})
        # only *.spec.md is scanned; .arch/.coverage are never candidates
        self.assertEqual(rsp.find_orphans(cfg, self.tmp), [])

    def test_specexempt_silences(self):
        self.write("vendor/thing.spec.md", "# vendor")
        cfg = self.cfg({"auth": {"pattern": "^src/auth/"}}, specExempt=["vendor/**"])
        self.assertEqual(rsp.find_orphans(cfg, self.tmp), [])


class TestTiers(Base):
    def test_colocated_tiers(self):
        t = rsp.tier_paths("src/ui/ui.spec.md")
        self.assertEqual(t["arch"], "src/ui/ui.arch.md")
        self.assertEqual(t["coverage"], "src/ui/ui.coverage.md")

    def test_centralized_tiers(self):
        t = rsp.tier_paths(".specs/auth/spec.md")
        self.assertEqual(t["arch"], ".specs/auth/arch.md")
        self.assertEqual(t["coverage"], ".specs/auth/coverage.md")


if __name__ == "__main__":
    unittest.main(verbosity=2)
