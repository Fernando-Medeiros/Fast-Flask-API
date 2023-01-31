class Base:
    data: dict

    @classmethod
    def invalid_user(cls, field: str = "email") -> dict:
        data = cls.data.copy()
        data[field] = data[field] + "    "
        return data

    @classmethod
    def get_one_invalid_field(cls, field: str) -> dict:
        return {field: cls.invalid_user(field).get(field)}

    @classmethod
    def get_one_valid_field(cls, field: str) -> dict:
        return {field: "new" + cls.data[field]}


class CaseCreate(Base):
    data = {
        "first_name": "joao",
        "last_name": "silva",
        "username": "joaoSilva",
        "email": "joaosilva@gmail.com",
        "password": "joaoteste@/[]()X",
    }


class CaseLogin(Base):
    data = {
        "first_name": "marcia",
        "last_name": "souza",
        "username": "marciaSouza",
        "email": "marciasouzaaaaaaaa@gmail.com",
        "password": "test123@@@@",
    }
    login = {"username": "marciasouzaaaaaaaa@gmail.com", "password": "test123@@@@"}
    content_type = {"Content-Type": "application/x-www-form-urlencoded"}
    headers = ["access_token", "refresh_token", "token_type"]


class CaseUserModel(Base):
    data = {
        "first_name": "marcia",
        "last_name": "souza",
        "email": "marciasouzaaaaaaaa@gmail.com",
        "password": "test123@@@@",
    }


class CaseProfileModel(Base):
    data = {
        "username": "marcia",
        "avatar": "t.png",
        "background": "t.png",
        "bio": "...",
    }
