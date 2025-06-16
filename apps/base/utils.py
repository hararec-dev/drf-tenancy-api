from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            "error": {
                "status_code": response.status_code,
                "detail": response.data.get("detail", str(exc)),
                "code": response.data.get("code", None),
            }
        }
        if isinstance(response.data, dict) and "detail" not in response.data:
            custom_response_data["error"]["errors"] = response.data

        response.data = custom_response_data
    else:
        return Response(
            {
                "error": {
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "detail": "An unexpected error occurred on the server.",
                    "code": "server_error",
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
