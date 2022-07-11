from ast import For
import code
from datetime import date, datetime
from itertools import count
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Sum, Max

import login
from hod.models import Internal_mark, attendance, attendance_record, batch, scheme, semester_result, subject, \
    subject_to_staff
from login.models import MyUser
from staff.models import profile
from student.models import parents, profile_student, qualifications
from hod.models import batch
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import hod
from django.contrib.auth.decorators import login_required
from autoscraper import AutoScraper


# Create your views here.
# print(make_password('123'))
# print(check_password('1', '1'))

@login_required
def hod_index(request):
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
        #request.session['notif'] = notif


    except:

        notif = {'data1': "KTU site cannot reach"}
        request.session['notif'] = notif

    current_user = request.user
    print(current_user.id)
    # print( request.session['user'])
    # return redirect(view_faculty)
    current_user = request.user
    staff_id = current_user.username
    # staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    # notif = request.session['notif']

    years = []
    data = []
    student_count = profile_student.objects.all().count()
    batch_data = batch.objects.all()
    for i in batch_data:
        dat = i.date_of_join
        print(dat.year)
        years.append(dat.year)
        st_count = profile_student.objects.filter(batch=i.id).count()
        data.append(st_count)
    print(years, data)
    staff_count = profile.objects.all().count()
    batch_count = batch.objects.all().count()
    return render(request, 'hod_index.html',
                  {
                      'context': context,
                      'data_for_self_profile': staff_details_1,
                      "staff_count": staff_count,
                      "student_count": student_count,
                      'batch_count': batch_count,
                      'years': years,
                      'data': data,
                      'notif': notif,
                  })


