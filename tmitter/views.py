from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import Tmeet, Connection, Notification, DmRoom, DmMessage
from .forms import TmeetForm, UserUpdateForm, DmForm
from django.contrib import messages
from django.http import JsonResponse 
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Context, loader
from django.shortcuts import get_object_or_404
import math
import datetime
import json

# デバッグ用
import pprint

CustomUser = get_user_model()
LOADING_COUNT = 35 # TmeetやUser等を一度に何件読み込むか
RANDOM_STRING = 'erghqorna;oerkglarn;gh'
FOLLOWED_NOTI_NUM = 1
LIKED_NOTI_NUM = 2
REPLIED_NOTI_NUM = 3

# def test(request):
#     success = True
#     try:
#         dm_text = request.POST.get('dm_text')
#         dm_room_id = request.POST.get('dm_room_id')
#         dm_room = DmRoom.objects.get(id=dm_room_id)

#         dm_message = DmMessage(
#             user=request.user,
#             content=dm_text,
#             dm_room=dm_room,
#         )
#         dm_message.save()

#         dm_room.last_updated_at = datetime.datetime.now()
#         dm_room.save()
#     except Exception as e:
#         success = False
#         print(e)

#     context = {
#         'success': success,
#     }

#     return JsonResponse(context)

@login_required
def top(request):
    return redirect('home')

@login_required
def home(request):
    form = TmeetForm()
    return render(request, 'tmitter/home.html', {'form': form, })

def home_tmeet_content(request):
    tmeets = Tmeet.objects.filter(parent=None)  
    paginator = Paginator(tmeets, LOADING_COUNT)
    page = request.GET.get('page', default=1)
    max_page_number = math.ceil(tmeets.count() / LOADING_COUNT)

    context = {
        'content': None
    }
    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/tmeet_content.html',{
                'page_obj': page_obj,
                'page': page,
                'loading_count': LOADING_COUNT,
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['max_page_number'] = max_page_number

    return JsonResponse(context)

def tmeet_detail_content(request):
    tmeet_id = request.GET.get('tmeet_id', -1)
    if tmeet_id == -1:
        return JsonResponse(None)
    else:
        parent_tmeet = Tmeet.objects.get(id=tmeet_id)
        tmeets = Tmeet.objects.filter(parent=parent_tmeet)
        
    paginator = Paginator(tmeets, LOADING_COUNT)
    page = request.GET.get('page', default=1)
    max_page_number = math.ceil(tmeets.count() / LOADING_COUNT)

    context = {
        'content': None
    }
    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/tmeet_content.html',{
                'page_obj': page_obj,
                'page': page,
                'loading_count': LOADING_COUNT,
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['max_page_number'] = max_page_number

    return JsonResponse(context)

def user_page(request, user_name):
    form = TmeetForm()

    try:
        display_user = CustomUser.objects.get(username=user_name)
    except Exception as e:
        print(e)
        return render(request, 'tmitter/not_exist_user.html', {'user_name': user_name, 'form': form, })

    # 表示ユーザーがフォローしているユーザーの id のリスト
    display_user_followings = Connection.objects.filter(follower=display_user).values_list('following', flat=True)

    # 表示ユーザーをフォローしているユーザー id のリスト
    display_user_followers = Connection.objects.filter(following=display_user).values_list('follower', flat=True)

    try:
        header_image_url = display_user.header_image.url
    except Exception as e:
        print(e)
        header_image_url = '/media/default/header_default.png'
    try:
        icon_image_url = display_user.icon_image.url
    except Exception as e:
        print(e)
        icon_image_url = '/media/default/icon_default.png'



    return render(request, 'tmitter/user_page.html', {
        'display_user': display_user,
        'display_user_followings': display_user_followings,
        'display_user_followers': display_user_followers,
        'header_image_url': header_image_url,
        'icon_image_url': icon_image_url,
        'user': display_user,
        'form': form,
        })

