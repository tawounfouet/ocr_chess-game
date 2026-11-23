"""R00-R01 regression tests: CLI navigation and read-only tournament inspection.

Run with: python -m unittest discover -s tests -v
Integration tests run the application against temporary JSON copies.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from views.view_app import ViewApp
from views.player import ViewPlayer
from views.tournament import TournamentView

REPO_ROOT = Path(__file__).resolve().parents[1]


class MenuTests(unittest.TestCase):
    def test_t01_main_menu_quits_on_4(self):
        with patch("builtins.input", return_value="4"):
            self.assertEqual(ViewApp().display_main_menu(), "4")

    def test_t02_main_menu_rejects_hidden_3(self):
        with patch("builtins.input", side_effect=["3", "4"]) as mocked:
            self.assertEqual(ViewApp().display_main_menu(), "4")
        self.assertEqual(mocked.call_count, 2)

    def test_t03_player_menu_returns_on_5(self):
        with patch("builtins.input", return_value="5"):
            self.assertEqual(ViewPlayer().display_player_menu(), "5")

    def test_t04_tournament_menu_returns_on_6(self):
        view = TournamentView.__new__(TournamentView)
        with patch("builtins.input", return_value="6"):
            self.assertEqual(view.display_tournament_menu(), "6")

    def test_t05_tournament_menu_rejects_hidden_5(self):
        view = TournamentView.__new__(TournamentView)
        with patch("builtins.input", side_effect=["5", "6"]) as mocked:
            self.assertEqual(view.display_tournament_menu(), "6")
        self.assertEqual(mocked.call_count, 2)

    def test_t06_input_message_returns_trimmed_text(self):
        view = TournamentView.__new__(TournamentView)
        with patch("builtins.input", return_value="  abc-123  "):
            self.assertEqual(view.input_message("UUID: "), "abc-123")


class IsolatedCliTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="p4-r00-r01-")
        self.run_dir = Path(self.workspace.name)
        (self.run_dir / "data").mkdir()
        self.reference = {}
        for name in ("players.json", "tournaments.json"):
            source = REPO_ROOT / "data" / name
            self.reference[name] = source.read_bytes()
            shutil.copyfile(source, self.run_dir / "data" / name)
        import json
        raw = json.loads(self.reference["tournaments.json"].decode("utf-8"))
        tournaments = raw.get("tournaments", {})
        self.uuid = next(
            (doc.get("tournament_id") for doc in tournaments.values()
             if isinstance(doc, dict) and doc.get("tournament_id")), None
        )
        if not self.uuid:
            self.fail("The fixture contains no tournament UUID")

    def tearDown(self):
        self.workspace.cleanup()

    def run_cli(self, commands):
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = str(REPO_ROOT)
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "main.py")],
            input="\n".join(commands) + "\n",
            cwd=str(self.run_dir),
            env=env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + "\n" + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result.stdout

    def test_t07_existing_tournament_details_by_uuid(self):
        output = self.run_cli(["1", "3", self.uuid, "6", "4"])
        self.assertIn("Tournament ID", output)
        self.assertIn(self.uuid, output)
        self.assertNotIn("not found", output.lower())

    def test_t08_unknown_tournament_details_do_not_crash(self):
        output = self.run_cli(["1", "3", "missing-uuid-123", "6", "4"])
        self.assertIn("not found", output.lower())
        self.assertIn("Goodbye!", output)

    def test_t09_rounds_by_uuid_and_return_to_tournament_menu(self):
        output = self.run_cli(["1", "4", self.uuid, "6", "4"])
        self.assertIn("Rounds for Tournament", output)
        self.assertIn("Round Name", output)
        self.assertGreaterEqual(output.count("Tournament Menu"), 2)

    def test_t10_unknown_rounds_uuid_do_not_crash(self):
        output = self.run_cli(["1", "4", "missing-uuid-123", "6", "4"])
        self.assertIn("not found", output.lower())
        self.assertIn("Goodbye!", output)

    def test_t11_end_to_end_menu_navigation(self):
        output = self.run_cli(["2", "5", "1", "6", "4"])
        self.assertIn("Player Menu", output)
        self.assertIn("Tournament Menu", output)
        self.assertIn("Goodbye!", output)

    def test_t12_read_only_actions_leave_json_bytes_unchanged(self):
        self.run_cli(["1", "3", self.uuid, "4", self.uuid, "6", "4"])
        for name, content in self.reference.items():
            self.assertEqual((self.run_dir / "data" / name).read_bytes(), content)
            self.assertEqual((REPO_ROOT / "data" / name).read_bytes(), content)

    def test_t13_launch_from_arbitrary_working_directory(self):
        output = self.run_cli(["4"])
        self.assertIn("Welcome to the Chess Tournament Manager", output)
        self.assertIn("Goodbye!", output)


if __name__ == "__main__":
    unittest.main()
