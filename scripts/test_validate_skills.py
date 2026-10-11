"""Regression checks for malformed metadata and broken local references."""

import tempfile
import unittest
from pathlib import Path

from validate_skills import validate_links, validate_metadata


class ValidationTests(unittest.TestCase):
    def metadata(self, fields, body="# Instructions"):
        return validate_metadata(
            Path("example/SKILL.md"), f"---\n{fields}\n---\n{body}"
        )[0]

    def test_valid_folded_description(self):
        self.assertEqual(self.metadata("name: example\ndescription: >-\n  Do work."), [])

    def test_duplicate_keys(self):
        self.assertTrue(self.metadata("name: example\nname: other\ndescription: Work"))

    def test_invalid_metadata(self):
        for fields in (
            "name: other\ndescription: Work",
            "name: example\ndescription: 123",
            "name: example\ndescription: Work\nmetadata: {version: 1}",
            "name: example\ndescription: Work\nunknown: value",
            "name: example\ndescription: " + "x" * 1025,
        ):
            with self.subTest(fields=fields):
                self.assertTrue(self.metadata(fields))

    def test_missing_frontmatter_and_empty_body(self):
        self.assertTrue(validate_metadata(Path("example/SKILL.md"), "# Work")[0])
        self.assertTrue(self.metadata("name: example\ndescription: Work", body=""))

    def test_links_and_images(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "existing file.md").touch()
            path = root / "SKILL.md"
            text = (
                "[valid](existing%20file.md#section)\n"
                "[web](https://example.com) [anchor](#section)\n"
                "`[code](missing.md)`\n"
                "[missing][ref] ![image](missing.png)\n\n"
                "[ref]: absent.md\n"
            )
            errors = validate_links(path, text)
            self.assertEqual(len(errors), 2)
            self.assertTrue(any("absent.md" in error for error in errors))
            self.assertTrue(any("missing.png" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
