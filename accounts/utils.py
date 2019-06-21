from django.contrib.auth import get_user_model


def get_or_create_user(requested_user_name, get_id_only=False):
    user = get_user_model().objects.get_or_create(username=requested_user_name)
    if get_id_only:
        return user[0].pk
    else:
        return user


def dummy_deleted_user(get_id_only=True):
    return get_or_create_user('deleted', get_id_only)


def default_user(get_id_only=True):
    return get_or_create_user('deleted', get_id_only)


def guest_account(get_id_only=True):
    return get_or_create_user('guest', get_id_only)
