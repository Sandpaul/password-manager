"""This module contains the definition for `create_secret()`."""

import boto3
from botocore import errorfactory


def create_secret(secret_identifier, user_id, password):
    """A function to create and store a new secret in AWS Secret Manager

    Args:
        secret_identifier (str): the name of the secret.
        user_id (str): user_id to be saved.
        password (str): password to be saved.
    
    Returns:
        status_code (int): the http status code from the request response.
    
    Raises:
        KeyError: if any of the keys are missing / empty.
        TypeError: if any of the keys are the wrong type.
        InvalidCharacterError: if secret_identifier contains any invalid characters.
    """

    sm = boto3.client("secretsmanager")

    try:
        response = sm.create_secret(
            Name = secret_identifier,
            SecretString = f"{{'user_id':{user_id}, 'password':{password}}}"
        )

        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        return status_code
    
    except sm.exceptions.ResourceExistsException as e:
        print(f"ResourceExistsException: {secret_identifier} already exists.")
        raise e
        
