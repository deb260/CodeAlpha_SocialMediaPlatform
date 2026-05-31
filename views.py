from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Profile, Post, Comment
from django import forms


# ── Signals: auto-create profile on user creation ───────────────────────────
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


# ── Forms ────────────────────────────────────────────────────────────────────

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "What's on your mind?", 'rows': 3}),
        max_length=500
    )
    class Meta:
        model = Post
        fields = ['content', 'image']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Write a comment...'}),
        max_length=300
    )
    class Meta:
        model = Comment
        fields = ['content']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']


# ── Auth ─────────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to SocialAlpha!')
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'social/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'social/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Feed ─────────────────────────────────────────────────────────────────────

@login_required
def feed(request):
    # Get posts from people the user follows + own posts
    profile, _ = Profile.objects.get_or_create(user=request.user)
    following_users = profile.followers.all()  # users this profile's followers field contains
    # Actually: followers field = users who follow this profile
    # We want: users that request.user follows
    following_ids = Profile.objects.filter(followers=request.user).values_list('user_id', flat=True)
    posts = Post.objects.filter(
        Q(author__in=following_ids) | Q(author=request.user)
    ).prefetch_related('likes', 'comments__author', 'author__profile')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post shared!')
            return redirect('feed')
    else:
        form = PostForm()

    # Suggested users to follow
    already_following = list(following_ids) + [request.user.id]
    suggested = User.objects.exclude(id__in=already_following).select_related('profile')[:5]

    return render(request, 'social/feed.html', {
        'posts': posts,
        'form': form,
        'suggested': suggested,
    })


# ── Post actions ──────────────────────────────────────────────────────────────

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.like_count()})
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# ── Profile ───────────────────────────────────────────────────────────────────

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user)
    posts = user.posts.all()
    is_following = request.user.is_authenticated and profile.followers.filter(id=request.user.id).exists()

    return render(request, 'social/profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'follower_count': profile.follower_count(),
        'following_count': profile.following_count(),
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'social/edit_profile.html', {'form': form})


@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return redirect('profile', username=username)
    profile, _ = Profile.objects.get_or_create(user=target_user)
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
        messages.success(request, f'Unfollowed {username}.')
    else:
        profile.followers.add(request.user)
        messages.success(request, f'Now following {username}!')
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# ── Explore / Search ──────────────────────────────────────────────────────────

@login_required
def explore(request):
    query = request.GET.get('q', '')
    users = []
    posts = Post.objects.all().prefetch_related('likes', 'comments', 'author__profile')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        ).exclude(id=request.user.id).select_related('profile')
        posts = posts.filter(content__icontains=query)
    return render(request, 'social/explore.html', {
        'posts': posts[:20],
        'users': users,
        'query': query,
    })
