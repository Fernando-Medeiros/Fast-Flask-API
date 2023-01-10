class CaseInvalid:
    valid_user: dict
    
    def invalid_user(self, field: str = 'email') -> dict:
        user = self.valid_user.copy()
        match field:
            case 'first_name':
                user['first_name'] = 'Fernando 22'
            case 'last_name':
                user['last_name'] = 'Medeiros 22'
            case 'username':
                user['username'] = '22-Medeiros 22'
            case 'email':
                user['email'] = '@gmail.com'
            case 'password':
                user['password'] = ''
        return user

    def get_one_invalid_field(self, field: str) -> dict:
        return {field: self.invalid_user(field)[field]}


class CaseCreate(CaseInvalid):
    valid_user = {
        'first_name': 'joao',
        'last_name': 'silva',
        'username': 'joaoSilva',
        'email': 'joaosilva@gmail.com',
        'password': 'joaoteste@/[]()X'
        }

    def get_one_valid_field(self, field: str) -> dict:
        return {field: 'new' + self.valid_user[field]}


class CaseLogin(CaseInvalid):
    valid_user = {
        'first_name': 'marcia',
        'last_name': 'souza',
        'username': 'marciaSouza',
        'email': 'marciasouza@gmail.com',
        'password': 'test123@@@@'
        }
    login = {
        'username': 'marciasouza@gmail.com',
        'password': 'test123@@@@'
        }
    content_type = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    headers = ['access_token', 'token_type']
