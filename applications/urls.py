from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='login.html'
    ),
    name='login'
  ),

  path(
    'register/',
    views.register,
    name='register'
  ),
  path(
    'logout/',
    views.logout_view,
    name='logout'
  ),

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'add/',
        views.add_application,
        name='add_application'
    ),

    path(
        'applications/',
        views.application_list,
        name='application_list'
    ),

    path(
        'edit/<int:application_id>/',
        views.edit_application,
        name='edit_application'
    ),

    path(
        'delete/<int:application_id>/',
        views.delete_application,
        name='delete_application'
    ),

    path('analytics/', views.analytics, name='analytics'),

    path(
    'application/<int:application_id>/',
    views.application_detail,
    name='application_detail'
   ),

   path(
    'application/<int:application_id>/status/',
    views.update_status,
    name='update_status'
   ),
]