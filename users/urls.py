from django.urls import path
from .import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    #New User Registration Page
    path('signup', views.signup, name='signup'),

    #Log In page.
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),

    #Log Out.
    path('logout', views.logout, name='logout'),

    # Current User Profile Page
    path('profile', views.profile, name='profile'),

    # Report Profile
    path('report_profile/<int:profile_id>/', views.report_profile, name='report_profile'),

    # Other User's Profile Page
    path('<str:username>/profile', views.profile, name='user_profile'),

    # Edit Profile Page
    path('edit_profile', views.edit_profile, name='edit_profile'),

    # Change Password Page
   	path('change_password', views.change_password, name='change_password'),
]
