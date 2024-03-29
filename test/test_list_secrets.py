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
def test_returns_list(
    mock_secretsmanager,
    secret_identifier,
    user_id,
    password,
):
    """list_secrets() should return a list."""
    create_secret(secret_identifier, user_id, password)
    result = list_secrets()
    assert isinstance(result, list)


@pytest.mark.describe("list_secrets()")
@pytest.mark.it("should return correct secret names")
def test_returns_correct_list(
    mock_secretsmanager,
    secret_identifier,
    user_id,
    password,
):
    """list_secrets() should return a containing the correct secret names."""
    create_secret(secret_identifier, user_id, password)
    result = list_secrets()
    assert result == ["test_secret"]


@pytest.mark.describe("list_secrets()")
@pytest.mark.it("should return correct secret names when there are multiple secrets")
def test_returns_correct_list_for_multiple_secrets(
    mock_secretsmanager,
    secret_identifier,
    user_id,
    password,
):
    """list_secrets() should return a containing the correct secret names when there are multiple secrets."""
    create_secret(secret_identifier, user_id, password)
    create_secret("test_secret2", user_id, password)
    create_secret("test_secret3", user_id, password)
    result = list_secrets()
    assert result == ["test_secret", "test_secret2", "test_secret3"]


@pytest.mark.describe("list_secrets()")
@pytest.mark.it("should return empty list when there are no secrets stored")
def test_no_secrets(mock_secretsmanager):
    """list_secrets() should return an empty list when there are no secrets stored."""
    result = list_secrets()
    assert result == []


@pytest.mark.describe("list_secrets()")
@pytest.mark.it("should not return secrets that have been marked for deletion")
def test_does_not_return_deleted_secrets(
    mock_secretsmanager,
    user_id,
    password,
):
    """list_secrets() should return an empty list when there are no secrets stored."""
    create_secret("test_secret1", user_id, password)
    create_secret("test_secret2", user_id, password)
    mock_secretsmanager.delete_secret(
        SecretId="test_secret1",
    )
    result = list_secrets()
    assert result == ["test_secret2"]
