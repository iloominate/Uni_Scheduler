from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {
                    "success": False,
                    "errors": "Permissions denied.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return func(request, *args, **kwargs)

    return wrapper


def handle_error(func):
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as ex:
            raise ValidationError(str(ex))

    return wrapper


def api_access(level: int):
    """
    level 1 - admin
    level 2 - guarantor
    level 3 - instructor
    level 4 - scheduler
    level 5 - student
    """
    if level not in [1, 2, 3, 4, 5]:
        raise ValueError(
            "Invalid level. Please provide a valid level (1, 2, 3, 4, 5)."
        )

    def decorator(func):
        @login_required
        def wrapper(request, *args, **kwargs):
            access = request.user.permission_id
            if access != 1 or access != level:
                return Response(
                    {
                        "success": False,
                        "errors": "Permissions denied.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
