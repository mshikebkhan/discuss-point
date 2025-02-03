from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin portal url config.
    path('admin/', admin.site.urls),

    # Core url config.
    path('', include(('core.urls', 'core'), namespace = 'core')),

    # Users url config.
    path('', include(('users.urls', 'users'), namespace = 'users')),

    # Discussion url config.
    path('', include(('discussion.urls', 'discussion'), namespace = 'discussion')),

    # Notifications url config.
    path('', include(('notifications.urls', 'notifications'), namespace = 'notifications')),

]

from django.contrib import admin

admin.site.site_header = 'DiscussPoint Adminstration'                    # default: "Django Administration"
admin.site.index_title = 'Site Administration'                 # default: "Site administration"
admin.site.site_title = "DiscussPoint"
