from django.shortcuts import render
from discussion.models import Discussion
from django.contrib.auth.decorators import login_required
from .models import AdminPost

def home(request):
    """Home Page"""
    # If user is logged in craete feed for him (based on interest).

    if request.user.is_authenticated:

        user = request.user
        discussions = []

        # Making list of category.titles from the categories user follows.
        followed_categories = user.profile.followed_categories.values_list('title', flat=True).distinct()
        all_discussions = Discussion.objects.all().order_by("-date_created")

        for discussion in all_discussions:
            if discussion.user !=  user and discussion.closed == False and  discussion.category in followed_categories:
                discussions.append(discussion)

        saved_discussions = user.profile.saved_discussions.all()
        liked_discussions = user.profile.liked_discussions.all()

        context={"discussions": discussions, "saved_discussions": saved_discussions, "liked_discussions": liked_discussions}

    else:
        context = {}

    return render(request, 'core/home.html', context)

@login_required
def most_popular(request):
    """Most Popular Discussions Page"""
    user = request.user

    discussions = Discussion.objects.all().order_by("-views")

    saved_discussions = user.profile.saved_discussions.all()
    liked_discussions = user.profile.liked_discussions.all()

    context={"discussions": discussions, "saved_discussions": saved_discussions, "liked_discussions": liked_discussions}

    return render(request, 'core/most_popular.html', context)

@login_required
def most_liked(request):
    """Most Liked Discussions Page"""
    user = request.user

    discussions = Discussion.objects.all().order_by("-likes")

    saved_discussions = user.profile.saved_discussions.all()
    liked_discussions = user.profile.liked_discussions.all()

    context={"discussions": discussions, "saved_discussions": saved_discussions, "liked_discussions": liked_discussions}

    return render(request, 'core/most_liked.html', context)


def admin_posts(request):
    """Official page of admin sahab where all posts (from admin) will appear."""
    posts = AdminPost.objects.all().order_by("-date_created")
    context = {"posts": posts}
    return render(request, 'core/admin_posts.html', context)

def privacy_policy(request):
    """Privacy Policy Page"""
    return render(request, 'core/privacy_policy.html')

def terms_and_conditions(request):
    """Terms & Conditions Page"""
    return render(request, 'core/terms_and_conditions.html')

def about_us(request):
    """About us Page"""
    return render(request, 'core/about_us.html')

def contact_us(request):
    """Contact us Page"""
    return render(request, 'core/contact_us.html')
