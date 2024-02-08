from django.urls import path
from education.api.views import *


urlpatterns = [
    # User's endpoints
    path("permission", get_permissions),
    path("user", get_users_or_create),
    path("user/<int:user_id>", rud_user),
    path("my-info", my_info),
    # Room's endpoints
    path("room", get_rooms_or_create),
    path("room/<int:room_id>", rud_room),
    # Subject's endpoints
    path("subject", get_subjects_or_create),
    path("subject/<int:subject_id>", rud_subject),
    # Student register subject
    path("register/<int:user_id>/<int:subject_id>", register_subject),
    # Activity
    path("activity", get_activity_or_create),
    path("activity/<int:activity_id>", delete_activity),
    path("activity/<int:activity_id>", get_activity),
    # Scheduler activity
    path("scheduler-activity/<int:activity_id>", activity_to_schedule),
    path("schedule-activity", schedule_activity),
    # Student subjects endpoint
    path("student_subjects/<int:student_id>", get_student_subjects),
    # Instructor register subject
    path("register_instructor/<int:instructor_id>/<int:subject_id>", register_instructor),
    # Instructor subject(s) endpoint
    path("instructor_subject/<int:instructor_id>", get_instructor_subject),
    # Get all instructos
    path("get_all_instructors", get_all_instructors),
    # Get all guarantor requests on this subject
    path("get_requests/<int:subject_id>", get_guarantor_requests),
    # Get all schedule subject activities
    path("subject_activities/<int:subject_id>", get_subject_activities),
    # Get all student activities in subject
    path("student_activities_subject/<int:student_id>/<int:subject_id>", get_student_activities_subject),
    # Student register activity
    path("student_register_activity/<int:student_id>/<int:activity_id>", student_register_activity),
    # Get all student activities
    path("student_activities/<int:student_id>", get_student_activities),
    # Instructor register activity
    path("instructor_register_activity/<int:instructor_id>/<int:activity_id>", instructor_register_activity),
    # Instructor get free activities
    path("instructor_free_activities/<int:subject_id>", get_instructor_free_activities),
    # Instructor activities
    path("instructor_activities/<int:instructor_id>", get_instructor_activities),

]
