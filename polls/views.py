from django.shortcuts import render
from django.db import connection
from django.contrib import messages
from .models import *

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def toLogin_view(request):
    link = '../index/'
    return render(request, 'login.html', {'link':link})

def Login_view(request):
    user = request.POST.get("user", '')
    pwd = request.POST.get("pwd", '')
    link = "../torewriteinfo/"
    if user and pwd:
        c0 = StudentInfo.objects.filter(stu_name=user,stu_pwd=pwd, stu_role='0').count()
        c1 = StudentInfo.objects.filter(stu_name=user, stu_pwd=pwd, stu_role='1').count()
        if c0 >= 1:
            for student in StudentInfo.objects.all():
                if student.stu_name == user:
                    break
            link = link + user + '/'
            drop_link = './' + user + '/drop/'
            add_link = './' + user + '/add/'
            academic_link = './' + user + '/show_academic/'
            courses_link = './' + user + '/show_courses/'
            return render(request, 'studentindex0.html', context={'student': student, 'link':link,
                                                                  'drop_link':drop_link, 'add_link':add_link,
                                                                  'show_academic_link': academic_link,
                                                                  'show_courses_link': courses_link
                                                                  })
        elif c1 >= 1:
            for student in StudentInfo.objects.all():
                if student.stu_name == user:
                    break
            link = link + user
            update_link = '../index/' + user + '/update/'
            return render(request, 'teacherindex0.html', context={'teacher': student, 'link':link,
                                                                  'update_link':update_link
                 })
        else:
            messages.success(request, "Something wrong with your username or password")
            return render(request, 'login.html')
    else:
        messages.success(request, "Username or password missing")
        return render(request, 'login.html')

def toregister_view(request):
    return render(request, 'register.html')

def register_view(request):
    role = request.POST.get("role", '')
    user = request.POST.get("user", '')
    pwd = request.POST.get("pwd", '')
    confirm_pwd = request.POST.get("confirm_pwd", '')
    email = request.POST.get("email", '')
    stu_id = request.POST.get("id", '')
    course = request.POST.get("course", '')
    if role and user and pwd and confirm_pwd and email and id and course:
        c = StudentInfo.objects.filter(stu_name=user).count()
        if c:
            messages.success(request, "User name already exists")
            return render(request, 'register.html')
        elif pwd != confirm_pwd:
            messages.success(request, "Please confirm your password")
            return render(request, 'register.html')
        else:
            if role == "teacher":
                stu_role = '1'
            else:
                stu_role = '0'
            stu = StudentInfo(stu_id=stu_id,stu_name=user,stu_pwd=pwd,stu_email=email,stu_course=course,stu_role=stu_role)
            stu.save()
            # messages.success(request, 'Success')
            return render(request, 'finish_register.html')
    else:
        # messages.success(request, "Lack of some information")
        return render(request, 'register.html')

def toRewrite_view(request, link):
    link = '../../rewriteinfo/' + link + '/'
    return render(request, 'rewriteinfo.html', context= {'link':link})

def Rewrite_view(request, link):
    for student in StudentInfo.objects.all():
        if student.stu_name == link:
            break
    link = '../../index/' + link + '/'
    email = request.POST.get("email", '')
    stu_id = request.POST.get("id", '')
    if stu_id and email:
        stu_name = student.stu_name
        pwd = student.stu_pwd
        course = student.stu_course
        role = student.stu_role
        StudentInfo.objects.get(stu_name=stu_name).delete()
        stu = StudentInfo(stu_id=stu_id, stu_name=stu_name, stu_pwd=pwd, stu_email=email, stu_role=role,
                          stu_course=course)
        stu.save()
        # messages.success(request, "Success")
        # if stu.stu_role == '0':
        #     return render(request, 'studentindex.html', context={'student': stu, 'link': link})
        # elif stu.stu_role == '1':
        #     return render(request, 'teacherindex.html', context={'teacher': stu, 'link': link})
        return render(request, 'finish_rewrite.html', context={'link':link})
    else:
        messages.success(request, "Lack of some information")
        return render(request, 'rewriteinfo.html', context= {'link':link})

