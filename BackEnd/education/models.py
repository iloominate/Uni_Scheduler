from django.db import models
from django.forms import ValidationError
from authorization.models import User


class Subject(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(
        User,
        through="StudentSubject",
        related_name="student_subjects",
    )
    guarantor = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="guarantor_subject",
    )
    instructors = models.ManyToManyField(
        User,
        through="InstructorSubject",
        related_name="instructors_subjects",
    )
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "subject"


class Room(models.Model):
    number = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "room"


class ActivityType(models.Model):
    notation = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "activity_type"


class ActivityRepetition(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "activity_repetition"


class Activity(models.Model):
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    activity_repetition = models.ForeignKey(ActivityRepetition, on_delete=models.PROTECT)
    guarantor_notes = models.CharField(max_length=255, null=True)
    instructor_notes = models.CharField(max_length=255, null=True)
    duration = models.IntegerField()
    students = models.ManyToManyField(
        User,
        through="StudentActivity",
        related_name="student_activity",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="activity",
    )
    date_from = models.DateField()
    date_to = models.DateField()
    time = models.TimeField(null=True)
    day = models.CharField(max_length=3, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name="activity")
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="activity")

    def schedule_update(self, day, time, room_id):
        if day and time and room_id:
            hours = int(str(time).split(":")[0])
            if (hours + self.duration) > 17:
                raise ValidationError("Too late for activity.")
            time_to = f"{hours + self.duration}:00:00"
            for activity in Activity.objects.filter(room_id=room_id, time__lt=time_to, day=day):
                activity_to = int(str(activity.time).split(":")[0]) + activity.duration
                if activity_to > hours:
                    raise ValidationError("Collision room and time.")
            for activity in Activity.objects.filter(instructor=self.instructor, time__lt=time_to, day=day):
                activity_to = int(str(activity.time).split(":")[0]) + activity.duration
                if activity_to > hours:
                    raise ValidationError("Collision instructor and time.")

        self.day = day
        self.time = time
        self.room_id = room_id
        self.save()

    class Meta:
        db_table = "activity"
        unique_together = (("day", "time", "room"), ("day", "time", "instructor"))


class StudentActivity(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    class Meta:
        db_table = "student_activity"
        unique_together = ("student", "activity")


class StudentSubject(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    class Meta:
        db_table = "student_subject"
        unique_together = ("student", "subject")


class InstructorSubject(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    class Meta:
        db_table = "instructor_subject"
        unique_together = ("instructor", "subject")
