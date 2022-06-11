from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
from django.contrib import messages


def projects(request):
    """ Функция проектов """
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                                 Q(owner__name__icontains=search_query) |
                                                 Q(tags__in=tags))

    context = {'projects': projects, 'search_query': search_query}
    return render(request, 'projects.html', context)


def project(request, pk):
    """ Функция отдельного проекта """
    project_obj = Project.objects.get(id=pk)

    # Комментарии и оценка
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()
        messages.success(request, 'Your review was posted')

        # Вызов функции подсчета голосов
        project_obj.get_vote


        return redirect('project', pk=project_obj.id)

    return render(request, 'single_project.html', {'project': project_obj, 'form': form})


@login_required(login_url='login')
def create_project(request):
    """ Функция создания проекта """
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Your review was posted')
            return redirect('projects')

    context = {'form': form}
    return render(request, 'project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    """ Функция обновления проекта """
    profile = request.user.profile  # Никто кроме владельца проекта не сможет изменить его
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    """ Функция удаления проекта """
    profile = request.user.profile  # Никто кроме владельца проекта не сможет изменить его
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, 'delete_template.html', context)