def index_view(request, link):
    student = StudentInfo.objects.get(stu_name=link)

    link = '../../torewriteinfo/' + link + '/'
    if student.stu_role == '1':
        return render(request, 'teacherindex.html', context={'teacher': student, 'link':link})
    else:
        return render(request, 'studentindex.html', context={'student': student, 'link':link})

# def teacher_view(request, user_name):
#     for student in StudentInfo.objects.all():
#         if student.stu_name == user_name:
#             break
#     link = '../../torewriteinfo/' + user_name + '/'
#     return render(request, 'teacherindex.html', context={'teacher': student, 'link': link})

def drop_view(request, user_name):
    for user in StudentInfo.objects.all():
        if user.stu_name == user_name:
            break
    courses_ids = user.stu_course.split(',')
    courses = []
    for course in CourseInfo.objects.all():
        if course.course_id in courses_ids:
            courses.append(course)
    return render(request, 'drop.html', context={'user':user, 'courses':courses})

def add_view(request, user_name):

    for user in StudentInfo.objects.all():
        if user.stu_name == user_name:
            break
    courses_ids = user.stu_course.split(',')
    courses = []
    for course in CourseInfo.objects.all():
        if course.course_id not in courses_ids:
            courses.append(course)
    return render(request, 'add.html', context={'user': user, 'courses': courses})


def stu_showCourses_view(request, user_name):
    for user in StudentInfo.objects.all():
        if user.stu_name == user_name:
            break
    courses_ids = user.stu_course.split(',')
    courses = []
    for course in CourseInfo.objects.all():
        if course.course_id in courses_ids:
            courses.append(course)
    return render(request, 'stu_showCourses.html', context={'user':user, 'courses':courses})


def Toadd_view(request, user_name):
    course_id = request.POST.get("course",'')
    if course_id:
        for user in StudentInfo.objects.all():
            if user.stu_name == user_name:
                break
        stu_id = user.stu_id
        stu_name = user.stu_name
        pwd = user.stu_pwd
        role = user.stu_role
        email = user.stu_email
        course = user.stu_course
        student_obj = StudentInfo.objects.get(stu_name=stu_name)
        course_obj = CourseInfo.objects.get(course_id=course_id)
        new_stu_course = course + ',' + course_id
        student_obj.stu_course = new_stu_course
        student_obj.save()
        mark_id = stu_name + course_id
        new_mark = Studentmark(mark_id=mark_id,stu_id=user,stu_name=stu_name,course_id=course_obj,assignment_1='0',assignment_2='0',assignment_3='0',assignment_4='0',assignment_5='0',assignment_6='0')
        new_mark.save()
    return render(request,'finish_add.html',context={'course':course_id})

def Todrop_view(request, user_name):
    course_id = request.POST.get("course",'')
    for user in StudentInfo.objects.all():
        if user.stu_name == user_name:
            break

    # Update the courses
    courses = user.stu_course.split(',')

    # Check if the course exists before removing
    if course_id in courses:
        courses.remove(course_id)

    # Join the remaining courses back into a string
    new_stu_course = ','.join(courses)

    # Create a new student record with updated course information
    new_student = StudentInfo(
        stu_id=user.stu_id,
        stu_name=user.stu_name,
        stu_pwd=user.stu_pwd,
        stu_email=user.stu_email,
        stu_role=user.stu_role,
        stu_course=new_stu_course
    )
    new_student.save()

    # Delete the associated student mark (if it exists)
    mark_id = f"{user.stu_name}{course_id}"
    try:
        student_mark = Studentmark.objects.get(mark_id=mark_id)
        student_mark.delete()
    except Studentmark.DoesNotExist:
        pass

    return render(request,'finish_drop.html',context={'course':course_id})

def update_view(request, user_name):
    user = StudentInfo.objects.get(stu_name=user_name)

    course = user.stu_course
    marks = []
    for mark in Studentmark.objects.all():
        if mark.course_id.course_id == course:
            marks.append(mark)
            
    for stu in StudentInfo.objects.all():
        if stu.stu_course.__contains__(course):
            course_obj = CourseInfo.objects.get(course_id=course)
            marks.append(Studentmark(stu_id=stu, stu_name=stu.stu_name, course_id=course_obj))
    
    # if duplicate stu name in mark in the marks get the first one
    marks = list({mark.stu_name:mark for mark in marks}.values())
            
    return render(request, "update_accdemic_record.html",context={'marks':marks})

