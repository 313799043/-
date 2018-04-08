from django.shortcuts import render, redirect, HttpResponse
import datetime
import json
from web import models
from rbac.service import initial_permission
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def login(request):
    print("views.....login")
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        print("views.....loginxxxxxxxxxxxxxxxxx")
        u = request.POST.get('username')
        p = request.POST.get('password')
        obj = models.UserInfo.objects.filter(user__username=u, user__password=p).first()
        print(u, p)
        print(obj)
        obj2 = models.UserInfo.objects.filter(user__username="aaa", user__password="aaa").first()
        print(obj2)
        if obj:
            print("验证正确")
            request.session['user_info'] = {'username': u, 'nickname': obj.nickname, 'nid': obj.id}

            # 得到的值
            # 角色     权限
            # request.session[settings.RBAC_PERMISSION_SESSION_KEY] = user_permission_dict
            # request.session[settings.RBAC_MENU_PERMISSION_SESSION_KEY] = {
            # 菜单
            #     settings.RBAC_MENU_KEY: menu_list,
            #     settings.RBAC_MENU_PERMISSION_KEY: menu_permission_list
            # }


            initial_permission(request, obj.user_id)
            return redirect('/index.html')
        else:
            return render(request, 'login.html')


def index(request):
    print("跳入首页")
    if not request.session.get('user_info'):
        print("没数据")
        return redirect('/login.html')
    print("有数据")
    return render(request, 'index.html')


# 个人操作
def add(request):
    print("addd")
    return render(request, 'trouble_add.html')


def mytrouble(request):
    if request.permission_code == "LOOK":
        trouble_list = models.Order.objects.filter(create_user_id=request.session['user_info']['nid'])

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(trouble_list, 5, request=request)
        trouble_list = p.page(page)
        return render(request, 'trouble.html', {'trouble_list': trouble_list})

    elif request.permission_code == "DEL":
        nid = request.GET.get('nid')
        models.Order.objects.filter(create_user_id=request.session['user_info']['nid'], id=nid).delete()
        return redirect('/trouble.html')
    elif request.permission_code == "DETAIL":
        print("EDIT--------******************")
        nid = request.GET.get('nid')
        print("nid", nid)
        content = models.Order.objects.filter(id=nid).first()
        print(content.title)

        return render(request, 'trouble_content.html', {'trouble_content': content})
    elif request.permission_code == "POST":
        if request.method == "GET":
            return render(request, 'trouble_add.html')
        else:
            print("添加客户")
            title = request.POST.get('title')
            content = request.POST.get('content')
            ctype = request.POST.get('jy')
            print(title)
            print(ctype)
            models.Order.objects.create(title=title, detail=content, ctype=ctype,
                                        create_user_id=request.session['user_info']['nid'])
            return redirect('/trouble.html')


##############################################
# **************公池
def update(request):
    print("进入公池")
    # return HttpResponse("aaaaaaaa")
    if request.permission_code == "LOOK":
        trouble_list = models.Order.objects.filter(status=1)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(trouble_list, 5, request=request)
        trouble_list = p.page(page)
        return render(request, 'trouble.html', {'trouble_list': trouble_list})

    elif request.permission_code == "DEL":
        nid = request.GET.get('nid')
        models.Order.objects.filter(create_user_id=request.session['user_info']['nid'], id=nid).delete()
        return redirect('/trouble.html')
    elif request.permission_code == "DETAIL":
        print("EDIT--------******************")
        nid = request.GET.get('nid')
        print("nid", nid)
        content = models.Order.objects.filter(id=nid).first()
        print(content.title)

        return render(request, 'trouble_content.html', {'trouble_content': content})
    elif request.permission_code == "bbb":
        print("aaaa")
        nid = request.GET.get('nid')
        models.Order.objects.filter(id=nid).update(status=1)
        return redirect('/trouble.html')
        return render(request, 'trouble_kill_look.html', {'trouble_list': trouble_list})


    elif request.permission_code == "POST":
        if request.method == "GET":
            return render(request, 'trouble_add.html')
        else:
            print("添加客户")
            title = request.POST.get('title')
            content = request.POST.get('content')
            ctype = request.POST.get('jy')
            print(title)
            print(ctype)
            models.Order.objects.create(title=title, detail=content, ctype=ctype,
                                        create_user_id=request.session['user_info']['nid'])
            return redirect('/trouble.html')



