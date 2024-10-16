import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings.dev")
django.setup()

from myapp.models import Talk, CustomUser

fakegen = Faker(["ja_JP"])

def create_users(n):
    '''
    ダミーのユーザーとチャットの文章を作る。
    n: 作成するユーザーの人数
    '''

    users = [
        CustomUser(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    CustomUser.objects.bulk_create(users, ignore_conflicts=True)

    