from django.http import HttpResponse
from django.shortcuts import render
from atexit import register

# import matplotlib as matplotlib
from autoscraper import AutoScraper
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from hod.models import (
    Internal_mark,
    attendance,
    attendance_record,
    batch,
    scheme,
    semester_result,
    subject,
    subject_to_staff,
)
from student.models import profile_student
from login.models import MyUser
from parent.models import parent_profile as ppdb
import login

from django.db.models import Sum, Max

# %matplotlib inline
# import matplotlib.pyplot as plt
import numpy as np


def parent_index(request):
    # Create your views here.

    # url = "https://ktu.edu.in/eu/core/announcements.htm"

    # try:
    # # url = 'https://ktu.edu.in/home.htm'

    # wanted_list = [
    # "ANNOUNCEMENTS",
    # "Dec 24, 2021",
    # "Exam Registration opened - B.Tech S3 and S5 (supplementary) " "Jan 2022",
    # ]
    # scraper = AutoScraper()
    # result = scraper.build(url, wanted_list)
    # data1 = result[0]
    # data2 = result[1]
    # data3 = result[2]

    # notif = {"data1": data1, "data2": data2, "data3": data3}
    # # request.session['notif'] = notif

    # except:

    notif = {"data1": "KTU site cannot reach"}
    current_user = request.user
    user_id = current_user.username
    stud_id = ppdb.objects.get(parent_id=user_id).register_no_id
    student_details_1 = profile_student.objects.get(id=stud_id)
    name = student_details_1.first_name + " " + student_details_1.last_name
    # id = request.session['student_id']
    context = {"name": current_user.first_name + " " + current_user.last_name}

    credit = 0
    subject_data = subject.objects.all()
    result_data_for_credit = semester_result.objects.filter(
        university_no=student_details_1.university_no, grade_point__gte=5
    )
    for i in result_data_for_credit:
        for j in subject_data:
            if j.id == i.subject_id:
                credit += j.credit
    # print(credit)
    supply = 0
    for i in subject_data:
        max_chance = semester_result.objects.filter(
            university_no=student_details_1.university_no, subject_id=i.id
        ).aggregate(Max("no_of_chances"))
        result_data_for_supply = semester_result.objects.filter(
            university_no=student_details_1.university_no,
            subject_id=i.id,
            no_of_chances=max_chance["no_of_chances__max"],
        )
        for j in result_data_for_supply:
            if j.grade_point < 5:
                supply += 1

    max_sem = semester_result.objects.filter(
        university_no=student_details_1.university_no
    ).aggregate(Max("semester"))
    highest_sem = 8
    #   highest_sem = max_sem['semester__max']

    data = []
    sem = []

    sgpa = 0
    for i in range(1, highest_sem + 1):
        sem_sgpa = 0
        # sem_credit =
        sem_credit = 1
        for j in subject_data:
            max_chance = semester_result.objects.filter(
                university_no=student_details_1.university_no,
                subject_id=j.id,
                semester=i,
            ).aggregate(Max("no_of_chances"))
            result_data = semester_result.objects.filter(
                university_no=student_details_1.university_no,
                subject_id=j.id,
                semester=i,
                no_of_chances=max_chance["no_of_chances__max"],
            )
            for k in result_data:
                if k.subject_id == j.id:
                    if k.grade_point == -1:
                        sem_sgpa += j.credit * 0
                    else:
                        sem_sgpa += j.credit * k.grade_point
                    sem_credit += j.credit

        sgpa += sem_sgpa / sem_credit
        data.append(sgpa)
        sem.append(i)
    cgpa = round(sgpa / highest_sem, 2)

    x = np.array(data)
    y = np.array(sem)
    x = x.reshape(len(x), 1)

    from sklearn.linear_model import LinearRegression

    model = LinearRegression()

    model.fit(x, y)
    ypred = model.predict(x)

    predicted_sem = 2  # ADDED NOW
    if highest_sem < 8:
        sem.append(highest_sem + 1)
        predict_sem = highest_sem + 1
        y = (model.coef_[0] * predict_sem) + model.intercept_
        predicted_sem = highest_sem + 1
        data.append(y)

    return render(
        request,
        "parent_index.html",
        {
            "context": context,
            "credit": credit,
            "supply": supply,
            "cgpa": cgpa,
            "notif": notif,
            "data": data,
            "sem": sem,
            "predicted_sem": predicted_sem,
        },
    )
    # return redirect(student_profile)


