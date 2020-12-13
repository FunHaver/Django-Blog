from django.contrib import admin

from .models import Author, Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Heading',
            {'fields': 
                ['post_title', 'author']
            }
        ), 
        ('Publish Date & URL',
            {'fields':
                ['pub_date', 'post_url']
            }
        ),
        ('Post Body',
            {'fields':
                ['post_body']
            }
        ),
    ]

    list_display = ('post_title', 'author', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'author__last_name']
    search_fields = ['post_title']
    list_per_page = 30

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
