from django.urls import path
from .import views


urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Admin Posts Page.
    path('admin_posts', views.admin_posts, name='admin_posts'),

    # Most Popular Discussions Page
    path('most_popular', views.most_popular, name='most_popular'),

    # Most Liked Discussions Page
    path('most_liked', views.most_liked, name='most_liked'),

    # Privacy Policy Page
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),

    # Terms & Conditions Page
    path('terms_and_conditions', views.terms_and_conditions, name='terms_and_conditions'),

    # About Us Page
    path('about_us', views.about_us, name='about_us'),

    # Contact Us Page
    path('contact_us', views.contact_us, name='contact_us'),

]
