"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


if __name__ == "__main__":

    parser = ArgumentParser(
        prog='A CLI application for interacting with the Postcode API',
        description="""Allows you to validate an inputted postcode, or
        get a list of autocompleted postcodes from the start of a postcode
        """,
        epilog='Uses UK Postcodes.io API'
    )

    parser.add_argument("--mode", "-m",
                        help="""The mode for the script 
                        - either 'validate' or 'complete'
                        """,
                        required=True,
                        choices=["validate", "complete"]
                        )
    parser.add_argument("postcode",
                        help="""The postcode that will either be 
                        validated or completed
                        """
                        )

    args = parser.parse_args()
    postcode = args.postcode

    if args.mode == "validate":
        if validate_postcode(postcode):
            print(f"{postcode.upper().strip()} is a valid postcode.")
        else:
            print(f"{postcode.upper().strip()} is not a valid postcode.")

    else:
        postcodes = get_postcode_completions(postcode)

        if postcodes is None:
            print(f"No matches for {postcode.upper().strip()}.")
        else:
            for i in range(5):
                print(postcodes[i])


"https://api.postcodes.io/postcodes/EH14 2AA/validate"
