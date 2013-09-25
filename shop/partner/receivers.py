from django.contrib.comments import get_model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify

Game = get_model('game', 'Game')
Partner = get_model('partner', 'Partner')

@receiver(post_save, sender=Game)
def create_update_partner(sender, **kwargs):
    game = kwargs['instance'] 
    name = '%s: %s' % (game.developer.name, game.name)
    code = slugify(name)
    if kwargs['created']:
        Partner.objects.create(game=game,
                               name=name,
                               code=code)
    else:
        Partner.objects.filter(game=game).update(name=name,
                                                 code=code)
