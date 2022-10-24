import json

from django.db import models

from users1c.models import Users1c


class RequestHeaders(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users1c, on_delete=models.CASCADE)
    http_user_agent = models.TextField()

    def __str__(self):
        return self.http_user_agent


def add_request_header(request):
    cu = Users1c.objects.filter(name=request.session['userLogged'].lower()).all().get()

    hua = request.META['HTTP_USER_AGENT']

    RequestHeaders.objects.create(user=cu, http_user_agent=hua)

    hual = hua.lower()

    return hual.find('android') + hual.find('ios') + hual.find('mobile') >= 0


