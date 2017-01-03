from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from app01 import models
from app01 import myform
from app01 import pagination
import re
import json
# Create your views here.

type_dict = {
    "1": "51区",
    "2": "段子",
    "3": "图片",
}


CURRENT_PART_ORDER = ["all", "time"]


def page(request):
    return render(request, 'page.html')


def query_order_list(current, part, order_type):
    CURRENT_PART_ORDER[0] = part
    CURRENT_PART_ORDER[1] = order_type
    if part == "all":
        obj = models.Article.objects.all()
    elif part == "51":
        obj = models.Article.objects.filter(type=1)
    elif part == "text":
        obj = models.Article.objects.filter(type=2)
    count = obj.count()
    my_pagination = pagination.PageInfo(current, count)
    begin = my_pagination.begin()
    end = my_pagination.end()
    total_page = my_pagination.total_page()
    if order_type == "time":
        article_list = obj.order_by("-add_time")[begin:end]
    elif order_type == "comment":
        article_list = obj.order_by("add_time")[begin:end]
    return article_list, total_page


def index(request):
    part = request.GET.get("part", CURRENT_PART_ORDER[0])
    order_type = request.GET.get("order_type", CURRENT_PART_ORDER[1])
    current = request.GET.get("p", 1)
    current = int(current)
    article_list, total_page = query_order_list(current, part, order_type)
    for article in article_list:
        article.add_time = article.add_time.strftime("%Y-%m-%d %H:%M:%S")
        article.type = type_dict[str(article.type)]
        article.url_2 = deal_url(article.url)
    page_string = pagination.custom_pager("/index/", current, total_page)
    username = request.session.get("username", None)
    return render(request, 'index.html',
                  {"article_list": article_list, "username": username,
                   "page_string": page_string, "CURRENT_PART_ORDER": CURRENT_PART_ORDER})


