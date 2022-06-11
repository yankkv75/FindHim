from django.shortcuts import render, redirect
from .models import Profile, Skill
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm, ProfileForm, SkillForm


def profiles(request):

    # Поиск по имени и скиллам
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__iexact=search_query)

    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                                 Q(skill__in=skills))
    context = {'profiles': profiles, 'search_query': search_query}
    return render(request, 'profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    main_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')

    context = {'profile': profile, 'main_skills': main_skills, 'other_skills': other_skills}
    return render(request, 'user_profile.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile

    main_skills = profile.skill_set.exclude(description__exact='')

    context = {'profile': profile, 'main_skills': main_skills}
    return render(request, 'account.html', context)


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'login_register.html')


def logout_user(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Account successfully created')

            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.success(request, 'An unknown error occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context=context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'edit_profile.html', context)


@login_required(login_url='login')
def edit_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'edit_skill.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)
