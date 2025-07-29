# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Article, ArticleReadStat
# 将功能注册到admin中
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'content']
@admin.register(ArticleReadStat)
class ArticleReadStatAdmin(admin.ModelAdmin):
    list_display = ['article', 'total_views', 'unique_visitors', 'updated_at']
    list_filter = ['updated_at']