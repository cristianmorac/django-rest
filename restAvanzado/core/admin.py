from atexit import register
#from distutils import core
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

class UserAdmin(BaseUserAdmin):
    # ordenado por
    ordering = ['id']
    # Datos que se van a mostrar
    list_display = ['email','name']
    fieldsets = (
        (None, {"fields": ('email','password')}),
        (_('Personal Info'),{'fields':('name',)}),
        (
            _('Permissions'),
            {'fields':('is_active','is_staff','is_superuser')}
        ),
        (_('Important Dates'),{'fields':('last_login',)})
    )

    #agregando usuarios
    add_fieldsets=(
        (None,{
            #parametros
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )

# Registrar los modelos
admin.site.register(models.user,UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
