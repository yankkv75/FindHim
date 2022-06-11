from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('account/', views.user_account, name='account'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('edit-skill/', views.edit_skill, name='edit-skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill')
]
