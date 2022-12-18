from django.contrib import admin

# Register your models here.
from users.models import User, IndividualUser, EntityUser

admin.site.register(User)
admin.site.register(IndividualUser)
admin.site.register(EntityUser)
