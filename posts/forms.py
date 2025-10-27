from django import forms
from .models import Post, Comment, Category, Tag


class PostForm(forms.ModelForm):
    # 标签字段（逗号分隔的文本输入）
    tag_input = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '输入标签，用逗号分隔（如：技术,编程,Python）'
        }),
        help_text='多个标签用逗号分隔'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入帖子标题（2-200个字符）'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入帖子内容，支持富文本格式',
                'rows': 15
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        help_texts = {
            'title': '标题长度在2-200个字符之间',
            'content': '内容不能为空',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置分类选项
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = '选择分类（可选）'
        
        # 如果是编辑模式，设置标签初始值
        if self.instance and self.instance.pk:
            tags = self.instance.tags.all()
            if tags:
                self.fields['tag_input'].initial = ', '.join([tag.name for tag in tags])
    
    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # 处理标签
            tag_input = self.cleaned_data.get('tag_input', '').strip()
            if tag_input:
                # 清除现有标签
                post.tags.clear()
                
                # 处理标签输入（逗号分隔）
                tag_names = [name.strip() for name in tag_input.split(',') if name.strip()]
                for tag_name in tag_names:
                    # 获取或创建标签
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
        
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入评论内容',
                'rows': 3
            }),
        }