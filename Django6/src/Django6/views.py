'''
Created on 2018. 10. 21.

@author: user
'''
from django.shortcuts import render_to_response, render
from django.template import RequestContext

#404 에러페이지 처리 뷰
def handler404(request, *args, **argv):
    response = render_to_response('404.html', {}, content_instance=RequestContext(request))
    
    response.status_code = 404 #에러코드(404)를 헤더파일에 입력
    
    return response
#500 에러페이지 처리 뷰
def handler500(request, *args, **argv):
    response = render_to_response('500.html', {}, context_instance = RequestContext(request))
    
    response.status_code = 500
    return response