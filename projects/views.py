from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from projects.forms import CreateTaskForm
from projects.models import Project, PriorityTask, Task, TaskList


def home(request):
    return render(request, 'home/home.html')

def create_modal(
        request,
        form,
        url,
        title,
        obj_instance=None,
        form_initial=None,
        func_fix_form=None,
        success_msg=None,
        refresh='content',
):
    options_form = {'instance': obj_instance}
    if form_initial:
        options_form['initial'] = form_initial

    if request.method == 'POST':
        f = form(request.POST, **options_form)

        if func_fix_form:
            func_fix_form(form=f)

        if f.is_valid():
            s = f.save()

            if success_msg:
                messages.success(request, f'{success_msg}')

            response = HttpResponse()

            # todo define ids - make id content of whole page - content
            response['X-IC-Script'] = f'Intercooler.refresh($("#{refresh}"));'

            return response

    # todo check if error think has to be post again
    f = form(**options_form)

    context = {
        'form': f,
        'url': url,
        'title': title
    }

    response = render(request, 'extra/create_forms.html', context=context)

    # todo check toggle
    response['X-IC-Script'] = '$("#modal_base").modal("show");'

    return response


# todo
# @login_required
def projects(request):

    # projects = Project.objects.filter(
    #     user_id=request.user.id
    # )

    project = Project.objects.all()

    return render(request, 'projects/projects_base.html', context={'projects': project})

# todo
# @login_required
def view_project(request, project_id):
    project = Project.objects.get(id=project_id)

    return render(request, 'projects/view_project.html', context={'item': project})


# @login_required todo
def drag_list(request):
    list_id = int(request.GET.get('list_id'))
    target_list = request.GET.get('target')
    index_after = int(request.GET.get('index_after'))

    print(list_id)
    print(target_list)
    print(index_after)

    list = TaskList.objects.get(id=list_id)

    # try:
    #     new_numero = Tarefa.objects.filter(
    #         projeto_id=project_id,
    #         status__gte=dictionary[target_list],
    #     )[index_after].ordem
    # except IndexError:
    #     new_numero = Tarefa.objects.filter(
    #         projeto_id=project_id,
    #         status__lte=dictionary[target_list],
    #     ).last().ordem
    #
    # Tarefa.objects.filter(
    #     id=tarefa_id
    # ).update(
    #     status=dictionary[target_list],
    #     ordem=new_order
    # )
    #
    # Tarefa.objects.filter(
    #     projeto_id=project_id,
    #     ordem__gte=new_order,
    # ).exclude(id=tarefa_id).update(ordem=F('ordem') + 1)

    return HttpResponse()


# @login_required todo
def drag_task(request, project_id):
    # tarefa_id = int(request.GET.get('tarefa_id'))
    # target_list = int(request.GET.get('target'))
    # index_after = int(request.GET.get('index_after'))
    # 
    # # Todo: check with one task
    # 
    # try:
    #     new_order = Task.objects.filter(
    #         projeto_id=project_id,
    #         list__numero__gte=target_list,
    #     )[index_after].ordem
    # except IndexError:
    #     new_order = Task.objects.filter(
    #         projeto_id=project_id,
    #         list__numero__lte=target_list,
    #     ).last().ordem
    # 
    # Task.objects.filter(
    #     id=tarefa_id
    # ).update(
    #     list_id=Task.objects.get(project_id=project_id, numero=target_list),
    #     ordem=new_order
    # )
    # 
    # Task.objects.filter(
    #     project_id=project_id,
    #     list__isnull=False,
    #     ordem__gte=new_order,
    # ).exclude(id=tarefa_id).update(ordem=F('ordem') + 1)

    return HttpResponse()


# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = ContactForm()
#
#     context = {'form': form}
#     return render(request, 'contacts/contact_page.html', context)