def user_page_content(request):
    try:
        user_name = request.GET.get('user_name')
        page = request.GET.get('page')
        display_user = CustomUser.objects.get(username=user_name)
    except Exception as e:
        print(e)
    tmeets = Tmeet.objects.filter(user=display_user)
    paginator = Paginator(tmeets, LOADING_COUNT)
    page = request.GET.get('page', default=1)
    max_page_number = math.ceil(tmeets.count() / LOADING_COUNT)

    context = {
        'content': None
    }
    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/tmeet_content.html', {
            'page_obj': page_obj,
            'page': page,
            'loading_count': LOADING_COUNT
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['max_page_number'] = max_page_number

    return JsonResponse(context)

@login_required
def create_tmeet(request):

    # 作成Tmeetが返信であるかどうか
    reply = False
    # 作成Tmeetの返信先のTmeet
    replied_tmeet = None
    # 作成Tmeetの返信先のTmeetのid
    replied_tmeet_id = request.GET.get('to', -1)

    # Tmeetを作成した時の処理
    if request.method == 'POST':
        form = TmeetForm(request.POST, request.FILES)
        if form.is_valid():
            tmeet = form.save(commit=False)
            tmeet.user = request.user
            tmeet.save()
            # Tmeetが返信として作成された場合
            if replied_tmeet_id != -1:
                replied_tmeet = Tmeet.objects.get(id=replied_tmeet_id)
                tmeet.parent = replied_tmeet
                tmeet.save()
                reply = True
                # 返信を受け取った通知を作成
                if replied_tmeet.user != request.user:
                    reply_notification = Notification(
                        kind = REPLIED_NOTI_NUM,
                        user = replied_tmeet.user,
                        tmeet = replied_tmeet,
                        by_tmeet = tmeet,
                    )
                    reply_notification.save()
            return redirect('home')
    # Tmeetをこれから作成する時の処理
    else:
        # Tmeetが返信として作成された場合
        if replied_tmeet_id != -1:
            replied_tmeet = Tmeet.objects.get(id=replied_tmeet_id)
            reply = True
        form = TmeetForm()

    return render(request, 'tmitter/create_tmeet.html', {
        'form': form,
        'to': replied_tmeet_id,
        'reply': reply,
        'tmeet': replied_tmeet,
    })

@login_required
def tmeet_detail(request, tmeet_id):
    tmeet = Tmeet.objects.get(id=tmeet_id)
    form = TmeetForm()

    return render(request, 'tmitter/tmeet_detail.html', {
        'tmeet': tmeet,
        'tmeet_id': tmeet_id,
        'form': form,
    })

@login_required
def like(request):
    tmeet_id = request.POST.get('tmeet_id')
    context = {
        'user': f'{request.user.username}',
    }
    # try:
    tmeet = get_object_or_404(Tmeet, id=tmeet_id)
    # いいねする処理
    if request.user not in tmeet.like.all():
        tmeet.like.add(request.user)
        tmeet.save()
        context['method'] = 'create'
        # いいねされた通知の作成
        if tmeet.user != request.user:
            liked_notification = Notification(
                kind = LIKED_NOTI_NUM,
                user = tmeet.user,
                by_user = request.user,
                tmeet = tmeet,
            )
            liked_notification.save()
    #いいね取り消しの処理
    else:
        tmeet.like.remove(request.user)
        tmeet.save()
        context['method'] = 'delete'
        # 通知の取り消し
        try:
            unliked_notification = Notification.objects.get(
                kind = LIKED_NOTI_NUM,
                user = tmeet.user,
                by_user = request.user,
                tmeet = tmeet,  
            )
            unliked_notification.delete()
        except Exception as e:
            print(e)

    # except Tmeet.DoesNotExist:
    #     pass
    #     # return Http404('該当Tmeetは存在しません')

    like_count = tmeet.like.count()
    context['like_count'] = like_count

    return JsonResponse(context)

