from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('/employee', views.employee, name='employee'),
    path('/employee/add', views.add_employee, name='add-employee'),
    path('employee/update/<int:emp_id>', views.update_employee),
    path('employee/delete/<int:emp_id>', views.delete_employee),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]