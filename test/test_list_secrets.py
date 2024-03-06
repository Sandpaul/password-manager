"""This module contains the test suite for `list_secrets()`."""

import os

import boto3
import pytest
from moto import mock_aws

from src.create_secret import create_secret
from src.list_secrets import list_secrets


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
    """Mock secretsmanager client"""
    with mock_aws():
        yield boto3.client("secretsmanager", region_name="eu-west-2")


@pytest.fixture
def secret_identifier():
    """create mock secret_identifier"""
    return "test_secret"


@pytest.fixture
def user_id():
    """create mock user_id"""
    return "test_id"


@pytest.fixture
def password():
    """create mock password"""
    return "test_password"


@pytest.mark.describe("list_secrets()")
@pytest.mark.it("should return a list")
def test_returns_list(mock_secretsmanager, secret_identifier, user_id, password):
    """list_secrets() should return a list."""
    create_secret(secret_identifier, user_id, password)
    result = list_secrets()
    assert isinstance(result, list)