@login_required
def delete_tmeet(request):
    tmeet_id = request.GET.get('tmeet_id')
    deleted = True
    try:
        tmeet = Tmeet.objects.get(id=tmeet_id)
        if (tmeet.user == request.user):
            tmeet.delete()
        else:
            deleted = False
    except Exception as e:
        print(e)
        deleted = False
    return JsonResponse({'deleted': deleted, })

@login_required
def follow(request):
    followed_user_id = request.POST.get('followed_user_id')
    try:
        #  ログインユーザー
        login_user = request.user
        #  表示ユーザー
        display_user = CustomUser.objects.get(id=followed_user_id)
    except CustomUser.DoesNotExist:
        pass
        # return Http404("存在しないユーザーです")

    context = dict()

    #  表示ユーザーがフォローしているユーザーの id のリスト
    display_user_followings = Connection.objects.filter(follower=display_user).values_list('following', flat=True)
    #  表示ユーザーをフォローしているユーザーの id のリスト
    display_user_followers = Connection.objects.filter(following=display_user).values_list('follower', flat=True)

    if display_user == login_user:
        pass
        # return Http404("自分はフォローもアンフォローもできません")
    # フォロー解除の処理
    elif login_user.id in display_user_followers:
        Connection.objects.get(follower=login_user, following=display_user).delete()
        context['method'] = 'unfollow'
        # フォローされた通知の削除
        try:
            unfollowed_notification = Notification.objects.get(
                kind = FOLLOWED_NOTI_NUM,
                user = display_user,
                by_user = request.user,
            )
            unfollowed_notification.delete()
        except Exception as e:
            print(e)
    # フォローする処理
    else:
        Connection.objects.create(follower=login_user, following=display_user)
        context['method'] = 'follow'
        # フォローされた通知の作成
        if display_user != request.user:
            followed_notification = Notification(
                kind = FOLLOWED_NOTI_NUM,
                user = display_user,
                by_user = request.user,
            )
            followed_notification.save()

    context['follower_cnt'] = Connection.objects.filter(following=display_user).count()

    return JsonResponse(context)


@login_required
def following_list(request, user_name):
    try:
        login_user = request.user
        display_user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        return Http404("存在しないユーザーです")

    #表示ユーザーがフォローしているユーザーの id のリスト
    display_user_followings_ids = Connection.objects.filter(follower=display_user).values_list('following', flat=True)
    #ログインユーザーがフォローしているユーザーの id のリスト
    followings = Connection.objects.filter(follower=login_user).values_list('following', flat=True)

    #表示ユーザーがフォローしているユーザーのリスト
    display_user_followings = []
    #ログインユーザーがフォローしているユーザーのリスト
    login_user_followings = []

    for id in display_user_followings_ids:
        user = CustomUser.objects.get(id=id)
        display_user_followings.append(user)
    
    for id in followings:
        user = CustomUser.objects.get(id=id)
        login_user_followings.append(user)

    form = TmeetForm()

    return render(request, 'tmitter/following_list.html',{
            'display_user': display_user,
            'display_user_followings': display_user_followings,
            'login_user_followings': login_user_followings,
            'form': form,
    })

def following_list_content(request):
    user_name = request.GET.get('user_name')
    try:
        login_user = request.user
        display_user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        return HttpResponse()("存在しないユーザーです")

    #表示ユーザーがフォローしているユーザーの id のリスト
    display_user_followings_ids = Connection.objects.filter(follower=display_user).values_list('following', flat=True)
    #ログインユーザーがフォローしているユーザーの id のリスト
    followings = Connection.objects.filter(follower=login_user).values_list('following', flat=True)

    #表示ユーザーがフォローしているユーザーのリスト
    display_user_followings = []
    #ログインユーザーがフォローしているユーザーのリスト
    login_user_followings = []

    for id in display_user_followings_ids:
        user = CustomUser.objects.get(id=id)
        display_user_followings.append(user)
    
    for id in followings:
        user = CustomUser.objects.get(id=id)
        login_user_followings.append(user)

    paginator = Paginator(display_user_followings, LOADING_COUNT)
    page = request.GET.get('page', default=1)
    max_page_number = math.ceil(len(display_user_followings) / LOADING_COUNT)

    context = {
        'content': None
    }
    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/user_content.html', {
            'page_obj': page_obj,
            'login_user_followings': login_user_followings,
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['max_page_number'] = max_page_number

    return JsonResponse(context)

