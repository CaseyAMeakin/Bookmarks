from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, HttpResponse, get_list_or_404, HttpResponseRedirect, Http404
from django.template import loader, RequestContext
from django.contrib.gis.geoip import GeoIP
from django.utils import timezone
from urlparse import urlparse
import socket

from .models import Bookmark


@login_required
def gotolink(request,bookmark_id):
    g = GeoIP()
    client_ip = request.META['REMOTE_ADDR']
    client_geo = g.city(client_ip)
    client_city = client_geo['city'] + ',' + client_geo['region']
    
    try:
        b = Bookmark.objects.get(pk=bookmark_id)
    except Bookmark.DoesNotExist:
        raise Http404("Weird -- Bookmark does not exist")

    b.accessCount += 1
    b.save()
    alist = b.accessinfo_set.filter(accessIP__contains=client_ip)
    if(len(alist)==0): 
        a = b.accessinfo_set.create(accessIP=client_ip,accessCount=1)
        a.save()
    elif(len(alist)==1):
        a = alist[0]
        a.accessCount += 1
        a.save()
    else:
        return Http404("Internal accounting error")
        
    return HttpResponseRedirect(b.url)


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('home/')
    else:
        return render(request, 'bookmarks/index.html')

        
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password']
        (user,created) = User.objects.get_or_create(username=username)
        if(created):
            user.set_password(password)
            user.email = email
            user.save()
            newUserName = username
        else:
            newUserName = 'Username already exists'
        return render(request, 'bookmarks/index.html', {'newUserName':newUserName})
    else:
        return render(request, 'bookmarks/index.html')


def userlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            bookmarks = get_list_or_404(Bookmark)
            return  HttpResponseRedirect('../home/')
        else:
            return HttpResponse("User error.")
    else:
        return render(request, 'bookmarks/index.html')

@login_required
def userlogout(request):
    logout(request)
    return render(request, 'bookmarks/index.html')

@login_required
def home(request):
    if request.user.is_authenticated():
        try:
            bookmarks = Bookmark.objects.filter(user__exact=request.user.username)
        except Bookmark.DoesNotExist:
            bookmarks = []

        return render(request, 'bookmarks/home.html', {'bookmarks': bookmarks })
    else:
        return render(request,'bookmarks/index.html')

@login_required
def detail(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, pk=bookmark_id)
    return render(request, 'bookmarks/detail.html', {'bookmark': bookmark} )

@login_required
def edit(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, pk=bookmark_id)
    return render(request, 'bookmarks/edit.html', {'bookmark': bookmark} )

@login_required
def enternew(request):
    return render(request, 'bookmarks/enternew.html', {})
    
@login_required
def bdelete(request, bookmark_id):
    try:
        b = Bookmark.objects.get(pk=bookmark_id)
    except Bookmark.DoesNotExist:
        raise Http404("Weird -- Bookmark does not exist")
    try:
        bookmarks = Bookmark.objects.filter(user__exact=request.user.username)
    except Bookmark.DoesNotExist:
        bookmarks = []
            
    b_desc_deleted = b.url_desc
    b.delete()
    return render(request, 'bookmarks/home.html', {'bookmarks': bookmarks, 'b_desc_deleted':b_desc_deleted })

@login_required
def bdelete_chk(request, bookmark_id):
    try:
        b_to_delete = Bookmark.objects.get(pk=bookmark_id)
    except Bookmark.DoesNotExist:
        raise Http404("Weird -- Bookmark does not exist")
    try:
        bookmarks = Bookmark.objects.filter(user__exact=request.user.username)
    except Bookmark.DoesNotExist:
        bookmarks = []

    return render(request, 'bookmarks/home.html', {'bookmarks': bookmarks, 'b_to_delete':b_to_delete })

@login_required
def submitedit(request, bookmark_id):
    try:
        b = Bookmark.objects.get(pk=bookmark_id)
    except Bookmark.DoesNotExist:
        raise Http404("Weird -- Bookmark does not exist")
    try:
        bookmarks = Bookmark.objects.filter(user__exact=request.user.username)
    except Bookmark.DoesNotExist:
        bookmarks =[]

    b.url      = request.POST['url']
    b.url_desc = request.POST['url_desc']
    b.url_keywords = request.POST['url_keywords']
    b.save()
    return render(request, 'bookmarks/home.html', {'bookmarks':bookmarks,'bedit' : b})
    

@login_required
def search(request):
    search_text = request.GET['search_text']
    try:
        b = Bookmark.objects.filter(url_keywords__contains=search_text,user__exact=request.user.username)
    except Bookmark.DoesNotExist:
        b = []
    return render(request,'bookmarks/search.html', {'bookmarks': b, 'search_text': search_text})


@login_required
def addlink(request):

    try:
        bookmarks = Bookmark.objects.filter(user__exact=request.user.username)
    except Bookmark.DoesNotExist:
        bookmarks = []

    if request.method == 'POST':
        url_new = request.POST['url'] 
        url_parsedat = urlparse(url_new)
        if 'http' in url_parsedat.scheme:
            url_ip_new = socket.gethostbyname('www.google.com')
            url_desc_new = request.POST['url_desc']
            url_keywords_new = request.POST['url_keywords']
            
            if(url_desc_new ==''): url_desc_new = url_new

            b = Bookmark(url=url_new,url_ip=url_ip_new,url_desc=url_desc_new,url_keywords=url_keywords_new,
                         pub_date=timezone.now(),user=request.user.username)
            b.save()

            return HttpResponseRedirect('../home/')
            
        else:
            alertText = 'Invalid URL (needs http prefix): ' + url_new
            return render(request, 'bookmarks/home.html', {'bookmarks':bookmarks, 'alertText': alertText} )
                          
    else:
        return HttpResponse("Not POST")

    return HttpResponse("Invalid form!" )

