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


def enrich_with_delta(stats, previous_record):
    """Enriches a record with delta time fields.

    Parameters
    ----------
    stats : dict
        The statistics record from PocketCasts as a dict.
    previous_record : dict
        The most current record in Airtable.

    Returns
    -------
    An dict with the calculated time deltas using the previous record.
    """
    enriched_record = dict(stats)

    # Calculate time deltas for all keys in stats
    for key,_ in stats.items():
        enriched_record[f"Delta ({key})"] = stats[key] - previous_record['fields'][key]

    return enriched_record

##############################
# PocketCasts
##############################

# Get the statistics from PocketCasts
stats = get_statistics(os.environ['POCKETCASTS_EMAIL'],os.environ['POCKETCASTS_PASSWORT'])


# Handle start date - we probably don't need it
start_date = stats['timesStartedAt']
del stats['timesStartedAt']

# Convert everything to int
stats = dict((k,int(v)) for k,v in stats.items())

##############################
# Airtable
##############################

# The API key for Airtable is provided by AIRTABLE_API_KEY (the lib uses that automatically)
airtable = Airtable(os.environ['AIRTABLE_BASE_ID'], os.environ['AIRTABLE_POCKETCASTS_TABLE'])

# Get previous record to calculate delta(s)
previous_record = airtable.get_all(view='data', maxRecords=1, sort=[("#No", 'desc')])

# Enrich record with delta data
stats = enrich_with_delta(stats, previous_record[0])

# Insert it into Airtable - we need to be sure we want it
airtable.insert(stats)

# Print the data
print(json.dumps(stats, sort_keys=True, indent=4))
