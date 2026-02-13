"""Load teams config and resolve team by id or name."""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "teams.json"


def load_config(path=None):
    path = path or CONFIG_PATH
    with open(path, "r") as f:
        return json.load(f)


def get_teams(path=None):
    return load_config(path=path)["teams"]


def get_team_by_id(team_id, path=None):
    teams = get_teams(path=path)
    for t in teams:
        if t["id"] == team_id:
            return t
    raise KeyError(f"Team not found: {team_id}")


def get_team_by_name(name, path=None):
    name_lower = name.strip().lower()
    teams = get_teams(path=path)
    for t in teams:
        if t["name"].strip().lower() == name_lower:
            return t
    raise KeyError(f"Team not found: {name}")
