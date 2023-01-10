
class CaseInvalid:
    invalid_content = {'content': ''}
    

class CaseUpdate:
    update_invalid_content = {'content': ''}
    update_valid_content = {'content': 'Hello Tech Recruiters!'}


class CaseCreate(CaseInvalid, CaseUpdate):
    valid_content = {
        'content': 'Hello World'
        }

    valid_model_content = {
        'id': 1,
        'author': 1,
        'date': '2023-01-09',
        'time': '20:08:50',
        'content': 'Hello World'
        }