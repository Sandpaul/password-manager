"""This module contains the definition for `create_secret()`."""

import re

import boto3


def create_secret(secret_identifier: str, user_id: str, password: str):
    """A function to create and store a new secret in AWS Secret Manager

    Args:
        secret_identifier (str): the name of the secret.
        user_id (str): user_id to be saved.
        password (str): password to be saved.
    
    Returns:
        status_code (int): the http status code from the request response.
    
    Raises:
        ResourceExistsException: if a secret with passed secret_identifier already exists.
        BlankArgumentError: if the function is passed an empty string as an argument.
        InvalidCharacterError: if secret_identifier contains any invalid characters.
    """

    if len(secret_identifier) == 0 or len(user_id) == 0 or len(password) == 0:
        raise BlankArgumentError(print("BlankArgumentError: arguments cannot be blank."))

    regex = r"[a-z]|[A-Z]|[0-9]|\/|_|\+|=|\.|@|-"

    regex_list = re.findall(regex, secret_identifier)

    if len(regex_list) != len(secret_identifier):
        raise InvalidCharacterError(print("InvalidCharacterError: secret_identity can only contain ASCII letters, numbers and the following characters: /_+=.@-"))

    sm = boto3.client("secretsmanager")

    try:
        response = sm.create_secret(
            Name = secret_identifier,
            SecretString = f"{{'user_id':{user_id}, 'password':{password}}}"
        )

        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        return status_code

    except sm.exceptions.ResourceExistsException as r:
        print(f"ResourceExistsException: {secret_identifier} already exists.")
        raise r

class BlankArgumentError(Exception):
    """Traps errors where blank arguments are passed."""

class InvalidCharacterError(Exception):
    """Traps errors where invalid characters are used in secret_identifier."""
