from . import models

from django.conf import settings

def initial_permission(request, user_id):
    print("进入rbac.service")
    """
    :param request:  request: 请求对象
    :param user_id: user_id: 当前用户id
    :return:
    """
    #先反向后正向,查找到用户的角色
    roles = models.Role.objects.filter(users__user_id=user_id)
    #根据角色查找能用的链接跟权限
    p2a = models.Permission2Action2Role.objects.filter(role__in=roles).values('permission__url',"action__code").distinct()

    user_permission_dict = {}
    for item in p2a:
        if item['permission__url'] in user_permission_dict:
            user_permission_dict[item['permission__url']].append(item['action__code'])
        else:
            user_permission_dict[item['permission__url']] = [item['action__code'], ]


    # RBAC_PERMISSION_SESSION_KEY = "rbac_permission_session_key"
    print("user_permission_dict",user_permission_dict)

    menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))
    print("menu_list列表")
    print(menu_list)
    #
    menu_permission_list = list(models.Permission2Action2Role.objects.filter(role__in=roles,permission__menu__isnull=False).values(
                                'permission_id','permission__url','permission__caption','permission__menu_id').distinct())

    print("menu_permission_list",)







    #把权限赋值给settings.....
    #菜单
    #个人所属菜单
    request.session[settings.RBAC_PERMISSION_SESSION_KEY] = user_permission_dict
    request.session[settings.RBAC_MENU_PERMISSION_SESSION_KEY] = {
        settings.RBAC_MENU_KEY: menu_list,
        settings.RBAC_MENU_PERMISSION_KEY: menu_permission_list
    }







