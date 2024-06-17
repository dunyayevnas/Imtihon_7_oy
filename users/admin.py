from django.contrib import admin

from users.models import VerificationCodeModel, TeamModel, AccountModel

# Register your models here.
admin.site.register(VerificationCodeModel)
admin.site.register(TeamModel)




@admin.register(AccountModel)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('full_name',  'phone')
    search_fields = ('full_name',  'phone')
    list_filter = ('full_name', 'phone')