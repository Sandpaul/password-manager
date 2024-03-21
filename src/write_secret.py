"""This module contains the definition for `write_secret()`."""


def write_secret(secret_id: str, secret_string: str):
    """A function to write the contents of a retrieved secret to a .txt file.

    Args:
        secret_id (str): the name of the secret to be saved.
        secret_string (str): the string to be saved to a text file.
    """

    with open(f"{secret_id}.txt", "w", encoding="utf-8") as f:
        f.write(secret_string)
