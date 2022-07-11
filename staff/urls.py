from django.urls import path, include
from staff.views import add_attendance,performance_analysis, add_internal, add_result, add_sem_result, report,  staff_index, log_out, staff_profile, tutor_subject_wise_report, university_result, update_class, update_class_of_tutor, update_student_profile, view_attendance, view_classes, view_internal_result, view_subjects

urlpatterns = [
    path('', staff_index, name='staff_index'),
    path('log_out/', log_out, name='log_out'),
    path('staff_profile/', staff_profile, name='staff_profile' ),
    path('view_subjects/', view_subjects, name='view_subjects' ),
    path('update_class/<int:batch_id>/<int:subject_id>/', update_class, name='update_class' ),
    path('attendance/<int:batch_id>/<int:subject_id>/', add_attendance, name='attendance' ),
    path('internal/<int:batch_id>/<int:subject_id>/', add_internal, name='internal' ),
    path('internal_result/<int:batch_id>/<int:subject_id>/', view_internal_result, name='view_internal_result' ),
    path('view_attendance/<int:record_id>/<int:batch_id>/<int:subject_id>/', view_attendance, name='view_attendance' ),
    path('view_classess/', view_classes, name='view_classes' ),
    path('update_class_of_tutor/<int:batch_id>/', update_class_of_tutor, name='update_class_of_tutor' ),
    path('tutorsubject_wise_report/<int:subject_id>/<int:batch_id>/', tutor_subject_wise_report, name='tutor_subject_wise_report' ),
    path('university_result/<int:batch_id>/', university_result, name='university_result' ),
    path('update_student_profile/<int:student_id>/', update_student_profile, name='update_student_profile' ),
    path('add_result/<int:batch_id>/', add_result, name='add_result' ),
    path('add_sem_result/<int:batch_id>/<str:month>/<int:year>/<int:semester>/', add_sem_result, name='add_sem_result' ),
    path('report/<int:batch_id>/<int:semester>/', report, name='report'),
    path('performance_analysis /<int:batch_id>/', performance_analysis, name='performance_analysis'),

]