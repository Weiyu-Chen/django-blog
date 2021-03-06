#-*- coding: utf-8 -*-
#!/usr/bin/python


from django.db import models
from django.utils.timezone import now

# Create your models here.


class Tag(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '标签名称'  # 指定后台显示模型名称
        verbose_name_plural = '标签列表'  # 指定后台显示模型复数名称
        db_table = "tag"  # 数据库表名


class Category(models.Model):
    name = models.CharField(verbose_name='类别名称', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "类别名称"
        verbose_name_plural = '分类列表'
        db_table = "category"  # 数据库表名



class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField(verbose_name='正文', blank=True, null=True)
    status = models.CharField(verbose_name='状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    pub_time = models.DateTimeField(verbose_name='发布时间', blank=True, null=True)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    # 类别, 外键，在数据库以 category_id 的字段 存储在 article 表中
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)

    # 一篇文章可以有多个 tag ， 一个tag可以存在在多篇文章。  不会有tags字段存在 article 表中
    tags = models.ManyToManyField(Tag, verbose_name='标签集合', blank=True)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.title

    # 更新浏览量
    def viewed(self):
        self.views += 1
        # UPDATE `article` SET `views` = 7 WHERE `article`.`id` = 2
        self.save(update_fields=['views'])


    # 下一篇
    def next_article(self):  # id比当前id大，状态为已发布，发布时间不为空
        # SELECT * FROM `article` WHERE (`article`.`id` > 2 AND `article`.`pub_time` IS NOT NULL AND `article`.`status` = 'p') ORDER BY `article`.`pub_time` ASC LIMIT 1
        return Article.objects.filter(id__gt=self.id, status='p', pub_time__isnull=False).order_by('pub_time').first()

    # 前一篇
    def prev_article(self):  # id比当前id小，状态为已发布，发布时间不为空
        # SELECT * FROM `article` WHERE (`article`.`id` < 2 AND `article`.`pub_time` IS NOT NULL AND `article`.`status` = 'p') ORDER BY `article`.`pub_time` DESC LIMIT 1
        return Article.objects.filter(id__lt=self.id, status='p', pub_time__isnull=False).first()

    class Meta:
        ordering = ['-pub_time']  # 按文章创建日期降序，即 每次插入数据是 unshift ,
        verbose_name = '文章'  # 指定后台显示模型名称
        verbose_name_plural = '文章列表'  # 指定后台显示模型复数名称
        db_table = 'article'  # 数据库表名
        get_latest_by = 'created_time' # 指定文章排序方式，作为 latest() 等 方法的默认参数