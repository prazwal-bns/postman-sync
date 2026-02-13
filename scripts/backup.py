#!/usr/bin/env python3
"""
Backup all Postman collections defined in config/teams.json.
Saves each collection to backup/<team_id>/<timestamp>.json.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from postman_sync.backup import backup_teams


def main(config_path=None):
    backup_teams(team_ids=None, config_path=config_path)
    print("Backup done.")


if __name__ == "__main__":
    main()
