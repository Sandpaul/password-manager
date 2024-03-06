"""This module contains the definition for `list_secrets()`."""

import boto3


def list_secrets() -> list:
    """A function to retrieve a list of all the secrets stored in AWS Secrets Manager.

    Returns:
        secret_list (list): a list of AWS Secrets Manager names.
    """

    sm = boto3.client("secretsmanager")

    response = sm.list_secrets(
        IncludePlannedDeletion=True,
    )

    secret_list = [
        secret["Name"]
        for secret in response["SecretList"]
        if "DeletedDate" not in str(secret)
    ]

    return secret_list
