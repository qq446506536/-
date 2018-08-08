from django.shortcuts import render,HttpResponse
from app01 import models
# Create your views here.
def index(request):
    #     a.查看所有学位课并打印学位课名称以及授课老师
    # 方法一
    # obj_all = models.DegreeCourse.objects.values('teachers__name')
    # print(obj_all)

    # 方法二
    # print(obj_all.get('teachers__name'))
    # for obj in obj_all :
    #     print(obj.name)
    #     print(obj.teachers.first().name)



    #     b.查看所有学位课并打印学位课名称以及学位课的奖学金
    # obj_all = models.DegreeCourse.objects.all()
    # for obj  in obj_all :
    #     for  money in obj.degreecourse_price_policy.all():
    #         print(obj.name,money.price)



    #     c.展示所有的专题课
    # ztk = models.Course.objects.filter(degree_course__isnull=True).all()
    # for i in ztk:
    #     print(i.name)




    #
    # d.查看id = 1
    # 的学位课对应的所有模块名称
    # course_name= models.Course.objects.filter(degree_course__isnull=False,id=1).all()
    # for obj in course_name:
    #     print(obj.name)


    # e.获取id = 2
    # 的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
    # all_obj = models.Course.objects.filter(degree_course__isnull=True,id=2).all()
    # print(all_obj)
    # for obj in all_obj :
    #     print(obj.name,obj.get_level_display(),obj.coursedetail.why_study,obj.coursedetail.what_to_study_brief,obj.coursedetail.recommend_courses.first().name)




    # f.获取id = 2
    # 的专题课，并打印该课程相关的所有常见问题
    # que_obj = models.OftenAskedQuestion.objects.filter(content_type=7,object_id=2).all()
    # for obj in que_obj:
    #     print(obj.question)
    # que_obj = models.OftenAskedQuestion.objects.filter(content_type=7, object_id=2).first()
    # print(que_obj.content_object.question)




    # g.获取id = 2
    # 的专题课，并打印该课程相关的课程大纲
    # all_obj = models.Course.objects.filter(degree_course__isnull=True, id=2).values('coursedetail__courseoutline__content')
    # for obj in all_obj:
    #     print(obj.get('coursedetail__courseoutline__content'))



    # h.获取id = 2
    # 的专题课，并打印该课程相关的所有章节
    # all_obj = models.CourseChapter.objects.filter(course__degree_course__isnull=True,course_id=2).all()
    # for obj in all_obj:
    #     print(obj.name,obj.chapter)




    # i.获取id = 2
    # 的专题课，并打印该课程相关的所有课时
    # 第1章·Python
    # 介绍、基础语法、流程控制
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 第1章·Python
    # 介绍、基础语法、流程控制
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # all_obj = models.CourseSection.objects.filter(chapter__course__degree_course__isnull=True,chapter__course_id=2).all()
    # for obj in all_obj:
    #     print(obj.name)



    # j.获取id = 2
    # 的专题课，并打印该课程相关的所有的价格策略
    # obj_all = models.PricePolicy.objects.filter(content_type=7).all()
    # print(obj_all)
    # for obj in obj_all:
    #     print(obj)

    return  HttpResponse('OK')