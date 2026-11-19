#!/usr/bin/env python3
"""Build a self-contained OpenAI plugin and local marketplace."""

import argparse
from fnmatch import fnmatchcase
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = Path("plugins/opsd")
MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
MARKER = ".opsd-plugin-build"
CONTENT_DIRECTORIES = ("skills", "assets")
EXCLUDED_PATTERNS = (
    ".env", ".env.*", ".git", "__pycache__", "*.pyc", "*.pyo",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv",
    ".DS_Store", ".idea", ".vscode", "*.swp", "*.swo", "*~", ".#*", "#*#",
)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def is_excluded(name):
    return any(fnmatchcase(name, pattern) for pattern in EXCLUDED_PATTERNS)


def copy_content(source, destination, parents=()):
    """Copy shared content, excluding local files and links outside its directories."""
    if is_excluded(source.name):
        return
    try:
        resolved = source.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ValueError(f"Cannot resolve package content: {source}") from error
    plugin_root = ROOT / PLUGIN_PATH
    relative = next((
        resolved.relative_to(plugin_root / directory)
        for directory in CONTENT_DIRECTORIES
        if resolved.is_relative_to(plugin_root / directory)
    ), None)
    if relative is None:
        raise ValueError(f"Package content resolves outside skills/ and assets/: {source}")
    # An alias must not bypass exclusions on the resolved file or its parents.
    if any(is_excluded(part) for part in relative.parts):
        return
    if resolved.is_dir():
        if resolved in parents:
            raise ValueError(f"Directory cycle in package content: {source}")
        destination.mkdir(parents=True)
        for child in sorted(resolved.iterdir()):
            copy_content(child, destination / child.name, (*parents, resolved))
    elif resolved.is_file():
        shutil.copy2(resolved, destination)
    else:
        raise ValueError(f"Package content is not a regular file or directory: {source}")


def build(config_path, output):
    config = read_json(config_path)
    fields = {"name", "title", "mcp_url", "marketplace_name", "marketplace_title"}
    if not isinstance(config, dict) or set(config) != fields or any(
        not isinstance(value, str) or not value.strip() for value in config.values()
    ):
        raise ValueError(f"Environment configuration must contain: {', '.join(sorted(fields))}")
    for field in ("name", "marketplace_name"):
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", config[field]):
            raise ValueError(f"{field} must be a lowercase, hyphen-separated name")
    url = urlsplit(config["mcp_url"])
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        raise ValueError("mcp_url must be an HTTPS URL without credentials")
    if url.query or url.fragment:
        raise ValueError("mcp_url must not contain a query or fragment")

    # Rebuild only generated output; never replace a source directory or symlink.
    if output.is_symlink():
        raise ValueError("Output must not be a symlink")
    output = output.resolve()
    for source in (ROOT, config_path.resolve()):
        if output == source or output in source.parents:
            raise ValueError("Output must not contain source files")
    for directory in ("plugins", ".agents", "scripts", "tests"):
        if ROOT / directory == output or ROOT / directory in output.parents:
            raise ValueError("Output must not be inside a source directory")
    if output.exists() and not (output / MARKER).is_file():
        raise ValueError(f"Refusing to replace a directory without {MARKER}: {output}")

    plugin_root = ROOT / PLUGIN_PATH
    manifest = read_json(plugin_root / ".codex-plugin/plugin.json")
    production_title = manifest["interface"]["displayName"]
    manifest["name"] = config["name"]
    manifest["interface"]["displayName"] = config["title"]
    manifest["interface"]["defaultPrompt"] = [
        prompt.replace(production_title, config["title"])
        for prompt in manifest["interface"]["defaultPrompt"]
    ]
    mcp = read_json(plugin_root / ".mcp.json")
    server = mcp["mcpServers"].pop("opsd")
    server["url"] = config["mcp_url"]
    mcp["mcpServers"][config["name"]] = server
    marketplace = read_json(ROOT / MARKETPLACE_PATH)
    marketplace["name"] = config["marketplace_name"]
    marketplace["interface"]["displayName"] = config["marketplace_title"]
    entry, = marketplace["plugins"]
    entry["name"] = config["name"]
    entry["source"]["path"] = f"./plugins/{config['name']}"

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".opsd-build-", dir=output.parent) as temp:
        generated = Path(temp) / "output"
        plugin = generated / "plugins" / config["name"]
        write_json(plugin / ".codex-plugin/plugin.json", manifest)
        write_json(plugin / ".mcp.json", mcp)
        for directory in CONTENT_DIRECTORIES:
            copy_content(plugin_root / directory, plugin / directory)
        write_json(generated / MARKETPLACE_PATH, marketplace)
        with ZipFile(generated / f"{config['name']}.zip", "w", ZIP_DEFLATED) as archive:
            for path in sorted(plugin.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(plugin))
        (generated / MARKER).write_text("Generated by opsd-plugins; do not edit.\n")
        if output.exists():
            shutil.rmtree(output)
        generated.rename(output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=["openai"], default="openai")
    parser.add_argument("--config", type=Path, default=ROOT / "production.json")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/openai")
    args = parser.parse_args()
    try:
        output = build(args.config, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Build failed: {error}\n")
    print(f"Built {args.provider} plugin and marketplace in {output}")


if __name__ == "__main__":
    main()
