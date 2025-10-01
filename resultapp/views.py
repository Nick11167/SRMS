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
            if not class_id or not subject_id:
                messages.error(request, "Please select both class and subject.")
            else:
                selected_class = Studentclass.objects.get(id=class_id)
                selected_subject = Subject.objects.get(id=subject_id)
                SubjectCombination.objects.create(
                    student_class=class_id,
                    subject=subject_id
                )
                messages.success(request, "Subject combination created successfully!")
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
    return render(request, 'add_subject_combination.html', {"classes": classes, "subjects": subjects})
