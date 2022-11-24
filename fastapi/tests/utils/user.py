class TestUser:
    
    def valid_user(self) -> dict:
        return {
            'name': 'Jose Silva Santos',
            'email': 'josesilvasantos@gmail.com',
            'password': 'test123'
        }

    def invalid_user(self, field: str = 'email') -> dict:
        
        user = self.valid_user()

        match field:
            case 'name':
                user['name'] = '123567GA 13'
            case 'email':
                user['email'] = '@gmail.com'
            case 'password':
                user['password'] = ''

        return user