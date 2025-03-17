from django.contrib import admin
from django.urls import path, include
from credits import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply/', views.submit_credit_application, name='apply_credit'),
    path('credit-applications/', views.credit_applications_list, name='credit_applications_list'),
    path('accounts/', include('django.contrib.auth.urls')),  # login/, logout/, password_reset/ и т. д.
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
