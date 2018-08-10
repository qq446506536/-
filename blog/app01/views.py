import json
from code_img.veryfication_code import  check_code
from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib import auth
from .models import Article,UserInfo,Tag,Category,Blog,ArticleUpDown,Comment,Article2Tag
from django.db.models import Avg,Sum,Min,Max,Count,F,Q
from .form import Userform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from wxpy import get_wechat_logger
logger = get_wechat_logger()
logger.warning('这是一条 WARNING 等级的日志，你收到了吗？')
try:
    def index(request):
        article_list = Article.objects.all()
        paginator = Paginator(article_list, 5)
        current_num = int(request.GET.get("page", 1))
        if paginator.num_pages > 11:

            if current_num - 5 < 1:
                pageRange = range(1, 11)
            elif current_num + 5 > paginator.num_pages:
                pageRange = range(current_num - 5, paginator.num_pages + 1)

            else:
                pageRange = range(current_num - 5, current_num + 6)

        else:
            pageRange = paginator.page_range
        try:
            article_list = paginator.page(current_num)
            # previous = article_list.previous_page_number()
            # print(previous,"##############33")
            # print(fuck,"*****************8")
        except EmptyPage:
            article_list = paginator.page(1)
        if request.user.is_authenticated:
            site_name = UserInfo.objects.filter(username=request.user.username).values('blog__site_name').first()
            site_name = site_name.get('blog__site_name')

        return  render(request,'index.html',locals())



        # article_user = UserInfo.objects.filter(article=)
        # if request.user.is_authenticated:
        #     site_name = UserInfo.objects.filter(username=request.user.username).values('blog__site_name').first()
        #     site_name = site_name.get('blog__site_name')
        # return render(request,'index.html',locals())


    def code_img(request):
        img,code = check_code()
        request.session['code'] = code
        from io import BytesIO
        stream = BytesIO()
        img.save(stream, 'png')
        return HttpResponse(stream.getvalue())


    def login(request):
        if request.is_ajax():
            ret = {'status':True,'url':None}
            username = request.POST.get('usm')
            pwd = request.POST.get('pwd')
            code = request.POST.get('code')
            user = auth.authenticate(username=username,password=pwd)
            if user and request.session['code']==code:
                auth.login(request,user)
                #获取跳转之前的url  这个方法在这里没有用 必须在用中间件限制用户登录的时候才能捕捉到 用户跳转之前的路由
                print(request.GET,"****************88")
                before_url = request.GET.get("next")
                print(before_url,777777777777)
                print(before_url)
                if before_url:
                    ret['url']=before_url
                else:
                    ret['url'] ='/index/'
            else:
                ret = {'status':False,'url':'/login/'}
            return JsonResponse(ret)
        return render(request,'login.html')


    def logout(request):
        auth.logout(request)
        return redirect(reverse('index'))


    def homesite(request,site_name,**kwargs):
        blog = Blog.objects.filter(site_name=site_name).first()
        if not blog :
            return render(request,'not_found.html')
        params = kwargs.get("params")
        user = UserInfo.objects.filter(username=request.user.username).first()
        if not kwargs :
            article_list = Article.objects.filter(user=user)


        elif kwargs.get('condition') == 'category':
            article_list = Article.objects.filter(user=user).filter(category__title=params)



        elif kwargs.get('condition') =='tag':
            article_list = Article.objects.filter(user=user).filter(tags__title=params)

        else:
            print(params)
            year,month = params.split('/')
            print(year,month,33333333333333)
            print(type(month))
            # if month[0] == '0':month=month[1]
            print(month)
            print(Article.objects.values('create_time'))
            article_list = Article.objects.filter(user=user).filter(create_time__year=year)
            print(article_list)
        return render(request, 'homesite.html', locals())


    def not_found(request):
        return render(request,'not_found.html')


    def article_detail(request,site_name,article_id):
        # user = UserInfo.objects.filter(username=request.user.username).first()
        blog =Blog.objects.filter(site_name=site_name).first()
        tag_list = Tag.objects.filter(blog=blog).annotate(count=Count('article__nid')).values("title", 'count')
        user = UserInfo.objects.filter(blog=blog).first()
        category_list = Category.objects.filter(blog=blog).annotate(
            count=Count('article__category_id')).values('title', 'count')
        comment_all = Comment.objects.filter(article_id=article_id).all()
        article_detailt = Article.objects.filter(nid=article_id).first()
        # print(article_detailt.title)
        date_list = Article.objects.filter(user=user).extra(
            select={'y_m_date': "DATE_FORMAT(create_time,'%%Y-%%m')"}).values("y_m_date").annotate(
            count=Count('title')).values('y_m_date', 'count')
        return render(request, 'article_detail.html', locals())


    from django.http import JsonResponse

    from django.db import transaction
    def up_down(request):
        msg = request.POST
        print(msg)
        user_id = request.user.nid
        article_id = msg.get('article_id')
        is_up = json.loads(msg.get('is_up'))
        print(66)
        print(is_up,'33333333',article_id)
        # article_choice_obj = ArticleUpDown.objects.create(article_id=article_id,user_id=user_id,is_up=is_up)
        # print(article_choice_obj)
        print(777777777)
        response = {'status':True,'msg':None}

        obj = ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id).first()
        if obj:
            response['status']=False
            response['msg'] = obj.is_up
        else:
            with transaction.atomic():  # 事物绑定  把两个操作绑定起来
                new_obj = ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
                if new_obj.is_up:
                    article_obj = Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
                else:
                    article_obj = Article.objects.filter(nid=article_id).update(up_count=F('down_count')+1)
                response['msg'] = new_obj.is_up


        return JsonResponse(response)
        # return  HttpResponse('hehe')



    def comment(request):
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        user_id = request.user.nid
        pid = request.POST.get('pid')

        #生成评论对象 并且将文章里面的评论数改变
        with transaction.atomic():
            comment_obj = Comment.objects.create(article_id=article_id,user_id=user_id,content=content,parent_comment_id=pid)
            article_obj = Article.objects.filter(nid=article_id).update(comment_count = F('comment_count')+1)
        response = {"status": True}
        response["timer"] = comment_obj.create_time.strftime("%Y-%m-%d %X")
        response["content"] = comment_obj.content
        response["username"] = request.user.username
        return JsonResponse(response)


    def back_stage(request):
        user = request.user.username
        if user:
            blog = request.user.blog
            article_list = Article.objects.filter(user=request.user).all()
            return render(request,'back/back_stage.html',locals())
        else:return redirect(reverse('login'))



    from bs4 import BeautifulSoup


    def add_article(request):
        caregory_list = Category.objects.filter(blog=request.user.blog)
        tag_list = Tag.objects.filter(blog=request.user.blog)
        if request.method=='POST':
            print(request.POST)
            title = request.POST.get('article_title')
            content = request.POST.get('content')
            caregory_id = request.POST.get('category_id')
            tags_id_list = request.POST.getlist('tag_id') #列表形式的tag_id
            soup = BeautifulSoup(content,'html.parser')  #  把提交内容中的HTML  js代码过滤掉 只留下纯文本 用来切片得到desc
            print(soup)
            #对文章切片 得到desc
            for tag in soup.find_all():
                #  去除文章中的js代码  以便存进数据库中
                if tag.name in ['script',]:
                    tag.decompose()
            print(soup)
            desc = soup.text[0:150]
            article_obj = Article.objects.create(title=title,content=str(soup),user=request.user,desc=desc,category_id=caregory_id)
            for tag in tags_id_list:
                obj = Article2Tag.objects.create(article_id=article_obj.nid,tag_id=tag)
            return redirect(reverse('back_stage'))
        return render(request,'back/add_article.html',locals())




    import os
    from blog.settings import BASE_DIR


    def upload(request):
        file = request.FILES
        print(file)
        file_obj = file.get('imgFile')
        file_name = file_obj.name
        path = os.path.join(BASE_DIR,'static','upload',file_name)
        with open(path,'wb') as f:
            for content in file_obj:
                f.write(content)
        return JsonResponse(
            {
                "error": 0,
                "url": "/static/upload/"+file_name
            }
        )


    def delete(request):
        print(request.POST)
        article_id = request.POST.get('article_id')
        obj = Article.objects.get(nid=article_id)
        Article.objects.get(nid=article_id).delete()
        # Article2Tag.objects.get(article_id=article_id).delete()  这种不行，因为用get拿到的是单个对象
        # return JsonResponse({'result':1,'msg':'删除成功'})
        # obj.tags.remove(article_id)
        Article2Tag.objects.filter(article_id=article_id).delete()
        #这个多对多删除关联对象时，如果用了中间模型，就不能用remove，set等这些操作，必须拿到这张表后对querryset  进行操作
        return JsonResponse({'result':1,'msg':'删除成功'})


    def update(request,article_id):
        if request.method=='GET':
            # article_id = request.GET.get('article_id')
            article_obj = Article.objects.filter(nid=article_id).first()
            article_tag_obj = Article2Tag.objects.filter(article_id=article_obj.nid)
            print(article_tag_obj,6666666666)
            tags_id_list =[]
            for obj in article_tag_obj:
                tags_id_list.append(obj.tag_id)
            print(tags_id_list,0000000000000)
            caregory_list = Category.objects.filter(blog=request.user.blog)
            tag_list = Tag.objects.filter(blog=request.user.blog)

            return render(request,'back/update.html',locals())
        else:
            title = request.POST.get('article_title')
            content = request.POST.get('content')
            caregory_id = request.POST.get('category_id')
            tags_id_list = request.POST.getlist('tag_id')  # 列表形式的tag_id
            print(tags_id_list,'hehehehehehehehhehe')
            soup = BeautifulSoup(content, 'html.parser')  # 把提交内容中的HTML  js代码过滤掉 只留下纯文本 用来切片得到desc
            print(soup)
            # 对文章切片 得到desc
            for tag in soup.find_all():
                #  去除文章中的js代码  以便存进数据库中
                if tag.name in ['script', ]:
                    tag.decompose()
            print(soup)
            desc = soup.text[0:150]
            article_obj = Article.objects.filter(nid=article_id).update(title=title, content=str(soup),desc=desc,
                                                 category_id=caregory_id)
            Article2Tag.objects.filter(article_id=article_id).delete()
            for  tag_id   in tags_id_list:
                Article2Tag.objects.create(article_id=article_id,tag_id=tag_id)
            return redirect(reverse('back_stage'))


    def register(request):
        if request.is_ajax():
            # print(request,6666)
            verify_msg =dict(request.POST) # 接受前端的消息  前端发送过来的数据是一个querrydict的数据类型   并且值是一个列表  所以在这里转换成有个字典
            # print(verify_msg,'122222222222222222222222')
            verify_msg['username']=verify_msg['username'][0]
            verify_msg['email'] = verify_msg['email'][0]
            verify_msg['pwd'] = verify_msg['pwd'][0]
            verify_msg['ensure_pwd'] = verify_msg['ensure_pwd'][0]
            verify_msg['telephone'] = verify_msg['telephone'][0]
            # print(verify_msg,'111111111111111111111111')
            # print(dict(verify_msg))
            # print(999999999999)
            # print(verify_msg)
            form = Userform(verify_msg)#验证前端发送过来的信息
            # print(form,"99999999999999999")
            # print(type(form),form.username)
            if form.is_valid():
                return HttpResponse(json.dumps({'djuge':1,'result':'可以使用'}))
            else:
                error_usm = form.errors.get('username')
                error_email = form.errors.get('email')
                error_telephone = form.errors.get('telephone')
                error_pwd_ensure = form.errors.get("__all__")
                print(error_pwd_ensure)
                if error_pwd_ensure:  # 这个只用来捕获全局钩子的错误
                    print(form.cleaned_data)
                    error_pwd_ensure = error_pwd_ensure[0]
                return HttpResponse(json.dumps({'djuge':0,'result':{'username':error_usm,'email':error_email,'telephone':error_telephone,'ensure_pwd':error_pwd_ensure}}))
        else:
            if request.method == 'POST':
                form = Userform(request.POST)
                print('这是form',form)
                if form.is_valid():
                    # print('成功了6666666666')
                    username = request.POST.get('username')
                    pwd = request.POST.get('ensure_pwd')
                    email = request.POST.get('email')
                    telephone = request.POST.get('telephone')
                    # user_write = Uesrs.objects.create(username=username,pwd=pwd,email=email,telphone=telephone)
                    # ret = Book.objects.all()
                    # request.session["log_dudge"] = True
                    # request.session['username'] = username
                    # request.session['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d %X')
                    blog_obj = Blog.objects.create(title=username, site_name='%s的博客' % username,
                                                   theme='egon.css')  # 这里正常的应该是注册成功之后选择主题  和自己的站点名字


                    # print(blog_obj.nid,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    ret = UserInfo.objects.create_user(username=username, password=pwd,blog_id=blog_obj.nid,
                                                       telephone=telephone
                                                 )  # 密文写入数据库
                    ret.save()
                    print('777777777777777777777')
                    user_obj = auth.authenticate(username=username,password=pwd)  #类似于session操作
                    auth.login(request,user_obj)
                    return redirect(reverse('index'))
                else:
                    error = form.errors.get("__all__")
                    if error:  #这个只用来捕获全局钩子的错误
                        print(form.cleaned_data)  # 用post提交的时候 所有的干净的信息  也就是正确的信息
                        error = error[0]
                        print(error,'^^^^^^^^^^^^^^^^^^^^^^^^^66')
                    return render(request,'register.html',locals())
            else:
                form = Userform()
                return render(request,'register.html',locals())



    import os
    import uuid
    # def upload_img(request):
    #     '''
    #     带图片预览
    #     :param request:
    #     :return:
    #     '''
    #     if request.method == "GET":
    #         return render(request,'upload_img.html')
    #     user = request.POST.get('user')
    #     avatar = request.POST.get('avatar')
    #     print(user,avatar)
    #     return HttpResponse('上传成功')


    def form_data_upload(request):
        """
        ajax上传头像
        :param request:
        :return:
        """
        if request.is_ajax():
            img_upload = request.FILES.get('img_upload')
            print(img_upload,"22222222222222222222222")
            file_name = str(uuid.uuid4()) + "." + img_upload.name.rsplit('.', maxsplit=1)[1]
            img_file_path = os.path.join('static', 'img', file_name)
            with open(img_file_path, 'wb') as f:
                for line in img_upload.chunks():
                    f.write(line)

            return HttpResponse(img_file_path)
        else:
            if request.method == 'POST':
                file_path = request.POST.get('avatar')
                print(file_path,'3333333333333')
                UserInfo.objects.filter(username=request.user.username).update(img=file_path)
                return redirect('/index/')
except Exception as e :
    logger.exception(e)






