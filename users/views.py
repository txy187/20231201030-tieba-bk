from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import UserProfileForm
from .models import UserProfile


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 创建用户资料
            UserProfile.objects.create(user=user)
            # 自动登录用户
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '注册成功！欢迎来到贴吧。')
                return redirect('posts:post_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """用户资料页面"""
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        # 获取用户发布的帖子
        from posts.models import Post
        user_posts = Post.objects.filter(author=request.user, is_published=True).order_by('-created_at')
        
        # 获取用户收藏的帖子（如果模型支持）
        try:
            from posts.models import Favorite
            favorite_posts = Favorite.objects.filter(user=request.user).select_related('post')
        except ImportError:
            favorite_posts = None
        
        return render(request, 'users/profile.html', {
            'profile': profile,
            'user_posts': user_posts,
            'favorite_posts': favorite_posts,
            'posts_count': user_posts.count()
        })
    except Exception as e:
        messages.error(request, f'加载用户资料时出错: {str(e)}')
        return redirect('posts:post_list')


@login_required
def profile_edit(request):
    """编辑用户资料"""
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                # 处理头像上传
                if 'avatar' in request.FILES:
                    # 可以在这里添加头像处理逻辑，如压缩、裁剪等
                    pass
                
                form.save()
                messages.success(request, '资料更新成功！')
                return redirect('users:profile')
            else:
                messages.error(request, '表单验证失败，请检查输入内容。')
        else:
            form = UserProfileForm(instance=profile)
        
        return render(request, 'users/profile_edit.html', {
            'form': form,
            'profile': profile
        })
    except Exception as e:
        messages.error(request, f'编辑资料时出错: {str(e)}')
        return redirect('users:profile')