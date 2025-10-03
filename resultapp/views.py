from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = "Invalid credentials or not authorized."
    return render(request, 'admin_login.html',locals())

def admin_dashboard(request):
     if not request.user.is_authenticated:
        return redirect('admin_login')
     return render(request,'admin_dashboard.html')

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

def add_subject_combination(request):
    classes = Studentclass.objects.all()
    subjects = Subject.objects.all()   
    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            subject_id = request.POST.get('subject')
            selected_class = Studentclass.objects.get(id=class_id)
            selected_subject = Subject.objects.get(id=subject_id)
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

def manage_students(request):
    students = Student.objects.all()
    
    return render(request,'manage_students.html', locals())

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

def add_result(request):
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
    return render(request, 'add_result.html', locals())

def manage_students(request):
    students = Student.objects.all()
    
    return render(request,'manage_students.html', locals())