def register(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        register_form = myform.RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            result = models.User.objects.filter(name=data["name"])
            if result:
                ret["message"] = "用户已经存在！"
            elif data["pwd"] != data["pwd_confirm"]:
                ret["message"] = "用户已经存在！"
            else:
                data.pop("pwd_confirm")
                models.User.objects.create(**data)
                request.session['username'] = data["name"]
                ret["status"] = True
        else:
            error_msg = json.loads(register_form.errors.as_json())
            error = ""
            for key in error_msg:
                error = error_msg[key][0]["message"]
            ret["message"] = error
    return HttpResponse(json.dumps(ret))


def login(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        login_form = myform.LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            result = models.User.objects.filter(name=data["name"])
            if result:
                if result[0].pwd != data["pwd"]:
                    ret["message"] = "用户名或密码错误！"
                else:
                    request.session['username'] = data["name"]
                    ret["status"] = True
            else:
                ret["message"] = "用户名或密码错误！"
    return HttpResponse(json.dumps(ret))


def logout(request):
    try:
        del request.session["username"]
    except:
        pass
    return redirect("/index/")


def gain(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        url_form = myform.UrlForm(request.POST)
        if url_form.is_valid():
            data = url_form.cleaned_data
            url = data["url"]
            title, abstract = spider(url)
            if not title:
                ret["message"] = "无法访问该地址！"
                return HttpResponse(json.dumps(ret))
            ret["status"] = True
            ret["message"] = []
            ret["message"].append(title)
            ret["message"].append(abstract)
            return HttpResponse(json.dumps(ret))
        else:
            ret["message"] = "链接地址格式错误！"
            return HttpResponse(json.dumps(ret))
    return redirect("/index/")


def spider(url):
    import requests
    try:
        data = requests.get(url)
    except:
        return False, False
    try:
        lang = re.findall(r'\scharset=([\w-]+)"?\s', data.text)[0].strip("\"")
    except IndexError:
        lang = "utf-8"
    data.encoding = lang
    try:
        title = re.findall(r'<title>(.+)</title>', data.text)[0]
    except IndexError:
        title = ""
    try:
        abstract = re.findall(r'<meta\sname="[dD]escription"\scontent="(.+)"', data.text)[0]
    except IndexError:
        abstract = ""

    return title, abstract


def login_confirm(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        user = request.session.get("username", None)
        if user:
            ret["status"] = True
        return HttpResponse(json.dumps(ret))
    return redirect("/index/")


def publish(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        data = {}
        data["url"] = request.POST.get("url", None)
        data["type"] = request.POST.get("type", None)
        data["title"] = request.POST.get("title", None)
        data["abstract"] = request.POST.get("abstract", None)
        data["user"] = models.User.objects.get(name=request.session.get("username"))
        if data["type"] == "51区":
            data["type"] = 1
        elif data["type"] == "段子":
            data["type"] = 2
        else:
            data["type"] = 3
        if data["url"].startswith("http://") or data["url"].startswith("https://"):
            pass
        else:
            data["url"] = "http://" + data["url"]
        models.Article.objects.create(**data)
        ret["status"] = True
        return HttpResponse(json.dumps(ret))

    return redirect("/index/")


def publish_text(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        data = {}
        count = models.Article.objects.all().count()
        data["url"] = "www.hotpoint.com/article/%s" % (int(count)+1)
        data["type"] = 2
        data["title"] = request.POST.get("title", None)
        data["abstract"] = ""
        data["user"] = models.User.objects.get(name=request.session.get("username"))
        models.Article.objects.create(**data)
        ret["status"] = True
        return HttpResponse(json.dumps(ret))
    return redirect("/index/")


def recommend(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        user = request.session.get("username", None)
        if user:

            title = request.POST.get("title", None)
            user = models.User.objects.get(name=user)
            article = models.Article.objects.get(title=title)
            if user in article.recommend.all():
                article.recommend.remove(user)
                ret["message"] = "remove"
            else:
                ret["message"] = "add"
                article.recommend.add(user)
            ret["status"] = True
        else:
            ret["message"] = "尚未登陆！"
        return HttpResponse(json.dumps(ret))

    return redirect("/index/")


def favorite(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        user = request.session.get("username", None)
        if user:
            title = request.POST.get("title", None)
            user = models.User.objects.get(name=user)
            article = models.Article.objects.get(title=title)
            if user in article.favorite.all():
                article.favorite.remove(user)
                ret["message"] = "remove"
            else:
                ret["message"] = "add"
                article.favorite.add(user)
            ret["status"] = True
        else:
            ret["message"] = "尚未登陆！"
        return HttpResponse(json.dumps(ret))
    return redirect("/index/")


def comment(request):
    # data用来保存html代码字符串
    # counter用来保存递归调用的次数，每递归一次，加一个元素（0），返回一次递归删除一个元素
    # 通过计算counter的长度来控制缩进的空格量。
    data = []
    counter = []

    def get_child_comment(father_comment):
        counter.append(0)
        data.append('<div class=" comment-line" style="margin: 10px 0px;"><span>')
        data.append("&nbsp;" * ((len(counter)-1) * 4))
        data.append(father_comment.text)
        data.append('</span><span> [')
        data.append(father_comment.user.name)
        data.append(']</span><span>')
        data.append(father_comment.add_time.strftime("%Y-%m-%d %H:%M:%S"))
        data.append('</span><span class="hidden reply btn btn-xs btn-primary">回复</span></div>')
        child_comments = models.Comment.objects.filter(father_comment=father_comment)
        if child_comments:
            for child in child_comments:
                get_child_comment(child)
        return counter.pop()

    ret = {"status": False, "message": None}
    if request.method == "POST":
        title = request.POST.get("title", None)
        comments = models.Comment.objects.filter(article__title=title, father_comment=False)
        for item in comments:
            counter.clear()
            get_child_comment(item)
            data.append('<hr style="height:1px;border:none;border-top:1px dashed #0066CC;" />')
        comment_str = "".join(data)
        ret["status"] = True
        ret["message"] = comment_str
        return HttpResponse(json.dumps(ret))
    return redirect("/index/")


def make_comment(request):
    ret = {"status": False, "message": None}
    if request.method == "POST":
        user = request.session.get("username", None)
        if user:
            title = request.POST.get("title", None)
            text = request.POST.get("comment", None)
            father_comment = request.POST.get("father_comment", None).strip()
            father_time = request.POST.get("father_time", None).strip()
            father_user = request.POST.get("father_user", None).strip().strip("[]")
            article = models.Article.objects.get(title=title)
            user = models.User.objects.get(name=user)
            if father_comment:
                father_objs = models.Comment.objects.filter(
                    text=father_comment,
                    user__name=father_user,
                )
                for obj in father_objs:
                    if obj.add_time.strftime("%Y-%m-%d %H:%M:%S") == father_time:
                        this_comment = models.Comment.objects.create(
                            user=user, article=article, text=text, father_comment=obj)
            else:

                this_comment = models.Comment.objects.create(
                    user=user, article=article, text=text)
            number = article.comment_set.count()
            time = this_comment.add_time.strftime("%Y-%m-%d %H:%M:%S")
            ret["message"] = []
            ret["message"].append(number)
            ret["message"].append(user.name)
            ret["message"].append(time)
            ret["status"] = True
        else:
            ret["message"] = "尚未登陆!"
        return HttpResponse(json.dumps(ret))
    return redirect("/index/")


# 处理url获取baseurl
def deal_url(url):
    try:
        domain = re.findall(r'https?://(.*?)/', url)[0]
    except:
        domain = url
    return domain
