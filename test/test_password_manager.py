"""This module contains the test suite for `password_manager()`."""

import os
from unittest.mock import patch

import boto3
import pytest
from moto import mock_aws

from src.create_secret import create_secret
from src.get_secret import get_secret
from src.list_secrets import list_secrets
from src.password_manager import password_manager


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


@pytest.mark.describe("password_manager()")
@pytest.mark.it("e: should successfully create a new secret")
@patch(
    "builtins.input",
    side_effect=[
        "e",
        "test_id",
        "test_user",
        "test_password",
        "x",
    ],
)
def test_creates_secret(mock_input, mock_secretsmanager):
    """password_manager() should create a new secret with passed data."""
    password_manager()
    assert get_secret("test_id") == "{'user_id':test_user, 'password':test_password}"


@pytest.mark.describe("password_manager()")
@pytest.mark.it("r: should successfully retrieve secret")
@patch(
    "builtins.input",
    side_effect=[
        "e",
        "test_id",
        "test_user",
        "test_password",
        "r",
        "test_id",
        "x",
    ],
)
def test_retrieves_secret(mock_input, mock_secretsmanager):
    """password_manager() should retrieve a secret and save it to a file."""
    password_manager()
    with open("test_id.txt", "r", encoding="utf-8") as f:
        assert f.read() == "{'user_id':test_user, 'password':test_password}"


@pytest.mark.describe("password_manager()")
@pytest.mark.it("d: should successfully delete secret")
@patch(
    "builtins.input",
    side_effect=[
        "d",
        "test_id",
        "x",
    ],
)
def test_deletes_secret(mock_input, mock_secretsmanager):
    """password_manager() should delete a secret."""
    create_secret("test_id", "test_user", "test_password")
    assert len(list_secrets()) == 1
    password_manager()
    assert len(list_secrets()) == 0
