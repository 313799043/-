from django.shortcuts import render,redirect,HttpResponse
import json
from web import models
from rbac.service import initial_permission
# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        obj = models.UserInfo.objects.filter(user__username=u,user__password=p).first()
        print(u,p)
        print(obj)
        obj2 = models.UserInfo.objects.filter(user__username="aaa", user__password="aaa").first()
        print(obj2)
        if obj:
            print("验证正确")
            request.session['user_info'] = {'username':u,'nickname':obj.nickname,'nid':obj.id}

            #得到的值
            #角色     权限
            # request.session[settings.RBAC_PERMISSION_SESSION_KEY] = user_permission_dict
            # request.session[settings.RBAC_MENU_PERMISSION_SESSION_KEY] = {
            #菜单
            #     settings.RBAC_MENU_KEY: menu_list,
            #     settings.RBAC_MENU_PERMISSION_KEY: menu_permission_list
            # }


            initial_permission(request, obj.user_id)
            return redirect('/index.html')
        else:
            return render(request,'login.html')


def index(request):
    if not request.session.get('user_info'):
        return redirect('/login.html')

    return render(request,'index.html')


def trouble(request):
    # request.permission_code_list
    if request.permission_code == "LOOK":
        trouble_list = models.Order.objects.filter(create_user_id=request.session['user_info']['nid'])
        return render(request,'trouble.html',{'trouble_list':trouble_list})

    elif request.permission_code == "DEL":
        nid = request.GET.get('nid')
        models.Order.objects.filter(create_user_id=request.session['user_info']['nid'],id=nid).delete()
        return redirect('/trouble.html')

    elif request.permission_code == "POST":
        if request.method == "GET":
            return render(request,'trouble_add.html')
        else:
            title = request.POST.get('title')
            content = request.POST.get('content')
            models.Order.objects.create(title=title,detail=content,create_user_id=request.session['user_info']['nid'])
            return redirect('/trouble.html')

def trouble_kill(request):
    nid = request.session['user_info']['nid']

    if request.permission_code == "LOOK":
        # 查看列表:未解决,当前用户已经解决或正在解决
        from django.db.models import Q
        trouble_list = models.Order.objects.filter(Q(status=1)|Q(processor_id=nid)).order_by('status')
        return render(request,'trouble_kill_look.html',{'trouble_list':trouble_list})
    elif request.permission_code == "EDIT":
        # http://127.0.0.1:8000/trouble-kill.html?md=edit&nid=1
        if request.method == 'GET':
            order_id = request.GET.get('nid')
            # 已经抢到了，未处理
            if models.Order.objects.filter(id=order_id,processor_id=nid,status=2):
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request,'trouble_kill_edit.html',{'obj':obj})
            # 开抢
            v = models.Order.objects.filter(id=order_id,status=1).update(processor_id=nid,status=2)
            if not v:
                return HttpResponse("小伙子，手速太慢了！！！")
            else:
                obj = models.Order.objects.filter(id=order_id).first()
                return render(request,'trouble_kill_edit.html',{'obj':obj})
        else:
            order_id = request.GET.get('nid')
            solution = request.POST.get('solution')
            models.Order.objects.filter(id=order_id,processor_id=nid).update(status=3,solution=solution,ptime=datetime.datetime.now())
            return redirect('/trouble-kill.html')

def report(request):
    if request.permission_code  == "LOOK":
        if request.method == 'GET':
            return render(request,'report.html')
        else:
            from django.db.models import Count
            # 饼图
            result = models.Order.objects.filter(status=3).values_list('processor__nickname').annotate(ct=Count('id'))
            # 分组：select * from xx group by processor_id,ptime(2017-11-11)
            # 折线图
            ymd_list = models.Order.objects.filter(status=3).extra(select={'ymd':"strftime('%%s',strftime('%%Y-%%m-%%d',ptime))"}).values('processor_id','processor__nickname','ymd').annotate(ct=Count('id'))
            ymd_dict = {}
            for row in ymd_list:
                key = row['processor_id']
                if key in ymd_dict:
                    ymd_dict[key]['data'].append([float(row['ymd'])*1000, row['ct']])
                else:
                    ymd_dict[key] = {'name':row['processor__nickname'],'data':[ [float(row['ymd'])*1000, row['ct']],  ]}
            response = {
                'pie': [['方少伟', 45.0],['吴永强',   40.0],['友情并',3],['尹树林',90]],
                'zhexian': list(ymd_dict.values())
            }
            return HttpResponse(json.dumps(response))




























