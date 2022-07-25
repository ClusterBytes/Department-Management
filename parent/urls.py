from django.urls import path, include
from hod.views import log_out
from parent.views import parent_index, parent_profile,parent_student_profile

urlpatterns = [
    path("", parent_index, name="parent_index"),
    path("log_out/", log_out, name="log_out"),
    path("parent_profile/", parent_profile, name="parent_profile"),
    path("parent_student_profile/",parent_student_profile,name="parent_student_profile"),
    # path('student_feedback/',feedback,name='student_feedback'),
]
