from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import post_save


class ProfileInLine(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInLine]


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

