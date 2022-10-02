"""constants, lists, dics"""

import os

from dotenv import load_dotenv

load_dotenv(".streamlit/secrets.toml")

PAGES: list = ["login", "graph", "meteo"]

AUTH_URL: str = "https://www.strava.com/oauth/token"
ACTIVITIES_URL: str = "https://www.strava.com/api/v3/athlete/activities"

REQUEST_DATA = {
    "client_id": os.getenv("STRAVA_CLIENT_ID"),
    "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
    "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
    "grant_type": "refresh_token",
    "f": "json",
}