# staff code
@login_required
def add_staff(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username
    # staff_id = request.session['hod_username']
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_joining = request.POST.get('date_of_joining')
        full_name = first_name + " " + last_name
        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')

        if password1 != password2:
            messages.error(request, 'Password mismatch')
        else:
            user = MyUser.objects.filter(username=username)
            if user:
                messages.error(request, 'User already exist')
            else:
                # enc_pswrd = make_password(password1)
                # user = super().save(commit=False)
                password = make_password(password1)
                MyUser.objects.create(username=username,
                                      first_name=first_name,
                                      last_name=last_name,
                                      password=password,
                                      is_faculty=True,
                                      is_active=True,
                                      is_student=False,
                                      is_hod=False

                                      )

                profile.objects.create(Faculty_unique_id=username, First_name=first_name, Last_name=last_name,
                                       Date_of_Joining=date_of_joining)
                messages.error(request, 'Faculty ' + full_name + ' successfully added')

    return render(request, 'add_staff.html', {"context": context, "data_for_self_profile": staff_details_1})


@login_required
def view_faculty(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username
    # print(staff)
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    staff_details = profile.objects.all()
    batch_data = batch.objects.all()

    return render(request, 'view_faculty.html',
                  {"staff_data": staff_details, "context": context, "data_for_self_profile": staff_details_1,
                   'batch_data': batch_data
                   })


@login_required
def delete_faculty(request, f_id):
    # check the faculty for delete is hod or not
    login_data = MyUser.objects.get(username=f_id)
    f_data = profile.objects.get(Faculty_unique_id=f_id)

    if login_data.is_hod:
        messages.error(request, 'Cannot delete your account ' + f_data.First_name + f_data.Last_name)
        return redirect(view_faculty)
    else:
        f_data.delete()
        login_delete = MyUser.objects.get(username=f_id)
        login_delete.delete()
        messages.error(request, 'Successfully deleted the faculty ' + f_data.First_name + f_data.Last_name)
        return redirect(view_faculty)


@login_required
def faculty_profile(request, f_id):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    staff_details = profile.objects.get(Faculty_unique_id=f_id)
    date = str(staff_details.Date_of_Joining)
    dob = str(staff_details.Date_of_Birth)

    print(staff_details.Profile_photo.url)

    if 'edit_profile' in request.POST:
        photo = request.POST.get('profile_photo')
        print(photo)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        faculty_unique_id = request.POST.get('faulty_unique_id')
        gender = request.POST.get('gender')
        print(first_name)
        if gender == '0':
            messages.error(request, 'Please select the valid gender')
        else:

            # please validate gender

            dob = request.POST.get('date_of_birth')
            phone_no = request.POST.get('phone_no')
            email = request.POST.get('email')
            aadhaar_no = request.POST.get('aadhaar_no')
            caste = request.POST.get('caste')
            religion = request.POST.get('religion')
            category = request.POST.get('category')
            pan = request.POST.get('pan')
            date_of_joining = request.POST.get('date_of_joining')
            aicte_unique_id = request.POST.get('aicte_unique_id')
            appointment_type = request.POST.get('appointment_type')
            cadre = request.POST.get('cadre')
            designation = request.POST.get('designation')
            specialisation = request.POST.get('specialisation')
            department_of_program = request.POST.get('department_of_program')
            examiner_institution = request.POST.get('examiner_institution')
            area_of_research = request.POST.get('area_of_research')

            # print(name, gender,faculty_unique_id, dob, phone_no,email, aadhaar_no, caste, religion, category, cadre)

            #  staff_details.Faculty_unique_id = faculty_unique_id
            staff_details.First_name = first_name
            staff_details.Last_name = last_name
            staff_details.Gender = gender
            staff_details.Date_of_Birth = dob
            staff_details.Aadhar_No = aadhaar_no
            staff_details.Caste = caste
            staff_details.Religion = religion
            staff_details.category = category
            staff_details.PAN = pan

            staff_details.Date_of_Joining = date_of_joining
            staff_details.AICTE_unique_Id = aicte_unique_id

            staff_details.Appointment_type = appointment_type
            staff_details.Cadre = cadre
            staff_details.Designation = designation
            staff_details.Specialisation = specialisation
            staff_details.Department_of_program = department_of_program
            staff_details.Examiner_institution = examiner_institution
            staff_details.Area_of_Research = area_of_research
            staff_details.email = email
            staff_details.phone_no = phone_no
            staff_details.save()

    if 'change_password' in request.POST:
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = MyUser.objects.get(username=f_id)
        if new_password != renew_password:
            messages.error(request, "Password mismatch")
        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")

    return render(request, 'faculty_profile.html',
                  {'context': context, 'staff_details': staff_details, 'date': date, 'date_dob': dob,
                   "data_for_self_profile": staff_details_1})


@login_required
# student view
@csrf_exempt
def check_user_exist(request):
    username = request.POST.get('username')
    subject_exist = MyUser.objects.filter(username=username).exists()
    if subject_exist:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required
def add_student(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data_class = batch.objects.all()  # for display the existing batch details
    # batch_data_year = batch.objects.all().distinct('date_of_join')
    scheme_data = scheme.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        batch_id_str = request.POST.get('batch_id')
        batch_id_int = int(batch_id_str)

        full_name = first_name + " " + last_name

        password1 = request.POST.get('password_1')
        password2 = request.POST.get('password_2')

        if batch_id_int == 0:
            messages.error(request, 'Please select Class')
        else:

            batch_data = batch.objects.get(id=batch_id_int)
            class_name = batch_data.class_name
            batch_year = batch_data.date_of_join
            semester = batch_data.semester

            if password1 != password2:
                messages.error(request, 'Password mismatch')
            else:

                user = MyUser.objects.filter(username=username)
                if user:
                    messages.error(request, 'User already exist')
                else:
                    # insert only the year in student profile (column : year_of_join)
                    password = make_password(password1)
                    MyUser.objects.create(username=username,
                                          first_name=first_name,
                                          last_name=last_name,
                                          password=password,
                                          is_faculty=False,
                                          is_active=True,
                                          is_student=True,
                                          is_hod=False

                                          )

                    profile_student.objects.create(
                        register_no=username,
                        first_name=first_name,
                        last_name=last_name,
                        batch=batch_id_int,
                        scheme_id=batch_data.scheme
                    )
                    s_id = MyUser.objects.latest('id')
                    qualifications.objects.create(s_id=s_id.id)
                    parents.objects.create(s_id=s_id.id)

                    messages.error(request, 'Student ' + full_name + ' successfully added in ' + batch_data.class_name)

    return render(request, 'add_student.html',
                  {
                      "batch_class": batch_data_class,
                      "context": context,
                      "scheme_data": scheme_data,
                      "data_for_self_profile": staff_details_1
                  }
                  )


@login_required
def view_student(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data = batch.objects.all()
    scheme_data = scheme.objects.all()

    if request.method == 'POST':

        batch_id = request.POST.get('batch_select')
        # print(batch_id)
        batch_id_int = int(batch_id)

        if batch_id == '0':

            messages.error(request, 'Please select Batch')

        else:

            batch_id = batch_id_int

            data = profile_student.objects.filter(batch=batch_id)

            batch_data1 = batch.objects.get(id=batch_id)
            scheme_data1 = scheme.objects.get(id=batch_data1.scheme)

            batch_data = batch.objects.all()
            scheme_data = scheme.objects.all()

            return render(request, 'view_student.html',
                          {"student_data": data, "scheme_data1": scheme_data1, 'batch_data1': batch_data1,
                           "context": context,
                           "scheme_data": scheme_data,
                           'batch': batch_data,
                           "data_for_self_profile": staff_details_1
                           })

    return render(request, 'view_student.html',

                  {
                      "batch": batch_data,
                      "scheme_data": scheme_data,
                      "context": context,
                      "data_for_self_profile": staff_details_1

                  }

                  )


'''def student_list(request):
    name = request.session['name']
    context = {'name': name}

    batch_id = request.session['batch_id']
    
    data = profile_student.objects.filter(batch=batch_id)


    batch_data = batch.objects.get(id=batch_id)
    scheme_data = scheme.objects.get(id=batch_data.scheme)
    return render(request, 'student_list.html', {"student_data": data, "scheme_data":scheme_data, 'batch_data': batch_data, "context": context})
'''


# batch details 

@login_required
def create_batch(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}
    scheme_data = scheme.objects.all()

    tutor_data = profile.objects.all()

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        date_of_join = request.POST.get('date_of_join')
        semester = request.POST.get('semester')
        scheme_input = request.POST.get('scheme')
        tutor_id = request.POST.get('tutor')
        scheme_input_int = int(scheme_input)
        tutor = int(tutor_id)

        if class_name == '0':
            messages.error(request, 'Please select class')
        elif semester == '0':
            messages.error(request, 'Please select Semester')
        elif scheme_input == '0':
            messages.error(request, 'Please select Scheme')
        elif tutor_id == '0':
            messages.error(request, 'Please select Tutor')
        else:
            data = batch.objects.filter(class_name=class_name, date_of_join=date_of_join, semester=semester,
                                        scheme=scheme_input_int, tutor_id=tutor)

            if data:
                messages.error(request, 'The class already exist')
            else:
                batch.objects.create(class_name=class_name, date_of_join=date_of_join, semester=semester,
                                     scheme=scheme_input_int, tutor_id=tutor)
                messages.error(request, 'Successfully added the class ' + class_name + ' year ' + date_of_join)

    return render(request, 'create_batch.html',
                  {"context": context, "scheme_data": scheme_data, "data_for_self_profile": staff_details_1,
                   "tutor_data": tutor_data})


@login_required
def view_batch(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    data = batch.objects.all()
    scheme_data = scheme.objects.all()
    tutor_data = profile.objects.all()
    return render(request, 'view_batch.html', {"batch_data": data, "scheme_data": scheme_data, "context": context,
                                               "data_for_self_profile": staff_details_1, "tutor_data": tutor_data})


@login_required
def edit_batch(request, b_id):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    edit_data = batch.objects.get(id=b_id)
    join_date = str(edit_data.date_of_join)
    edit_scheme_id = edit_data.scheme
    scheme_data = scheme.objects.all()
    tutor_data = profile.objects.all()

    edit_scheme_data = scheme.objects.get(id=edit_scheme_id)
    student_data = profile_student.objects.filter(batch=b_id)
    staff_data = profile.objects.all()
    subject_data = subject.objects.all()
    subject_in_sem = subject_to_staff.objects.filter(batch_id=b_id)
    assign_subject_data = subject_to_staff.objects.filter(batch_id=b_id)

    sem_result_list = []
    for i in assign_subject_data:
        for st_data in student_data:
            max_chances = semester_result.objects.filter(subject_id=i.subject_id,
                                                         university_no=st_data.university_no).aggregate(
                Max('no_of_chances'))

            sem_result_data = semester_result.objects.filter(subject_id=i.subject_id,
                                                             university_no=st_data.university_no,
                                                             no_of_chances=max_chances['no_of_chances__max'])

            print(max_chances['no_of_chances__max'])
            for result in sem_result_data:
                print(result)
                sem_result_tuple = (
                    i.subject_id, st_data.university_no, i.semester, result.grade_point, result.no_of_chances)
                sem_result_list.append(sem_result_tuple)
    print(sem_result_list)
    sem_result = semester_result.objects.filter(batch_id=b_id)

    if request.method == 'POST':
        # class_name = request.POST.get('class_name')
        # date_of_join = request.POST.get('date_of_join')
        semester = request.POST.get('semester')
        tutor = request.POST.get('tutor')
        # scheme_input = request.POST.get('scheme')

        ''' 
        if class_name == '0':
            messages.error(request, 'Please select class')
        elif semester == '0':
            messages.error(request, 'Please select semester')
        elif scheme_input == '0':
            messages.error(request, 'Please select Scheme')
        '''

        if semester == '0':
            messages.error(request, 'Please select semester')
        else:
            edit_data1 = batch.objects.get(id=b_id)
            edit_data1.semester = str(semester)
            edit_data1.tutor_id = int(tutor)
            # print(semester)
            edit_data1.save()
            messages.error(request, 'Successfully Updated')
            return redirect(hod.views.view_batch)

    return render(request, 'edit_batch.html',
                  {
                      'edit_data': edit_data, 'context': context, 'scheme_data': scheme_data, 'date': join_date,
                      "data_for_self_profile": staff_details_1
                      , 'present_scheme': edit_scheme_data,
                      'tutor_data': tutor_data,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'assign_subject_data': assign_subject_data,
                      'staff_data': staff_data,
                      'sem_result_list': sem_result_list,
                      'subject_in_sem': subject_in_sem,
                      'batch_id': b_id

                  })


@login_required
def delete_batch(request, b_id):
    # Print(join_date, class_name1)

    batch_data = batch.objects.get(id=b_id)
    student_data = profile_student.objects.filter(batch=b_id)

    # print(student_data)
    # print(student_data == [])

    if not student_data:
        a = batch.objects.get(id=b_id)
        a.delete()
        messages.error(request, 'Successfully deleted')
        return redirect(view_batch)

    else:
        messages.error(request,
                       'Some students have the class '
                       + batch_data.class_name +
                       ' So can not delete without changing their class'
                       )
        return redirect(view_batch)


# Manage scheme

@login_required
def create_scheme(request):
    # name = request.session['name']
    current_user = request.user

    staff_id = current_user.username
    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    if request.method == 'POST':
        scheme_input = request.POST.get('scheme')
        scheme_count = scheme.objects.filter(scheme=scheme_input)
        if scheme_count:
            messages.error(request,
                           'Already exist ' + scheme_input)
            return redirect(create_scheme)
        else:
            scheme.objects.create(scheme=scheme_input)
            messages.error(request,
                           'Successfully created ' + scheme_input)
            return redirect(create_scheme)

    return render(request, 'create_scheme.html', {'context': context, "data_for_self_profile": staff_details_1})


@login_required
def view_scheme(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()

    return render(request, 'view_scheme.html',
                  {'context': context, "scheme_data": scheme_data, "data_for_self_profile": staff_details_1})


# Manage Subject

@login_required
def create_subject(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()
    if 'create_subject' in request.POST:
        subject_code_input = request.POST.get('subject_code')
        subject_name_input = request.POST.get('subject_name')
        subject_credit = request.POST.get('subject_credit')
        scheme_id = request.POST.get('scheme')
        scheme_id_int = int(scheme_id)

        subject_code = subject_code_input.upper()
        subject_name = subject_name_input.upper()

        # check the subject already exist
        subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id_int).count()
        if subject_exist == 0:
            subject.objects.create(code=subject_code, subject_name=subject_name, credit=subject_credit,
                                   scheme=scheme_id_int)
            messages.error(request, "The Subject " + subject_name + " successfully added")

            return redirect(create_subject)
            # return redirect(request, 'create_subject.html',
            #             {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:
            messages.error(request, "The Subject code already exist!")
            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

    return render(request, 'create_subject.html',
                  {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})



@csrf_exempt
def check_subject_exist(request):
    subject_code = request.POST.get('subject_code')
    scheme_id = request.POST.get('scheme_id')
    subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id).exists()
    if subject_exist:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@login_required

def view_subject(request):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()
    view_subject_all = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.all()
    none = "None"
    staff_data = profile.objects.all()
    batch_data = batch.objects.all()

    if 'view_subject' in request.POST:
        scheme_id = request.POST.get('scheme_id')
        scheme_id_int = int(scheme_id)
        print(scheme_id_int)

        if scheme_id_int == 0:
            messages.error(request, "Please select scheme")
            return render(request, 'view_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:

            scheme_details = scheme.objects.filter(id=scheme_id_int)

            # for subject and scheme details
            for i in scheme_details:
                scheme_name = i.scheme
                scheme_input_id = i.id

            view_subject = subject.objects.filter(scheme=scheme_id_int)
            return render(request, 'view_subject.html',
                          {'context': context, 'scheme_data': scheme_data, 'view_subject': view_subject,
                           'scheme_input_id': scheme_input_id,
                           'scheme_name': scheme_name, "data_for_self_profile": staff_details_1,
                           'assign_subject_data': assign_subject_data,
                           'none': none,
                           'staff_data': staff_data,
                           'batch_data': batch_data
                           })

    return render(request, 'view_subject.html',
                  {'context': context,
                   'scheme_data': scheme_data,
                   "data_for_self_profile": staff_details_1,
                   "view_subject": view_subject_all,
                   'assign_subject_data': assign_subject_data,
                   'none': none,
                   'staff_data': staff_data,
                   'batch_data': batch_data
                   })


@login_required
def edit_subject(request, subject_id):
    # name = request.session['name']
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    scheme_data = scheme.objects.all()

    previous_subject_data = subject.objects.get(id=subject_id)
    previous_scheme_id = previous_subject_data.scheme
    previous_scheme_data = scheme.objects.get(id=previous_scheme_id)

    if 'edit_subject' in request.POST:
        subject_code = request.POST.get('subject_code')
        subject_name = request.POST.get('subject_name')
        subject_credit = request.POST.get('subject_credit')
        scheme_id = request.POST.get('scheme')
        scheme_id_int = int(scheme_id)

        # check the subject already exist
        subject_exist = subject.objects.filter(code=subject_code, scheme=scheme_id_int).count()

        if subject_exist == 0:
            update_subject = subject.objects.get(id=subject_id)
            update_subject.code = subject_code
            update_subject.subject_name = subject_name
            update_subject.credit = subject_credit
            update_subject.scheme = scheme_id_int
            update_subject.save()

            messages.error(request, "The Subject " + subject_name + " successfully Updated")

            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

        else:
            messages.error(request, "The Subject code already exist!")
            return render(request, 'create_subject.html',
                          {'context': context, 'scheme_data': scheme_data, "data_for_self_profile": staff_details_1})

    return render(request, 'edit_subject.html',
                  {'context': context, 'scheme_data': scheme_data, 'previous_subject_data': previous_subject_data,
                   'previous_scheme_data': previous_scheme_data, "data_for_self_profile": staff_details_1
                   })


@login_required
def assign_subject_to_staff(request):
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    batch_data_class = batch.objects.all()
    scheme_data = scheme.objects.all()
    subject_data = subject.objects.all()
    faculty = profile.objects.all()

    assign_subject_data = subject_to_staff.objects.all()
    faculty_data = profile.objects.all()

    if request.method == 'POST':
        batch_id = int(request.POST.get('batch_id'))
        subject_id = int(request.POST.get('subject_id'))
        faculty_id = int(request.POST.get('faculty_id'))
        sem = int(request.POST.get('semester'))

        batch_id_data = batch.objects.filter(id=batch_id)
        subject_id_data = subject.objects.filter(id=subject_id)
        valid_scheme = False

        for i in batch_id_data:
            for j in subject_id_data:
                if i.scheme == j.scheme:
                    valid_scheme = True

        if batch_id == 0:
            messages.error(request, "Select Class")
        elif subject_id == 0:
            messages.error(request, "Select Subject")
        elif valid_scheme == False:
            messages.error(request, "Select Subject with same scheme")
        elif sem == 0:
            messages.error(request, "Select Semester")
        elif faculty_id == 0:
            messages.error(request, "Select Faculty")
        else:

            check_exist = subject_to_staff.objects.filter(subject_id=subject_id, batch_id=batch_id)
            if check_exist:
                messages.error(request, "Subject Exist")
            else:
                subject_to_staff.objects.create(subject_id=subject_id, batch_id=batch_id, staff_id=faculty_id,
                                                semester=sem)
                messages.error(request, "Successfully added")

    return render(request, 'assign_subject_to_staff.html',
                  {'context': context, "data_for_self_profile": staff_details_1,
                   'batch_class': batch_data_class,
                   'scheme_data': scheme_data,
                   'subject_data': subject_data,
                   'faculty': faculty,
                   'assign_subject_data': assign_subject_data,
                   'faculty_data': faculty_data
                   })


@login_required
def delete_subject(request, subject_id):
    subject_for_delete = subject.objects.get(id=subject_id)
    subject_for_delete.delete()

    return redirect(hod.views.view_subject)


# manage all batch data 

@login_required
def batch_details(request, b_id):
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}
    return render(request, 'batch_details.html', {'context': context, "data_for_self_profile": staff_details_1})


# manage tutors

@login_required
def view_tutor(request):
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}
    return render(request, 'view_tutor.html', {'context': context, "data_for_self_profile": staff_details_1})


@login_required
def subject_wise_report(request, subject_id, batch_id):
    print(subject_id)
    current_user = request.user
    staff_id = current_user.username
    user_id = staff_id

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    # staff_id = staff_details.id
    # check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    internal_mark = Internal_mark.objects.filter()

    total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id).aggregate(
        Sum('no_of_hours'))

    attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    total_hour = total_attendance['no_of_hours__sum']
    if total_hour == None:
        messages.error(request, "Attendance not entered ")
        return redirect(edit_batch, batch_id)
    print(total_attendance, total_hour, type(total_hour))

    attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=subject_id)

    attenance_list = []
    for i in student_data:
        hour = 0
        for j in attendance_data:
            if i.id == j.student_id:
                if j.present == True:
                    id1 = j.attendance_record_id
                    # print('id',id1, type(id1))
                    no_of_hours_taken = attendance_record.objects.get(id=id1)

                    hour = hour + int(no_of_hours_taken.no_of_hours)

        percentage_attendance = (hour / total_hour) * 100
        # print(i.first_name, hour)
        att_tuple = (i.register_no, percentage_attendance)
        attenance_list.append(att_tuple)

    mark_data = Internal_mark.objects.filter(subject_id=subject_id)

    total_mark_list = []
    for i in student_data:
        for j in mark_data:
            if i.id == j.student_id:
                sum_of_mark = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id).aggregate(
                    Sum('mark'))
                total_internal = sum_of_mark['mark__sum']
                mark_tupple = (i.register_no, total_internal)
        total_mark_list.append(mark_tupple)

    return render(request, 'hod_subject_wise_report.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      # 'check_subject_exist': check_subject_exist,
                      'internal_mark': internal_mark,
                      'attendance_data': attendance_data,
                      'attendance_record_data': attendance_record_data,
                      'attendance_list': attenance_list,
                      'total_mark_list': total_mark_list
                  })


