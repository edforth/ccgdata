from django.contrib import admin

# Register your models here.
from .models import Game, Set, Item, User, Collection, CollectionItem, Artist

admin.site.register(Game)
admin.site.register(Set)
admin.site.register(Item)
admin.site.register(User)
admin.site.register(Collection)
admin.site.register(CollectionItem)
admin.site.register(Artist)