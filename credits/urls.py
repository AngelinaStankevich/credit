from django.contrib import admin
from django.urls import path, include
from credits import views
from django.contrib.auth import views as auth_views
from .views import manage_applications, review_application


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply/', views.submit_credit_application, name='apply_credit'),
    path('credit-applications/', views.credit_applications_list, name='credit_applications_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('manage/', manage_applications, name='manage_applications'),
    path('review/<int:application_id>/', review_application, name='review_application'),
    path('submit-credit-application/', views.submit_credit_application, name='submit_credit_application'),
    path('profile/', views.profile, name='profile'),
]
