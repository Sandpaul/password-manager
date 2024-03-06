"""This module contains the test suite for `delete_secret()`."""

import os

import boto3
import pytest
from moto import mock_aws

from src.create_secret import create_secret
from src.list_secrets import list_secrets
from src.delete_secret import delete_secret, BlankArgumentError


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


@pytest.mark.describe("delete_secret()")
@pytest.mark.it("should successfully delete a secret")
def test_deletes_secret(
    mock_secretsmanager,
    secret_identifier,
    user_id,
    password,
):
    """delete_secret() should successfully delete a secret from AWS Secrets Manager."""
    create_secret(secret_identifier, user_id, password)
    assert list_secrets() == ["test_secret"]
    result = delete_secret(secret_identifier)
    assert list_secrets() == []
    assert result == 200


@pytest.mark.describe("delete_secret()")
@pytest.mark.it("should raise error when no secret found")
def test_errors_when_secret_not_found(
    mock_secretsmanager,
):
    """delete_secret() raise an error when no secret with the passed secret_identifier is found."""
    with pytest.raises(mock_secretsmanager.exceptions.ResourceNotFoundException):
        delete_secret("missile_codes")


@pytest.mark.describe("delete_secret()")
@pytest.mark.it("should raise error when passed blank secret_id")
def test_errors_when_passed_secret_id_is_blank(
    mock_secretsmanager,
):
    """delete_secret() raise an error when passed secret_id is blank."""
    with pytest.raises(BlankArgumentError):
        delete_secret("")
