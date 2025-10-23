from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import Notification

def index(request):
    return render(request, 'authentication/login.html')



def dashboard(request):
    unread_notification = Notification.objects.filter(user = request.user , is_read = False)
    unread_notification_count = unread_notification.count()

    context = {
        'unread_notification': unread_notification,
        'unread_notification_count': unread_notification_count,
    }
    return render(request, 'students/student-dashboard.html' ,context)

def mark_notification_as_read(request):
    if request.method == 'POST':
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden("Invalid request method.")


def clear_all_notification(request):
    if request.method == 'POST':
        notifications = Notification.objects.filter(user=request.user)
        notifications.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden("Invalid request method.")

def index_view(request):
    return render(request ,'Home/index.html')

