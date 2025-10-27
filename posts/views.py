from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Post, Comment
from .forms import PostForm, CommentForm


def index(request):
    """首页 - 带分页的帖子列表"""
    # 获取所有帖子并按创建时间倒序排列
    posts_list = Post.objects.all().order_by('-created_at')
    
    # 分页设置
    paginator = Paginator(posts_list, 9)  # 每页显示9个帖子
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是整数，显示第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出范围，显示最后一页
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'index.html', {'posts': posts})


def post_list(request):
    """帖子列表页面"""
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """帖子详情页面"""
    post = get_object_or_404(Post, pk=pk)
    # 增加浏览量
    post.views += 1
    post.save()
    
    # 处理评论提交
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论发表成功！')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'form': form
    })


@login_required
def post_create(request):
    """创建新帖子"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '帖子发表成功！')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, pk):
    """编辑帖子"""
    post = get_object_or_404(Post, pk=pk)
    
    # 检查权限
    if post.author != request.user:
        messages.error(request, '您没有权限编辑此帖子。')
        return redirect('posts:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '帖子更新成功！')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    """删除帖子"""
    post = get_object_or_404(Post, pk=pk)
    
    # 检查权限
    if post.author != request.user:
        messages.error(request, '您没有权限删除此帖子。')
        return redirect('posts:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, '帖子删除成功！')
        return redirect('posts:post_list')
    
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required
def add_comment(request, pk):
    """添加评论"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论发表成功！')
    
    return redirect('posts:post_detail', pk=post.pk)


def search_posts(request):
    """搜索帖子功能"""
    query = request.GET.get('q', '').strip()
    time_range = request.GET.get('time_range', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'relevance')
    
    # 获取搜索历史（从本地存储获取，这里模拟数据）
    search_history = []
    
    # 构建基础查询集
    posts = Post.objects.all()
    
    # 关键词搜索
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )
    
    # 时间范围筛选
    if time_range:
        now = datetime.now()
        if time_range == 'today':
            start_date = now - timedelta(days=1)
            posts = posts.filter(created_at__gte=start_date)
        elif time_range == 'week':
            start_date = now - timedelta(weeks=1)
            posts = posts.filter(created_at__gte=start_date)
        elif time_range == 'month':
            start_date = now - timedelta(days=30)
            posts = posts.filter(created_at__gte=start_date)
        elif time_range == 'year':
            start_date = now - timedelta(days=365)
            posts = posts.filter(created_at__gte=start_date)
    
    # 分类筛选（这里需要根据实际模型字段调整）
    if category:
        # 假设Post模型有category字段
        # posts = posts.filter(category=category)
        pass  # 暂时不实现，需要先添加category字段
    
    # 排序方式
    if sort == 'newest':
        posts = posts.order_by('-created_at')
    elif sort == 'oldest':
        posts = posts.order_by('created_at')
    elif sort == 'popular':
        posts = posts.order_by('-views', '-created_at')
    else:  # relevance 相关度（默认）
        # 这里可以添加更复杂的相关度排序逻辑
        posts = posts.order_by('-created_at')
    
    # 分页
    paginator = Paginator(posts, 9)  # 每页9个
    page = request.GET.get('page')
    
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    
    # 模拟搜索历史（实际项目中可以从数据库或session获取）
    if query and query not in search_history:
        search_history.insert(0, query)
        search_history = search_history[:10]  # 限制历史记录数量
    
    context = {
        'query': query,
        'time_range': time_range,
        'category': category,
        'sort': sort,
        'posts': posts_page,
        'results_count': posts.count(),
        'search_history': search_history,
        'page_obj': posts_page,
        'is_paginated': posts_page.has_other_pages(),
    }
    
    return render(request, 'posts/search.html', context)