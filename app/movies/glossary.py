from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TypeFilmwork(TextChoices):
    """Тип кинопроизведения"""

    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV_show')


class RolePerson(TextChoices):
    """Роль в кинопроизведении"""

    ACTOR = 'actor', _('Actor')
    WRITER = 'writer', _('Writer')
    DIRECTOR = 'director', _('Director')
