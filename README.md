# Postman collection backup and cross-sync

Backup all Postman collections and sync any collection to any other (cross-team). Add as many teams as you want via config.

## Setup

1. **Config**  
   Copy the example config and set up your teams:
   ```bash
   cp config/teams.json.example config/teams.json
   ```
   
   Edit `config/teams.json` and set `collection_uid` and `api_key` for each team:
   
   ```json
   {
     "teams": [
       {
         "id": "team-a",
         "name": "Team A",
         "collection_uid": "abc-123...",
         "api_key": "PMAK-xxxxx..."
       },
       {
         "id": "team-b",
         "name": "Team B",
         "collection_uid": "def-456...",
         "api_key": "PMAK-yyyyy..."
       }
     ]
   }
   ```
   
   - **Collection UID**: open the collection in Postman → **...** → **View collection info** → copy the **ID** (UID)
   - **API Key**: get from [Postman API keys](https://go.postman.co/settings/me/api-keys). Each team must have an `api_key` set (cannot be `null`)
   
   **Note**: `config/teams.json` is gitignored to keep your API keys private. Use `config/teams.json.example` as a template.

4. **Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Backup

Back up every configured collection to `backup/<team_id>/<timestamp>.json`:

```bash
python scripts/backup.py
```

Run on a schedule (e.g. cron) if you want regular backups.

## Cross-sync

Overwrite one team’s collection with another team’s collection:

```bash
# Sync Team A → Team B (B will get A's collection)
python scripts/sync.py team-a team-b

# Sync Team B → Team C
python scripts/sync.py team-b team-c
```

Order: `source_team_id` → `target_team_id`. The target collection is replaced by the source. Source and target are auto-backed up before each sync (same timestamp in `backup/<team_id>/`).

## Adding more teams

1. Open `config/teams.json`.
2. Add a new object to `teams` with `id`, `name`, `collection_uid`, and `api_key`.
3. Backup and sync scripts will pick it up; no code changes needed.

Example:

```json
{
  "id": "team-d",
  "name": "Team D",
  "collection_uid": "your-new-collection-uid",
  "api_key": "PMAK-xxxxx..."
}
```

## File layout

- `config/teams.json` – team ids, names, and collection UIDs (edit to add/remove teams).
- `scripts/backup.py` – backup all collections.
- `scripts/sync.py` – sync from one team to another.
- `postman_sync/` – shared config and API helpers.
- `backup/` – created by backup script; one folder per team, timestamped JSON files.
