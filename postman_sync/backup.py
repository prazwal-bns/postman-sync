"""Backup Postman collections for given teams."""
import json
import sys
from datetime import datetime
from pathlib import Path

from postman_sync.api import get_collection
from postman_sync.config import get_teams, get_team_by_id

ROOT = Path(__file__).resolve().parent.parent


def backup_teams(team_ids, config_path=None):
    """
    Backup collections for the given team ids.
    team_ids: list of team id strings, or None to backup all teams.
    Returns the timestamp string used for backup filenames.
    """
    teams = get_teams(path=config_path)
    if team_ids is not None:
        teams = [get_team_by_id(tid, path=config_path) for tid in team_ids]
    backup_dir = ROOT / "backup"
    backup_dir.mkdir(exist_ok=True)
    now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    for team in teams:
        team_id = team["id"]
        uid = team["collection_uid"]
        if not uid or uid.startswith("YOUR_"):
            print(f"Skip {team_id}: no collection_uid set")
            continue
        try:
            api_key = team.get("api_key")
            if not api_key:
                raise ValueError(
                    f"Team {team_id} ({team.get('name', '')}) has no api_key set. "
                    f"Set api_key in config/teams.json for this team."
                )
            data = get_collection(uid, api_key=api_key)
            team_backup = backup_dir / team_id
            team_backup.mkdir(exist_ok=True)
            out_file = team_backup / f"{now}.json"
            with open(out_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Backed up {team_id} -> {out_file}")
        except Exception as e:
            print(f"Error backing up {team_id}: {e}", file=sys.stderr)
            raise

    return now
