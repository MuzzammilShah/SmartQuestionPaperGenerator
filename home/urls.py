from django.urls import path
from django.contrib.auth import views as auth_views
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('change_password_complete/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
    path('home/', views.homePage, name="home"),
    path('adminPage/', views.adminPage, name='adminPage'),
    path('adminPage/createUser/', views.create_user, name='create_user'),
    path('get_email/', views.get_email, name='get_email'),
    path('adminPage/createDept/', views.create_group, name='create_group'),
    path('adminPage/createCourse/', views.create_course, name='create_course'),
    path('adminPage/generatePaperForm/', views.generate_paper_form, name='generate_paper_form'),
    path('get_course_options/', views.get_course_options, name='get_course_options'),
    path('adminPage/viewPaper/<str:pk>/', views.view_paper, name='view_paper'),
    path('adminPage/downloadPaper/<str:pk>/', views.download_paper, name='download_paper'),
    path('adminPage/deletePaper/<str:pk>/', views.delete_paper, name='delete_paper'),
    path('userAdmin/dept/', views.dept, name='dept'),
    path('userAdmin/updateDept/<str:pk>/', views.update_group, name='update_group'),
    path('userAdmin/deleteDept/<str:pk>/', views.delete_group, name='delete_group'),
    path('userAdmin/dept/<str:pk>/', views.dept_info, name='dept_info'),
    path('userAdmin/dept/teachers/<str:pk>/', views.dept_users, name='dept_users'),
    path('userAdmin/dept/teachers/updateTeacher/<str:pk>/', views.update_user, name='update_user'),
    path('userAdmin/dept/teachers/deleteTeacher/<str:pk>/', views.delete_user, name='delete_user'),
    path('userAdmin/dept/courses/<str:pk>/', views.course_admin, name='course_admin'),
    path('userAdmin/dept/updateCourse/<str:pk>/', views.update_course, name='update_course'),
    path('userAdmin/dept/deleteCourse/<str:pk>/', views.delete_course, name='delete_course'),
    path('dept/<str:pk>/', views.course, name='course'),
    path('dept/course/<str:pk>/', views.modules, name='modules'),
    path('dept/course/createModule/<str:pk>/', views.create_module, name='create_module'),
    path('dept/course/updateModule/<str:pk>/', views.update_module, name='update_module'),
    path('dept/course/deleteModule/<str:pk>/', views.delete_module, name='delete_module'),
    path('dept/course/module/<str:pk>/', views.questions, name='questions'),
    path('dept/course/module/mcqQuestions/<str:pk>/', views.mcq_questions, name='mcq_questions'),
    path('dept/course/module/theoryQuestions/<str:pk>/', views.theory_questions, name='theory_questions'),
    path('dept/course/module/createMcq/<str:pk>/', views.create_mcq, name='create_mcq'),
    path('dept/course/module/updateMcq/<str:pk>/', views.update_mcq, name='update_mcq'),
    path('dept/course/module/deleteMcq/<str:pk>/', views.delete_mcq, name='delete_mcq'),
    path('dept/course/module/createQuestion/<str:pk>/', views.create_question, name='create_question'),
    path('dept/course/module/updateQuestion/<str:pk>/', views.update_question, name='update_question'),
    path('dept/course/module/deleteQuestion/<str:pk>/', views.delete_question, name='delete_question'),
]