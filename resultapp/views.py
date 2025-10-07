from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



def index(request):
    notices = Notice.objects.all().order_by('-id')
    return render(request, 'index.html', locals())

def notice_detail(request, notice_id):
    notices = Notice.objects.get(id=notice_id)
    return render(request, 'notice_detail.html', locals())

# @login_required
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, "admin_login.html", {"error": "Invalid credentials or not authorized."})
    return render(request, "admin_login.html")


from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

def admin_register(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists. Please try another one.")
            return redirect('admin_register')

        # check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_register')

        # create user and mark as admin
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.save()

        # auto-login newly registered user
        login(request, user)
        messages.success(request, "Registration successful! You are now logged in.")
        return redirect('admin_dashboard')  # change this to your admin home page

    return render(request, "admin_register.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_classes = Studentclass.objects.count()
    total_results = Result.objects.values('student').distinct().count()
    return render(request,'admin_dashboard.html', locals())

# @login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def create_class(request):
    if request.method == 'POST':
        try:
            streamName = request.POST.get('streamName')
            yearStream = request.POST.get('yearStream')
            section = request.POST.get('section')
            Studentclass.objects.create(
                streamName=streamName,
                yearStream=yearStream,
                section=section
            )
            messages.success(request, "Class created successfully!")
            return redirect('create_class') 
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('create_class') 
    return render(request, 'create_class.html')



@login_required
def manage_classes(request):
    classes = Studentclass.objects.all()
    if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            class_to_delete = Studentclass.objects.get(id=class_id)
            class_to_delete.delete()
            messages.success(request, 'Class deleted successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: (str{e})')
            return redirect('manage_classes')
    return render(request,'manage_classes.html', locals())

@login_required
def edit_class(request,class_id):
    class_to_delete = Studentclass.objects.get(id=class_id)
    
    if request.method == 'POST':
        streamName = request.POST.get('streamName')
        yearStream = request.POST.get('yearStream')
        section = request.POST.get('section')
        try:
            class_to_delete.streamName = streamName
            class_to_delete.yearStream = yearStream
            class_to_delete.section = section
            class_to_delete.save()
            messages.success(request, 'Class updated successfully!')
            return redirect('manage_classes') 
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
            return redirect('manage_classes') 
    
    return render(request, 'edit_class.html', {'class_to_delete': class_to_delete})

@login_required
def create_subject(request):
    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subjectName')
            subject_code = request.POST.get('subjectCode')
            Subject.objects.create(
                subject_name=subject_name,
                subject_code=subject_code,
            )
            messages.success(request, "Subject created successfully!") 
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('create_subject') 
    return render(request, 'create_subject.html')

@login_required
def manage_subject(request):
    subjects = Subject.objects.all()
    if request.GET.get('delete'):
        try:
            subject_id = request.GET.get('delete')
            subject_to_delete = Subject.objects.get(id=subject_id)
            subject_to_delete.delete()
            messages.success(request, 'Subject deleted successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: (str{e})')
        return redirect('manage_subject')
    return render(request,'manage_subject.html', locals())

@login_required
def edit_subject(request,subject_id):
    subject_to_delete = Subject.objects.get(id=subject_id)
    if request.method == 'POST':
        subject_name = request.POST.get('subjectName')
        subject_code = request.POST.get('subjectCode')
        try:
            subject_to_delete.subject_name = subject_name
            subject_to_delete.subject_code = subject_code
            subject_to_delete.save()
            messages.success(request, 'Subject updated successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('manage_subject') 
    
    return render(request, 'edit_subject.html',locals())

@login_required
def add_subject_combination(request):
    classes = Studentclass.objects.all()
    subjects = Subject.objects.all()   

    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            subject_id = request.POST.get('subject')

            selected_class = Studentclass.objects.get(id=class_id)
            selected_subject = Subject.objects.get(id=subject_id)

            # ✅ Check if combination already exists
            if SubjectCombination.objects.filter(student_class=selected_class, subject=selected_subject).exists():
                messages.warning(request, "This subject combination already exists!")
            else:
                SubjectCombination.objects.create(
                    student_class=selected_class,
                    subject=selected_subject,
                    status=1
                )
                messages.success(request, "Subject combination added successfully!")

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')

        return redirect('add_subject_combination')

    return render(request, 'add_subject_combination.html', locals())

@login_required
def manage_subject_combination(request):
    combinations = SubjectCombination.objects.all()
    aid = request.GET.get('aid')
    if request.GET.get('aid'):
        try:
            SubjectCombination.objects.filter(id = aid).update(status = 1)
            messages.success(request, 'Subject Combination activated successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: (str{e})')
        return redirect('manage_subject_combination')
    did = request.GET.get('did')
    if request.GET.get('did'):
        try:
            SubjectCombination.objects.filter(id = did).update(status = 0)
            messages.success(request, 'Subject Combination Deactivated successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: (str{e})')
        return redirect('manage_subject_combination')
    return render(request,'manage_subject_combination.html', locals())

@login_required
def add_student(request):
    classes = Studentclass.objects.all() 
    if request.method == 'POST':
        try:
            name = request.POST.get('fullname')
            roll_no = request.POST.get('rollno')
            email_id = request.POST.get('emailid')
            gender = request.POST.get('gender')
            class_id = request.POST.get('class')
            dob = request.POST.get('dob')
            student_class = Studentclass.objects.get(id=class_id)
            Student.objects.create(
                name=name,
                roll_number=roll_no,
                email=email_id,
                gender=gender,
                date_of_birth=dob,
                student_class=student_class
            )
            messages.success(request, "Subject info added successfully!")
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('add_student')
    return render(request, 'add_student.html', locals())

@login_required
def manage_students(request):
    students = Student.objects.all()
    
    return render(request,'manage_students.html', locals())

@login_required
def edit_student(request,student_id):
    student_to_delete = Student.objects.get(id=student_id)
    if request.method == 'POST':
        try:
            student_to_delete.name = request.POST.get('fullname')
            student_to_delete.roll_number = request.POST.get('rollno')
            student_to_delete.email = request.POST.get('emailid')
            student_to_delete.gender = request.POST.get('gender')
            student_to_delete.date_of_birth = request.POST.get('dob')
            student_to_delete.status = request.POST.get('status')
            student_to_delete.save()
            messages.success(request, 'Student updated successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('manage_students') 
    
    return render(request, 'edit_student.html',locals())

@login_required
def add_notice(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            details = request.POST.get('details')
            Notice.objects.create(
                title=title,
                detail=details
            )
            messages.success(request, "Notice added successfully!")
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('add_notice')
    return render(request, 'add_notice.html', locals())

@login_required
def manage_notice(request):
    notices = Notice.objects.all()
    if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            notice_to_delete = Notice.objects.get(id=notice_id)
            notice_to_delete.delete()
            messages.success(request, 'Notice deleted successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: (str{e})')
        return redirect('manage_notice')
    return render(request,'manage_notice.html', locals())

@login_required
def add_result(request):
    classes = Studentclass.objects.all() 
    if request.method == 'POST':
        try:
            class_id = request.POST.get('classid')
            student_id = request.POST.get('studentid')
            marks_data = {key.split('_')[1]:value for key, value in request.POST.items() if key.startswith('marks_')}
            for subject_id, marks in marks_data.items():
                Result.objects.create(
                    student_id=student_id,
                    student_class_id=class_id,
                    subject_id=subject_id,
                    marks=marks
                )
            messages.success(request, "Result info added successfully!")
            return redirect('add_result')
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('add_result')
    return render(request, 'add_result.html', locals())

@login_required
def manage_students(request):
    students = Student.objects.all()
    
    return render(request,'manage_students.html', locals())

from django.http import JsonResponse

@login_required
def get_students_subjects(request):
    class_id = request.GET.get('class_id')

    if class_id:
        students = list(
            Student.objects.filter(student_class_id=class_id)
            .values('id', 'name', 'roll_number')
        )

        subject_combination = SubjectCombination.objects.filter(
            student_class_id=class_id, status=1
        ).select_related('subject')

        subjects = [
            {'id': sc.subject.id, 'name': sc.subject.subject_name} 
            for sc in subject_combination
        ]

        return JsonResponse({'students': students, 'subjects': subjects})

    return JsonResponse({'students': [], 'subjects': []})

@login_required
def manage_result(request):
    results = Result.objects.select_related('student', 'student_class').all()
    students = {}
    for res in results:
        stu_id = res.student.id
        if stu_id not in students:
            students[stu_id] = {
                'student': res.student,
                'class': res.student_class
            }
    return render(request,'manage_result.html',{'results' : students.values()})

@login_required
def edit_result(request, stid):
    student = Student.objects.get(id=stid)
    results = Result.objects.filter(student=student)

    if request.method == 'POST':
        ids = request.POST.getlist('id[]')
        marks = request.POST.getlist('marks[]')

        for i in range(len(ids)):
            result = Result.objects.get(id=ids[i])
            result.marks = marks[i]
            result.save()
        messages.success(request, "Results updated successfully!")
        # return redirect('edit_result', stid=student.id)
        return redirect('manage_result')
    return render(request,'edit_result.html',locals())

from django.contrib.auth import update_session_auth_hash
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Important to keep the user logged in
        messages.success(request, "Password changed successfully!")
        return redirect('admin_dashboard')


    return render(request, 'change_password.html')


def search_result(request):
    classes = Studentclass.objects.all()
    return render(request, 'search_result.html', locals())

def check_result(request):
    if request.method == 'POST' :
        rollid = request.POST['rollid']
        class_id = request.POST['class']

        try:
            student = Student.objects.get(roll_number=rollid, student_class_id=class_id)
            results = Result.objects.filter(student=student).select_related('subject')

            total_marks = sum([r.marks for r in results])
            subject_count = results.count()
            max_total = subject_count * 100  # Assuming each subject is out of 100
            percentage = (total_marks / max_total) * 100 if max_total > 0 else 0
            percentage = round(percentage, 2)
            return render(request, 'result_page.html', locals())
        except Exception as e:
            messages.error(request, "No result found. Please check your Roll Number and Class.")
            return redirect('search_result')
    
   