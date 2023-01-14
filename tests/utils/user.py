class CaseInvalid:
    valid_user: dict

    @classmethod
    def invalid_user(cls, field: str = "email") -> dict:
        user = cls.valid_user.copy()
        match field:
            case "first_name":
                user["first_name"] = "Fernando 22"
            case "last_name":
                user["last_name"] = "Medeiros 22"
            case "username":
                user["username"] = "22-Medeiros 22"
            case "email":
                user["email"] = "@gmail.com"
            case "password":
                user["password"] = ""
        return user

    @classmethod
    def get_one_invalid_field(cls, field: str) -> dict:
        return {field: cls.invalid_user(field)[field]}


class CaseCreate(CaseInvalid):
    valid_user = {
        "first_name": "joao",
        "last_name": "silva",
        "username": "joaoSilva",
        "email": "joaosilva@gmail.com",
        "bday": "22",
        "bmonth": "8",
        "byear": "94",
        "password": "joaoteste@/[]()X",
    }

    @classmethod
    def get_one_valid_field(cls, field: str) -> dict:
        return {field: "new" + cls.valid_user[field]}


class CaseLogin(CaseInvalid):
    valid_user = {
        "first_name": "marcia",
        "last_name": "souza",
        "username": "marciaSouza",
        "email": "marciasouza@gmail.com",
        "bday": "01",
        "bmonth": "01",
        "byear": "2001",
        "password": "test123@@@@",
    }
    login = {"username": "marciasouza@gmail.com", "password": "test123@@@@"}
    content_type = {"Content-Type": "application/x-www-form-urlencoded"}
    headers = ["access_token", "refresh_token", "token_type"]
