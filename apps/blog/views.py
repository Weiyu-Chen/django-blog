#-*- coding: utf-8 -*-
#!/usr/bin/python

from django.shortcuts import render
from apps.blog.models import Article, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings

category_list = Category.objects.all()

tags = Tag.objects.all()  # 获取全部的标签对象

def home(request):  # 主页
    posts = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM, 作为分页器处理
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)  # 取第 page 页的数据
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {
        'post_list': post_list,
        'category_list': category_list
    })


def detail(request, id):  # 查看文章详情
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()   # 更新浏览次数
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {
        'post': post,
        'tags': tags,
        'category_list': category_list,

        'prev_post': post.prev_article(),  # model 定义的新方法
        'next_post': post.next_article()
    })



def category(request, id):
    posts = Article.objects.filter(category_id=str(id))  # 获取全部的Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM, 作为分页器处理
    page = request.GET.get('page')  # 获取URL中page参数的值
    category_list = Category.objects.all()
    try:
        post_list = paginator.page(page)  # 取第 page 页的数据
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {
        'post_list': post_list,
        'category_list': category_list
    })



def tag(request, tag):
    posts = Article.objects.filter(tags__name__contains=tag)  # 获取全部的Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM, 作为分页器处理
    page = request.GET.get('page')  # 获取URL中page参数的值
    category_list = Category.objects.all()
    try:
        post_list = paginator.page(page)  # 取第 page 页的数据
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {
        'post_list': post_list,
        'category_list': category_list
    })