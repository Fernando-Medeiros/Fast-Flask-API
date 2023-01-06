class CaseInvalid:
    valid_user: dict
    
    def invalid_user(self, field: str = 'email') -> dict:
        user = self.valid_user.copy()
        match field:
            case 'name':
                user['name'] = 'Fernando 22 Medeiros'
            case 'email':
                user['email'] = '@gmail.com'
            case 'password':
                user['password'] = ''
        return user


class CaseCreate(CaseInvalid):
    valid_user = {
        'name': 'user da silva',
        'email': 'user1silva@gmail.com',
        'password': 'test123'
        }


class CaseLogin(CaseInvalid):
    valid_user = {
        'name': 'user de souza',
        'email': 'usersouza@gmail.com',
        'password': 'test123'
        }
    valid_login = {
        'username': 'usersouza@gmail.com',
        'password': 'test123'
    }


class CaseAuth:
    valid_user = {
        'name': 'user das neves',
        'email': 'userneves@gmail.com',
        'password': 'test123'
    }
    data = {
        'username': 'userneves@gmail.com',
        'password': 'test123'
    }    
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }