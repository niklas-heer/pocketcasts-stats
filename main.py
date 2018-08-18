import os
import json
import datetime
from requests import request
from airtable import Airtable


def get_statistics(username, password):
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
    data = f'{{"email":"{username}","password":"{password}","scope":"webplayer"}}'
    headers = {"origin": "https://playbeta.pocketcasts.com"}
    response = request("POST", login_url, data=data, headers=headers).json()

    if "message" in response:
        raise Exception("Login Failed")
    else:
        token = response['token']

    # Get the statistics through the API
    req = request("POST", "https://api.pocketcasts.com/user/stats/summary", data={}, headers={'authorization': f'Bearer {token}', 'origin': "https://playbeta.pocketcasts.com"})

    if not req.ok:
        raise Exception("Invalid request")

    return req.json()


def enrich_with_delta(record, previous_record):
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
    for key,_ in record.items():
        enriched_record[f"Delta ({key})"] = record[key] - previous_record[key]

    return enriched_record

##############################
# PocketCasts
##############################

# Get the statistics from PocketCasts
record = get_statistics(os.environ['POCKETCASTS_EMAIL'],os.environ['POCKETCASTS_PASSWORT'])

# Handle start date - we probably don't need it
start_date = record['timesStartedAt']
del record['timesStartedAt']

# Convert everything to int
record = dict((k,int(v)) for k,v in record.items())

##############################
# Airtable
##############################

# The API key for Airtable is provided by AIRTABLE_API_KEY (the lib uses that automatically)
airtable = Airtable(os.environ['AIRTABLE_BASE_ID'], os.environ['AIRTABLE_POCKETCASTS_TABLE'])

# Get previous record to calculate delta(s)
previous_record = airtable.get_all(view='data', maxRecords=1, sort=[("#No", 'desc')])

# Check if it is the first time we are doing it
if previous_record:
    # Enrich record with delta data
    record = enrich_with_delta(record, previous_record[0]['fields'])
else:
    record = enrich_with_delta(record, record)

# Insert it into Airtable - we need to be sure we want it
airtable.insert(record)

# Print the data
print(json.dumps(record, sort_keys=True, indent=4))
