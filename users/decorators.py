from django.contrib.auth.decorators import user_passes_test

@user_passes_test
def group_required(group_name, url):
    def in_group(user):
        return user.groups.filter(name=group_name).exists() or user.is_superuser
    return user_passes_test(in_group, login_url=url)
