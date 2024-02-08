from rest_framework import serializers
from authorization.models import Permission, User
from education.models import Activity, ActivityType, Room, Subject
from django.core.validators import MinValueValidator, MaxValueValidator


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = "__all__"


class ReadUserSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "permission",
        )


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    permission_id = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="ID of user's permission. \
            Get enum on 'api/auth/permissions/'",
    )

    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        existing_user = User.objects.filter(email=value).exclude(id=user_id).exists()

        if existing_user:
            raise serializers.ValidationError("User with this email already exists.")

        return value

    def validate_username(self, value):
        user_id = self.instance.id if self.instance else None
        existing_user = User.objects.filter(username=value).exclude(id=user_id).exists()

        if existing_user:
            raise serializers.ValidationError("User with this username already exists.")

        return value


class ReadRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ("id", "number", "description")


class RoomSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True)

    def validate_number(self, value):
        room_id = self.instance.id if self.instance else None
        existing_room = Room.objects.filter(number=value).exclude(id=room_id).exists()

        if existing_room:
            raise serializers.ValidationError("Room with this number already exists.")
        return value


class ReadSubjectSerializer(serializers.ModelSerializer):
    guarantor = ReadUserSerializer()

    class Meta:
        model = Subject
        fields = "__all__"


class SubjectSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    guarantor_id = serializers.IntegerField()

    def validate_code(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Subject code consists of 3 characters.")
        
        subject_id = self.instance.id if self.instance else None
        existing_subject = Subject.objects.filter(code=value).exclude(id=subject_id).exists()

        if existing_subject:
            raise serializers.ValidationError("Subject with this code already exists.")
        return value


class ReadActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = "__all__"


class ReadActivitySerializer(serializers.ModelSerializer):
    subject = ReadSubjectSerializer()
    activity_type = ReadActivityTypeSerializer()
    room = ReadRoomSerializer()
    instructor = ReadUserSerializer()

    class Meta:
        model = Activity
        fields = "__all__"


class ActivityGuarantorSerializer(serializers.Serializer):
    guarantor_notes = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    duration = serializers.IntegerField(validators=[MinValueValidator(1)])
    activity_type_id = serializers.IntegerField(
       help_text="ID of activity's type. \
           Get enum on 'api/auth/activity-type/'"
    )
    subject_id = serializers.IntegerField(
        help_text="ID of subject."
    )
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    activity_repetition_id = serializers.IntegerField(
       help_text="ID of activity's repetition. \
           Get enum on 'api/auth/activity-repetition/'"
    )


class ActivityInstructorSerializer(serializers.Serializer):
    #instructor_id = serializers.IntegerField()
    instructor_notes = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )


class ActivitySchedulerSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(validators=[MinValueValidator(1)])
    time = serializers.TimeField(
        help_text="Format HH:MM"
    )
    day = serializers.CharField(max_length=3)


class RegisterInstructorSerializer(serializers.Serializer):
    instructor = serializers.IntegerField(validators=[MinValueValidator(1)])
    subject = serializers.IntegerField(validators=[MinValueValidator(1)])
