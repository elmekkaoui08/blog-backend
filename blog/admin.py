from django.contrib import admin
from .models import *

# @admin.register(CommonModel)
# class CommonModelAdmin(admin.ModelAdmin):
#    list_display = ('created_by', 'created_at', 'updated_by', 'updated_by')
#    ordering = ('created_by', 'updated_by')
#  search_fields = ('created_by', 'updated_by')


admin.site.register(Role)
admin.site.register(User)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Member)
admin.site.register(Author)
admin.site.register(Admin)
admin.site.register(Article)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)