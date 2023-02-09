from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)


class FilmGenre(models.Model):
    title = models.CharField(max_length=255, verbose_name='название жанра')
    slug = models.SlugField()
    icon = models.ImageField(upload_to='media/icon_genre/',
                             blank=True,
                             null=True,
                             default='media/default/def_img.jpg',
                             verbose_name='изображение жанра')
    descr = models.TextField(blank=True, verbose_name='описание жанра')
    keyword = models.TextField(max_length=400, blank=True, verbose_name='meta запрос жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.pk}, {self.title}'


class Film(models.Model):
    autor = models.CharField(max_length=255, verbose_name='автор')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    short_story = models.TextField(verbose_name='краткое описание фильма')
    full_story = models.TextField(verbose_name='полное описание фильма')
    xfields = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, unique=True, verbose_name='название фильма')
    descr = models.TextField(verbose_name='описание')
    keywords = models.CharField(max_length=255, verbose_name='meta слова фильма')
    category = models.CharField(max_length=255, blank=True, null=True)
    alt_name = models.TextField()
    comm_num = models.IntegerField(null=True, blank=True)
    allow_comm = models.BooleanField(default=True, blank=True)
    allow_main = models.BooleanField(default=True, blank=True, null=True)
    approve = models.BooleanField(default=True, blank=True, null=True)
    fixed = models.BooleanField(default=False, blank=True, null=True)
    allow_br = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='media/icon_film/',
                              blank=True,
                              default='media/default/def_img.jpg',
                              verbose_name='Изображение для фильма')
    tags = models.CharField(verbose_name='теги', max_length=255)
    tags_table = TaggableManager(verbose_name='таблица тегов')
    metatitle = models.TextField(verbose_name='meta запрос фильма')
    kp_id_movie = models.IntegerField(unique=True, verbose_name='id кинопоиска')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('film_detail', kwargs={'move_pk': self.pk})

    def get_review(self):
        return self.re_films.filter(parent_isnull=True)


class BindingTable(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(FilmGenre, related_name='genre')
    move = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='move')

    def __str__(self):
        return f'{self.title}'


class RatingStar(models.Model):
    # Звезда рейтинга
    val = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], verbose_name='Звёзды')

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['-val']

    def __str__(self):
        return f'{self.val}'


class Rating(models.Model):
    # Рейтинг
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    star = models.ForeignKey(RatingStar,
                             on_delete=models.CASCADE,
                             related_name='stars',
                             verbose_name='рейтинг')
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name='films',
                             verbose_name='фильм')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.star} - {self.film}'


class Reviews(models.Model):
    # Комментарий
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Отзыв', max_length='6000')
    parent = models.ForeignKey('self',
                               verbose_name='Родитель',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    film = models.ForeignKey(Film,
                             on_delete=models.CASCADE,
                             related_name='re_films',
                             verbose_name='Фильм')
    user_like = models.ManyToManyField(User,
                                       related_name='reviews_liked',
                                       blank=True,
                                       verbose_name='Лайки')
    user_dislike = models.ManyToManyField(User,
                                          related_name='reviews_disliked',
                                          blank=True,
                                          verbose_name='Дизлайки')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f'{self.name} - {self.film}'
