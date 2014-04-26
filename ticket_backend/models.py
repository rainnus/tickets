#-*- coding:UTF-8 -*-
from __future__ import division
from django.db import models
from django.db.models.fields.files import ImageFieldFile
import os
from PIL import Image
from ticket_dispatch.settings import MEDIA_ROOT

# Create your models here.

class Catagory(models.Model):
    """这个模型为活动的分类，科技讲座、人文讲座、交流活动等等"""
    catagory_name = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return self.catagory_name

class User(models.Model):
    """这个模型定义了学生，每个学生以一卡通号码（也就是并非以默认的id）为唯一标识，但是也储存姓名
        一卡通号应该是唯一的，防止一个学生多次点击报名"""
    name = models.CharField(max_length=10, blank=True)
    card_id = models.CharField(max_length=50)

    def __unicode__(self):
        return self.card_id

class Author(models.Model):
    """提交活动的管理员（意义不大）"""
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' %(self.name)

def make_thumb(path, size = 480):
    pixbuf = Image.open(path)
    width, height = pixbuf.size
    if width > size:
        delta = width / size
        height = int(height / delta)
        pixbuf.thumbnail((size, height), Image.ANTIALIAS)
    return pixbuf

class Media(models.Model):
    """这个模型为图像对象，在保存的时候自动生成缩略图"""
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to = './upload/')
    thumb = models.ImageField(upload_to = './upload/thumb', blank = True)
    upload_date = models.DateTimeField(auto_now_add = True)

    def save(self):
        super(Media, self).save() #将上传的图片先保存一下，否则报错
        base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.image.name))
        THUMB_ROOT = 'upload/thumb'
        relate_thumb_path = os.path.join(THUMB_ROOT, base + '.thumb' + ext)
        thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_pixbuf.save(thumb_path)
        self.thumb = ImageFieldFile(self, self.thumb, relate_thumb_path)
        super(Media, self).save() #再保存一下，包括缩略图等

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']

class Activity(models.Model):
    """活动模型，其中储存活动的介绍、类别、申请人数、起止时间等等"""
    caption = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    actType = models.CharField(max_length=100)
    # actAuthor = models.CharField(max_length=100)
    destruction = models.TextField(blank=True, null=True)
    posters = models.ForeignKey(Media, blank=True, null=True)
    catagories = models.ManyToManyField(Catagory, blank=True)
    ticket_number = models.IntegerField()
    #我本意是让 ticket_requests 成为 Ticket_request 的 ForeignKey，但是无法实现
    ticket_requests = models.ManyToManyField(User, blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    activity_time = models.DateTimeField()
    activity_place = models.CharField(max_length=100)
    request_begin_time = models.DateTimeField(auto_now=True)
    request_deadline = models.DateTimeField()
    tickets_dispatched = models.BooleanField()

    def __unicode__(self):
        return u'%s %s %s' %(self.caption, self.author, self.publish_time)

    class Meta:
        ordering = ['-publish_time']

class Ticketrequest(models.Model):
    """这个模型为“申请”模型，记录一次申请的项目、申请人、申请时间，Ticket_request在保存和删除的时候自动处理Activity的关系，并且保证同一人对于同一个活动的申请不是重复的"""
    target = models.ForeignKey(Activity)
    person = models.ForeignKey(User)
    accepted = models.BooleanField()
    request_time = models.DateTimeField(auto_now=True)

    def save(self):
        #判断是否是重复的申请
        try:
            former_request = Ticketrequest.objects.get(target=self.target, person=self.person)
            if former_request.id == self.id:
                super(Ticketrequest, self).save()
        except Ticketrequest.DoesNotExist:
            super(Ticketrequest, self).save()
            self.target.ticket_requests.add(self.person)

    def delete(self):
        super(Ticketrequest, self).delete()
        self.target.ticket_requests.remove(self.person)

    def __unicode__(self):
        return u'%s %s %s' %(self.target, self.person, self.request_time)

    class Meta:
        ordering = ['-request_time']