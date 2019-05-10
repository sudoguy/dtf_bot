from rest_framework.exceptions import APIException


class EntryNotFound(APIException):
    status_code = 400
    default_detail = "Entry not found"
    default_code = "entry_not_found"


class InternalServiceError(APIException):
    status_code = 500
    default_detail = "Internal error"
    default_code = "internal_error"
