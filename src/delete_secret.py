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
    """

    sm = boto3.client("secretsmanager")

    response = sm.delete_secret(
        SecretId=secret_id,
        ForceDeleteWithoutRecovery=True,
    )

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]

    return status_code