@login_required
def follower_list(request, user_name):
    try:
        login_user = request.user
        display_user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        return Http404("存在しないユーザーです")

    #表示ユーザーをフォローしているユーザーの id のリスト
    display_user_followers_ids = Connection.objects.filter(following=display_user).values_list('follower', flat=True)
    #ログインユーザーがフォローしているユーザーの id のリスト
    followings = Connection.objects.filter(follower=login_user).values_list('following', flat=True)

    #表示ユーザーをフォローしているユーザーのリスト
    display_user_followers = []
    #ログインユーザーがフォローしているユーザーのリスト
    login_user_followings = []

    for id in display_user_followers_ids:
        user = CustomUser.objects.get(id=id)
        display_user_followers.append(user)
    
    for id in followings:
        user = CustomUser.objects.get(id=id)
        login_user_followings.append(user)

    form = TmeetForm()

    return render(request, 'tmitter/follower_list.html', {
            'display_user': display_user,
            'display_user_followers': display_user_followers,
            'login_user_followings': login_user_followings,
            'form': form,
    })

def follower_list_content(request):
    user_name = request.GET.get('user_name')
    try:
        login_user = request.user 
        display_user = CustomUser.objects.get(username=user_name)
    except CustomUser.DoesNotExist:
        return HttpResponse(user_name)
    #表示ユーザーをフォローしているユーザーの id のリスト
    display_user_followers_ids = Connection.objects.filter(following=display_user).values_list('follower', flat=True)
    #ログインユーザーがフォローしているユーザーの id のリスト
    followings = Connection.objects.filter(follower=login_user).values_list('following', flat=True)

    #表示ユーザーをフォローしているユーザーのリスト
    display_user_followers = []
    #ログインユーザーがフォローしているユーザーのリスト
    login_user_followings = []

    for id in display_user_followers_ids:
        user = CustomUser.objects.get(id=id)
        display_user_followers.append(user)
    
    for id in followings:
        user = CustomUser.objects.get(id=id)
        login_user_followings.append(user)

    paginator = Paginator(display_user_followers, LOADING_COUNT)
    page = request.GET.get('page', default=1)
    max_page_number = math.ceil(len(display_user_followers) / LOADING_COUNT)

    context = {
        'content': None
    }
    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/user_content.html', {
            'page_obj': page_obj,
            'login_user_followings': login_user_followings,
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['max_page_number'] = max_page_number

    return JsonResponse(context)

@login_required()
def explore(request):
    # #クエリから値を取り出す
    search_value = request.GET.get('q', RANDOM_STRING)
    form = TmeetForm()

    return render(request, 'tmitter/explore.html', {
        'search_value': search_value,
        'random_string': RANDOM_STRING,
        'form': form,
    })

def explored_tmeet_content(request):
    search_value = request.GET.get('q')
    page = request.GET.get('page', default=1)
    tmeets = Tmeet.objects.filter(content__contains=search_value)
    paginator = Paginator(tmeets, LOADING_COUNT)
    max_page_number = math.ceil(tmeets.count() / LOADING_COUNT)

    context = {
        'content': None
    }
    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/tmeet_content.html', {
            'page_obj': page_obj,
            'page': page,
            'loading_count': LOADING_COUNT
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['tmeet_max_page_number'] = max_page_number

    return JsonResponse(context)

