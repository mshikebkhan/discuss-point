from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Discussion, Category, Thread
from .forms import DiscussionForm
from notifications.models import Notification

@login_required
def create_discussion(request):
    """Create Discussion Page"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = DiscussionForm()
    else:
        # POST data submitted; process data.
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.user = request.user
            discussion.save()
            messages.success(request, 'Your discussion has been created successfully.')
            return redirect('discussion:discussions')
        else:
            messages.error(request, f' Unable to create! Please correct the error below.')

    context = {'form': form}
    return render(request, 'discussion/create_discussion.html', context)


@login_required
def submit_thread(request, discussion_id):
    """Submit thread with JS"""
    if request.method =="POST":
        response_data= {}
        if Discussion.objects.filter(id=discussion_id).exists():
            discussion = Discussion.objects.get(id=discussion_id)
            if not discussion.closed:
                content = request.POST.get('content')
                if len(content) > 0 and len(content) < 301 :
                    thread = Thread.objects.create(user=request.user, discussion=discussion, content=content)
                    response_data['status'] = "submitted"
                    response_data['user'] = thread.user.first_name+' '+thread.user.last_name
                    response_data['content'] = content
                    response_data['id'] = thread.id
                else:
                    response_data['status'] = 'error'
            else:
                response_data['status'] = 'closed'
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404


@login_required
def delete_discussion(request, discussion_id):
    """Delete discussion with JS."""
    if request.method =="POST":
        response_data= {}
        if Discussion.objects.filter(id=discussion_id).exists():
            discussion = Discussion.objects.get(id=discussion_id)
            if discussion.user == request.user:
                discussion.delete()
                response_data['status'] = "deleted"
            else:
                raise Http404
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def close_discussion(request, discussion_id):
    """Close discussion with JS (Users will not be able to submit threads on the discussion)."""
    if request.method =="POST":
        response_data= {}
        if Discussion.objects.filter(id=discussion_id).exists():
            discussion = Discussion.objects.get(id=discussion_id)
            if discussion.user == request.user:
                if discussion.closed == False:
                    discussion.closed = True
                    discussion.save()
                    response_data['status'] = "closed"
                else:
                    discussion.closed = False
                    discussion.save()
                    response_data['status'] = "open"
            else:
                response_data['status'] = 'error'
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def save_discussion(request, discussion_id):
    """Save discussion with JS."""
    response_data={}
    if request.method == 'POST':
        if Discussion.objects.filter(id=discussion_id).exists():
            discussion = Discussion.objects.get(id=discussion_id)
            profile = request.user.profile
            if discussion not in profile.saved_discussions.all():
                profile.saved_discussions.add(discussion)
                profile.save()
                response_data['status'] = 'saved'
            else:
                profile.saved_discussions.remove(discussion)
                profile.save()
                response_data['status'] = 'removed'
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def save_thread(request, thread_id):
    """Save thread with JS."""
    response_data={}
    if request.method == 'POST':
        if Thread.objects.filter(id=thread_id).exists():
            thread = Thread.objects.get(id=thread_id)
            profile = request.user.profile
            if thread not in profile.saved_threads.all():
                profile.saved_threads.add(thread)
                profile.save()
                response_data['status'] = 'saved'
            else:
                profile.saved_threads.remove(thread)
                profile.save()
                response_data['status'] = 'removed'
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def like_discussion(request, discussion_id):
    """Like discussion with JS."""
    profile = request.user.profile
    response_data={}
    if request.method == 'POST':
        if Discussion.objects.filter(id=discussion_id).exists():
            discussion = Discussion.objects.get(id=discussion_id)
            if discussion.user != request.user:
                if discussion not in profile.liked_discussions.all():
                    profile.liked_discussions.add(discussion)
                    profile.save()
                    discussion.likes += 1
                    discussion.save()
                    response_data['status'] = 'liked'
                    notify = Notification.objects.create(discussion=discussion,  sender=request.user, user=discussion.user, notification_type=1)

                else:
                    profile.liked_discussions.remove(discussion)
                    profile.save()
                    discussion.likes -= 1
                    discussion.save()
                    response_data['status'] = 'unliked'
                    if Notification.objects.filter(discussion=discussion,  sender=request.user, user=discussion.user, notification_type=1).exists():
                        notify = Notification.objects.get(discussion=discussion,  sender=request.user, user=discussion.user, notification_type=1)
                        notify.delete()
            else:
                raise Http404
        else:
            response_data['status'] = 'not_exists'
            print("not exists")
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def like_thread(request, thread_id):
    """Like thread with JS."""
    profile = request.user.profile
    response_data={}
    if request.method == 'POST':
        if Thread.objects.filter(id=thread_id).exists():
            thread = Thread.objects.get(id=thread_id)
            if thread.user != request.user:
                if thread not in profile.liked_threads.all():
                    profile.liked_threads.add(thread)
                    profile.save()
                    thread.likes += 1
                    thread.save()
                    response_data['status'] = 'liked'
                    notify = Notification.objects.create(thread=thread,  sender=request.user, user=thread.user, notification_type=2)

                else:
                    profile.liked_threads.remove(thread)
                    profile.save()
                    thread.likes -= 1
                    thread.save()
                    response_data['status'] = 'unliked'
                    if Notification.objects.filter(thread=thread,  sender=request.user, user=thread.user, notification_type=2).exists():
                        notify = Notification.objects.get(thread=thread,  sender=request.user, user=thread.user, notification_type=2)
                        notify.delete()
            else:
                raise Http404
        else:
            response_data['status'] = 'not_exists'
            print("not exists")
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def report_discussion(request, discussion_id):
    """Report discussion with JS"""
    if request.method =="POST":
        response_data= {}
        if Discussion.objects.filter(id=discussion_id).exists():
            discussion = Discussion.objects.get(id=discussion_id)
            if discussion.user != request.user:
                if discussion.reported == False:
                    discussion.reported = True
                    discussion.save()
                    response_data['status'] = "reported"
                else:
                    discussion.reported = False
                    discussion.save()
                    response_data['status'] = "already_reported"
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def report_thread(request, thread_id):
    """Report thread with JS"""
    if request.method =="POST":
        response_data= {}
        if Thread.objects.filter(id=thread_id).exists():
            thread = Thread.objects.get(id=thread_id)
            if thread.user != request.user:
                if thread.reported == False:
                    thread.reported = True
                    thread.save()
                    response_data['status'] = "reported"
                else:
                    thread.reported = False
                    thread.save()
                    response_data['status'] = "already_reported"
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def discussion_detail(request, discussion_id, anchor=None):
    """Discussion Detail Page"""
    user = request.user
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if discussion.user != request.user:
        discussion.views +=1
        discussion.save()
    threads = Thread.objects.filter(discussion=discussion).order_by("-date_created")

    saved_threads = user.profile.saved_threads.all()
    saved_discussions = user.profile.saved_discussions.all()
    followers = discussion.followers.all()
    liked_discussions = user.profile.liked_discussions.all()
    liked_threads = user.profile.liked_threads.all()

    if anchor:
        anchor = anchor

    context = {"discussion": discussion, "threads": threads, "anchor": anchor, "followers": followers, "liked_threads": liked_threads, "saved_threads": saved_threads,  "saved_discussions": saved_discussions, "liked_discussions": liked_discussions}

    return render(request, 'discussion/discussion_detail.html', context)


@login_required
def interest(request):
    """Customize interest Page"""
    categories = Category.objects.all()
    followed_categories = request.user.profile.followed_categories.all()
    context = {'categories': categories, 'followed_categories': followed_categories}
    return render(request, 'discussion/interest.html', context)

@login_required
def category_detail(request, category_title):
    """Category Detail Page"""
    user = request.user
    category_title = category_title
    category = get_object_or_404(Category, title=category_title)
    discussions = Discussion.objects.filter(category=category).order_by("-date_created")

    saved_discussions = user.profile.saved_discussions.all()
    liked_discussions = user.profile.liked_discussions.all()
    followed_categories = user.profile.followed_categories.all()

    context = {"category": category, "discussions": discussions,
     "saved_discussions": saved_discussions, "liked_discussions": liked_discussions,
     "followed_categories": followed_categories}

    return render(request, 'discussion/category_detail.html', context)


@login_required
def follow_category(request, category_id):
    """Follow category with JS."""
    response_data={}
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        profile = request.user.profile
        if category not in profile.followed_categories.all():
            profile.followed_categories.add(category)
            profile.save()
            category.followers += 1 # Increase follower of category.
            category.save()
            response_data['status'] = 'followed'
        else:
            profile.followed_categories.remove(category)
            profile.save()
            category.followers -= 1 # Decrease follower of category.
            category.save()
            response_data['status'] = 'unfollowed'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def follow_discussion(request, discussion_id):
    """Follow discussion with JS."""
    response_data={}
    if request.method == 'POST':
        if Discussion.objects.filter(id=discussion_id).exists():
            discussion = get_object_or_404(Discussion, id=discussion_id)
            if discussion.user != request.user:
                user = request.user
                profile = user.profile
                if user not in discussion.followers.all():
                    discussion.followers.add(user)
                    discussion.save()
                    profile.followed_discussions.add(discussion)
                    profile.save()
                    response_data['status'] = 'followed'
                else:
                    discussion.followers.remove(user)
                    discussion.save()
                    profile.followed_discussions.remove(discussion)
                    profile.save()
                    response_data['status'] = 'unfollowed'
            else:
                raise Http404
        else:
            response_data['status'] = "not_exists"
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def discussions(request, username=None):
    """Discussions Page"""
    if username:# For other users
        user = get_object_or_404(User, username = username)
        discussions = Discussion.objects.filter(user = user).order_by("-date_created")
        discussions_count = discussions.count()
    else:# For current user
        user = request.user
        discussions = Discussion.objects.filter(user = user).order_by("-date_created")
        discussions_count = discussions.count()

    liked_discussions = request.user.profile.liked_discussions.all()
    saved_discussions = request.user.profile.saved_discussions.all()

    context = {
    'discussions': discussions, 'user': user, 'discussions_count': discussions_count, 'liked_discussions': liked_discussions, 'saved_discussions': saved_discussions
    }
    return render(request, 'discussion/discussions.html', context)

@login_required
def threads(request, username=None):
    """Threads Page"""
    if username:# For other users
        user = get_object_or_404(User, username = username)
        threads = Thread.objects.filter(user = user).order_by("-date_created")
        threads_count = threads.count()
    else:# For current user
        user = request.user
        threads = Thread.objects.filter(user = user).order_by("-date_created")
        threads_count = threads.count()

    liked_threads = request.user.profile.liked_threads.all()
    saved_threads = request.user.profile.saved_threads.all()

    context = {
    'threads': threads, 'user': user, 'threads_count': threads_count, 'liked_threads': liked_threads, 'saved_threads': saved_threads
    }
    return render(request, 'discussion/threads.html', context)


@login_required
def saved_discussions(request):
    """Saved Discussions Page"""
    user = request.user
    discussions = request.user.profile.saved_discussions.all()
    discussions_count = discussions.count()

    liked_discussions = request.user.profile.liked_discussions.all()

    context = {
    'discussions': discussions, 'user': user, 'liked_discussions': liked_discussions, 'discussions_count': discussions_count, 'saved_discussions': discussions
    }
    return render(request, 'discussion/saved_discussions.html', context)


@login_required
def followed_discussions(request):
    """Saved Discussions Page"""
    user = request.user
    discussions = request.user.profile.followed_discussions.all()
    discussions_count = discussions.count()

    liked_discussions = request.user.profile.liked_discussions.all()
    saved_discussions = request.user.profile.saved_discussions.all()

    context = {
    'discussions': discussions, 'user': user, 'discussions_count': discussions_count, 'liked_discussions': liked_discussions, 'saved_discussions': saved_discussions, 'followed_discussions': discussions
    }
    return render(request, 'discussion/followed_discussions.html', context)


@login_required
def saved_threads(request):
    """Saved Threads Page"""
    user = request.user
    threads = request.user.profile.saved_threads.all()
    threads_count = threads.count()
    liked_threads = user.profile.liked_threads.all()
    context = {
    'threads': threads, 'user': user, "liked_threads": liked_threads, 'threads_count': threads_count, 'saved_threads': threads
    }
    return render(request, 'discussion/saved_threads.html', context)


@login_required
def delete_thread(request, thread_id):
    """Delete thread with JS."""
    if request.method =="POST":
        response_data= {}
        if Thread.objects.filter(id=thread_id).exists():
            thread = Thread.objects.get(id=thread_id)
            if thread.user == request.user:
                thread.delete()
                response_data['status'] = "deleted"
            else:
                raise Http404
        else:
            response_data['status'] = 'not_exists'
        return JsonResponse(response_data)
    else:
        raise Http404

from re import search

from difflib import get_close_matches

@login_required
def search_discussion(request):

    query = request.GET['discussion_query']
    raw_query=query

    if len(query) >= 3 and len(query) <= 70:

        query = query.split()
        #Search results
        search_results = []

        discussions = list(Discussion.objects.all().order_by('-likes'))

        #Preparing serach results
        for query_text in query:
            for discussion in discussions:
                similar_query = get_close_matches(query_text.lower(), discussion.title.lower().split(),3,0.7)
                for similar_query_text in similar_query:
                    if  search(similar_query_text.lower(), discussion.title.lower())  and discussion not in search_results:
                        search_results.append(discussion)



    else:
        search_results = ''

    liked_discussions = request.user.profile.liked_discussions.all()
    saved_discussions = request.user.profile.saved_discussions.all()

    context = {
              'discussions': search_results,
               'searched_query': raw_query,
               'liked_discussions': liked_discussions,
               'saved_discussions': saved_discussions,
    }

    return render(request, 'discussion/search_discussion.html', context)
