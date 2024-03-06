"""This module contains the test suite for `create_secret()`."""

import os
from pprint import pprint

from moto import mock_aws
import boto3
import pytest

from src.create_secret import create_secret


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def mock_secretsmanager(aws_credentials):
    """Mock secretsmanager client
    """
    with mock_aws():
        yield boto3.client("secretsmanager", region_name='eu-west-2')


@pytest.mark.describe("create_secret()")
@pytest.mark.it("should successfully create a secret in AWS secrets manager")
def test_secret_created(mock_secretsmanager):
    """create_secret() should return 200 status code when successfully creating a new secret.
    """
    secret_identifier = "test_secret"
    user_id = "test_id"
    password = "test_password"
    result = create_secret(secret_identifier, user_id, password)
    assert result == 200
