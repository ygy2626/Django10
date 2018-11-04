from django.shortcuts import render
from .forms import SigninForm, SignupForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

#회원가입
def signup(request):
    #GET/POST 분리
    if request.method == "GET":
        #SingupForm 객체 생성 및 HTML 문서 전달
        form1 = SignupForm()
        return render(request, 'customlogin/signup.html', {'form':form1} )
    elif request.method == "POST":
        #request.POST를 기반으로 SingupForm 객체 생성
        form1 = SignupForm(request.POST)
        #유효한 값인지 확인(아이디 중복체크, 아이티형식 체크, 비밀번호 형식 체크)
        if form1.is_valid():
            #비밀번호와 비밀번호 확인 값이 같은지 체크
            if form1.cleaned_data['password'] == form1.cleaned_data['password_check']:
                #새로운 회원 생성
                new_user = User.objects.create_user(form1.cleaned_data['username'], form1.cleaned_data['email'], form1.cleaned_data['password'])
                
                #추가사항 입력 및 데이터베이스에 저장
                new_user.first_name = form1.cleaned_data['first_name']
                new_user.last_name = form1.cleaned_data['last_name']
                new_user.save()
                return HttpResponseRedirect( reverse ('index') )
            else:#비밀번호가 다른경우에 처리
                return render(request, 'customlogin/signup.html', {'form':form1} )
        
        else:
            return render(request, 'customlogin/signup.html', {'form':form1} )
from django.contrib.auth import login, authenticate
#login ; 해당 요청을 한 클라이언에 로그이 처리
#authenticate : 비미번호를 암호화한 뒤, 아이디와 암호된 비밀번호 모두 일치하는 User객체를 추출
#로그인
def signin(request):
    if request.method == "GET":
        f = SigninForm()
        #login_required로 로그인페이지 접근했을 때 사용자가 이전에 요청했던 URL 주소를 추출
        nexturl = request.GET.get('next')
        return render(request, 'customlogin/signin.html', {'form' : f, 'nexturl':nexturl} )
    elif request.method == "POST":
        #아이디나 비밀번호가 일치하지않는 겨우 사용자 입력을 넘겨줄 모델폼객체를 미리 생성
        f = SigninForm(request.POST)
        #사용자 요청에 포함된 데이터 중 아이디와 비밀번호 값 추출
        id = request.POST.get('username')
        pw = request.POST.get('password')
        #f.is_valid() 호출 후 cleaned_data를 사용할 수 없음
        #-> id 중복체크를 해버리기 때문에 로그인을 수행할 수 없음(항상 False 반환)
        #아이디와 비밀번호가 일치하는 유저를 반환해 u변수에 저장
        #일치하지 않는경우  None 값을 반환
        u = authenticate(username = id, password = pw)
        if u is not None : #u변수가 None 값이 아닌 경우(아이디와 비밀번호가 일치하는 유저가 있음)
            #해당 요청을 가진 클라이언트가 u에 저장된 User 객체로 로그인하느 작업을 수행
            login(request, user = u)
            nexturl = request.POST.get('nexturl')
            if nexturl != '':
                return HttpResponseRedirect(nexturl)
            return HttpResponseRedirect( reverse('index') )
        else: #아이디나 비밀번호가 일치하지않음
            return render(request, 'customlogin/signin.html', {'form':f, 'error' : "아이디 또는 비밀번호가 일치하지 않음"} )

from django.contrib.auth import logout
#로그아웃
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index') )









