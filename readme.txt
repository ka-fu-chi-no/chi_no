liangzi/
├── manage.py                		# Django项目管理脚本
├── db.sqlite3               		# SQLite数据库文件
└── liangzi/                 		
    ├── __init__.py          		
    ├── settings.py          		# Django项目配置
    ├── urls.py              		# URL路由配置
    ├── wsgi.py              		
    ├── asgi.py              		
    ├── models.py            		# 数据模型定义
    ├── views.py             		# 视图函数
    ├── cache.py             		# Redis缓存封装
    ├── admin.py             		# Django管理后台配置
    └── templates/           		
        └── article_detail.html  	# 文章详情页模板
进入http://127.0.0.1:8000/admin/可管理用户和文章，预先设定好超级管理员用户名：gaoyuanhao，密码123456；预先设好普通用户：111，密码1234....

进入http://127.0.0.1:8000/article/1/、http://127.0.0.1:8000/article/2/、http://127.0.0.1:8000/article/3/，可以看到预先放置的三个模拟博客文章的页面，下方显示阅读总量、访客数、当前用户阅读次数，最下方有同步数据到数据库、查看缓存命中率功能。