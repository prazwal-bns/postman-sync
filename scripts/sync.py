#!/usr/bin/env python3
"""
Cross-sync a Postman collection from one team to another.
Usage:
  python scripts/sync.py <source_team_id> <target_team_id>
  python scripts/sync.py team-a team-b   # copy Team A collection into Team B
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from postman_sync.api import get_collection, put_collection
from postman_sync.backup import backup_teams
from postman_sync.config import get_teams, get_team_by_id


def main():
    if len(sys.argv) != 3:
        teams = get_teams()
        ids = [t["id"] for t in teams]
        print("Usage: python scripts/sync.py <source_team_id> <target_team_id>")
        print(f"Teams in config: {', '.join(ids)}")
        sys.exit(1)

    source_id = sys.argv[1].strip().lower()
    target_id = sys.argv[2].strip().lower()

    if source_id == target_id:
        print("Source and target must be different.")
        sys.exit(1)

    source = get_team_by_id(source_id)
    target = get_team_by_id(target_id)

    print(f"Syncing: {source['name']} ({source_id}) -> {target['name']} ({target_id})")

    # Auto-backup both source and target before syncing
    print("Backing up source and target collections...")
    backup_teams([source_id, target_id])
    print("Backup done. Syncing...")

    # Use source team's API key for fetching, target team's API key for updating
    source_api_key = source.get("api_key")
    target_api_key = target.get("api_key")
    
    if not source_api_key:
        print(f"Error: {source['name']} ({source_id}) has no api_key set in config/teams.json", file=sys.stderr)
        sys.exit(1)
    if not target_api_key:
        print(f"Error: {target['name']} ({target_id}) has no api_key set in config/teams.json", file=sys.stderr)
        sys.exit(1)

    payload = get_collection(source["collection_uid"], api_key=source_api_key)
    collection_body = payload.get("collection")
    if not collection_body:
        print("Invalid response: no 'collection' in response")
        sys.exit(1)

    put_collection(target["collection_uid"], collection_body, api_key=target_api_key)
    print("Sync completed.")


if __name__ == "__main__":
    main()
