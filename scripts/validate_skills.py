"""Validate tracked Markdown and skill metadata; also check new skill files."""

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate metadata keys instead of silently overwriting them."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValueError("metadata keys must be unique strings")
        result[key] = loader.construct_object(value_node)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def validate_metadata(path, text):
    errors = []
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return ["missing YAML frontmatter delimiters"], text
    end = lines.index("---", 1)
    body = "\n".join(lines[end + 1 :])
    try:
        metadata = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    except (yaml.YAMLError, ValueError) as exc:
        return [f"invalid YAML frontmatter: {exc}"], body
    if not isinstance(metadata, dict):
        return ["frontmatter must be a mapping"], body
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for key in metadata.keys() - allowed:
        errors.append(f"unsupported frontmatter field: {key}")
    name = metadata.get("name")
    if not isinstance(name, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", name
    ) or len(name) > 64:
        errors.append("name must be 1–64 lowercase letters/digits with single hyphens")
    elif name != path.parent.name:
        errors.append("name must match its skill directory")
    for field, limit in (("description", 1024), ("compatibility", 500)):
        if field == "compatibility" and field not in metadata:
            continue
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            errors.append(f"{field} must be a non-empty string of at most {limit} characters")
    for field in ("license", "allowed-tools"):
        if field in metadata and not isinstance(metadata[field], str):
            errors.append(f"{field} must be a string")
    extra = metadata.get("metadata", {})
    if not isinstance(extra, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in extra.items()
    ):
        errors.append("metadata must map strings to strings")
    if not body.strip():
        errors.append("skill instructions must not be empty")
    return errors, body


def validate_links(path, text):
    errors = []
    for token in MarkdownIt().parse(text):
        for child in token.children or []:
            if child.type not in ("link_open", "image"):
                continue
            target = child.attrGet("href" if child.type == "link_open" else "src")
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            if not (path.parent / unquote(url.path)).exists():
                errors.append(f"missing local link target: {target}")
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root, check=True, capture_output=True,
    )
    paths = sorted({Path(name) for name in result.stdout.decode().split("\0") if name})
    errors = []
    count = 0
    for relative in paths:
        path = root / relative
        if path.suffix != ".md" or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
            problems = []
            if path.name == "SKILL.md":
                count += 1
                problems, text = validate_metadata(path, text)
            problems.extend(validate_links(path, text))
        except (UnicodeError, ValueError, OSError) as exc:
            problems = [str(exc)]
        errors.extend(f"{relative}: {problem}" for problem in problems)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {count} skills and local Markdown links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
