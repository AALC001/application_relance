from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.conf import settings

class IsCC:

    def __init__(self, get_response):
        self.get_response = get_response

    def is_only_staff(self, request:HttpRequest) -> bool:
        return request.user.is_staff and not request.user.is_admin and not request.user.is_super

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self.is_only_staff(request) and request.path_info == settings.DASHBOARD_URL:
            return redirect(settings.CC_LOGIN_URL)


class IsSuper:

    def __init__(self, get_response):
        self.get_response = get_response

    def is_super(self, request:HttpRequest) -> bool:
        return request.user.is_staff and request.user.is_admin and request.user.is_super

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self.is_super(request) and request.path_info == settings.DASHBOARD_URL:
            return redirect(settings.SUPER_LOGIN_URL)