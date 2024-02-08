from rest_framework.response import Response
from rest_framework.decorators import api_view
from authorization.decorators import handle_error
from authorization.models import Permission, User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from education.models import *
from education.api.serializers import *
from education.api.doc_responses import *
from django.db.models import Q
from datetime import datetime


def api_access(request, level):
    user = request.user
    if (not user.is_authenticated) or user.permission.level > level:
        raise ValidationError("Permissions denied.")


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_PERMISSION,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_permissions(request):
    """Get all permission levels"""

    api_access(request, 5)
    permissions = Permission.objects.all()
    serializator = PermissionSerializer(permissions, many=True)
    return Response({"data": serializator.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_USER,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def my_info(request):
    api_access(request, 5)
    serializer = ReadUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_USER,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="post",
    request_body=UserSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["GET", "POST"])
@handle_error
def get_users_or_create(request):
    """Read users or create new"""

    if request.method == "GET":
        api_access(request, 2)
        params = request.GET.dict()
        users = User.objects.filter(**params)
        serializator = ReadUserSerializer(users, many=True)
        return Response({"data": serializator.data})
    elif request.method == "POST":
        api_access(request, 1)
        serializator = UserSerializer(data=request.data)
        if serializator.is_valid():
            User.objects.create_user(**serializator.data)
            return Response({"success": True, "errors": None})
        else:
            return Response(
                {"success": False, "errors": serializator.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_USER,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="put",
    request_body=UserSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_USER,
    },
)
@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_USER,
    },
)
@api_view(["GET", "PUT", "DELETE"])
@handle_error
def rud_user(request, user_id):
    """Read, update or delete user"""

    if request.method == "GET":
        api_access(request, 5)
        user = User.objects.get(id=user_id)
        serializator = ReadUserSerializer(user)
        return Response({"data": serializator.data})
    elif request.method == "PUT":
        api_access(request, 1)
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return Response(
                {
                    "success": False,
                    "errors": "User does not exist.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializator = UserSerializer(instance=user[0], data=request.data)
        if serializator.is_valid():
            user.update(**serializator.validated_data)
            return Response({"success": True, "errors": None})
        else:
            return Response(
                {"success": False, "errors": serializator.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == "DELETE":
        api_access(request, 1)
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return Response(
                {
                    "success": False,
                    "errors": "User does not exist.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        subject = Subject.objects.filter(guarantor=user[0]).first()
        if subject:
            return Response(
                {
                    "errors": [f"Cannot delete guarantor before subject '{subject.code}'"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.delete()
        return Response({"success": True, "errors": None})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_ROOM,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="post",
    request_body=RoomSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["GET", "POST"])
@handle_error
def get_rooms_or_create(request):
    """Read rooms or create new"""

    if request.method == "GET":
        api_access(request, 4)
        rooms = Room.objects.all()
        serializator = ReadRoomSerializer(rooms, many=True)
        return Response({"data": serializator.data})
    elif request.method == "POST":
        api_access(request, 1)
        serializator = RoomSerializer(data=request.data)
        if serializator.is_valid():
            Room.objects.create(**serializator.data)
            return Response({"success": True, "errors": None})
        else:
            return Response(
                {"success": False, "errors": serializator.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_ROOM,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="put",
    request_body=RoomSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_ROOM,
    },
)
@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_ROOM,
    },
)
@api_view(["GET", "PUT", "DELETE"])
@handle_error
def rud_room(request, room_id):
    """Read, update or delete room"""

    if request.method == "GET":
        api_access(request, 4)
        room = Room.objects.get(id=room_id)
        serializator = ReadRoomSerializer(room)
        return Response({"data": serializator.data})
    elif request.method == "PUT":
        room = Room.objects.filter(id=room_id)
        if not room.exists():
            return Response(
                {
                    "success": True,
                    "errors": "Room does not exist.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializator = RoomSerializer(instance=room[0], data=request.data)
        if serializator.is_valid():
            room.update(**serializator.validated_data)
            return Response({"success": True, "errors": None})
        else:
            return Response(
                {"success": False, "errors": serializator.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == "DELETE":
        api_access(request, 1)
        room = Room.objects.filter(id=room_id)
        if not room.exists():
            return Response(
                {
                    "success": True,
                    "errors": "Room does not exist.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        room.delete()
        return Response({"success": True, "errors": None})


@swagger_auto_schema(
    method="get",
    manual_parameters=get_parameters_from_serializer(ReadSubjectSerializer),
    responses={
        200: OK_200_RESPONSE_SUBJECT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="post",
    request_body=SubjectSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["GET", "POST"])
@handle_error
def get_subjects_or_create(request):
    """Read subjects or create new"""

    if request.method == "GET":
        params = request.GET.dict()
        subjects = Subject.objects.filter(**params)
        serializator = ReadSubjectSerializer(subjects, many=True)
        return Response({"data": serializator.data})
    elif request.method == "POST":
        api_access(request, 1)
        serializator = SubjectSerializer(data=request.data)
        if serializator.is_valid():
            subject = Subject.objects.create(**serializator.data)
            InstructorSubject.objects.create(
                subject=subject, instructor=subject.guarantor
            )
            return Response({"success": True, "errors": None})
        else:
            return Response(
                {"success": False, "errors": serializator.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_SUBJECT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="put",
    request_body=SubjectSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_SUBJECT,
    },
)
@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_SUBJECT,
    },
)
@api_view(["GET", "PUT", "DELETE"])
@handle_error
def rud_subject(request, subject_id):
    """Read, update or delete subject"""

    if request.method == "GET":
        subject = Subject.objects.get(id=subject_id)
        serializator = ReadSubjectSerializer(subject)
        return Response({"data": serializator.data})
    elif request.method == "PUT":
        api_access(request, 1)
        subject = Subject.objects.filter(id=subject_id)
        if not subject.exists():
            return Response(
                {
                    "success": True,
                    "errors": "Subject does not exist.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializator = SubjectSerializer(instance=subject[0], data=request.data)
        if serializator.is_valid():
            subject.update(**serializator.validated_data)
            return Response({"success": True, "errors": None})
        else:
            return Response(
                {"success": False, "errors": serializator.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == "DELETE":
        api_access(request, 1)
        subject = Subject.objects.filter(id=subject_id)
        if not subject.exists():
            return Response(
                {
                    "success": True,
                    "errors": "Subject does not exist.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        InstructorSubject.objects.filter(subject=subject[0]).delete()
        subject.delete()
        return Response({"success": True, "errors": None})


@swagger_auto_schema(
    method="post",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_STUDENT_SUBJECT,
    },
)
@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_STUDENT_SUBJECT,
    },
)
@api_view(["POST", "DELETE"])
def register_subject(request, user_id, subject_id):
    """Register subject to user"""
    api_access(request, 5)
    if request.method == "POST":
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return Response(
                {
                    "success": False,
                    "errors": "User doesn't exist.",
                }
            )

        if user[0].permission_id != 5:
            return Response(
                {
                    "success": False,
                    "errors": "User can't register subject.",
                }
            )

        subject = Subject.objects.filter(id=subject_id)
        if not subject.exists():
            return Response(
                {
                    "success": False,
                    "errors": "Subject doesn't exist.",
                }
            )

        StudentSubject.objects.create(
            student=user[0],
            subject=subject[0],
        )
        return Response(
            {
                "success": True,
                "errors": None,
            }
        )
    elif request.method == "DELETE":
        student_subject = StudentSubject.objects.filter(
            student_id=user_id,
            subject_id=subject_id,
        )

        if not student_subject.exists():
            return Response(
                {
                    "success": False,
                    "errors": "Student didn't register subject.",
                }
            )

        student_subject.delete()
        # Delete registered activities
        user = User.objects.get(id=user_id)
        subject = Subject.objects.get(id=subject_id)

        activities = subject.activity.all()
        student_activities = StudentActivity.objects.filter(student=user, activity__in=activities)
        student_activities.delete()

        return Response(
            {
                "success": True,
                "errors": None,
            }
        )


@swagger_auto_schema(
    method="get",
    manual_parameters=get_parameters_from_serializer(ReadActivitySerializer),
    responses={
        200: OK_200_RESPONSE_SUBJECT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="post",
    request_body=ActivityGuarantorSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_STUDENT_SUBJECT,
    },
)
@api_view(["GET", "POST"])
@handle_error
def get_activity_or_create(request):
    if request.method == "GET":
        params = request.GET.dict()
        if params.get("instructor__isnull"):
            print(bool(params["instructor__isnull"]))
            params["instructor__isnull"] = bool(params["instructor__isnull"])
        activity = Activity.objects.filter(**params)
        serializator = ReadActivitySerializer(activity, many=True)
        return Response({"data": serializator.data})
    elif request.method == "POST":
        api_access(request, 4)
        serializator = ActivityGuarantorSerializer(data=request.data)
        if serializator.is_valid():
            Activity.objects.create(**serializator.data)
            return Response({"success": True, "errors": None})
        else:
            return Response(
                {"success": False, "errors": serializator.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_USER,
    },
)
@api_view(["DELETE"])
@handle_error
def delete_activity(request, activity_id):
    api_access(request, 4)
    activity = Activity.objects.filter(id=activity_id)
    if not activity.exists():
        return Response(
            {
                "success": True,
                "errors": "Activity does not exist.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    activity.delete()
    return Response({"success": True, "errors": None})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_USER,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_activity(request, activity_id):
    api_access(request, 5)
    activity = Activity.objects.filter(id=activity_id)
    if not activity.exists():
        return Response(
            {
                "success": False,
                "errors": "Activity doesn't exist"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializator = ReadSubjectSerializer(activity)
    return Response({"data": serializator.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_SUBJECT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_student_subjects(request, student_id):
    api_access(request, 5)
    student = User.objects.get(id=student_id)
    subjects = student.student_subjects
    serializer = ReadSubjectSerializer(subjects, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def schedule_activity(request):
    api_access(request, 4)
    activity = Activity.objects.filter(instructor__isnull=False)
    serializator = ReadActivitySerializer(activity, many=True)
    return Response({"data": serializator.data})


@swagger_auto_schema(
    method="post",
    request_body=ActivitySchedulerSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_ACTIVITY,
    },
)
@swagger_auto_schema(
    method="delete",
    request_body=ActivitySchedulerSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_ACTIVITY,
    },
)
@api_view(["POST", "DELETE"])
@handle_error
def activity_to_schedule(request, activity_id):
    if request.method == "POST":
        api_access(request, 4)
        serializator = ActivitySchedulerSerializer(data=request.data)
        if serializator.is_valid():
            activity = Activity.objects.get(id=activity_id)
            activity.schedule_update(**serializator.validated_data)
            return Response({"success": True, "errors": None})
    elif request.method == "DELETE":
        api_access(request, 4)
        activity = Activity.objects.get(id=activity_id)
        activity.schedule_update(room_id=None, time=None, day=None)
        return Response({"success": True, "errors": None})


@swagger_auto_schema(
    method="post",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["POST", "DELETE"])
@handle_error
def register_instructor(request, instructor_id, subject_id):
    api_access(request, 2)
    # add check if its instructor
    if request.method == "POST":
        try:
            User.objects.get(id=instructor_id)
            Subject.objects.get(id=subject_id)

        except User.DoesNotExist or Subject.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Instructor or Subject does not exist.",

                }, status=status.HTTP_400_BAD_REQUEST
            )

        InstructorSubject.objects.create(
            instructor_id=instructor_id,
            subject_id=subject_id,
        )

        return Response({"success": True, "errors": None})

    elif request.method == "DELETE":

        instructor_subject = InstructorSubject.objects.filter(
            instructor_id=instructor_id,
            subject_id=subject_id,
        )

        if not instructor_subject.exists():
            return Response(
                {
                    "success": False,
                    "errors": "Instructor didn't registered on the subject.",
                }
            )

        activities = Activity.objects.filter(instructor_id=instructor_id, subject_id=subject_id)
        for a in activities:
            a.students.clear()
        activities.update(instructor_id=None, day=None, time=None, room_id=None)

        instructor_subject.delete()
        return Response(
            {
                "success": True,
                "errors": None,
            }
        )


@swagger_auto_schema(
    method="post",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["POST"])
@handle_error
def get_instructor_subject(request, instructor_id):
    api_access(request, 3)
    instructor = User.objects.get(id=instructor_id)
    subjects = instructor.instructors_subjects
    serializer = ReadSubjectSerializer(subjects, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_all_instructors(request):
    api_access(request, 2)
    instructors = User.objects.filter(
        Q(permission__id=3)
    )

    serializer = ReadUserSerializer(instructors, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_guarantor_requests(request, subject_id):
    api_access(request, 4)
    activities = Activity.objects.filter(
        Q(subject__id=subject_id) & Q(time__isnull=True)
    )
    serializer = ReadActivitySerializer(activities, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_subject_activities(request, subject_id):
    api_access(request, 5)
    activities = Activity.objects.filter(
        Q(subject__id=subject_id) & Q(time__isnull=False)
    )
    serializer = ReadActivitySerializer(activities, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_student_activities_subject(request, student_id, subject_id):
    api_access(request, 5)
    student = User.objects.get(id=student_id)
    activities = student.student_activity.filter(Q(subject__id=subject_id))
    serializer = ReadActivitySerializer(activities, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="post",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["POST", "DELETE"])
@handle_error
def student_register_activity(request, student_id, activity_id):
    api_access(request, 5)
    if request.method == "POST":
        try:
            User.objects.get(id=student_id)
            Activity.objects.get(id=activity_id)

        except User.DoesNotExist or Activity.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Student or Activity does not exist.",

                }, status=status.HTTP_400_BAD_REQUEST
            )

        StudentActivity.objects.create(
            student_id=student_id,
            activity_id=activity_id,
        )

        return Response({"success": True, "errors": None})

    elif request.method == "DELETE":

        student_activity = StudentActivity.objects.filter(
            student_id=student_id,
            activity_id=activity_id,
        )

        if not student_activity.exists():
            return Response(
                {
                    "success": False,
                    "errors": "Student didn't register this activity.",
                }
            )

        student_activity.delete()
        return Response(
            {
                "success": True,
                "errors": None,
            }
        )


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_SUBJECT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_student_activities(request, student_id):
    api_access(request, 5)
    student = User.objects.get(id=student_id)
    # params = request.GET.dict()
    # activities = student.student_activity.filter(**params)
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    def get_week_number(date):
        return datetime.strptime(date, "%Y-%m-%d").isocalendar()[1]

    activities = student.student_activity.all()

    if date_from and date_to:
        activities = activities.filter(date_from__lte=date_to, date_to__gte=date_from)

        week_number_from = get_week_number(date_from)

        for activity in activities:
            repetition_name = activity.activity_repetition.name

            if repetition_name in ['Every week', 'One time']:
                continue

            if (repetition_name == 'Even week' and week_number_from % 2 == 0) or \
                    (repetition_name == 'Odd week' and week_number_from % 2 != 0):
                continue
            else:
                activities = activities.exclude(id=activity.id)

    serializer = ReadActivitySerializer(activities, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="delete",
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@swagger_auto_schema(
    method="post",
    request_body=ActivityInstructorSerializer,
    responses={
        200: OK_200_RESPONSE_DEFAULT,
        403: ERROR_403_RESPONSE_DEFAULT,
        404: ERROR_404_RESPONSE_DEFAULT,
    },
)
@api_view(["POST", "DELETE"])
@handle_error
def instructor_register_activity(request, instructor_id, activity_id):
    api_access(request, 3)
    if request.method == "POST":
        try:
            instructor = User.objects.get(id=instructor_id)
            activity = Activity.objects.get(id=activity_id)

        except User.DoesNotExist or Activity.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Instructor or Activity does not exist.",

                }, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ActivityInstructorSerializer(data=request.data)
        if serializer.is_valid():
            activity.instructor = instructor
            activity.instructor_notes = request.data['instructor_notes']
            activity.save()

            return Response({"success": True, "errors": None})

    elif request.method == "DELETE":
        try:
            activity = Activity.objects.get(id=activity_id)
            instructor = User.objects.get(id=instructor_id)

        except User.DoesNotExist or Activity.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": "Instructor or Activity does not exist.",

                }, status=status.HTTP_400_BAD_REQUEST

            )

        if activity.instructor == instructor:

            activity.instructor = None
            activity.instructor_notes = None
            activity.room_id = None
            activity.time = None
            activity.day = None

            StudentActivity.objects.filter(activity_id=activity_id).delete()

            activity.save()
            return Response(
                {
                    "success": True,
                    "errors": None,
                }
            )
        else:
            return Response(
                {
                    "success": False,
                    "error": "Instructor does not match.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_SUBJECT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_instructor_free_activities(request, subject_id):
    api_access(request, 3)
    activities = Activity.objects.filter(
        Q(subject__id=subject_id) &
        Q(instructor__isnull=True) &
        Q(time__isnull=True)
    )

    serializer = ReadActivitySerializer(activities, many=True)
    return Response({"data": serializer.data})


@swagger_auto_schema(
    method="get",
    responses={
        200: OK_200_RESPONSE_SUBJECT,
        403: ERROR_403_RESPONSE_DEFAULT,
    },
)
@api_view(["GET"])
@handle_error
def get_instructor_activities(request, instructor_id):
    api_access(request, 3)
    instructor = User.objects.get(id=instructor_id)

    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    def get_week_number(date):
        return datetime.strptime(date, "%Y-%m-%d").isocalendar()[1]

    activities = instructor.activity.filter(Q(time__isnull=False))

    if date_from and date_to:
        activities = activities.filter(date_from__lte=date_to, date_to__gte=date_from)

        week_number_from = get_week_number(date_from)

        for activity in activities:
            repetition_name = activity.activity_repetition.name

            if repetition_name in ['Every week', 'One time']:
                continue

            if (repetition_name == 'Even week' and week_number_from % 2 == 0) or \
                    (repetition_name == 'Odd week' and week_number_from % 2 != 0):
                continue
            else:
                activities = activities.exclude(id=activity.id)

    serializer = ReadActivitySerializer(activities, many=True)
    return Response({"data": serializer.data})

