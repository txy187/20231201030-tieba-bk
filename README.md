# 百度贴吧毕业设计项目

一个基于Django框架开发的类似百度贴吧的社区平台。

## 项目简介

本项目是一个完整的贴吧系统，包含用户管理、帖子发布、评论系统、搜索功能等核心功能。

## 功能特性

### 用户管理
- 用户注册/登录
- 个人资料管理
- 头像上传功能
- 密码修改

### 帖子系统
- 帖子发布/编辑/删除
- 帖子分类管理
- 标签系统
- 分页显示

### 评论系统
- 评论发布
- 评论管理
- 评论回复

### 搜索功能
- 关键词搜索
- 分类筛选
- 时间范围筛选
- 多种排序方式

## 技术栈

- **后端**: Django 4.x
- **数据库**: SQLite (开发环境)
- **前端**: HTML5, CSS3, JavaScript, Bootstrap
- **模板引擎**: Django Templates

## 项目结构

```
tieba/
├── posts/           # 帖子应用
├── users/           # 用户应用
├── templates/       # 模板文件
├── static/          # 静态文件
├── media/           # 媒体文件
└── tieba/           # 项目配置
```

## 安装和运行

1. 克隆项目
```bash
git clone <repository-url>
cd tieba
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 数据库迁移
```bash
python manage.py migrate
```

4. 创建超级用户
```bash
python manage.py createsuperuser
```

5. 运行开发服务器
```bash
python manage.py runserver
```

6. 访问应用
打开浏览器访问 http://127.0.0.1:8000/

## 主要页面

- **首页**: http://127.0.0.1:8000/
- **帖子详情**: http://127.0.0.1:8000/post/1/
- **创建帖子**: http://127.0.0.1:8000/create/
- **搜索页面**: http://127.0.0.1:8000/search/
- **个人中心**: http://127.0.0.1:8000/profile/

## 开发进度

✅ 已完成功能：
- 用户注册登录系统
- 帖子发布和管理
- 评论系统
- 搜索功能
- 个人中心

🔄 待完善功能：
- 帖子点赞功能
- 关注系统
- 消息通知
- 管理员后台

## 许可证

本项目仅供学习和毕业设计使用。

## 贡献

欢迎提交Issue和Pull Request来改进项目。