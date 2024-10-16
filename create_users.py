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

    my_id = CustomUser.objects.get(username="ニューアドミン").id

    # values_list メソッドを使うと、User オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    user_ids = CustomUser.objects.exclude(id=my_id).values_list("id", flat=True)

    talks = []
    for _ in range(len(user_ids)):
        sent_talk = Talk(
            sender_id=my_id,
            receiver_id = random.choice(user_ids),
            message = fakegen.text(),
        )
        received_talk = Talk(
            sender_id = random.choice(user_ids),
            receiver_id = my_id,
            message = fakegen.text()
        )
        talks.extend([sent])

    