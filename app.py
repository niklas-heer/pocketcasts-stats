import json
from environs import Env
from requests import request
from airtable import Airtable


def get_statistics(username: str, password: str) -> dict:
    """Gets the user statistics from the PocketCasts API

    Parameters
    ----------
    username : str
        Your login email address for PocketCasts.
    password : str
        Your login password for PocketCasts.

    Returns
    -------
    An dict all the statistics about your profile.
    """

    # Login and get a tocken from PocketCasts
    login_url = "https://api.pocketcasts.com/user/login"
    data = (
        f'{{"email":"{username}","password":"{password}","scope":"webplayer"}}'
    )
    headers = {"origin": "https://playbeta.pocketcasts.com"}
    response = request("POST", login_url, data=data, headers=headers).json()

    if "message" in response:
        raise Exception("Login Failed")
    else:
        token = response["token"]

    # Get the statistics through the API
    req = request(
        "POST",
        "https://api.pocketcasts.com/user/stats/summary",
        data={},
        headers={
            "authorization": f"Bearer {token}",
            "origin": "https://playbeta.pocketcasts.com",
        },
    )

    if not req.ok:
        raise Exception("Invalid request")

    return req.json()


def enrich_with_delta(record: dict, previous_record: dict) -> dict:
    """Enriches a record with delta time fields.

    Parameters
    ----------
    record : dict
        The statistics record from PocketCasts as a dict.
    previous_record : dict
        The most current record in Airtable.

    Returns
    -------
    An dict with the calculated time deltas using the previous record.
    """
    enriched_record = dict(record)

    # Calculate time deltas for all keys in stats
    for key, _ in record.items():
        enriched_record[f"Delta ({key})"] = record[key] - previous_record[key]

    return enriched_record


# Handle environment variables
env = Env()
env.read_env()

# Override in env.txt for local development
DEBUG = env.bool("DEBUG", default=False)

##############################
# PocketCasts
##############################

# Get the statistics from PocketCasts
record = get_statistics(env("POCKETCASTS_EMAIL"), env("POCKETCASTS_PASSWORT"))

# Delete the start date because we don't need it
del record["timesStartedAt"]

# Convert everything to int
record = dict((k, int(v)) for k, v in record.items())

##############################
# Airtable
##############################

# The API key for Airtable is provided by AIRTABLE_API_KEY automatically
airtable = Airtable(env("AIRTABLE_BASE_ID"), env("AIRTABLE_POCKETCASTS_TABLE"))

# Get previous record to calculate delta(s)
previous_record = airtable.get_all(
    view="data",
    maxRecords=1,
    sort=[("#No", "desc")],
    fields=[
        "Delta (timeSilenceRemoval)",
        "Delta (timeSkipping)",
        "Delta (timeIntroSkipping)",
        "Delta (timeVariableSpeed)",
        "Delta (timeListened)",
        "timeSilenceRemoval",
        "timeSkipping",
        "timeIntroSkipping",
        "timeVariableSpeed",
        "timeListened",
    ],
)

# Check if it is the first time we are doing it
if previous_record:
    # Enrich record with delta data
    record = enrich_with_delta(record, previous_record[0]["fields"])
else:
    record = enrich_with_delta(record, record)

# Allow to omit actually writing to the database by an environment variable
if not DEBUG:
    # Insert it into Airtable - we need to be sure we want it
    if (
        previous_record[0]["fields"] != record
        and record["Delta (timeListened)"] != 0
    ):
        airtable.insert(record)
        print("[INFO] Written new entry to Airtable.")
    else:
        print("[INFO] Skip writing empty entry.")

# Print the data
print(json.dumps(record, sort_keys=True, indent=4))
