from atexit import register

import matplotlib as matplotlib
from autoscraper import AutoScraper
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from hod.models import Internal_mark, attendance, attendance_record, batch, scheme, semester_result, subject, \
    subject_to_staff
from student.models import profile_student
from login.models import MyUser
import login

from django.db.models import Sum, Max

# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np


def student_index(request):
    # Create your views here.

    url = 'https://ktu.edu.in/eu/core/announcements.htm'

    try:
        # url = 'https://ktu.edu.in/home.htm'

        wanted_list = ['ANNOUNCEMENTS', 'Dec 24, 2021', 'Exam Registration opened - B.Tech S3 and S5 (supplementary) '
                                                        'Jan 2022']
        scraper = AutoScraper()
        result = scraper.build(url, wanted_list)
        data1 = result[0]
        data2 = result[1]
        data3 = result[2]

        notif = {'data1': data1,
                 'data2': data2,
                 'data3': data3
                 }
        # request.session['notif'] = notif


    except:

        notif = {'data1': "KTU site cannot reach"}
    current_user = request.user
    user_id = current_user.username

    student_details_1 = profile_student.objects.get(register_no=user_id)
    name = student_details_1.first_name + " " + student_details_1.last_name
    # id = request.session['student_id']
    context = {'name': name}

    credit = 0
    subject_data = subject.objects.all()
    result_data_for_credit = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                            grade_point__gte=5)
    for i in result_data_for_credit:
        for j in subject_data:
            if j.id == i.subject_id:
                credit += j.credit

    supply = 0
    for i in subject_data:
        max_chance = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                    subject_id=i.id).aggregate(Max('no_of_chances'))
        result_data_for_supply = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                                subject_id=i.id,
                                                                no_of_chances=max_chance['no_of_chances__max'])
        for j in result_data_for_supply:
            if j.grade_point < 5:
                supply += 1

    max_sem = semester_result.objects.filter(university_no=student_details_1.university_no).aggregate(Max('semester'))
    highest_sem = max_sem['semester__max']

    data = []
    sem = []

    sgpa = 0
    for i in range(1, highest_sem + 1):
        sem_sgpa = 0
        sem_credit = 0
        for j in subject_data:
            max_chance = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                        subject_id=j.id, semester=i).aggregate(Max('no_of_chances'))
            result_data = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                         subject_id=j.id, semester=1,
                                                         no_of_chances=max_chance['no_of_chances__max'])
            for k in result_data:
                if k.subject_id == j.id:
                    if k.grade_point == -1:
                        sem_sgpa += (j.credit * 0)
                    else:
                        sem_sgpa += (j.credit * k.grade_point)
                    sem_credit += j.credit

        sgpa += (sem_sgpa / sem_credit)
        data.append(sgpa)
        sem.append(i)
    cgpa = sgpa / highest_sem

    x = np.array(data)
    y = np.array(sem)
    x = x.reshape(len(x), 1)

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()

    model.fit(x, y)
    ypred = model.predict(x)
    if highest_sem < 8:
        sem.append(highest_sem + 1)
        predict_sem = highest_sem + 1
        y = (model.coef_[0] * predict_sem) + model.intercept_
        predicted_sem = highest_sem + 1
        data.append(y)

    return render(request, 'student_index.html', {
        'context': context,
        'credit': credit,
        'supply': supply,
        'cgpa': cgpa,
        'notif': notif,
        'data': data,
        'sem': sem,
        'predicted_sem': predicted_sem
    })
    # return redirect(student_profile)