@login_required
def view_student_details(request, student_id):
    current_user = request.user
    staff_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=staff_id)
    name = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': name}

    print(student_id)
    id = int(student_id)
    student_data = profile_student.objects.filter(id=id)

    student_q_details = qualifications.objects.filter(s_id=id)
    parent_details = parents.objects.filter(s_id=id)

    for i in student_data:
        batch_id = i.batch
        date_of_birth = i.date_of_birth
        name_first = i.first_name
        name_last = i.last_name

    batch_data = batch.objects.get(id=batch_id)
    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    subject_data = subject.objects.all()
    date_dob = str(date_of_birth)  # dob can only display in html only as string type
    internal_mark_data = Internal_mark.objects.filter(student_id=student_id)
    for i in internal_mark_data:
        print(i.exam_type, i.mark)
    total_mark_list = []
    attendance_list = []
    sem_result_list = []

    for i in assign_subject_data:

        sum_of_mark = Internal_mark.objects.filter(student_id=id, subject_id=i.subject_id).aggregate(Sum('mark'))
        total_internal = sum_of_mark['mark__sum']
        st_data = profile_student.objects.get(id=id)
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
    # print(total_mark_list)

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
        university_no = request.POST.get('university_no')
        roll_no = request.POST.get('roll_no')

        if gender == '0':
            messages.error(request, "Please select a valid Gender")
            return redirect(view_student_details, student_id)
        elif blood_group == '0':
            messages.error(request, "Please select a valid blood Group")
            return redirect(view_student_details, student_id)
        else:

            student_data1 = profile_student.objects.get(id=id)
            username = student_data1.register_no
            user_data = MyUser.objects.get(username=username)

            user_data.first_name = f_name
            user_data.last_name = l_name
            user_data.save()  # update the first and second name in login table

            student_data1.university_no = university_no
            student_data1.roll_no = roll_no
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
            return redirect(view_student_details, student_id)

    if 'change_password' in request.POST:
        # current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')
        student_data1 = profile_student.objects.get(id=id)

        user_data = MyUser.objects.get(username=student_data1.register_no)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")
            return redirect(view_student_details, student_id)
        # elif current_password != user_password:
        #    messages.error(request, "incorrect old password")
        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")
            return redirect(view_student_details, student_id)

    return render(request, 'view_student_details.html',
                  {
                      'student_data': student_data,
                      'scheme_data': scheme_data,
                      'batch_data': batch_data,
                      'date_dob': date_dob,
                      'context': context,
                      'assign_subject_data': assign_subject_data,
                      'subject_data': subject_data,
                      'internal_mark_data': internal_mark_data,
                      "data_for_self_profile": staff_details_1,
                      'total_mark_list': total_mark_list,
                      'attendance_list': attendance_list,
                      'sem_result_list': sem_result_list,
                      'student_q_details': student_q_details,
                      'parent_details': parent_details
                  })


