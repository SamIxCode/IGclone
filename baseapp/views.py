from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import NewUserForm, EditProfile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Post, LikePost, FollowerCount
from itertools import chain
import random

# Create your views here.


def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_following_list = []
    feed = []
    user_following = FollowerCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)

    for username in user_following_list:
        feed_lists = Post.objects.filter(username=username)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [
        x for x in list(all_users) if (x not in list(user_following_all))
    ]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [
        x for x in list(new_suggestions_list) if (x not in list(current_user))
    ]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(
        request,
        "index.html",
        {
            "user_profile": user_profile,
            "posts": feed_list,
            "suggestions_username_profile_list": suggestions_username_profile_list[:4],
        },
    )


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            user_instance = User.objects.get(username=request.user.username)
            new_profile = Profile(id_user=request.user.id, user=user_instance)
            new_profile.save()
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request, template_name="signup.html", context={"register_form": form}
    )


def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"id": request.user.id, "email": request.user.email})
        else:
            return JsonResponse({"msg": "wrong credentials"})
    else:
        return render(request, "signin.html")


@login_required(login_url="sign_in")
def sign_out(request):
    logout(request=request)
    return JsonResponse({"msg": "logged out", "if user": request.user.id})


def render_settings(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, "settings.html", {"user_profile": user_profile})


@login_required(login_url="sign_in")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = EditProfile(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            if request.FILES.get != None:
                image = request.FILES.get("image")
                user_profile.profile_image = image
            form.save()
            user_profile = Profile.objects.get(user=request.user)
            messages.success(request, "edit successful", {"user_profile": user_profile})
            user_profile = Profile.objects.get(user=request.user)
            return render_settings(request)
        else:
            messages.error(request, "edit unsuccessful")
            return render(request, "settings.html", {"user_profile": user_profile})
    else:
        user_profile = Profile.objects.get(user=request.user)
        messages.error(request, "get request")
        return render(request, "settings.html", {"user_profile": user_profile})


@login_required(login_url="sign_in")
def upload_post(request):
    if request.method == "POST":
        id_user = request.user.id
        username = request.user.username
        image = request.FILES.get("image")
        caption = request.POST["caption"]

        newpost = Post.objects.create(
            id_user=id_user, image=image, caption=caption, username=username
        )
        newpost.save()

        return JsonResponse({"msg": "success"})
    else:
        return JsonResponse({"msg": "failed"})


@login_required(login_url="sign_in")
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.likes = post.likes + 1
        post.save()
        return redirect("homepage")
    else:
        like_filter.delete()
        post.likes = post.likes - 1
        post.save()
        return redirect("homepage")


@login_required(login_url="sign_in")
def profile(request, pk):
    user_obj = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_obj)
    user_posts = Post.objects.filter(username=pk)
    total_post = len(user_posts)
    follower = request.user.username
    user = pk
    if FollowerCount.objects.filter(follower=follower, user=user):
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    userfollowers = len(FollowerCount.objects.filter(user=pk))
    userfollowing = len(FollowerCount.objects.filter(follower=pk))

    context = {
        "userobject": user_obj,
        "user_profile": user_profile,
        "user_posts": user_posts,
        "total_post": total_post,
        "button_text": button_text,
        "user_followers": userfollowers,
        "user_following": userfollowing,
    }
    return render(request, "profile.html", context=context)


@login_required(login_url="sign_in")
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]
        if FollowerCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowerCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            print(user)
            return redirect("/profile/" + user)

        else:
            new_follower = FollowerCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect("/profile/" + user)

    else:
        return redirect("homapge")


@login_required(login_url="sign_in")
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    username_profile = []
    username_profile_list = []

    if request.method == "POST":
        username = request.POST["username"]
        username_obj = User.objects.filter(username__icontains=username)
        for users in username_obj:
            username_profile.append(users.id)

        for id in username_profile:
            profile_list = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile_list)

    username_profile_list = list(chain(*username_profile_list))
    return render(
        request,
        "search.html",
        {"user_profile": user_profile, "username_profile_list": username_profile_list},
    )
