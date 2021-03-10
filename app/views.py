from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from app.models import *
from app.forms import *
from django import forms


@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def employee(request):
    list = Employee.objects.all()
    context = {'list': list, 'segment': 'employees'}

    html_template = loader.get_template('employees.html')
    return HttpResponse(html_template.render(context, request))


class EmployeeCreate(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['fio', 'position', ]


def add_employee(request):
    upload = EmployeeCreate()
    if request.method == 'POST':
        upload = EmployeeCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('/%2Femployee')
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : '/%2Femployee'}}">reload</a>""")
    else:
        list = Position.objects.all()
        context = {
            "upload_form": upload,
            "list": list,
            "action": "Добавить"
        }
        return render(request, 'add-employee.html', context)

@login_required(login_url="/admin-panel/login/")
def update_employee(request, emp_id: int):
    try:
        emp_sel = Employee.objects.get(pk=emp_id)
    except emp_id.DoesNotExist:
        return redirect('/%2Femployee')
    news_form = EmployeeCreate(request.POST, request.FILES or None, instance=emp_sel)
    if news_form.is_valid():
        news_form.save()
        return redirect('/%2Femployee')

    list = Position.objects.all()
    context = {
        "ProductForm": news_form,
        "ProductModel": emp_sel,
        "list": list,
        "action": "Обновить"
    }
    return render(request, 'add-employee.html', context)


@login_required(login_url="/admin-panel/login/")
def delete_employee(request, emp_id: int):
    try:
        emp_sel = Employee.objects.get(pk=emp_id)
    except emp_id.DoesNotExist:
        return redirect('/%2Femployee')
    emp_sel.delete()
    return redirect('/%2Femployee')


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
