class CaseInvalid:
    invalid_content = {"content": ""}


class CaseUpdate:
    update_invalid_content = {"content": ""}
    update_valid_content = {"content": "Hello Tech Recruiters!"}


class CaseCreate(CaseInvalid, CaseUpdate):
    valid_content = {"content": "Hello World"}
