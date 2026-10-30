"""
weather.py
----------
Weather-based advice for AgriDoctor AI -- e.g. "rain expected, delay spraying."

Uses Open-Meteo (https://open-meteo.com), a free weather API that needs no
API key and no sign-up, which keeps this feature usable immediately without
another account/credential to set up (a lesson learned from how much
friction TensorFlow's download already caused during setup).

Two calls are made:
  1. Geocoding: city name -> latitude/longitude
  2. Forecast: latitude/longitude -> next 24h precipitation probability

Both are wrapped in try/except so a missing internet connection or an
unrecognized city name degrades gracefully instead of crashing the app --
the Scan page simply skips the weather banner if advice isn't available.
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

RAIN_THRESHOLD = 50  # percent chance of rain that triggers a "delay spraying" warning


def _geocode(city: str):
    """Return (lat, lon, resolved_name) for a city name, or None if not found."""
    try:
        resp = requests.get(GEOCODE_URL, params={"name": city, "count": 1}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results")
        if not results:
            return None
        r = results[0]
        label = r.get("name", city)
        if r.get("admin1"):
            label += f", {r['admin1']}"
        return r["latitude"], r["longitude"], label
    except Exception as e:
        print(f"[weather.py] Geocoding failed for '{city}': {e}")
        return None


def get_rain_advice(city: str) -> dict:
    """
    Returns structured forecast data for the given city -- no message text
    is built here, since that needs to be language-aware. The caller (see
    app.py) builds the actual sentence to display using i18n.t() with these
    fields:

        {
            "available": bool,
            "location": str,             # only present if available
            "max_rain_chance": int,      # percent, 0-100
            "should_delay_spraying": bool,
            "error": str,                # "city_not_found" | "forecast_failed", only if not available
        }
    """
    geo = _geocode(city)
    if geo is None:
        return {"available": False, "error": "city_not_found"}

    lat, lon, label = geo
    try:
        resp = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "precipitation_probability",
                "forecast_days": 2,
                "timezone": "auto",
            },
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        probs = data.get("hourly", {}).get("precipitation_probability", [])
        next_24h = probs[:24] if probs else []
        max_chance = int(max(next_24h)) if next_24h else 0
    except Exception as e:
        print(f"[weather.py] Forecast lookup failed for {label}: {e}")
        return {"available": False, "error": "forecast_failed", "location": label}

    return {
        "available": True,
        "location": label,
        "max_rain_chance": max_chance,
        "should_delay_spraying": max_chance >= RAIN_THRESHOLD,
    }


if __name__ == "__main__":
    # Manual smoke test (needs internet).
    print(get_rain_advice("Chennai"))
