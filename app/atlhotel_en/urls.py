from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import main_en,home, rooms, gallery, event, area, contact, covid, resto, room_type,sitemap,icons
urlpatterns = [
	path('Home/<str:hotel>/',home, name='home'),
	path('<str:hotel>/Rooms/',rooms, name='rooms'),
	path('<str:hotel>/Rooms/<str:room_type>/', room_type, name='rooms'),
    path('<str:hotel>/Gallery/',gallery,name='gallery'),
    path('<str:hotel>/Events/', event, name='events'),
    path('<str:hotel>/Area/<str:area>', area, name='area'),
    path('<str:hotel>/contact', contact, name='contact'),
    path('<str:hotel>/Covid', covid, name='covid'),
    path('<str:hotel>/Restaurants/<str:nom_resto>', resto, name='food'),
    path('Sitemap/',sitemap, name="sitemap_en"),
    path('icons/',icons, name="icons_en"),

]