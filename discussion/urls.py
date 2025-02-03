from django.urls import path
from .import views


urlpatterns = [

    # Create Discussion
    path('create_discussion/', views.create_discussion, name='create_discussion'),

    #Submit thread on discussion.
    path('submit_thread/<int:discussion_id>/', views.submit_thread),

    # Delete Discussion
    path('delete_discussion/<int:discussion_id>/', views.delete_discussion),

    # Delete Thread
    path('delete_thread/<int:thread_id>/', views.delete_thread),

    # Close Discussion
    path('close_discussion/<int:discussion_id>/', views.close_discussion),

    # Save Discussion
    path('save_discussion/<int:discussion_id>/', views.save_discussion),

    # Save Thread
    path('save_thread/<int:thread_id>/', views.save_thread),

    # Follow Discussion
    path('follow_discussion/<int:discussion_id>/', views.follow_discussion),

    # Report Discussion
    path('report_discussion/<int:discussion_id>/', views.report_discussion),

    # Report Thread
    path('report_thread/<int:thread_id>/', views.report_thread),

    # Like Discussion
    path('like_discussion/<int:discussion_id>/', views.like_discussion),

    # Like Thread
    path('like_thread/<int:thread_id>/', views.like_thread),

    # Discuss Detail Page
    path('discussion/<int:discussion_id>', views.discussion_detail, name='discussion_detail'),

    # Specefic  Thread Page
    path('discussion/<int:discussion_id>/<int:anchor>', views.discussion_detail, name='specefic_thread'),

    # Customize Interest Page
    path('interest', views.interest, name='interest'),

    # Category Detail Page
    path('explore/category/<str:category_title>', views.category_detail, name='category_detail'),

    # Follow category
    path('follow_category/<str:category_id>/', views.follow_category),

    # Current User's Discussions
    path('discussions', views.discussions, name='discussions'),

    # Current User's Threads
    path('threads', views.threads, name='threads'),

    # Other User's Discussions
    path('<str:username>/discussions', views.discussions, name='user_discussions'),

    # Other User's Threads
    path('<str:username>/threads', views.threads, name='user_threads'),


    # Current User's Saved Discussions
    path('saved_discussions', views.saved_discussions, name='saved_discussions'),

    # Current User's Followed Discussions
    path('followed_discussions', views.followed_discussions, name='followed_discussions'),

    # Current User's Saved Threads
    path('saved_threads', views.saved_threads, name='saved_threads'),

    #Search discussion returns HttPResponse.
    path('search_discussion', views.search_discussion, name='search_discussion'),
]