# todo
# @login_required
def create_project(request):

    def fix_form(form):
        form.instance.user_id = request.user.id

    return create_modal(
        request,
        modelform_factory(Project, fields=['name', 'description']),
        f'/create_project',
        'Create Project',
        func_fix_form=fix_form,
        success_msg='Project {s.name} created successfully',
    )

# todo
# @login_required
def edit_project(request, project_id):
    return create_modal(
        request,
        modelform_factory(Project, fields=['name', 'description']),
        f'/edit_project/{project_id}',
        'Edit Project',
        obj_instance=Project.objects.get(id=project_id),
        success_msg='Project {s.name} edited successfully',
    )

# todo
# @login_required
@require_POST
def delete_project(request, project_id):
    # Task.objects.filter(
    #     project_id=project_id
    # ).delete()
    #
    # TaskList.objects.filter(
    #     project_id=project_id
    # ).delete()
    # todo testar sem pra ver se faz cascade ou se precisa fazer assim

    Project.objects.get(id=project_id).delete()

    messages.success(request, 'Project deleted successfully')

    response = HttpResponse()

    # todo check content
    response['X-IC-Script'] = f'Intercooler.refresh($("#content"));'

    return response


# @login_required todo
def create_task(request, list_id):
    tlist = TaskList.objects.get(id=list_id)

    def fix_form(form):
        form.instance.list_id = tlist.id

    return create_modal(
        request,
        CreateTaskForm,
        f'/create_task/{list_id}',
        'Create New Task',
        form_initial={'project': tlist.project},
        func_fix_form=fix_form,
        success_msg='Task {s.title} create successfully',
    )

# todo
# @login_required
@require_POST
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()

    messages.success(request, 'Task deleted successfully')

    response = HttpResponse()

    # todo check content
    response['X-IC-Script'] = f'Intercooler.refresh($("#content"));'

    return response

# todo
# @login_required
@require_POST
def delete_all_task_list(request, list_id):
    Task.objects.filter(
        list_id=list_id,
    ).delete()

    messages.success(request, 'Task deleted successfully')

    response = HttpResponse()

    # todo check content
    response['X-IC-Script'] = f'Intercooler.refresh($("#content"));'

    return response

# todo
# @login_required
def edit_list(request, list_id):
    return create_modal(
        request,
        modelform_factory(TaskList, fields=['name']),
        f'/edit_list/{list_id}',
        'Edit List',
        obj_instance=TaskList.objects.get(id=list_id),
        success_msg='List edited successfully',
    )


# @login_required todo
def create_priority_task(request, project_id):
    name = request.POST.get('priority', None)

    response = HttpResponse()

    if request.method == "POST":
        if name:
            PriorityTask.objects.create(
                name=name,
                project_id=project_id
            )

            messages.success(request, 'Priority Created Successively')

    # todo check content
    response['X-IC-Script'] = f'Intercooler.refresh($("#content"));'

    return response

# @login_required #todo
def edit_priority(request, priority_id):
    return create_modal(
        request,
        modelform_factory(PriorityTask, fields=['name']),
        f'/edit_priority/{priority_id}',
        'Edit Priority',
        obj_instance=PriorityTask.objects.get(id=priority_id),
        success_msg='Priority edited successfully',
    )


# @login_required # todo
@require_POST
def delete_priority(request, priority_id):
    print('ENTROU NA VIEW')
    PriorityTask.objects.get(id=priority_id).delete()

    messages.success(request, 'Priority deleted successfully')

    response = HttpResponse()

    # todo nao ta dando refresh
    response['X-IC-Script'] = f'Intercooler.refresh($("#content"));'

    return response

# todo
# @login_required
def delete_list(request, list_id):
    # Task.objects.filter(
    #     list_id=list_id
    # ).delete()
    # todo testar sem pra ver se faz cascade ou se precisa fazer assim

    TaskList.objects.get(id=list_id).delete()

    messages.success(request, 'Task List deleted successfully')

    response = HttpResponse()

    # todo check content
    response['X-IC-Script'] = f'Intercooler.refresh($("#content"));'

    return response
