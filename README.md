![PocketCasts statistics](https://raw.github.com/niklas-heer/pocketcasts-stats/master/.github/img/screenshot_01.png "Airtable Dashboard")

<h2 align="center">Pocket Casts statistics</h2>

<p align="center">
    <a href="https://github.com/niklas-heer/pocketcasts-stats/actions/workflows/test.yml"><img alt="Test Status" src="https://github.com/niklas-heer/pocketcasts-stats/actions/workflows/test.yml/badge.svg"></a>
    <a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

This project lets you fetch your Pocket Casts statistics and put them into Airtable.

## Quick Start with GitHub Actions

The easiest way to use this project is with GitHub Actions:

1. Fork this repository
2. Set up the required secrets (see [Environment variables](#environment-variables))
3. The workflow runs automatically every 2 hours, or trigger it manually from the Actions tab

## Configuration

### Airtable

For the tool to work you'll need a [free Airtable account](https://airtable.com/invite/r/V2q23fXk).

1. Go to this example base: <https://airtable.com/shryxs3YOERmBeHl1>

2. Click on `Copy base` in the top right corner

3. Once copied delete the example records

4. Create a [Personal Access Token](https://airtable.com/create/tokens) with the following scopes:
   - `data.records:read`
   - `data.records:write`
   - Add access to your copied base
   - Save the token for `AIRTABLE_API_KEY`

5. Get your Base ID from the URL when viewing your base:
   - URL looks like: `https://airtable.com/appXXXXXXXXXXXXXX/...`
   - The `appXXXXXXXXXXXXXX` part is your `AIRTABLE_BASE_ID`

### GitHub Actions (Recommended)

1. Fork this repository

2. Go to `Settings` > `Secrets and variables` > `Actions`

3. Add the following repository secrets:
   - `POCKETCASTS_EMAIL`
   - `POCKETCASTS_PASSWORD`
   - `AIRTABLE_API_KEY`
   - `AIRTABLE_BASE_ID`
   - `AIRTABLE_POCKETCASTS_TABLE`

4. The workflow runs automatically every 2 hours. You can also trigger it manually from the `Actions` tab.
   If any of the secrets above are missing, the sync workflow will skip the run.

### GitLab CI (Alternative)

1. Make a new project on [Gitlab.com](https://gitlab.com)

2. Import this repository as the base for your project

3. Go to `Settings` > `CI / CD` > `Variables` and add all environment variables

4. Set up the Pipeline Scheduler:
   - Go to `CI / CD` > `Schedules`
   - Click `New schedule`
   - Use cron pattern: `0 */2 * * *` (runs every 2 hours)
   - Select your `master` branch and ensure `Active` is checked

### Environment variables

| Variable | Description |
|----------|-------------|
| `POCKETCASTS_EMAIL` | Your PocketCasts login email |
| `POCKETCASTS_PASSWORD` | Your PocketCasts password |
| `AIRTABLE_BASE_ID` | The ID of your Airtable base (starts with `app`) |
| `AIRTABLE_API_KEY` | Your Airtable Personal Access Token |
| `AIRTABLE_POCKETCASTS_TABLE` | The table name to store data (e.g., `PocketCasts`) |

**Note**: Avoid special characters like `.!$/\|` in environment variables.

## Local Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (recommended) or Python 3.11+

### Setup

```bash
# Clone the repository
git clone https://github.com/niklas-heer/pocketcasts-stats.git
cd pocketcasts-stats

# Install dependencies
uv sync

# Copy and configure environment
cp .env_example .env
# Edit .env with your credentials

# Run the app
uv run python app.py

# Run tests
uv run pytest
```

### Docker

```bash
# Build and run
make

# Or step by step
make build
make run

# Run tests in Docker
make test-docker
```

## Contribution

Please run [`black`](https://github.com/ambv/black) on your code before committing:

```bash
uv run black .
```

## Attribution

- [Pocket Casts](https://www.pocketcasts.com/) - awesome podcast player
- [pyairtable](https://github.com/gtalarico/pyairtable) - Python library for Airtable API
- [Airtable](https://airtable.com/invite/r/V2q23fXk) - database/spreadsheet tool
- [uv](https://docs.astral.sh/uv/) - fast Python package manager
- [pytest](https://github.com/pytest-dev/pytest) - testing framework
- [black](https://github.com/ambv/black) - code formatter
