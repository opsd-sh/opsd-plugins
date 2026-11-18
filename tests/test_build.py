import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("packager", ROOT / "scripts/build.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.output = self.directory / "output"
        self.source = self.directory / "source"
        # Use a clean fixture so local caches and excluded files cannot change
        # the expected package contents or require writes to the real checkout.
        for name in (
            "production.json", "providers/openai/plugin.json",
            "providers/openai/mcp.json", "skills/businesses/SKILL.md",
            "skills/members/SKILL.md", "skills/billing/SKILL.md",
            "skills/payroll-setup/SKILL.md",
            "skills/employees/SKILL.md",
            "skills/payroll/SKILL.md", "skills/tax-year-rollovers/SKILL.md",
            "assets/icon.svg",
        ):
            destination = self.source / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)
        root_patch = patch.object(packager, "ROOT", self.source)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def test_production_archive_is_self_contained(self):
        packager.build(self.source / "production.json", self.output)
        with ZipFile(self.output / "opsd.zip") as archive:
            expected = {".codex-plugin/plugin.json", ".mcp.json"}
            for directory in ("skills", "assets"):
                expected.update(
                    str(path.relative_to(self.source))
                    for path in (self.source / directory).rglob("*") if path.is_file()
                )
            self.assertEqual(set(archive.namelist()), expected)
            for name in expected - {".codex-plugin/plugin.json", ".mcp.json"}:
                self.assertEqual(archive.read(name), (self.source / name).read_bytes())
            mcp = json.loads(archive.read(".mcp.json"))
            self.assertEqual(mcp["mcpServers"]["opsd"]["url"], "https://api.opsd.sh/mcp")
            self.assertEqual(
                mcp["mcpServers"]["opsd"]["scopes"],
                ["api:read", "api:write", "hmrc:submit"],
            )
            manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["name"], "opsd")
            for name in archive.namelist():
                self.assertNotIn(b"api.dev.opsd.sh", archive.read(name))

    def test_environment_changes_identity_without_changing_shared_files(self):
        template_path = self.source / "providers/openai/plugin.json"
        template = packager.read_json(template_path)
        template["interface"]["defaultPrompt"] = ["Show my latest payroll run in {title}."]
        packager.write_json(template_path, template)
        config = packager.read_json(self.source / "production.json")
        config.update(
            name="opsd-test", title="Opsd Test", mcp_url="https://test.example.com/mcp",
            marketplace_name="opsd-test", marketplace_title="Opsd Test Plugins",
        )
        config_path = self.directory / "test.json"
        packager.write_json(config_path, config)
        packager.build(config_path, self.output)
        plugin = self.output / "plugins/opsd-test"
        manifest = packager.read_json(plugin / ".codex-plugin/plugin.json")
        self.assertEqual(manifest["interface"]["displayName"], "Opsd Test")
        self.assertEqual(manifest["interface"]["defaultPrompt"], ["Show my latest payroll run in Opsd Test."])
        mcp = packager.read_json(plugin / ".mcp.json")
        self.assertEqual(set(mcp["mcpServers"]), {"opsd-test"})
        self.assertEqual(mcp["mcpServers"]["opsd-test"]["url"], config["mcp_url"])
        self.assertEqual(
            mcp["mcpServers"]["opsd-test"]["scopes"],
            ["api:read", "api:write", "hmrc:submit"],
        )
        with ZipFile(self.output / "opsd-test.zip") as archive:
            self.assertEqual(json.loads(archive.read(".mcp.json")), mcp)

        production_output = self.directory / "production"
        packager.build(self.source / "production.json", production_output)
        production_manifest = packager.read_json(production_output / "plugins/opsd/.codex-plugin/plugin.json")
        self.assertEqual(production_manifest["interface"]["defaultPrompt"], ["Show my latest payroll run in Opsd."])
        production_mcp = packager.read_json(
            production_output / "plugins/opsd/.mcp.json"
        )
        combined = {**production_mcp["mcpServers"], **mcp["mcpServers"]}
        self.assertEqual(
            {name: server["url"] for name, server in combined.items()},
            {
                "opsd": "https://api.opsd.sh/mcp",
                "opsd-test": "https://test.example.com/mcp",
            },
        )
        for directory in ("skills", "assets"):
            for source in (self.source / directory).rglob("*"):
                if source.is_file():
                    self.assertEqual(source.read_bytes(), (plugin / source.relative_to(self.source)).read_bytes())
        marketplace = packager.read_json(self.output / ".agents/plugins/marketplace.json")
        self.assertEqual(marketplace["name"], "opsd-test")
        self.assertEqual((self.output / marketplace["plugins"][0]["source"]["path"]).resolve(), plugin)

    def test_rebuild_removes_stale_generated_files(self):
        packager.build(self.source / "production.json", self.output)
        stale = self.output / "plugins/opsd/skills/removed.md"
        stale.write_text("Removed skill")
        packager.build(self.source / "production.json", self.output)
        self.assertFalse(stale.exists())
        with ZipFile(self.output / "opsd.zip") as archive:
            self.assertNotIn("skills/removed.md", archive.namelist())

    def test_refuses_unrelated_output_directory_and_symlink(self):
        self.output.mkdir()
        sentinel = self.output / "keep.txt"
        sentinel.write_text("User file")
        with self.assertRaises(ValueError):
            packager.build(self.source / "production.json", self.output)
        alias = self.directory / "alias"
        alias.symlink_to(self.output, target_is_directory=True)
        with self.assertRaises(ValueError):
            packager.build(self.source / "production.json", alias)
        self.assertEqual(sentinel.read_text(), "User file")

    def test_rejects_invalid_environment_before_replacing_output(self):
        packager.build(self.source / "production.json", self.output)
        archive = self.output / "opsd.zip"
        original = archive.read_bytes()
        for field, value in [
            ("name", "../../outside"), ("mcp_url", "http://example.com/mcp"),
            ("mcp_url", "https://token@example.com/mcp"), ("title", ""),
        ]:
            with self.subTest(field=field, value=value):
                config = packager.read_json(self.source / "production.json")
                config[field] = value
                config_path = self.directory / "invalid.json"
                packager.write_json(config_path, config)
                with self.assertRaises(ValueError):
                    packager.build(config_path, self.output)
                self.assertEqual(archive.read_bytes(), original)

    def test_refuses_output_inside_shared_content(self):
        for directory in ("skills", "assets"):
            with self.subTest(directory=directory), self.assertRaises(ValueError):
                packager.build(self.source / "production.json", self.source / directory / "build-output")

    def test_excludes_local_files_from_directory_and_archive(self):
        excluded = [
            "skills/businesses/.env",
            "skills/businesses/references/.env.development",
            "skills/businesses/scripts/__pycache__/helper.cpython-312.pyc",
            "skills/businesses/scripts/helper.pyc",
            "skills/businesses/scripts/helper.pyo",
            "skills/businesses/.pytest_cache/state",
            "skills/businesses/.venv/bin/python",
            "assets/.DS_Store",
            "assets/.git/config",
            "assets/.vscode/settings.json",
            "skills/businesses/SKILL.md~",
            "skills/businesses/.SKILL.md.swp",
            "skills/businesses/.#SKILL.md",
            "skills/businesses/#SKILL.md#",
        ]
        for name in excluded:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Synthetic local-only fixture")
        included = {
            "skills/businesses/scripts/helper.py": "print('Example helper')\n",
            "skills/businesses/references/guide.md": "Example reference\n",
        }
        for name, content in included.items():
            (self.source / name).write_text(content)
        script = "skills/businesses/scripts/helper.py"
        (self.source / script).chmod(0o755)

        packager.build(self.source / "production.json", self.output)
        plugin = self.output / "plugins/opsd"
        with ZipFile(self.output / "opsd.zip") as archive:
            for name in excluded:
                self.assertFalse((plugin / name).exists(), name)
                self.assertNotIn(name, archive.namelist())
            for name, content in included.items():
                self.assertEqual((plugin / name).read_text(), content)
                self.assertEqual(archive.read(name), content.encode())
            self.assertTrue(archive.getinfo(script).external_attr >> 16 & 0o100)
        self.assertTrue((plugin / script).stat().st_mode & 0o100)

    def test_materializes_internal_file_and_directory_links(self):
        skill = self.source / "skills/businesses"
        (skill / "icon.svg").symlink_to("../../assets/icon.svg")
        (skill / "shared-assets").symlink_to("../../assets", target_is_directory=True)
        packager.build(self.source / "production.json", self.output)
        icon = (self.source / "assets/icon.svg").read_bytes()
        with ZipFile(self.output / "opsd.zip") as archive:
            for name in ("skills/businesses/icon.svg", "skills/businesses/shared-assets/icon.svg"):
                path = self.output / "plugins/opsd" / name
                self.assertFalse(path.is_symlink())
                self.assertEqual(path.read_bytes(), icon)
                self.assertEqual(archive.read(name), icon)

    def test_links_cannot_bypass_content_exclusions(self):
        skill = self.source / "skills/businesses"
        (skill / ".env.local").write_text("Synthetic local-only fixture")
        cache = skill / "__pycache__"
        cache.mkdir()
        (cache / "data.txt").write_text("Synthetic cache fixture")
        (skill / "alias.txt").symlink_to(".env.local")
        (skill / "alias-directory").symlink_to("__pycache__", target_is_directory=True)
        (skill / "alias-file.txt").symlink_to("__pycache__/data.txt")
        packager.build(self.source / "production.json", self.output)
        with ZipFile(self.output / "opsd.zip") as archive:
            for name in ("alias.txt", "alias-directory", "alias-file.txt"):
                path = f"skills/businesses/{name}"
                self.assertFalse((self.output / "plugins/opsd" / path).exists())
                self.assertFalse(any(entry.startswith(path) for entry in archive.namelist()))

    def test_external_links_fail_without_replacing_previous_package(self):
        packager.build(self.source / "production.json", self.output)
        original = (self.output / "opsd.zip").read_bytes()
        outside_file = self.directory / "outside.txt"
        outside_file.write_text("Synthetic external fixture")
        outside_directory = self.directory / "outside"
        outside_directory.mkdir()
        (outside_directory / "data.txt").write_text("Synthetic external fixture")
        repository_file = self.source / "private.txt"
        repository_file.write_text("Synthetic non-package fixture")
        for directory in ("skills/businesses", "assets"):
            for target in (outside_file, outside_directory, repository_file):
                with self.subTest(directory=directory, target=target.name):
                    link = self.source / directory / "external"
                    link.symlink_to(target, target_is_directory=target.is_dir())
                    try:
                        with self.assertRaisesRegex(ValueError, "outside skills/ and assets/"):
                            packager.build(self.source / "production.json", self.output)
                    finally:
                        link.unlink()
                    self.assertEqual((self.output / "opsd.zip").read_bytes(), original)

    def test_rejects_symlinked_content_root_outside_allowed_directories(self):
        assets = self.source / "assets"
        moved = self.directory / "external-assets"
        assets.rename(moved)
        assets.symlink_to(moved, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "outside skills/ and assets/"):
            packager.build(self.source / "production.json", self.output)
        self.assertFalse(self.output.exists())

    def test_broken_links_and_cycles_preserve_previous_package(self):
        packager.build(self.source / "production.json", self.output)
        original = (self.output / "opsd.zip").read_bytes()
        skill = self.source / "skills/businesses"
        for name, target in (
            ("broken", "missing.txt"),
            ("directory-cycle", "."),
            ("self-cycle", "self-cycle"),
        ):
            with self.subTest(name=name):
                link = skill / name
                link.symlink_to(target)
                try:
                    with self.assertRaises(ValueError):
                        packager.build(self.source / "production.json", self.output)
                finally:
                    link.unlink()
                self.assertEqual((self.output / "opsd.zip").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
