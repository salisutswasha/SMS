from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages  
from django.utils import timezone
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/index.html')

#for showing signup/login button for teacher(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/adminclick.html')

#for showing signup/login button for teacher(by sumit)
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/teacherclick.html')

#for showing signup/login button for student(by sumit)
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/studentclick.html')

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()

            # Create AdminExtra with pending status
            admin_extra = models.AdminExtra.objects.create(user=user, status=False)

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            # Send email notification to super admin
            try:
                subject = f'New Admin Registration: {user.first_name} {user.last_name}'
                message = f'''
                A new admin has registered and is waiting for approval.
                
                Details:
                - Name: {user.first_name} {user.last_name}
                - Username: {user.username}
                - Email: {user.email if user.email else 'Not provided'}
                
                To approve this admin, click the following link:
                http://127.0.0.1:8000/approve-admin-email/{admin_extra.id}/
                
                To reject this admin, click the following link:
                http://127.0.0.1:8000/reject-admin-email/{admin_extra.id}/
                
                Or you can manage all pending admins at:
                http://127.0.0.1:8000/admin-approve-admin
                '''
                
                # Send to the email configured in settings
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],  # Send to yourself
                    fail_silently=False
                )
            except Exception as e:
                print(f"Email sending failed: {e}")

            return HttpResponseRedirect('adminlogin')
    return render(request,'school/adminsignup.html',{'form':form})

def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'school/studentsignup.html',context=mydict)

def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        
        print(f"Form1 is valid: {form1.is_valid()}")
        print(f"Form2 is valid: {form2.is_valid()}")
        
        if form1.is_valid() and form2.is_valid():
            print("Both forms are valid, creating teacher...")
            user=form1.save()
            user.set_password(user.password)
            user.save()
            
            f2=form2.save(commit=False)
            f2.user=user
            f2.date_of_application = timezone.now().date()  # Set application date
            f2.status = False  # Explicitly set status to False
            user2=f2.save()
            print(f"TeacherExtra created with status: {f2.status}")

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            print(f"Teacher added to group: {my_teacher_group[0].name}")

        else:
            print(f"Form1 errors: {form1.errors}")
            print(f"Form2 errors: {form2.errors}")
        
        return HttpResponseRedirect('teacherlogin')
    return render(request,'school/teachersignup.html',context=mydict)
# --- UPDATED: role checks -----------------------------------------------------

# Treat superusers as admins as well
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='ADMIN').exists()

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

# --- UPDATED: after login routing --------------------------------------------

def afterlogin_view(request):
    # Superuser: always allow straight to admin dashboard (no approval needed)
    if request.user.is_superuser:
        return redirect('admin-dashboard')

    if is_admin(request.user):
        accountapproval = models.AdminExtra.objects.filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('admin-dashboard')
        else:
            return render(request,'school/admin_wait_for_approval.html')

    elif is_teacher(request.user):                    # User is in TEACHER group
        accountapproval = models.TeacherExtra.objects.filter(
            user_id=request.user.id,
            status=True                               # Check if approved
        )
        if accountapproval:                          # If approved
            return redirect('teacher-dashboard')    # → Dashboard
        else:                                       # If NOT approved
            return render(request,'school/teacher_wait_for_approval.html')

    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'school/student_wait_for_approval.html')

    # No role assigned: show a message and a gentle page (do NOT auto-logout)
    messages.error(request, "Your account does not have a role yet. Please contact an administrator for access.")
    # Create a simple template at templates/school/no_role_assigned.html
    return render(request, 'school/no_role_assigned.html')

# ----------------- admin dashboards & other views (unchanged) ----------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=models.TeacherExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

    admincount=models.AdminExtra.objects.all().filter(status=True).count()
    pendingadmincount=models.AdminExtra.objects.all().filter(status=False).count()

    teachersalary=models.TeacherExtra.objects.filter(status=True).aggregate(Sum('salary'))
    pendingteachersalary=models.TeacherExtra.objects.filter(status=False).aggregate(Sum('salary'))

    studentfee=models.StudentExtra.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=models.StudentExtra.objects.filter(status=False).aggregate(Sum('fee'))

    notice=models.Notice.objects.all()

    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,
        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,
        'admincount':admincount,
        'pendingadmincount':pendingadmincount,
        'teachersalary':teachersalary['salary__sum'],
        'pendingteachersalary':pendingteachersalary['salary__sum'],
        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],
        'notice':notice
    }
    return render(request,'school/admin_dashboard.html',context=mydict)

# (Everything else in your file remains exactly the same...)
# ------------------------------------------------------------------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'school/admin_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request,'school/admin_add_teacher.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_teacher.html',{'teachers':teachers})