def explored_user_content(request):
    search_value = request.GET.get('q')
    users = CustomUser.objects.filter(
        Q(nickname__contains=search_value) |
        Q(username__contains=search_value)
    ).distinct()

    #ログインユーザーがフォローしているユーザーの id のリスト
    followings = Connection.objects.filter(follower=request.user).values_list('following', flat=True)

    #ログインユーザーがフォローしているユーザーのリスト
    login_user_followings = []

    for id in followings:
        user = CustomUser.objects.get(id=id)
        login_user_followings.append(user)

    paginator = Paginator(users, LOADING_COUNT)
    page = request.GET.get('page', default=1)
    max_page_number = math.ceil(len(users) / LOADING_COUNT)

    context = {
        'content': None
    }
    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/user_content.html', {
            'page_obj': page_obj,
            'login_user_followings': login_user_followings,
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['user_max_page_number'] = max_page_number

    return JsonResponse(context)

@login_required
def setting(request):
    user = request.user
    if request.method == 'POST':
        profile_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
    else:
        profile_form = UserUpdateForm(instance=user)
    
    try:
        header_image_url = user.header_image.url
    except Exception as e:
        print(e)
        header_image_url = '/media/default/header_default.png'
    
    try:
        icon_image_url = user.icon_image.url
    except Exception as e:
        print(e)
        icon_image_url = '/media/default/icon_default.png'

    form = TmeetForm()

    return render(request, 'tmitter/setting.html',{
        'profile_form': profile_form,
        'header_image_url': header_image_url,
        'icon_image_url': icon_image_url,
        'form': form,
        })

@login_required
def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    for notification in notifications:
        if notification.be_read == True:
            notification.pre_be_read = True
            notification.save()

    new_notifications = Notification.objects.filter(user=request.user, be_read=False)
    for new_notification in new_notifications:
        new_notification.be_read = True
        new_notification.save()

    form = TmeetForm()

    return render(request, 'tmitter/notification.html', {
        'notifications': notifications,
        'followed': FOLLOWED_NOTI_NUM,
        'liked': LIKED_NOTI_NUM,
        'replied': REPLIED_NOTI_NUM, 
        'form': form,
    })

@login_required
def messages(request):
    dm_rooms = DmRoom.objects.filter(users=request.user)

    form = TmeetForm()
    return render(request, 'tmitter/messages.html', {
        'dm_rooms': dm_rooms,
        'form': form,
        })

@login_required
def search_talk_with_user(request):
    search_value = request.GET.get('q', RANDOM_STRING)
    form = TmeetForm()

    return render(request, 'tmitter/search_talk_with_user.html', {
        'search_value': search_value,
        'random_string': RANDOM_STRING,
        'form': form,
    })

def search_talk_with_user_content(request):
    search_value = request.GET.get('q', RANDOM_STRING)
    context = {
        'content': None,
    }
    if search_value == RANDOM_STRING:
        return JsonResponse(context)

    users = CustomUser.objects.filter(
        Q(nickname__contains=search_value) |
        Q(username__contains=search_value)
    ).distinct()

    page = request.GET.get('page', default=1)
    paginator = Paginator(users, LOADING_COUNT)
    max_page_number = math.ceil(users.count() / LOADING_COUNT)

    context = {
        'content': None,
    }    

    try:
        page_obj = paginator.page(page)
        context['content'] = render(request, 'tmitter/user_content.html', {
            'page_obj': page_obj,
            'for_dm_room': True,
        }).content.decode('utf-8')
    except PageNotAnInteger:
        pass
    except EmptyPage:
        pass

    context['user_max_page_number'] = max_page_number

    return JsonResponse(context)

