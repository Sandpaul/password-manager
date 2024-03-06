"""This module contains the definition for `delete_secret()`."""

import boto3

from pprint import pprint

def delete_secret(secret_id: str):
    """A function to delete a specified secret from AWS Secret Manager.

    Args:
        secret_id (str): string of the name of the secret to be deleted
    
    Returns:
        status_code (int): the http status code from the request response.
    
    Raises:
        ResourceNotFoundError: if no resource with the given secret_id is found.
        BlankArgumentError: if passed a blank secret_id.
        
    """

    if len(secret_id) == 0:
        raise BlankArgumentError(
            print("BlankArgumentError: secret_id cannot be blank.")
        )

    sm = boto3.client("secretsmanager")

    try:
        response = sm.delete_secret(
            SecretId=secret_id,
        )

        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        return status_code

    except sm.exceptions.ResourceNotFoundException as r:
        print(f"ResourceNotFound: {secret_id}.")
        raise r

class BlankArgumentError(Exception):
    """Traps errors where blank arguments are passed."""