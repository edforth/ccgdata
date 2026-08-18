from django.contrib import admin

# Register your models here.
from .models import Game, Set, Item

admin.site.register(Game)
admin.site.register(Set)
admin.site.register(Item)