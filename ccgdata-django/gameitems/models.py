from django.db import models
import uuid

# Create your models here.

class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    links = models.JSONField(default=dict, blank=True)
    artist_name_slug = models.TextField(unique=True)
    def __str__(self):
        return self.artist_name_slug


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    links = models.JSONField(default=dict, blank=True)
    release_year = models.IntegerField(blank=True, null=True)
    release_month = models.IntegerField(blank=True, null=True)
    release_day = models.IntegerField(blank=True, null=True)
    original_release = models.DateField(blank=True, null=True)
    game_name_slug = models.TextField(unique=True)
    source_notes = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return self.game_name_slug


class Set(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    set_name_slug = models.TextField(unique=True)
    game = models.ForeignKey(Game, models.SET_NULL, blank=True, null=True)
    source_notes = models.JSONField(default=dict, blank=True)
    release_year = models.IntegerField(blank=True, null=True)
    release_month = models.IntegerField(blank=True, null=True)
    release_day = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.set_name_slug


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    game = models.ForeignKey(Game, models.SET_NULL, blank=True, null=True)
    set = models.ForeignKey(Set, models.SET_NULL, blank=True, null=True)
    artist = models.ForeignKey(Artist, models.SET_NULL, blank=True, null=True)
    attributes = models.JSONField(default=dict)
    images = models.JSONField(default=dict)
    source = models.TextField()
    source_notes = models.JSONField(default=dict, blank=True)
    functional_name = models.TextField()
    item_name_slug = models.TextField(unique=True)
    imaged = models.BooleanField(blank=True, null=True)
    documented = models.BooleanField(blank=True, null=True)
    def __str__(self):
        return self.item_name_slug


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    user_name_slug = models.TextField(unique=True)
    def __str__(self):
        return self.user_name_slug


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    owner_user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    is_inventory = models.BooleanField(default=False)
    collection_name_slug = models.TextField(unique=True)
    def __str__(self):
        return self.collection_name_slug


class CollectionItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    collection = models.ForeignKey(Collection, models.SET_NULL, blank=True, null=True)
    item = models.ForeignKey(Item, models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0)