@login_required
def hod_subject_wise_report(request, subject_id, batch_id, ):
    print(subject_id)
    current_user = request.user
    user_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    # staff_id = staff_details.id
    # check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    internal_mark = Internal_mark.objects.filter()

    total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id).aggregate(
        Sum('no_of_hours'))

    attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    total_hour = total_attendance['no_of_hours__sum']
    if total_hour == None:
        messages.error(request, "Attendance not entered ")
        return redirect(edit_batch, batch_id)
    print(total_attendance, total_hour, type(total_hour))

    attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=subject_id)

    attenance_list = []
    for i in student_data:
        hour = 0
        for j in attendance_data:
            if i.id == j.student_id:
                if j.present == True:
                    id1 = j.attendance_record_id
                    # print('id',id1, type(id1))
                    no_of_hours_taken = attendance_record.objects.get(id=id1)

                    hour = hour + int(no_of_hours_taken.no_of_hours)

        percentage_attendance = (hour / total_hour) * 100
        # print(i.first_name, hour)
        att_tuple = (i.register_no, percentage_attendance)
        attenance_list.append(att_tuple)

    mark_data = Internal_mark.objects.filter(subject_id=subject_id)

    total_mark_list = []
    for i in student_data:
        for j in mark_data:
            if i.id == j.student_id:
                sum_of_mark = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id).aggregate(
                    Sum('mark'))
                total_internal = sum_of_mark['mark__sum']
                mark_tupple = (i.register_no, total_internal)
        total_mark_list.append(mark_tupple)

    return render(request, 'hod_subject_wise_report.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      # 'check_subject_exist': check_subject_exist,
                      'internal_mark': internal_mark,
                      'attendance_data': attendance_data,
                      'attendance_record_data': attendance_record_data,
                      'attendance_list': attenance_list,
                      'total_mark_list': total_mark_list,
                      "data_for_self_profile": staff_details_1
                  })


