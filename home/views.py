from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm

from .forms import *
from .decorators import *
from .paper import *
import json
import re

import datetime
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# Create your views here.
@unauthenticated_user
def index(request):
    return render(request, 'index.html')

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username/password is incorrect')

    context={}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def homePage(request):
    return render(request, 'home.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def adminPage(request):
    papers=Paper.objects.all().order_by('-date')
    context={'papers':papers}
    return render(request, 'admin.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def send_otp_email(request, email):
    otp = get_random_string(length=6, allowed_chars='0123456789')
    otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)

    session = request.session
    session.setdefault('otp_data', {})
    session['otp_data'][email] = {
        'otp': otp,
        'expiry': otp_expiry.strftime('%Y-%m-%d %H:%M:%S')
    }
    session.modified = True

    send_mail(subject='OTP for Validation', message=f'Welcome to Smart QpGenerator!\nWe have received your request for account creation.\n\nYour OTP is: {otp}\nThis OTP is valid for 10 minutes.\n\nThanks for using our site!\n-The QpGenerator team', from_email="officialqpgenerator@gmail.com", recipient_list=[email])
    return

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def get_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            send_otp_email(request, email)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def create_user(request):
    form=UserProfileForm()
    if request.method == 'POST':
        form=UserProfileForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with that email already exists.')
            else:
                otp = form.cleaned_data['otp']

                session = request.session
                otp_data = session.get('otp_data', {})

                for stored_email, stored_data in otp_data.copy().items():
                    stored_expiry = datetime.datetime.strptime(stored_data['expiry'], '%Y-%m-%d %H:%M:%S')
                    if datetime.datetime.now() > stored_expiry:
                        del otp_data[stored_email]
                session['otp_data'] = otp_data
                session.modified = True

                if email in otp_data:
                    stored_otp = otp_data[email]['otp']
                    expiry = datetime.datetime.strptime(otp_data[email]['expiry'], '%Y-%m-%d %H:%M:%S')

                    if otp == stored_otp and datetime.datetime.now() < expiry:
                        del otp_data[email]  
                        session['otp_data'] = otp_data
                        session.modified = True

                        user = form.save()

                        group = request.POST.get('group')
                        user.groups.add(group)

                        send_mail(subject='We are thrilled to have you aboard!', message=f'Your account was created successfully!\n\nYou will receive a reset password link shortly. Kindly reset your password and you are all set to login to your account.\n\nThanks for using our site!\n-The QpGenerator team', from_email="officialqpgenerator@gmail.com", recipient_list=[email])

                        reset_form = PasswordResetForm()
                        reset_form.initial = {'email': email}
                        PasswordResetView.as_view()(request=request) 
                        messages.info(request, 'Created user successfully')
                        if request.POST.get("create_user_add"):
                            return redirect('create_user')
                        elif request.POST.get("create_user"):
                            return redirect('adminPage')
                    
                    else:
                        form.add_error('otp', 'The OTP you entered is wrong. Please enter the correct OTP.')
                
                else:
                    form.add_error(None, 'OTP expired/Email id is wrong. Please verify your Email id and click on Resend OTP.')
        
    context={'form': form}
    return render(request, 'create_user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def create_group(request):
    form=CreateGroupForm()
    if request.method == 'POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Department created successfully')
            if request.POST.get("create_group_add"):
                return redirect('create_group')
            elif request.POST.get("create_group"):
                return redirect('adminPage')
        
    context={'form': form}
    return render(request, 'create_group.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_group(request, pk):
    group=Group.objects.get(id=pk)
    form=CreateGroupForm(instance=group)
    if request.method == 'POST':
        form=CreateGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.info(request, 'Department updated successfully')
            return redirect('dept')
        
    context={'form': form}
    return render(request, 'update_group.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_group(request, pk):
    group=Group.objects.get(id=pk)
    group.delete()
    messages.info(request, 'Department deleted successfully')
    return redirect('dept')
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def create_course(request):
    form=CreateCourseForm()
    if request.method == 'POST':
        form=CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Created course successfully')
            if request.POST.get("create_course_add"):
                return redirect('create_course')
            elif request.POST.get("create_course"):
                return redirect('adminPage')

    context={'form':form}
    return render(request, 'create_course.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_course(request, pk):
    course=Course.objects.get(id=pk)
    form=CreateCourseForm(instance=course)
    if request.method == 'POST':
        form=CreateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.info(request, 'Course updated successfully')
            return redirect('course_admin', course.dept.id)
        
    context={'form': form, 'pk':course.dept.id}
    return render(request, 'update_course.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_course(request, pk):
    course=Course.objects.get(id=pk)
    id=course.dept.id
    course.delete()
    messages.info(request, 'Course deleted successfully')
    return redirect('course_admin', id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def generate_paper_form(request):
    form=GeneratePaperForm()
    if request.method == 'POST':
        form=GeneratePaperForm(request.POST)
        if form.is_valid():
            dept=form.cleaned_data['group']
            sem=form.cleaned_data['sem']
            course=form.cleaned_data['course']
            pname=course
            difficulty=form.cleaned_data['difficulty']
            term=form.cleaned_data['term']
            exam_date=form.cleaned_data['exam_date']
            #print(dept, pname, sem, course, term, exam_date)
            qp=paper_data(request, course, difficulty)
            if qp==None:    
                return redirect('adminPage')
            else:
                encoded_qp = json.dumps(qp)
                p=Paper(pname=pname, term=term, exam_date=exam_date, dept=dept, sem=sem, course=course, difficulty=difficulty, qp=encoded_qp)
                p.save()
                messages.info(request, 'Paper Generated Successfully')
                return redirect('adminPage')

    context={'form':form}
    return render(request, 'generate_paper_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def get_course_options(request):
    dept = request.GET.get('dept')
    sem = request.GET.get('sem')

    # Filter the foreign key queryset based on the selection value
    if dept:
        if sem:
            filtered_courses = Course.objects.filter(dept=dept, sem=sem)
        else:
            filtered_courses = Course.objects.filter(dept=dept)
    else:
        if sem:
            filtered_courses = Course.objects.filter(sem=sem)
        else:
            filtered_courses = Course.objects.all()
    # Create the options HTML
    options = ''.join([f'<option value="">---------</option>'] + [f'<option value="{obj.id}">{obj}</option>' for obj in filtered_courses])

    return JsonResponse({'options': options})

def remove_text_in_brackets(text):
    pattern = r'\([^)]*\)'  # Matches anything between parentheses including the parentheses themselves
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def view_paper(request, pk):
    SEM={1:'First', 2:'Second', 3:'Third', 4:'Fourth', 5:'Fifth', 6:'Sixth', 7:'Seventh', 8:'Eighth'}
    # DEPT={2:'Computer Science and Engineering', 3:'Information Science and Engineeing', 5:'Electronics and Communication Engineering', 6:'Data Science and Engineering', 8:'Artificial Intelligence and Machine Learning'}
    paper=Paper.objects.get(id=pk)
    pname=paper.pname
    course=paper.course
    exam_date=paper.exam_date
    s=paper.sem
    sem=SEM[int(s)]
    d=paper.dept.name
    #dept=DEPT[d]
    mod=range(1,6)

    dept = remove_text_in_brackets(d)

    qp = json.loads(paper.qp)

    m = qp['mcq']['question']
    option1 = qp['mcq']['option1']
    option2 = qp['mcq']['option2']
    option3 = qp['mcq']['option3']
    option4 = qp['mcq']['option4']
    mcq_mark = qp['mcq']['mark']

    mcq=zip(m, option1, option2, option3, option4, mcq_mark)

    q1a = qp['q1a']['question']
    q1b = qp['q1b']['question']
    q2a = qp['q2a']['question']
    q2b = qp['q2b']['question']
    q3a = qp['q3a']['question']
    q3b = qp['q3b']['question']
    q4a = qp['q4a']['question']
    q4b = qp['q4b']['question']
    q5a = qp['q5a']['question']
    q5b = qp['q5b']['question']

    q1a_mark = qp['q1a']['mark']
    q1b_mark = qp['q1b']['mark']
    q2a_mark = qp['q2a']['mark']
    q2b_mark = qp['q2b']['mark']
    q3a_mark = qp['q3a']['mark']
    q3b_mark = qp['q3b']['mark']
    q4a_mark = qp['q4a']['mark']
    q4b_mark = qp['q4b']['mark']
    q5a_mark = qp['q5a']['mark']
    q5b_mark = qp['q5b']['mark']
    
    context={'pname': pname, 'course': course, 'sem': sem, 'dept': dept, 'exam_date': exam_date, 'mod': mod,
        'mcq': mcq, 
        'q1a': q1a, 'q1b': q1b, 'q2a': q2a, 'q2b': q2b, 'q3a': q3a, 'q3b': q3b, 'q4a': q4a, 'q4b': q4b, 'q5a': q5a, 'q5b': q5b,
        'q1a_mark': q1a_mark, 'q1b_mark': q1b_mark, 'q2a_mark': q2a_mark, 'q2b_mark': q2b_mark, 'q3a_mark': q3a_mark, 'q3b_mark': q3b_mark, 'q4a_mark': q4a_mark, 'q4b_mark': q4b_mark, 'q5a_mark': q5a_mark, 'q5b_mark': q5b_mark
    }
    
    # getting the template
    pdf = html_to_pdf('generate_paper.html', context)
        
    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def download_paper(request, pk):
    
    SEM={1:'First', 2:'Second', 3:'Third', 4:'Fourth', 5:'Fifth', 6:'Sixth', 7:'Seventh', 8:'Eighth'}
    #DEPT={2:'Computer Science and Engineering', 3:'Information Science and Engineeing', 5:'Electronics and Communication Engineering', 6:'Data Science and Engineering', 8:'Artificial Intelligence and Machine Learning'}
    paper=Paper.objects.get(id=pk)
    pname=paper.pname
    course=paper.course
    exam_date=paper.exam_date
    s=paper.sem
    sem=SEM[int(s)]
    d=paper.dept.name
    #dept=DEPT[d]
    mod=range(1,6)

    dept = remove_text_in_brackets(d)

    qp = json.loads(paper.qp)

    m = qp['mcq']['question']
    option1 = qp['mcq']['option1']
    option2 = qp['mcq']['option2']
    option3 = qp['mcq']['option3']
    option4 = qp['mcq']['option4']
    mcq_mark = qp['mcq']['mark']

    mcq=zip(m, option1, option2, option3, option4, mcq_mark)

    q1a = qp['q1a']['question']
    q1b = qp['q1b']['question']
    q2a = qp['q2a']['question']
    q2b = qp['q2b']['question']
    q3a = qp['q3a']['question']
    q3b = qp['q3b']['question']
    q4a = qp['q4a']['question']
    q4b = qp['q4b']['question']
    q5a = qp['q5a']['question']
    q5b = qp['q5b']['question']

    q1a_mark = qp['q1a']['mark']
    q1b_mark = qp['q1b']['mark']
    q2a_mark = qp['q2a']['mark']
    q2b_mark = qp['q2b']['mark']
    q3a_mark = qp['q3a']['mark']
    q3b_mark = qp['q3b']['mark']
    q4a_mark = qp['q4a']['mark']
    q4b_mark = qp['q4b']['mark']
    q5a_mark = qp['q5a']['mark']
    q5b_mark = qp['q5b']['mark']
    
    context={'pname': pname, 'course': course, 'sem': sem, 'dept': dept, 'exam_date': exam_date, 'mod': mod,
        'mcq': mcq, 
        'q1a': q1a, 'q1b': q1b, 'q2a': q2a, 'q2b': q2b, 'q3a': q3a, 'q3b': q3b, 'q4a': q4a, 'q4b': q4b, 'q5a': q5a, 'q5b': q5b,
        'q1a_mark': q1a_mark, 'q1b_mark': q1b_mark, 'q2a_mark': q2a_mark, 'q2b_mark': q2b_mark, 'q3a_mark': q3a_mark, 'q3b_mark': q3b_mark, 'q4a_mark': q4a_mark, 'q4b_mark': q4b_mark, 'q5a_mark': q5a_mark, 'q5b_mark': q5b_mark
    }
    
    # getting the template
    pdf = html_to_pdf('generate_paper.html', context)
        
    # rendering the template
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "%s.pdf" %(str(pname)+" "+str(exam_date))
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    return response

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_paper(request, pk):
    paper=Paper.objects.get(id=pk)
    paper.delete()
    messages.info(request, 'Question Paper deleted successfully')
    return redirect('adminPage')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def dept(request):
    groups=Group.objects.exclude(name="Admin")
    context={'groups':groups}
    return render(request, 'dept.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def dept_info(request, pk):
    group=Group.objects.get(id=pk)
    context={'group':group}
    return render(request, 'dept_info.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def dept_users(request, pk):
    group=Group.objects.get(id=pk)
    users=User.objects.filter(groups=group.id)
    context={'group':group, 'users':users, 'pk':group.id}
    return render(request, 'dept_users.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_user(request, pk):
    user=User.objects.get(id=pk)
    group=user.groups.all()[0].id
    email = user.email
    form=UpdateUserForm(instance=user, initial={'group':group,'email_disabled':email})
    if request.method == 'POST':
        form=UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            u = form.save()
            new_group=form.cleaned_data['group']
            u.groups.clear()
            u.groups.add(new_group)
            messages.info(request, 'User updated successfully')
            return redirect('dept_users', group)
        
    context={'form': form, 'pk':group}
    return render(request, 'update_user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_user(request, pk):
    user=User.objects.get(id=pk)
    id=user.groups.all()[0].id
    user.delete()
    messages.info(request, 'User deleted successfully')
    return redirect('dept_users', id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def course_admin(request, pk):
    group=Group.objects.get(id=pk)
    courses=Course.objects.filter(dept__name=group)
    sem1=courses.filter(sem=1)
    sem2=courses.filter(sem=2)
    sem3=courses.filter(sem=3)
    sem4=courses.filter(sem=4)
    sem5=courses.filter(sem=5)
    sem6=courses.filter(sem=6)
    sem7=courses.filter(sem=7)
    sem8=courses.filter(sem=8)
    context={'group':group, 'sem1':sem1, 'sem2':sem2, 'sem3':sem3, 'sem4':sem4, 'sem5':sem5, 'sem6':sem6, 'sem7':sem7, 'sem8':sem8, 'pk':pk}
    return render(request, 'course_admin.html', context)

@login_required(login_url='login')
@allowed_dept
def course(request, pk):
    group=Group.objects.get(id=pk)
    courses=Course.objects.filter(dept__name=group)
    sem1=courses.filter(sem=1)
    sem2=courses.filter(sem=2)
    sem3=courses.filter(sem=3)
    sem4=courses.filter(sem=4)
    sem5=courses.filter(sem=5)
    sem6=courses.filter(sem=6)
    sem7=courses.filter(sem=7)
    sem8=courses.filter(sem=8)
    context={'group':group, 'sem1':sem1, 'sem2':sem2, 'sem3':sem3, 'sem4':sem4, 'sem5':sem5, 'sem6':sem6, 'sem7':sem7, 'sem8':sem8}
    return render(request, 'course.html', context)

@login_required(login_url='login')
@allowed_course
def modules(request, pk):
    course=Course.objects.get(id=pk)
    modules=Module.objects.filter(course=pk).order_by('modno')
    context={'modules':modules, 'course_id':pk, 'course_name':course, 'pk':course.dept.id}
    return render(request, 'modules.html', context)

@login_required(login_url='login')
@allowed_course
def create_module(request, pk):
    form=CreateModuleForm(initial={'course':pk, 'course_disabled':pk})
    if request.method == 'POST':
        form=CreateModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Created module successfully')
            if request.POST.get("create_module_add"):
                return redirect('create_module', pk)
            elif request.POST.get("create_module"):
                return redirect('modules', pk)

    context={'form':form, 'pk':pk}
    return render(request, 'create_module.html', context)

@login_required(login_url='login')
@allowed_module
def update_module(request, pk):
    module=Module.objects.get(id=pk)
    form=CreateModuleForm(instance=module, initial={'course_disabled':module.course.id})
    if request.method == 'POST':
        form=CreateModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.info(request, 'Module updated successfully')
            return redirect('modules', module.course.id)

    context={'form':form, 'pk':module.course.id}
    return render(request, 'update_module.html', context)

@login_required(login_url='login')
@allowed_module
def delete_module(request, pk):
    module=Module.objects.get(id=pk)
    id=module.course.id
    module.delete()
    messages.info(request, 'Module deleted successfully')
    return redirect('modules', id)

@login_required(login_url='login')
@allowed_module
def questions(request, pk):
    module=Module.objects.get(id=pk)
    context={'module':module, 'pk':module.course.id}
    return render(request, 'questions.html', context)

@login_required(login_url='login')
@allowed_module
def mcq_questions(request, pk):
    module=Module.objects.get(id=pk)
    questions=Mcq.objects.filter(module=pk)
    context={'questions':questions, 'module':module,'pk':pk}
    return render(request, 'mcq_questions.html', context)

@login_required(login_url='login')
@allowed_mcq
def update_mcq(request, pk):
    question=Mcq.objects.get(id=pk)
    form=CreateMcqForm(instance=question, initial={'module_disabled':question.module.id})
    if request.method == 'POST':
        form=CreateMcqForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.info(request, 'MCQ updated successfully')
            return redirect('mcq_questions', question.module.id)

    context={'form':form,'pk':question.module.id}
    return render(request, 'update_mcq.html', context)

@login_required(login_url='login')
@allowed_mcq
def delete_mcq(request, pk):
    question=Mcq.objects.get(id=pk)
    id=question.module.id
    question.delete()
    messages.info(request, 'MCQ deleted successfully')
    return redirect('mcq_questions', id)

@login_required(login_url='login')
@allowed_module
def theory_questions(request, pk):
    module=Module.objects.get(id=pk)
    questions=Question.objects.filter(module=pk)
    context={'questions':questions, 'module':module,'pk':pk}
    return render(request, 'theory_questions.html', context)

@login_required(login_url='login')
@allowed_question
def update_question(request, pk):
    question=Question.objects.get(id=pk)
    form=CreateQuestionForm(instance=question, initial={'module_disabled':question.module.id})
    if request.method == 'POST':
        form=CreateQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.info(request, 'Question updated successfully')
            return redirect('theory_questions', question.module.id)

    context={'form':form,'pk':question.module.id}
    return render(request, 'update_question.html', context)

@login_required(login_url='login')
@allowed_question
def delete_question(request, pk):
    question=Question.objects.get(id=pk)
    id=question.module.id
    question.delete()
    messages.info(request, 'Question deleted successfully')
    return redirect('theory_questions', id)

@login_required(login_url='login')
@allowed_module
def create_mcq(request, pk):
    form=CreateMcqForm(initial={'module':pk, 'module_disabled':pk})
    if request.method == 'POST':
        form=CreateMcqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Created mcq successfully')
            if request.POST.get("create_mcq_add"):
                return redirect('create_mcq', pk)
            elif request.POST.get("create_mcq"):
                return redirect('questions', pk)
            
    context={'form':form,'pk':pk}
    return render(request, 'create_mcq.html', context)

@login_required(login_url='login')
@allowed_module
def create_question(request, pk):
    form=CreateQuestionForm(initial={'module':pk, 'module_disabled':pk})
    if request.method == 'POST':
        form=CreateQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Created question successfully')
            if request.POST.get("create_question_add"):
                return redirect('create_question', pk)
            elif request.POST.get("create_question"):
                return redirect('questions', pk)
            
    context={'form':form,'pk':pk}
    return render(request, 'create_question.html', context)
