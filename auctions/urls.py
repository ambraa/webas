from django.urls import path

from . import views
from django.conf import settings  
from django.conf.urls.static import static  

urlpatterns = [
    path("", views.index, name="index"),
    path("menu2", views.menu2, name="menu2"),
    path("uzsakymai", views.uzsakymai, name="uzsakymai"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addwatchlist/<str:product_id>", views.addwatchlist, name="addwatchlist"),
    path("watchlist_remove/<str:product_id>", views.watchlist_remove, name="watchlist_remove"),
    path("category/<str:category>", views.category, name="category"),
    path("<int:product_id>", views.listing, name="listing"),
    path("remove_listing/<str:product_id>", views.remove_listing, name="remove_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:  
#         urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 