@login_required
def hod_view_my_subject(request):
    current_user = request.user
    user_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': fullname}
    scheme_data = scheme.objects.all()
    view_subject_all = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.all()
    none = "None"
    staff_data = profile.objects.all()
    batch_data = batch.objects.all()

    assigned_subject_to_this_staff = subject_to_staff.objects.filter(staff_id=staff_details_1.id)

    return render(request, 'hod_view_my_subject.html',
                  {
                      'scheme_data': scheme_data,
                      "view_subject": view_subject_all,
                      'assign_subject_data': assign_subject_data,
                      'none': none,
                      'staff_data': staff_data,
                      'batch_data': batch_data,
                      'context': context,
                      'subject_to_this_staff': assigned_subject_to_this_staff,
                      "data_for_self_profile": staff_details_1
                  })


@login_required
def hod_update_class(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': fullname}

    # print(batch_id, subject_id)
    batch_id = int(batch_id)
    subject_id = int(subject_id)

    staff_id = staff_details_1.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)

    subject_data = subject.objects.all()
    student_data = profile_student.objects.all()
    batch_data = batch.objects.all()
    staff_data = profile.objects.all()
    att_record = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    subject_to_staff_data = subject_to_staff.objects.filter(batch_id=batch_id, subject_id=subject_id)

    from datetime import date
    today = date.today()

    check_today_attendance_marked = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id,
                                                                     date=today)
    if check_today_attendance_marked:
        marked = True
    else:
        marked = False

    for i in batch_data:
        # Join date
        date = str(i.date_of_join)

    if 'assign' in request.POST:
        # request.session['batch_id'] = batch_id
        # request.session['subject_id'] = subject_id
        return redirect(hod_my_subject_add_attendance, batch_id, subject_id)

    if 'internal' in request.POST:
        # request.session['batch_id'] = batch_id
        # request.session['subject_id'] = subject_id
        return redirect(hod_my_subject_add_internal, batch_id, subject_id)

    if 'result' in request.POST:
        # request.session['batch_id'] = batch_id
        # request.session['subject_id'] = subject_id
        return redirect(hod_my_subject_view_internal_result, batch_id, subject_id)

    # if 'view_attendance' in request.POST:
    #    return redirect(view_attendance, batch_id, subject_id, )

    return render(request, 'hod_update_class.html', {
        'context': context,
        'check_subject_exist': check_subject_exist,
        'subject_data': subject_data,
        'student_data': student_data,
        'batch_data': batch_data,
        'staff_data': staff_data,
        'date': date,
        'attendance_record': att_record,
        'marked': marked,
        'subject_to_staff_data': subject_to_staff_data,
        "data_for_self_profile": staff_details_1

    })


