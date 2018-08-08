# !user/bin/python3
# Author:Mr.Yuan
# -*- coding:utf-8 -*-
# @time: 2018/8/7 15:51

from rest_framework import serializers
from app01 import models


# 展示所有的专题课
class CourseSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    # name = serializers.CharField()
    degree = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['degree']

    def get_degree(self, row):
        if not row.degree_course:
            return row.name


class CourseModeSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    hours = serializers.CharField(source='coursedetail.hours')
    course_slogan = serializers.CharField(source='coursedetail.course_slogan')
    recommend_courses = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'level_name', 'hours', 'course_slogan', 'recommend_courses']

    def get_recommend_courses(self, row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [{'id': item.id, 'name': item.name} for item in recommend_list]


# 学位课老师  奖金  学位课 课程名字相关信息
class DgreeCourseSeria(serializers.ModelSerializer):
    # degreecourse_price_policy = serializers.CharField(source='')
    degreecourse_price = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ['name', 'degreecourse_price', 'teacher']
        # depth = 1

    def get_teacher(self, row):
        teacher_list = row.teachers.all()
        return [{'id': item.id, 'name': item.name} for item in teacher_list]

    def get_degreecourse_price(self, row):
        scholarships = row.scholarship_set.all()
        return [{'percent': item.time_percent, 'value': item.value} for item in scholarships]


class Deg(serializers.ModelSerializer):

    class Meta:
        model = models.Course
        fields = ['name']


# 获取id = 2的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
class D5(serializers.ModelSerializer):
    name = serializers.CharField()
    level_name = serializers.CharField(source='get_level_display')
    recommend_courses = serializers.SerializerMethodField()
    why_study = serializers.CharField(source='coursedetail.why_study')
    what_to_study_brief = serializers.CharField(source='coursedetail.what_to_study_brief')

    class Meta:
        model = models.Course
        fields = ['name', 'level_name', 'recommend_courses', 'what_to_study_brief', 'why_study']

    def get_recommend_courses(self, row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [{'id': item.id, 'name': item.name} for item in recommend_list]


# 获取id = 2的专题课，并打印该课程相关的所有常见问题
class D6(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = models.OftenAskedQuestion
        fields = ['question']

    def get_question(self, row):
        question_list = row.asked_question.all()
        for item in  question_list:
            return [{'id': item.id, 'name': item.question} for item in question_list]


# g.获取id = 2的专题课，并打印该课程相关的课程大纲
class D7(serializers.ModelSerializer):
    class Meta:
        model = models.CourseOutline
        fields = ['title','order','content']


# h.获取id = 2的专题课，并打印该课程相关的所有章节
class D8(serializers.ModelSerializer):
    class Meta:
        model = models.CourseChapter
        fields = ['chapter','name','summary']
