from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.home, name='home'),

    path('about/', views.about, name='about'),

    path('why-children/', views.why_children, name='why_children'),

    path('child-education/', views.child_education, name='child_education'),

    path('child-health/', views.child_health, name='child_health'),

    path('stop-child-labour/', views.stop_child_labour, name='stop_child_labour'),

    path('contact/', views.contact, name='contact'),

    path('faqs/', views.faqs, name='faqs'),

    path('register/', views.register, name='register'),

    path('login/', views.login_user, name='login'),

    path('logout/', views.logout_user, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('donate/', views.donate, name='donate'),

    path('payment-success/', views.payment_success, name='payment_success'),

    path(
    'forgot-password/',
    auth_views.PasswordResetView.as_view(
        template_name='forgot_password.html',
        success_url='/password-reset-done/'
    ),
    name='forgot_password'
),

path(
    'password-reset-done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ),
    name='password_reset_complete'
),
 
]
