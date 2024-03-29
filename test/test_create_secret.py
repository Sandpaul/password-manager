"""This module contains the test suite for `create_secret()`."""

import os

import boto3
import pytest
from moto import mock_aws

from src.create_secret import create_secret, BlankArgumentError, InvalidCharacterError


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


@pytest.mark.describe("create_secret()")
@pytest.mark.it("should successfully create a secret in AWS secrets manager")
def test_secret_created(mock_secretsmanager, secret_identifier, user_id, password):
    """create_secret() should return 200 status code when successfully creating a new secret."""
    result = create_secret(secret_identifier, user_id, password)
    assert result == 200


@pytest.mark.describe("create_secret()")
@pytest.mark.it("should save SecretString correctly")
def test_secret_created_correctly(
    mock_secretsmanager, secret_identifier, user_id, password
):
    """create_secret() should create new secret with the correct SecretString."""
    create_secret(secret_identifier, user_id, password)
    response = mock_secretsmanager.get_secret_value(SecretId=secret_identifier)
    expected = "{'user_id':test_id, 'password':test_password}"
    assert response["SecretString"] == expected


@pytest.mark.describe("create_secret()")
@pytest.mark.it("should error when secret_identifier already exists")
def test_secret_already_exists_error(
    mock_secretsmanager, secret_identifier, user_id, password
):
    """create_secret() should raise an error if the secret_identifier already exists."""
    create_secret(secret_identifier, user_id, password)
    with pytest.raises(mock_secretsmanager.exceptions.ResourceExistsException):
        create_secret(secret_identifier, user_id, password)


@pytest.mark.describe("create_secret()")
@pytest.mark.it("should error when any argument is blank")
def test_blank_arguments_error(
    mock_secretsmanager, secret_identifier, user_id, password
):
    """create_secret() should raise an error if the any argument is blank."""
    blank_secret_identifier = ""
    blank_user_id = ""
    blank_password = ""
    with pytest.raises(BlankArgumentError):
        create_secret(blank_secret_identifier, user_id, password)
    with pytest.raises(BlankArgumentError):
        create_secret(secret_identifier, blank_user_id, password)
    with pytest.raises(BlankArgumentError):
        create_secret(secret_identifier, user_id, blank_password)


@pytest.mark.describe("create_secret()")
@pytest.mark.it("should error when invalid characters are used in secret_identifier")
def test_invalid_character_error(
    mock_secretsmanager, secret_identifier, user_id, password
):
    """create_secret() should raise an error if passed secret_identifier with invalid characters."""
    invalid_secret_identifier = "±±±"
    with pytest.raises(InvalidCharacterError):
        create_secret(invalid_secret_identifier, user_id, password)