def Toupdate_view(request, user_name):
    user = StudentInfo.objects.get(stu_name=user_name)

    course = user.stu_course
    course_obj = CourseInfo.objects.get(course_id=course)
    for mark in Studentmark.objects.all():
        if mark.course_id.course_id == course:
            a_1 = request.POST.get(mark.stu_name + "a1", '')
            a_2 = request.POST.get(mark.stu_name + "a2", '')
            a_3 = request.POST.get(mark.stu_name + "a3", '')
            a_4 = request.POST.get(mark.stu_name + "a4", '')
            a_5 = request.POST.get(mark.stu_name + "a5", '')
            a_6 = request.POST.get(mark.stu_name + "a6", '')
            flag1,flag2,flag3,flag4,flag5,flag6 = 0,0,0,0,0,0
            if not a_1:
                a_1 = '0'
            if not a_2:
                a_2 = '0'
            if not a_3:
                a_3 = '0'
            if not a_4:
                a_4 = '0'
            if not a_5:
                a_5 = '0'
            if not a_6:
                a_6 = '0'
            if a_1 != mark.assignment_1:
                flag1 = 1
            if a_2 != mark.assignment_2:
                flag2 = 1
            if a_3 != mark.assignment_3:
                flag3 = 1
            if a_4 != mark.assignment_4:
                flag4 = 1
            if a_5 != mark.assignment_5:
                flag5 = 1
            if a_6 != mark.assignment_6:
                flag6 = 1
            if flag1 or flag2 or flag3 or flag4 or flag5 or flag6:
                mark_id = mark.mark_id
                stu_name = mark.stu_name
                stu_id = mark.stu_id
                try:
                    std_mark = Studentmark.objects.get(mark_id=mark_id)
                    std_mark.assignment_1 = a_1
                    std_mark.assignment_2 = a_2
                    std_mark.assignment_3 = a_3
                    std_mark.assignment_4 = a_4
                    std_mark.assignment_5 = a_5
                    std_mark.assignment_6 = a_6
                    std_mark.save()
                except Studentmark.DoesNotExist:
                    new_mark = Studentmark(mark_id=mark_id,stu_id=stu_id,stu_name=stu_name,course_id=course_obj,assignment_1=a_1,assignment_2=a_2,assignment_3=a_3,assignment_4=a_4,assignment_5=a_5,assignment_6=a_6)
                    new_mark.save()

    return render(request, 'finish_update.html', context={'course':course})


def show_academic_view(request, user_name):
    user = StudentInfo.objects.get(stu_name=user_name)
    cur_stu_id = user.stu_id

    marks = []
    for cur_row in Studentmark.objects.all():
        if cur_row.stu_id.stu_id == cur_stu_id:
            marks.append(cur_row)
    return render(request, 'show_academic.html', context={'user':user, 'courses':marks})

def show_courses_view(request, user_name):
    for user in StudentInfo.objects.all():
        if user.stu_name == user_name:
            break
    courses_ids = user.stu_course.split(',')
    courses = []
    for course in CourseInfo.objects.all():
        if course.course_id in courses_ids:
            courses.append(course)
    return render(request, 'show_courses.html', context={'user':user, 'courses':courses})

def Toquery_view(request, user_name):
    return render(request, 'query.html')

def query_view(request, user_name):
    stu_name = request.POST.get('stu_name','')
    a = request.POST.get('a', '')

    try:
        user = StudentInfo.objects.get(stu_name=user_name)

        mark = Studentmark.objects.get(stu_name=stu_name, course_id=user.stu_course)

        if a == 'assignment1':
            score = mark.assignment_1
        elif a == 'assignment2':
            score = mark.assignment_2
        elif a == 'assignment3':
            score = mark.assignment_3
        elif a == 'assignment4':
            score = mark.assignment_4
        elif a == 'assignment5':
            score = mark.assignment_5
        elif a == 'assignment6':
            score = mark.assignment_6
        else:
            score = 'something wrong'
    except Studentmark.DoesNotExist:
        score = 0
        
    return render(request, 'finish_query.html',context={'name':stu_name, 'num':a, 'score':score})