@login_required
def hod_my_subject_add_attendance(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': fullname}

    # batch_id = request.session['batch_id']
    # subject_id = request.session['subject_id']

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details_1.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    for i in check_subject_exist:
        sem = i.semester

    if request.method == 'POST':
        today = date.today()
        from_time = request.POST.get('from_time')
        end_time = request.POST.get('end_time')
        no_of_hours = request.POST.get('no_of_hours')

        from_time = datetime.strptime(from_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        print(from_time, end_time, type(from_time), type(end_time))
        no_of_hours = int(no_of_hours)

        att_record = attendance_record.objects.filter(date=today, from_time=from_time, subject_id=subject_id,
                                                      batch_id=batch_id)

        if att_record:
            messages.error(request, "Attendance already Marked")
            return redirect(hod_my_subject_add_attendance, batch_id, subject_id)
        else:

            attendance_record.objects.create(date=today, marked=True, subject_id=subject_id, batch_id=batch_id,
                                             from_time=from_time, end_time=end_time, no_of_hours=no_of_hours)
            record_id = attendance_record.objects.get(date=today, marked=True, subject_id=subject_id, batch_id=batch_id,
                                                      from_time=from_time, end_time=end_time, no_of_hours=no_of_hours)

            for i in student_data:
                x = i.register_no
                att_mark = request.POST.get(str(x))
                # print(att_mark, type(att_mark))

                attendance.objects.create(attendance_record_id=record_id.id, student_id=i.id, subject_id=subject_id,
                                          batch_id=batch_id, present=att_mark, semester=sem)
            messages.error(request, "Attendance successfully added")
            return redirect('update_class', batch_id, subject_id)

    return render(request, 'hod_attendance.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      "data_for_self_profile": staff_details_1
                  })


@login_required
def hod_my_subject_view_attendance(request, record_id, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': fullname}

    record_id = int(record_id)
    batch_id = int(batch_id)
    subject_id = int(subject_id)
    print(record_id, batch_id, subject_id)

    attendance_data = attendance.objects.filter(attendance_record_id=record_id)
    for i in attendance_data:
        print(i.present, type(i.present))
    attendance_record_data = attendance_record.objects.filter(id=record_id)
    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details_1.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)

    return render(request, 'hod_view_attendance.html',
                  {
                      'context': context,
                      'attendance_data': attendance_data,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      'attendance_record_data': attendance_record_data,
                      "data_for_self_profile": staff_details_1
                  })


# Internal

@login_required
def hod_my_subject_add_internal(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': fullname}

    # batch_id = request.session['batch_id']
    # subject_id = request.session['subject_id']

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details_1.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    internal_mark = Internal_mark.objects.filter()

    for i in check_subject_exist:
        sem = i.semester

    if 'internal' in request.POST:
        for i in student_data:
            x = i.roll_no
            mark = request.POST.getlist(str(x))
            print(mark)

            exist_ass1 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                      exam_type='Assignment 1').count()
            exist_ass2 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                      exam_type='Assignment 2').count()
            exist_internal1 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                           exam_type='Internal 1').count()
            exist_internal2 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                           exam_type='Internal 2').count()
            print(exist_ass1, exist_ass2, exist_internal1, exist_internal2)
            if exist_ass1 > 0:
                update_ass1 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                        exam_type='Assignment 1')
                update_ass1.mark = mark[0]
                update_ass1.save()

            if exist_ass2 > 0:
                update_ass2 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                        exam_type='Assignment 2')
                update_ass2.mark = mark[1]
                update_ass2.save()

            if exist_internal1 > 0:
                update_internal1 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                             exam_type='Internal 1')
                update_internal1.mark = mark[2]
                update_internal1.save()

            if exist_internal2 > 0:
                update_internal2 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                             exam_type='Internal 2')
                update_internal2.mark = mark[3]
                update_internal2.save()

            if exist_ass1 == 0 and exist_ass2 == 0 and exist_internal1 == 0 and exist_internal2 == 0:
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[0],
                                             exam_type='Assignment 1')
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[1],
                                             exam_type='Assignment 2')
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[2],
                                             exam_type='Internal 1')
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[3],
                                             exam_type='Internal 2')

        return redirect('hod_update_class', batch_id, subject_id)

    return render(request, 'hod_internal.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      'internal_mark': internal_mark,
                      "data_for_self_profile": staff_details_1

                  })



