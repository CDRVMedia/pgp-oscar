from django.db.models.loading import get_model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

Game = get_model('game', 'Game')
Category = get_model('catalogue', 'Category')

@receiver(post_save, sender=Game)
def update_category_slugs(sender, **kwargs):
    Category.objects.filter(game=kwargs['instance']).save()