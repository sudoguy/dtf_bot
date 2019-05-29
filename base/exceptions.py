from rest_framework.exceptions import APIException


class ObjectNotFound(APIException):
    status_code = 400
    default_detail = "Object not found"
    default_code = "object_not_found"


class InternalServiceError(APIException):
    status_code = 500
    default_detail = "Internal error"
    default_code = "internal_error"
