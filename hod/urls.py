from django.urls import path, include
from hod.views import assign_subject_to_staff, delete_subject, hod_index, add_staff, log_out, subject_wise_report, \
    view_faculty, add_student, create_batch, view_student, view_student_details, view_tutor, hod_subject_wise_report, \
    hod_view_my_subject, hod_update_class, hod_my_subject_view_attendance, hod_my_subject_view_internal_result, \
    hod_my_subject_add_internal, hod_my_subject_add_attendance
from hod.views import view_batch, edit_batch, delete_batch, delete_faculty, faculty_profile, create_scheme
from hod.views import view_scheme, create_subject, view_subject, edit_subject
from hod.views import check_subject_exist, check_user_exist, batch_details



urlpatterns = [
    
    
    path('', hod_index, name='hod_index'),
    path('add_staff/', add_staff, name='add_staff'),
    path('log_out/', log_out, name='log_out'),
    path('view_faculty/', view_faculty, name='view_faculty'),
    path('add_student/', add_student, name='add_student'),
    path('create_batch/', create_batch, name='create_batch'),
    path('view_student/', view_student, name='view_student'),
    path('view_batch/', view_batch, name='view_batch'),
    path('edit_batch/<b_id>/', edit_batch, name='edit_batch'),
    path('delete_batch/<b_id>/', delete_batch, name='delete_batch'),
    path('delete_faculty/<f_id>/', delete_faculty, name='delete_faculty'),
    path('faculty_profile/ <f_id>/', faculty_profile, name='faculty_profile'),
    path('create_scheme/', create_scheme, name='create_scheme'),
    path('view_scheme/', view_scheme, name='view_scheme'),
    path('create_subject/', create_subject, name='create_subject'),
    path('view_subject/', view_subject, name='view_subject'),
    path('assign_subject/', assign_subject_to_staff, name='assign_subject_to_staff'),
    path('delete_subject/<subject_id>/', delete_subject, name='delete_subject'),
    path('edit_subject/<subject_id>/', edit_subject, name='edit_subject'),
    path('check_subject_exist', check_subject_exist, name='check_subject_exist'),
    path('check_user_exist', check_user_exist, name='check_user_exist'),
    path('batch_details/<b_id>/', batch_details, name='batch_details'),
    path('subject_wise_report/<int:subject_id>/<int:batch_id>/', hod_subject_wise_report, name='hod_subject_wise_report' ),
    path('view_student_details/<int:student_id>/', view_student_details, name='view_student_details' ),

    path('hod_view_my_subject/', hod_view_my_subject, name='hod_view_my_subject'),
    path('hod_update_class/<int:batch_id>/<int:subject_id>/', hod_update_class, name='hod_update_class'),
    path('hod_my_subject_attendance/<int:batch_id>/<int:subject_id>/', hod_my_subject_add_attendance, name='hod_my_subject_add_attendance'),
    path('hod_my_subject_internal/<int:batch_id>/<int:subject_id>/', hod_my_subject_add_internal, name='hod_my_subject_add_internal'),
    path('hod_my_subject_internal_result/<int:batch_id>/<int:subject_id>/', hod_my_subject_view_internal_result, name='hod_my_subject_view_internal_result'),
    path('hod_my_subject_view_attendance/<int:record_id>/<int:batch_id>/<int:subject_id>/', hod_my_subject_view_attendance, name='hod_my_subject_view_attendance'),
]