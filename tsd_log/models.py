import json

from django.db import models

from users1c.models import Users1c


class TsdLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return self.text


# def add_request_header(request):
#     cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()
#
#     hua = request.META['HTTP_USER_AGENT']
#
#     RequestHeaders.objects.create(user=cu, http_user_agent=hua)
#
#     hual = hua.lower()
#
#     return hual.find('android') + hual.find('ios') + hual.find('mobile') >= 0
#
#
