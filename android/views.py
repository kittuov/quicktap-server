from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def android_interface(request):
    return render(request, "android/android.html")
