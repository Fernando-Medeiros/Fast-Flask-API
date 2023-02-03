import pytest
from werkzeug.security import check_password_hash

from app.models.user import RecoverPassword, UpdatePassword
from tests.utils.client import CaseCreate


@pytest.mark.passwordModelRequest
def test_request_recover_password():
    request = RecoverPassword(**CaseCreate.data)

    assert request.email == CaseCreate.data.get("email")


@pytest.mark.passwordModelRequest
def test_request_update_password():
    request = UpdatePassword(**CaseCreate.data)

    assert check_password_hash(request.password, CaseCreate.data.get("password"))
