import json
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import Mock

import pytest
import tank_game


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.setattr(tank_game, "SCORE_FILE", str(tmp_path / "score.json"))
    return tank_game.Api()


def test_score_roundtrip_and_high_score_is_preserved(api):
    assert api.get_high_score() == 0
    api.save_high_score(30)
    api.save_high_score(10)
    assert api.get_high_score() == 30


@pytest.mark.parametrize("content", ['broken', '{"high": null}', '[]', '{"high": -10}'])
def test_corrupt_score_does_not_break_startup(api, content):
    Path(tank_game.SCORE_FILE).write_text(content, encoding="utf-8")
    assert api.get_high_score() == 0


def test_window_controls_use_current_window(api, monkeypatch):
    window = Mock()
    monkeypatch.setattr(tank_game, "win_instance", window)
    api.toggle_fullscreen()
    api.quit()
    window.toggle_fullscreen.assert_called_once()
    window.destroy.assert_called_once()


def test_frontend_entry_references_existing_local_assets():
    class Assets(HTMLParser):
        paths = []
        def handle_starttag(self, tag, attrs):
            for name, value in attrs:
                if name in {"src", "href"} and value.startswith("./"):
                    self.paths.append(value)
    entry = Path(tank_game.GAME_HTML)
    parser = Assets()
    parser.feed(entry.read_text(encoding="utf-8"))
    assert parser.paths
    assert all((entry.parent / path).is_file() for path in parser.paths)