def student_profile(request):
    # name = request.session['student_name']
    current_user = request.user
    user_id = current_user.username

    student_details_1 = profile_student.objects.get(register_no=user_id)
    name = student_details_1.first_name + " " + student_details_1.last_name

    id = user_id
    student_data = profile_student.objects.filter(register_no=id)

    for i in student_data:
        print('student', i.id)
        student_id = i.id
        batch_id = i.batch
        date_of_birth = i.date_of_birth
        name_first = i.first_name
        name_last = i.last_name

    print(student_id)
    name = name_first + " " + name_last
    context = {'name': name}  # display the name

    batch_data = batch.objects.get(id=batch_id)
    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)

    date_dob = str(date_of_birth)  # dob can only display in html only as string type
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    internal_mark_data = Internal_mark.objects.filter(student_id=student_id)
    subject_data = subject.objects.all()
    for i in internal_mark_data:
        print(i.exam_type, i.mark)
    total_mark_list = []
    attendance_list = []
    sem_result_list = []

    st_id = student_details_1.id
    for i in assign_subject_data:

        sum_of_mark = Internal_mark.objects.filter(student_id=st_id, subject_id=i.subject_id).aggregate(Sum('mark'))
        print(sum_of_mark['mark__sum'])
        total_internal = sum_of_mark['mark__sum']
        print(total_internal)
        st_data = profile_student.objects.get(id=student_id)
        mark_tupple = (i.subject_id, st_data.register_no, i.semester, total_internal)
        # x print(mark_tupple)
        total_mark_list.append(mark_tupple)

        total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=i.subject_id).aggregate(
            Sum('no_of_hours'))
        attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=i.subject_id)
        total_hour = total_attendance['no_of_hours__sum']
        print('total_hour', total_hour, type(total_hour))
        attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=i.subject_id)

        if total_hour == None:
            att_tuple = (i.subject_id, st_data.register_no, i.semester, 0)
            attendance_list.append(att_tuple)

        else:
            hour = 0
            for j in attendance_data:
                if st_data.id == j.student_id:
                    if j.present == True:
                        id1 = j.attendance_record_id
                        # print('id',id1, type(id1))
                        no_of_hours_taken = attendance_record.objects.get(id=id1)

                        hour = hour + no_of_hours_taken.no_of_hours
            percentage_attendance = round((hour / total_hour) * 100, 2)
            print(st_data.first_name, hour)
            att_tuple = (i.subject_id, st_data.register_no, i.semester, percentage_attendance)
            attendance_list.append(att_tuple)

        max_chances = semester_result.objects.filter(subject_id=i.subject_id,
                                                     university_no=st_data.university_no).aggregate(
            Max('no_of_chances'))

        sem_result_data = semester_result.objects.filter(subject_id=i.subject_id, university_no=st_data.university_no,
                                                         no_of_chances=max_chances['no_of_chances__max'])

        print(max_chances['no_of_chances__max'])
        for result in sem_result_data:
            print(result)
            sem_result_tuple = (i.subject_id, st_data.register_no, i.semester, result.grade_point, result.no_of_chances)
            sem_result_list.append(sem_result_tuple)
    # print(attendance_list)
    print(total_mark_list)

    if 'edit_profile' in request.POST:

        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('date_of_birth')
        ph_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        address = request.POST.get('address')
        aadhaar_no = request.POST.get('aadhaar_no')
        caste = request.POST.get('caste')
        religion = request.POST.get('religion')
        nationality = request.POST.get('nationality')
        native_place = request.POST.get('native_place')
        blood_group = request.POST.get('blood_group')

        if gender == '0':
            messages.error(request, "Please select a valid Gender")
        elif blood_group == '0':
            messages.error(request, "Please select a valid blood Group")
        else:

            student_data1 = profile_student.objects.get(register_no=id)
            user_data = MyUser.objects.get(username=id)

            user_data.first_name = f_name
            user_data.last_name = l_name
            user_data.save()  # update the first and second name in login table

            student_data1.first_name = f_name
            student_data1.first_name = f_name
            student_data1.last_name = l_name
            student_data1.aadhar_no = aadhaar_no
            student_data1.address = address
            student_data1.phone_no = ph_no
            student_data1.email = email
            student_data1.sex = gender
            student_data1.date_of_birth = dob
            student_data1.nationality = nationality
            student_data1.religion = religion
            student_data1.caste = caste
            student_data1.native_place = native_place
            student_data1.blood_group = blood_group

            student_data1.save()

            messages.error(request, "Successfully updated")
            # return render(request, 'student_profile.html',
            #              {'student_data': student_data, 'scheme_data': scheme_data, 'batch_data': batch_data,
            #               'date_dob': date_dob, 'context': context})
            return redirect(student_profile)

    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = MyUser.objects.get(username=id)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")
        elif current_password != user_password:
            messages.error(request, "incorrect old password")
        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")
            return render(request, 'student_profile.html',
                          {'student_data': student_data, 'scheme_data': scheme_data, 'batch_data': batch_data,
                           'date_dob': date_dob, 'context': context})

    return render(request, 'student_profile.html',
                  {
                      'student_data': student_data,
                      'scheme_data': scheme_data,
                      'batch_data': batch_data,
                      'date_dob': date_dob,
                      'context': context,
                      'assign_subject_data': assign_subject_data,
                      'subject_data': subject_data,
                      'internal_mark_data': internal_mark_data,
                      'total_mark_list': total_mark_list,
                      'attendance_list': attendance_list,
                      'sem_result_list': sem_result_list
                  })


# logout
def log_out(request):
    logout(request)
    return redirect(login.views.login)
