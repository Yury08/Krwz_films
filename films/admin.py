from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    FilmGenre,
    Film,
    BindingTable,
    RatingStar,
    Rating,
    Reviews
)



@admin.register(FilmGenre)
class AdminFilmGenre(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'icon', 'descr', 'keyword')
    list_display_links = ('title',)
    readonly_fields = ('get_icon',)
    prepopulated_fields = {'slug': ('title',)}

    def get_icon(self, obj):
        return mark_safe(f'<img src="{obj.icon.url}" width="200" height="300"/>')


class InlinesReviews(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'text')


@admin.register(Film)
class AdminFilm(admin.ModelAdmin):
    list_display = ('id', 'alt_name', 'autor', 'short_story',
                    'date', 'image', 'full_story',
                    'title', 'descr', 'keywords',
                    'tags', 'tags_table', 'metatitle', 'allow_main', 'allow_comm', 'fixed', 'kp_id_movie')
    list_filter = ('category',)
    search_fields = ('title', 'category__title')
    inlines = [InlinesReviews]
    prepopulated_fields = {'tags': ('tags_table', )}
    list_editable = ('allow_main', 'allow_comm', 'fixed')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="150" height="150"/>')


@admin.register(Reviews)
class AdminReview(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'film')
    readonly_fields = ('name',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'user', 'film',)


admin.site.register(RatingStar)

admin.site.register(BindingTable)
