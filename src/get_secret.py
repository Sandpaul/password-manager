"""This module contains the definition for `get_secret()`."""

import boto3


def get_secret(secret_id: str):
    """A function to retrieve the details of a secret from AWS Secret Manager and save them to a text file.

    Args:
        secret_id (str): the name of the secret to be retrieved.
    
    Returns:
        secret_string (str): a string of the retrieved secret user_id and password.
    
    Raises:
    """
    
    if len(secret_id) == 0:
        raise BlankArgumentError(
            print("BlankArgumentError: secret_id cannot be blank.")
        )
    
    sm = boto3.client("secretsmanager")
    
    response = sm.get_secret_value(
            SecretId=secret_id
    )
    return response['SecretString']


class BlankArgumentError(Exception):
    """Traps errors where blank arguments are passed."""