# Teachers waiting for approval
def admin_approve_teacher_view(request):
    print("Checking for pending teachers...")
    teachers = models.TeacherExtra.objects.all().filter(status=False)
    print(f"Found {teachers.count()} pending teachers")
    for teacher in teachers:
        print(f"Teacher: {teacher.username.first_name} {teacher.username.last_name}, status: {teacher.status}")
    return render(request, 'school/admin_approve_teacher.html', {'teachers': teachers})
    
# Students waiting for approval  
def admin_approve_student_view(request):
    students = models.StudentExtra.objects.all().filter(status=False)
    return render(request, 'school/admin_approve_student.html', {'students': students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request, pk):
    teacher = models.TeacherExtra.objects.get(id=pk)
    teacher.status = True                    # Change status to True
    teacher.save()                           # Save to database
    return redirect(reverse('admin-approve-teacher'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request,'school/admin_update_teacher.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers=models.TeacherExtra.objects.all()
    return render(request,'school/admin_view_teacher_salary.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_student.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'school/admin_update_student.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_student.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-approve-student'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request,cl):
    students=models.StudentExtra.objects.all()
    return render(request,'school/admin_view_student_fee.html',{'students':students})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'school/admin_attendance.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request,'school/admin_take_attendance.html',{'students':students,'aform':aform})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/admin_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/admin_view_attendance_ask_date.html',{'cl':cl,'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request,'school/admin_fee.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request,cl):
    feedetails=models.StudentExtra.objects.all().filter(cl=cl)
    return render(request,'school/admin_view_fee.html',{'feedetails':feedetails,'cl':cl})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'school/admin_notice.html',{'form':form})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'salary':teacherdata[0].salary,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'school/teacher_attendance.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'school/teacher_take_attendance.html',{'students':students,'aform':aform})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/teacher_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/teacher_view_attendance_ask_date.html',{'cl':cl,'form':form})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'school/teacher_notice.html',{'form':form})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'notice':notice
    }
    return render(request,'school/student_dashboard.html',context=mydict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=studentdata[0].cl,roll=studentdata[0].roll)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/student_view_attendance_ask_date.html',{'form':form})

def aboutus_view(request):
    return render(request,'school/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form':sub})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_admin_view(request):
    admins = models.AdminExtra.objects.filter(status=False)
    return render(request, 'school/admin_approve_admin.html', {'admins': admins})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_admin_view(request, pk):
    admin_extra = models.AdminExtra.objects.get(id=pk)
    admin_extra.status = True
    admin_extra.save()
    return redirect(reverse('admin-approve-admin'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_admin_view(request, pk):
    admin_extra = models.AdminExtra.objects.get(id=pk)
    user = User.objects.get(id=admin_extra.user_id)
    user.delete()
    admin_extra.delete()
    return redirect('admin-approve-admin')

# Email approval views for admin registration
def approve_admin_email_view(request, pk):
    try:
        admin_extra = models.AdminExtra.objects.get(id=pk, status=False)
        admin_extra.status = True
        admin_extra.save()
        
        # Send approval email to the admin
        try:
            subject = 'Admin Account Approved'
            message = f'''
            Dear {admin_extra.user.first_name} {admin_extra.user.last_name},
            
            Your admin account has been approved successfully!
            
            You can now login to the school management system at:
            http://127.0.0.1:8000/adminlogin
            
            Username: {admin_extra.user.username}
            
            Best regards,
            School Management System
            '''
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [admin_extra.user.email] if admin_extra.user.email else [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
        except Exception as e:
            print(f"Approval email sending failed: {e}")
        
        return render(request, 'school/admin_approval_success.html', {
            'admin_name': f"{admin_extra.user.first_name} {admin_extra.user.last_name}",
            'action': 'approved'
        })
    except models.AdminExtra.DoesNotExist:
        return render(request, 'school/admin_approval_error.html', {
            'message': 'Admin not found or already approved'
        })

def reject_admin_email_view(request, pk):
    try:
        admin_extra = models.AdminExtra.objects.get(id=pk, status=False)
        user = admin_extra.user
        
        # Send rejection email to the admin
        try:
            subject = 'Admin Account Application Rejected'
            message = f'''
            Dear {user.first_name} {user.last_name},
            
            We regret to inform you that your admin account application has been rejected.
            
            If you believe this is an error, please contact the system administrator.
            
            Best regards,
            School Management System
            '''
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email] if user.email else [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
        except Exception as e:
            print(f"Rejection email sending failed: {e}")
        
        # Delete the user and admin_extra
        user.delete()
        admin_extra.delete()
        
        return render(request, 'school/admin_approval_success.html', {
            'admin_name': f"{user.first_name} {user.last_name}",
            'action': 'rejected'
        })
    except models.AdminExtra.DoesNotExist:
        return render(request, 'school/admin_approval_error.html', {
            'message': 'Admin not found or already processed'
        })
