$('.rbac-menu-header').click(function () {
    $(this).next().toggleClass('rbac-hide');
    //$(this).next().removeClass('rbac-hide').parent().siblings().find('.rbac-menu-body').addClass('rbac-hide');
});
$(document).ready(function() {
	$('.inactive').click(function(){
		if($(this).siblings('ul').css('display')=='none'){
			$(this).parent('li').siblings('li').removeClass('inactives');
			$(this).addClass('inactives');
			$(this).siblings('ul').slideDown(100).children('li');
			if($(this).parents('li').siblings('li').children('ul').css('display')=='block'){
				$(this).parents('li').siblings('li').children('ul').parent('li').children('a').removeClass('inactives');
				$(this).parents('li').siblings('li').children('ul').slideUp(100);

			}
		}else{
			//����������+��
			$(this).removeClass('inactives');
			//��������˵����Ӳ˵�����
			$(this).siblings('ul').slideUp(100);
			//���������Ӳ˵����+��
			$(this).siblings('ul').children('li').children('ul').parent('li').children('a').addClass('inactives');
			//��������˵����Ӳ˵�����
			$(this).siblings('ul').children('li').children('ul').slideUp(100);

			//����ͬ���˵�ֻ����һ����չ���ģ�-����ʾ��
			$(this).siblings('ul').children('li').children('a').removeClass('inactives');
		}
	})
});