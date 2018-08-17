# PocketCasts statistics

A tool to fetch your poketcasts statistics an put them into Airtable

## Configuration

### Airtable

TODO

### Gitlab

For this to work you'll need a free Gitlab.com account. If you don't have one - make one.

1. Make a new project on [Gitlab.com](https://gitlab.com).
2. Import this repository as the base for your project.
3. Setup all environment variables in the project.
    * Go to `Settings` > `CI / CD` (on the left)
    * Insert variables under `Variables` (click expand, also see `Environment variables`)
4. Setup the Pipeline Scheduler
    * Go to `CI / CD` > `Schedules` (on the left)
    * Click the green button on the right `New schedule`
    * Give it a description (eg. "Get new stats every 2h")
    * Select `Custom ( Cron syntax )` under `Interval Pattern`
    * Insert the following into the field: `0 */2 * * *` (runs every 2 hours)
    * Make sure under `Target Branch` you selected your `master` branch
    * Make sure the checkbox `Active` is checked
    * Click the `Save pipeline schedule`
5. Profit! :)

### Environment variables

* `POCKETCASTS_EMAIL` - the email address of your PocketCasts login
* `POCKETCASTS_PASSWORT` - the password to login to PocketCasts
* `AIRTABLE_BASE_ID` - the ID of the Airtable base which is used to store the data
* `AIRTABLE_API_KEY` - your account API key to access Airtable
* `AIRTABLE_POCKETCASTS_TABLE` - the table to store the PocketCasts information in

__IMPORTANT__: You cannot use the `$` symbol in the environment variables!

## Local testing

1. Make a copy of the `env-example.txt` file and name it `env.txt`
2. Put in your credentials as mentioned in __Environment variables__
3. Test the app via docker with: `make`
4. Profit! :)

## Attribution

* [airtable-python-wrapper](https://github.com/gtalarico/airtable-python-wrapper) as an awesome library to connect to Airtable
* [furgoose/Pocket-Casts](https://github.com/furgoose/Pocket-Casts) as a good reference how to query the PocketCasts "API"
* [Airtable](https://airtable.com) for being just an awesome tool!
* [Gitlab](https://gitlab.com) and `GitlabCI` for being an all in one solution
* Gitlab Scheduler for Pipelines because without it you would need a server.
