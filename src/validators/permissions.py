from django.contrib.auth.decorators import user_passes_test


def group_required(*group_names):
    """ Grupos, checar si pertenece a grupo """

    def check(user):
        if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
            return True
        else:
            return False
    
    return user_passes_test(check, login_url='/prohibido/')