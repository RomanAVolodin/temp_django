import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.glossary import TypeFilmwork, RolePerson


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = ('film_work', 'genre')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'), unique=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Участник фильма'
        verbose_name_plural = 'Участники фильмов'

    def __str__(self) -> str:
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=RolePerson.choices, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = ('film_work', 'person', 'role')


class Filmwork(UUIDMixin, TimeStampedMixin):
    type = models.TextField(_('type'), choices=TypeFilmwork.choices)
    title = models.TextField(_('title'))
    creation_date = models.DateField(_('creation_date'), blank=True)
    rating = models.FloatField(
        _('rating'), blank=True,
        validators=[MinValueValidator(0, 'Min rating is 0!'),
                    MaxValueValidator(100.0, 'Max rating is 100.0!')])
    description = models.TextField(_('description'), blank=True)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title