# テスト中
@login_required
def create_dm_room(request, user_id):
    # dmをする相手
    opp_user = get_object_or_404(CustomUser, id=user_id)

    # 相手と既にトークルームが作成されているかの判定
    my_rooms = DmRoom.objects.filter(users=request.user)
    opp_rooms = DmRoom.objects.filter(users=opp_user)

    for room in my_rooms:
        for opp_room in opp_rooms:
            if room == opp_room and room.users.count() == 2:
                return redirect(reverse('dm_room', kwargs={
                    'user_name': opp_user.username,
                    'dm_room_id': room.id,
                }))

    # 相手とのトークルームが無く、新規に作成する場合
    dm_room = DmRoom.objects.create(last_updated_at=datetime.datetime.now())
    dm_room.users.add(request.user)
    dm_room.users.add(opp_user)
    dm_room.has_read_users.add(request.user)
    dm_room.has_read_users.add(opp_user)
    dm_room.save()

    return redirect(reverse('dm_room', kwargs={
                'user_name': opp_user.username,
                'dm_room_id': dm_room.id,
            }),)

@login_required
def dm_room(request, user_name, dm_room_id):
    dm_room = get_object_or_404(DmRoom, id=dm_room_id)
    opp_user = get_object_or_404(CustomUser, username=user_name)

    dm_room.has_read_users.add(request.user)
    dm_room.save()

    # 自分が参加していないトークルームを表示しようとした時
    if request.user not in dm_room.users.all():
        raise PermissionDenied
    if opp_user not in dm_room.users.all():
        raise PermissionDenied

    # dm_room_idでDmMessageを抽出する
    dm_form = DmForm()

    form = TmeetForm()

    return render(request, 'tmitter/dm_room.html', {
        'opp_user': opp_user,
        'dm_form': dm_form,
        'dm_room_id': dm_room_id,

        'form': form,
    })

def dm_room_content(request, user_name, dm_room_id):
    dm_room = get_object_or_404(DmRoom, id=dm_room_id)
    opp_user = get_object_or_404(CustomUser, username=user_name)

    # 自分が参加していないトークルームを表示しようとした時
    if request.user not in dm_room.users.all():
        raise PermissionDenied
    if opp_user not in dm_room.users.all():
        raise PermissionDenied

    # dmを作成して送信した時
    if request.method == 'POST':
        dm_form = DmForm(request.POST)
        if dm_form.is_valid():
            message = dm_form.save(commit=False)
            message.dm_room = dm_room
            message.user = request.user
            message.save()
    
            dm_room.last_updated_at = datetime.datetime.now()
            dm_room.save()


    # dm_room_idでDmMessageを抽出する
    messages = DmMessage.objects.filter(dm_room=dm_room)
    dm_form = DmForm()

    return render(request, 'tmitter/dm_room_content.html', {
        'messages': messages.reverse(),
        'opp_user': opp_user,
        'dm_form': dm_form,
        'dm_room_id': dm_room_id,
    })

def send_message(request):
    success = True
    try:
        dm_text = request.POST.get('dm_text')
        dm_room_id = request.POST.get('dm_room_id')
        dm_room = DmRoom.objects.get(id=dm_room_id)

        dm_message = DmMessage(
            user=request.user,
            content=dm_text,
            dm_room=dm_room,
        )
        dm_message.save()

        dm_room.last_updated_at = datetime.datetime.now()
        dm_room.has_read_users.clear()
        dm_room.has_read_users.add(request.user)
        dm_room.save()
    except Exception as e:
        success = False
        print(e)

    context = {
        'success': success,
    }

    return JsonResponse(context)

# 最新の通知、DMがあるかどうかをJson形式で返す関数
@login_required
def check_new_noti_and_dm(request):
    new_notifications = Notification.objects.filter(user=request.user, be_read=False)
    new_dm_rooms = DmRoom.objects.filter(users=request.user).exclude(has_read_users=request.user)
    context = {
        'new_notifications': new_notifications.count(),
        'new_dm_rooms': new_dm_rooms.count(),
    }

    return JsonResponse(context)