# view_internal_result
@login_required
def hod_my_subject_view_internal_result(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details_1 = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details_1.First_name + " " + staff_details_1.Last_name
    context = {'name': fullname}

    # batch_id = request.session['batch_id']
    # subject_id = request.session['subject_id']

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details_1.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    internal_mark = Internal_mark.objects.filter()

    total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id).aggregate(
        Sum('no_of_hours'))

    attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    total_hour = total_attendance['no_of_hours__sum']
    if total_hour == None:
        messages.error(request, "Attendance not entered ")
        return redirect(hod_update_class, batch_id, subject_id)
    # print(total_attendance, total_hour, type(total_hour))

    attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=subject_id)

    attenance_list = []
    for i in student_data:
        hour = 0
        for j in attendance_data:
            if i.id == j.student_id:
                if j.present == True:
                    id1 = j.attendance_record_id
                    # print('id',id1, type(id1))
                    no_of_hours_taken = attendance_record.objects.get(id=id1)

                    hour = hour + no_of_hours_taken.no_of_hours
        percentage_attendance = (hour / total_hour) * 100
        # print(i.first_name, hour)
        att_tuple = (i.register_no, percentage_attendance)
        attenance_list.append(att_tuple)

    mark_data = Internal_mark.objects.filter(subject_id=subject_id)

    total_mark_list = []
    for i in student_data:
        for j in mark_data:
            if i.id == j.student_id:
                sum_of_mark = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id).aggregate(
                    Sum('mark'))
                total_internal = sum_of_mark['mark__sum']
                mark_tupple = (i.register_no, total_internal)
                # x print(mark_tupple)
        total_mark_list.append(mark_tupple)
        # total_mark_list.append(mark_tupple)

    print(total_mark_list)

    return render(request, 'hod_internal_result.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      'internal_mark': internal_mark,
                      'attendance_data': attendance_data,
                      'attendance_record_data': attendance_record_data,
                      'attendance_list': attenance_list,
                      'total_mark_list': total_mark_list,
                      "data_for_self_profile": staff_details_1

                  })


# logout
def log_out(request):
    logout(request)

    return HttpResponseRedirect('/login/')
