
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
import re
class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        exclued_path = ["user/login/", "user/logout/"]

        url_path = request.path
        for each in exclued_path:
            if 'user' in url_path:
                return

        try:
            if request.session['is_login']:
                return
        except:
            return JsonResponse({'redirectUrl':""})

        if request.session:
            pass
