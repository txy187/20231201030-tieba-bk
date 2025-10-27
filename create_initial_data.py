#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tieba.settings')
django.setup()

from posts.models import Category, Tag

def create_initial_data():
    """创建初始的分类和标签数据"""
    
    # 创建分类
    categories = [
        ('技术讨论', '技术相关的问题和讨论'),
        ('生活分享', '日常生活分享'),
        ('学习交流', '学习经验和知识分享'),
        ('娱乐八卦', '娱乐新闻和八卦'),
        ('求助问答', '求助和问题解答'),
        ('资源分享', '资源分享和推荐'),
        ('意见建议', '对贴吧的建议和意见'),
        ('其他', '其他类型的内容')
    ]
    
    for name, description in categories:
        Category.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
    
    # 创建一些常用标签
    tags = [
        'Python', 'Django', 'JavaScript', 'Vue', 'React',
        '编程', '技术', '学习', '分享', '求助',
        '生活', '娱乐', '新闻', '资源', '工具'
    ]
    
    for tag_name in tags:
        Tag.objects.get_or_create(name=tag_name)
    
    print("初始数据创建完成！")
    print(f"创建了 {Category.objects.count()} 个分类")
    print(f"创建了 {Tag.objects.count()} 个标签")

if __name__ == '__main__':
    create_initial_data()