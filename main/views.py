from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
def register(request):
    if request.method == "POST":
        contex = dict()
        username, password, name = RegisterData(request).get_data()
        if username == None:
            contex['err_msg'] = "数据不合法或邀请码错误"
            return render(request, "login/register.html", contex)
        contex['name'] = name
        contex['username'] = username
        response=User.objects.filter(username=username)
        if response.exists():
            contex['err_msg'] = "用户名已存在"
            return render(request, "login/register.html", contex)
        User.objects.create_user(username=username,password=password,first_name=name)
        request.session['tip'] = "注册成功，请您登陆"
        return HttpResponseRedirect("/login")
    if request.method == "GET":
        contex = dict()
        if 'tip' in request.session:
            contex['tip'] = request.session['tip']
            del request.session['tip']
        return render(request, "login/register.html", contex)


def login(request):
    if request.method == "POST":
        contex = dict()
        username, password = LoginData(request).get_data()
        if username == None:
            contex['err_msg'] = "数据不合法"
            return render(request, "login/login.html", contex)
        user = auth.authenticate(username=username, password=password)

        contex['username']=username
        if user is None:
            contex['err_msg'] = "用户名或密码错误"
            return render(request,"login/login.html",contex)
        auth.login(request,user)
        next=request.GET.get('next')
        if next == None:
            return HttpResponseRedirect("/qr")
        else:
            return HttpResponseRedirect(next)
    if request.method == "GET":
        contex = dict()
        if 'tip' in request.session:
            contex['tip'] = request.session['tip']
            del request.session['tip']
        return render(request, "login/login.html", contex)


def logout(request):
    auth.logout(request)
    request.session['tip'] = "您已成功登出，请重新登陆"
    return HttpResponseRedirect('/login')

def qr(request):
    context=dict()
    context['name']=request.user.first_name
    return render(request,"main/qr.html",context)

def certification(request):
    return HttpResponse("123")
class GetPostData:
    def __init__(self, request):
        self.receive_data = request.POST
        self.username = self.receive_data.get('username')
        self.password = self.receive_data.get('password')
        if not self.post_lawful():
            self.username = None  # 如果数据不合法，就将self.username置为None，方便后面的判断

    # 防止绕过前端验证，提交非法内容
    def post_lawful(self):
        if self.username is None or self.password is None \
                or len(self.username) < 3 or len(self.username)  > 30 \
                or len(self.password) <6 or len(self.password) > 30:
            return False
        else:
            return True


class RegisterData(GetPostData):

    def __init__(self, request):
        super().__init__(request)
        self.name = self.receive_data.get('name')
        self.code=self.receive_data.get('code')

    def get_data(self):
        if self.username is not None and self.lawful():
            return self.username, self.password, self.name
        else:
            return None, None, None

    def lawful(self):

        from common import conf
        print(conf.get('register', 'code'))
        print(self.code)
        if self.name is None or len(self.name) < 2 or len(self.name)>30 or self.code!=conf.get('register','code'):
            return False
        else:
            return True


class LoginData(GetPostData):
    def __init__(self, request):
        super().__init__(request)

    def get_data(self):
        return self.username, self.password
