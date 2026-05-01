"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    with open("postcode_cache.json", "r") as f:
        data = json.load(f)
    return data


def save_cache(cache: dict) -> None:
    """Saves the cache to a file as JSON"""
    with open("postcode_cache.json", "r") as f:
        data = json.load(f)

    data.update(cache)

    with open("postcode_cache.json", "w") as f:
        json.dump(data, f, indent=4)


# saving a cache works here, but not in the functions?
# when in the functions, it deletes the postcode_cache.json
data = load_cache()
print(data)
cache = {"TN12 FFF":
         {"valid": True,
             "completions": ["TN12 0AA"]
          }
         }


# for k in cache.keys():
#     if k in data.keys():
#         print("True")
#     else:
#         print("False")

save_cache(cache)
data = load_cache()
print(data)


def validate_postcode(postcode: str) -> bool:
    """Determines whether a postcode is valid (True) or invalid (False)
    Using the UK postcode API
    """
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    # check if postcode is validated in cache
    data = load_cache()
    if postcode.upper().strip() in data.keys():
        return data[postcode]["valid"]

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate")

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if response.status_code == 200:
        # add validation to cache
        cache = {postcode.upper().strip():
                 {"valid": data["result"],
                  "completions": [postcode.upper().strip()]
                  }
                 }
        save_cache(cache)

        return data["result"]


def get_postcode_for_location(lat: float, long: float) -> str:
    """Returns the postcode for a given latitude and longitude"""
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")

    response = req.get(
        f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}")

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if data["result"] == None:
        raise ValueError("No relevant postcode found.")

    if response.status_code == 200:
        return data["result"][0]["postcode"]


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Returns a list of autocompleted postcodes from the given start"""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")

    # check if postcode is completed in cache
    data = load_cache()
    if postcode_start.upper().strip() in data.keys():
        return data[postcode_start]["completions"]

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete")

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if data["result"] == None:
        # add to cache here
        cache = {postcode_start.upper().strip():
                 {"valid": False,
                  "completions": None
                  }
                 }
        save_cache(cache)

        return None

    if response.status_code == 200:
        # add to cache here
        cache = {postcode_start.upper().strip():
                 {"valid": False,
                  "completions": data["result"]
                  }
                 }
        save_cache(cache)

        return data["result"]


def get_postcodes_details(postcodes: list[str]) -> list[dict]:
    """"""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for item in postcodes:
        if not isinstance(item, str):
            raise TypeError("Function expects a list of strings.")

    response = req.post(
        f"https://api.postcodes.io/postcodes",
        json=postcodes
    )

    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")

    data = response.json()

    if data["result"] == None:
        return None

    if response.status_code == 200:
        return data["result"]
