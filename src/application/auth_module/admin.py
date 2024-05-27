from django.contrib import admin
from .models import Persons, Genders, Document_types, Resources,  Resources_roles, User


# Register your models here.
admin.site.register(Persons);
admin.site.register(Genders);
admin.site.register(Document_types);
admin.site.register(Resources);
admin.site.register(Resources_roles);
# admin.site.register(Roles);
admin.site.register(User);
# admin.site.register(User_roles);

