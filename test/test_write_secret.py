"""This module contains the test suite for `write_secret()`."""

import os

import boto3
import pytest
from moto import mock_aws

from src.create_secret import create_secret
from src.get_secret import get_secret
from src.write_secret import write_secret


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
def secret_id():
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


@pytest.mark.describe("write_secret()")
@pytest.mark.it("should create a new text file")
def test_creates_new_file(
    mock_secretsmanager,
    secret_id,
    user_id,
    password,
    tmp_path,
):
    """get_secret() should successfully create a new text file"""
    create_secret(secret_id, user_id, password)
    secret_string = get_secret(secret_id)
    d = tmp_path / "sub"
    d.mkdir()
    p = d / secret_id
    assert len(list(d.iterdir())) == 0
    write_secret(p, secret_string)
    assert len(list(d.iterdir())) == 1


@pytest.mark.describe("write_secret()")
@pytest.mark.it("should create a new text file containing the correct secret string")
def test_saves_correct_data(
    mock_secretsmanager,
    secret_id,
    user_id,
    password,
    tmp_path,
):
    """get_secret() should save the retrieved secret user_id and password in a .txt file."""
    create_secret(secret_id, user_id, password)
    secret_string = get_secret(secret_id)
    d = tmp_path / "sub"
    d.mkdir()
    p = d / secret_id
    print(p)
    write_secret(p, secret_string)
    p2 = d / f"{secret_id}.txt"
    assert p2.read_text(encoding="utf-8") == secret_string
