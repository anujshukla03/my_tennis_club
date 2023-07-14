from django.urls import path
from . import views
 

urlpatterns = [
#========================================================================ticket-url
    path('new-ticket/', views.new_ticket, name='new_ticket'),
    path('manage-tickets/', views.manage_tickets, name='manage_tickets'),
    path('delete-ticket/<int:id>/', views.delete_ticket, name='delete_ticket'),
#=========================================================================department-user
    path('department_list/', views.department_list , name='department_list'),
    path('user_list/', views.user_list , name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/assign-department/', views.assign_department, name='assign_department'),
    path('departments/create/', views.create_department, name='create_department'),
    path('departments/<int:department_id>/update/', views.update_department, name='update_department'),
    path('departments/<int:department_id>/delete/', views.delete_department, name='delete_department'),
#==========================================================================login
    path('', views.login_view, name='login'),
    path('signup' , views.signup , name="signup"),
    path('homepage' , views.homepage , name="homepage"),
]