def trouble(request):
    # request.permission_code_list
    if request.permission_code == "LOOK":
        trouble_list = models.Order.objects.filter(create_user_id=request.session['user_info']['nid'])






        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(trouble_list, 5, request=request)
        trouble_list = p.page(page)
        return render(request, 'trouble.html', {'trouble_list': trouble_list})







    elif request.permission_code == "DEL":
        nid = request.GET.get('nid')
        models.Order.objects.filter(create_user_id=request.session['user_info']['nid'], id=nid).delete()
        return redirect('/trouble.html')
    elif request.permission_code == "DETAIL":
        print("EDIT--------******************")
        nid = request.GET.get('nid')
        print("nid", nid)
        content = models.Order.objects.filter(id=nid).first()
        print(content.title)

        return render(request, 'trouble_content.html', {'trouble_content': content})
    elif request.permission_code == "POST":
        if request.method == "GET":
            return render(request, 'trouble_add.html')
        else:
            print("添加客户")
            title = request.POST.get('title')
            content = request.POST.get('content')
            ctype = request.POST.get('jy')
            print(title)
            print(ctype)
            models.Order.objects.create(title=title, detail=content, ctype=ctype,
                                        create_user_id=request.session['user_info']['nid'])
            return redirect('/trouble.html')



    elif request.permission_code == "BBB":
        print(request.session['user_info']['nid'])
        print(request.session['user_info']['nickname'])
        if request.method == 'GET':
            # print(request.session.user_info.nickname)
            order_id = request.GET.get('nid')
            obj = models.Order.objects.filter(id=order_id).first()
            obj2=models.Update.objects.filter(aa=obj.id)
            # print(obj2.detail)






            # try:
            #     page = request.GET.get('page', 1)
            # except PageNotAnInteger:
            #     page = 1
            #     # 这里指从allorg中取五个出来，每页显示5个
            # p = Paginator(obj2, 5, request=request)
            # obj2 = p.page(page)




            return render(request, 'trouble_kill_edit.html', {'obj2': obj2,'obj': obj})

        else:
            print("dddd")
            print(request.session['user_info']['nid'])
            order_id = request.GET.get('nid')
            solution = request.POST.get('solution')
            # bb = request.session['user_info']['nid']
            models.Update.objects.create(aa_id=order_id , detail=solution,bb_id=request.session['user_info']['nid'],
                                        ptime=datetime.datetime.now())
            order_id = request.GET.get('nid')
            obj = models.Order.objects.filter(id=order_id).first()
            obj2=models.Update.objects.filter(aa=obj.id)
            return render(request, 'trouble_kill_edit.html', {'obj2': obj2, 'obj': obj})


    # 添加为公户
    elif request.permission_code == "ADDALL":
        nid = request.GET.get('nid')
        models.Order.objects.filter(id=nid).update(status=1)
        return HttpResponse("ssss")
        #


def trouble_kill(request):
    nid = request.session['user_info']['nid']

    if request.permission_code == "LOOK":
        # 查看列表:未解决,当前用户已经解决或正在解决
        from django.db.models import Q
        trouble_list = models.Order.objects.filter(Q(status=1) | Q(processor_id=nid)).order_by('status')
        return render(request, 'trouble_kill_look.html', {'trouble_list': trouble_list})
    elif request.permission_code == "EDIT":
        # http://127.0.0.1:8000/trouble-kill.html?md=edit&nid=1
        if request.method == 'GET':
            order_id = request.GET.get('nid')
            # 已经抢到了，未处理
            if models.Order.objects.filter(id=order_id, processor_id=nid, status=2):
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request, 'trouble_kill_edit.html', {'obj': obj})
            # 开抢
            v = models.Order.objects.filter(id=order_id, status=1).update(processor_id=nid, status=2)
            if not v:
                return HttpResponse("小伙子，手速太慢了！！！")
            else:
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request, 'trouble_kill_edit.html', {'obj': obj})
        else:
            order_id = request.GET.get('nid')
            solution = request.POST.get('solution')
            models.Order.objects.filter(id=order_id, processor_id=nid).update(status=3, solution=solution,
                                                                              ptime=datetime.datetime.now())
            return redirect('/trouble-kill.html')


def report(request):
    if request.permission_code == "LOOK":
        if request.method == 'GET':
            return render(request, 'report.html')
        else:
            from django.db.models import Count
            # 饼图
            result = models.Order.objects.filter(status=3).values_list('processor__nickname').annotate(ct=Count('id'))
            # 分组：select * from xx group by processor_id,ptime(2017-11-11)
            # 折线图
            ymd_list = models.Order.objects.filter(status=3).extra(
                select={'ymd': "strftime('%%s',strftime('%%Y-%%m-%%d',ptime))"}).values('processor_id',
                                                                                        'processor__nickname',
                                                                                        'ymd').annotate(ct=Count('id'))
            ymd_dict = {}
            for row in ymd_list:
                key = row['processor_id']
                if key in ymd_dict:
                    ymd_dict[key]['data'].append([float(row['ymd']) * 1000, row['ct']])
                else:
                    ymd_dict[key] = {'name': row['processor__nickname'],
                                     'data': [[float(row['ymd']) * 1000, row['ct']], ]}
            response = {
                'pie': [['方少伟', 45.0], ['吴永强', 40.0], ['友情并', 3], ['尹树林', 90]],
                'zhexian': list(ymd_dict.values())
            }
            return HttpResponse(json.dumps(response))
