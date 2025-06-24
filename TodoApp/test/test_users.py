from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



def test_return_user(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'MatthewTest'
    assert response.json()['email'] == 'matt@gmail.com'
    assert response.json()['first_name'] == 'Matthew'
    assert response.json()['last_name'] == 'Alexander'
    assert response.json()['user_role'] == 'admin'
    assert response.json()['phone_number'] == '+1-555-123-4567'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={"old_password":
                                                      "testpassword123",
                                                  "new_password":
                                                      "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_user(test_user):
    response = client.put("/user/password", json={"old_password":
                                                      "testwrongpassword123",
                                                  "new_password":
                                                      "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change."}


def test_change_phone_number_success(test_user):
    response = client.put("user/phone_number", json={
        "phone_number": "+1-555-111-2222"})

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_invalid_phone_number(test_user):
    """
    Test invalid phone numbers from users -> checked by
    PhoneNumberUpdate(BaseModel) in users.py
    :param test_user:
    :return:
    """

    response = client.put("user/phone_number", json={
        "phone_number": "+1-5x5-1x1-2@1"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json()['detail']) == 1
    assert response.json() == {
        'detail': [
            {'type': 'value_error',
             'loc': ['body', 'phone_number'],
             'msg': 'Value error, Invalid phone number format',
             'input': '+1-5x5-1x1-2@1',
             'ctx': {'error': {}}
             }
        ]
    }