def parent_profile(request):
    # name = request.session['student_name']
    current_user = request.user
    user_id = current_user.username
    parent_data = ppdb.objects.get(parent_id=user_id)

    context = {"name": current_user.first_name + " " + current_user.last_name}

    if "edit_profile" in request.POST:

        f_name = request.POST.get("first_name")
        l_name = request.POST.get("last_name")
        ph_no = request.POST.get("phone_no")
        email = request.POST.get("email")

        user_data = MyUser.objects.get(username=user_id)

        user_data.first_name = f_name
        user_data.last_name = l_name
        user_data.save()  # update the first and second name in login table

        parent_data.first_name = f_name
        parent_data.last_name = l_name
        parent_data.phone_no = ph_no
        parent_data.email = email

        parent_data.save()

        messages.error(request, "Successfully updated")

        return render(
            request,
            "parent_profile.html",
            {"parent_data": parent_data, "context": context, "s": 1},
        )

    if "change_password" in request.POST:
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        renew_password = request.POST.get("renew_password")

        user_data = MyUser.objects.get(username=user_id)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")
        elif current_password != user_password:
            messages.error(request, "incorrect old password")
        elif current_password == new_password:
            messages.error(request, "same password")
        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")
        return render(
            request,
            "parent_profile.html",
            {"parent_data": parent_data, "context": context, "s": 2},
        )
    return render(
        request,
        "parent_profile.html",
        {"parent_data": parent_data, "context": context, "s": 0},
    )


def parent_student_profile(request):
    # name = request.session['student_name']
    current_user = request.user
    user_id = current_user.username
    stud_id = ppdb.objects.get(parent_id=user_id).register_no_id

    student_details_1 = profile_student.objects.get(id=stud_id)
    name = student_details_1.first_name + " " + student_details_1.last_name

    id = stud_id
    student_data = profile_student.objects.filter(id=id)

    for i in student_data:
        student_id = i.id
        batch_id = i.batch
        date_of_birth = i.date_of_birth
        name_first = i.first_name
        name_last = i.last_name

    name = name_first + " " + name_last
    context = {
        "name": current_user.first_name + " " + current_user.last_name
    }  # display the name

    batch_data = batch.objects.get(id=batch_id)
    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)

    # dob can only display in html only as string type
    date_dob = str(date_of_birth)
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    internal_mark_data = Internal_mark.objects.filter(student_id=student_id)
    subject_data = subject.objects.all()
    total_mark_list = []
    attendance_list = []
    sem_result_list = []

    st_id = student_details_1.id
    for i in assign_subject_data:

        sum_of_mark = Internal_mark.objects.filter(
            student_id=st_id, subject_id=i.subject_id
        ).aggregate(Sum("mark"))
        total_internal = sum_of_mark["mark__sum"]
        st_data = profile_student.objects.get(id=student_id)
        mark_tupple = (i.subject_id, st_data.register_no, i.semester, total_internal)
        total_mark_list.append(mark_tupple)

        total_attendance = attendance_record.objects.filter(
            batch_id=batch_id, subject_id=i.subject_id
        ).aggregate(Sum("no_of_hours"))
        attendance_record_data = attendance_record.objects.filter(
            batch_id=batch_id, subject_id=i.subject_id
        )
        total_hour = total_attendance["no_of_hours__sum"]
        attendance_data = attendance.objects.filter(
            batch_id=batch_id, subject_id=i.subject_id
        )

        if total_hour == None:
            att_tuple = (i.subject_id, st_data.register_no, i.semester, 0)
            attendance_list.append(att_tuple)

        else:
            hour = 0
            for j in attendance_data:
                if st_data.id == j.student_id:
                    if j.present == True:
                        id1 = j.attendance_record_id
                        no_of_hours_taken = attendance_record.objects.get(id=id1)

                        hour = hour + no_of_hours_taken.no_of_hours
            percentage_attendance = round((hour / total_hour) * 100, 2)
            att_tuple = (
                i.subject_id,
                st_data.register_no,
                i.semester,
                percentage_attendance,
            )
            attendance_list.append(att_tuple)

        max_chances = semester_result.objects.filter(
            subject_id=i.subject_id, university_no=st_data.university_no
        ).aggregate(Max("no_of_chances"))

        sem_result_data = semester_result.objects.filter(
            subject_id=i.subject_id,
            university_no=st_data.university_no,
            no_of_chances=max_chances["no_of_chances__max"],
        )

        for result in sem_result_data:
            sem_result_tuple = (
                i.subject_id,
                st_data.register_no,
                i.semester,
                result.grade_point,
                result.no_of_chances,
            )
            sem_result_list.append(sem_result_tuple)

    return render(
        request,
        "parent_student_profile.html",
        {
            "student_data": student_data,
            "scheme_data": scheme_data,
            "batch_data": batch_data,
            "date_dob": date_dob,
            "context": context,
            "assign_subject_data": assign_subject_data,
            "subject_data": subject_data,
            "internal_mark_data": internal_mark_data,
            "total_mark_list": total_mark_list,
            "attendance_list": attendance_list,
            "sem_result_list": sem_result_list,
            "stud_name": name,
        },
    )


# logout
def log_out(request):
    logout(request)
    return redirect(login.views.login)


# Create your views here
