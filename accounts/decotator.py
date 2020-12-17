from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def supplier_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/accounts/login/supplier'):
    # 出品者のみがアクセスできるようにするためのデコレーター

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_supplier,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator