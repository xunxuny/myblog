#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# from django.template import Context, Template
# from forms import SurveyForm
# from models import  Survey,Option
# from django.utils import simplejson
# from datetime import datetime
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
from models import Article,Comment

from django.utils.encoding import force_unicode
try:
    from simplejson import JSONEncoder
except ImportError:
    try:
        from json import JSONEncoder
    except ImportError:
        from django.utils.simplejson import JSONEncoder

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj



def home(request):
    template_name = 'home.html'
    objs = Article.objects.filter(status='finished')
    ctx={'objs':objs}
    return render(request, template_name, ctx)

def search(request):
    template_name = 'home.html'
    title = request.POST.get('title','')
    objs = Article.objects.filter(status='finished')
    objs = objs.filter(Q(name__icontains=title)|Q(content__icontains=title))
    ctx={'objs':objs}
    return render(request, template_name, ctx) 
 
def page(request,id):
    template_name = 'page.html'
    obj=get_object_or_404(Article,id=id)
    ctx={'obj':obj}
    return render(request, template_name, ctx)
 
@csrf_exempt
def add_comment(request,id):
    info = ''
    obj=get_object_or_404(Article,id=id)
    name = request.POST.get('name','')
    content = request.POST.get('comment','')
    if not content:
        info = u"评论为空"
    else:
        if not name and not request.user.is_authenticated():
            name = u"匿名"    
        com = Comment(name=name,content=content)
        com.article = obj
        if request.user.is_authenticated():
            com.created_by = request.user 
        com.save()
        info = u"添加成功"
    data = {'info':info}
    return HttpResponse(LazyEncoder().encode(data), mimetype='application/json')