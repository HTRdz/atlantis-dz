from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, sitemap, covid, rooms, room_type,gallery, resto,event, area, contact,icons
urlpatterns = [
	path('Home/<str:hotel>/',home, name='home_ar'),
    path('<str:hotel>/Covid', covid, name='covid_ar'),
	path('<str:hotel>/Rooms/',rooms, name='rooms_ar'),
	path('<str:hotel>/Rooms/<str:room_type>/', room_type, name='rooms_ar'),
    path('<str:hotel>/Gallery/',gallery,name='gallery_ar'),
    path('<str:hotel>/Restaurants/<str:nom_resto>', resto, name='food_ar'),
    path('<str:hotel>/Events/', event, name='events_ar'),
    path('<str:hotel>/Area/<str:area>', area, name='area_ar'),
    path('<str:hotel>/contact', contact, name='contact_ar'),
    path('Sitemap',sitemap, name="sitemap_ar"),
    path('icons/',icons, name="icons_ar"),



]