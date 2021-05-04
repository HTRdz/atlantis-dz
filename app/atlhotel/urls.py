from django.urls import path
from atlhotel.views import home,icons,chambres,main,chambre_details,gallery,contact, resto, region, event, covid, sitemap
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<str:hotel>/',home,name='hotel'),
    path('<str:hotel>/Chambres',chambres,name='chambre'),
    path('<str:hotel>/Chambres/<str:type_chambre>',chambre_details,name='chambre'),
    path('<str:hotel>/Galerie',gallery,name='galerie'),
    path('<str:hotel>/contact', contact, name='contacte'),
    path('<str:hotel>/Restaurants/<str:nom_resto>', resto, name='restaurants'),
    path('<str:hotel>/Region/<str:region>', region, name='region'),
    path('<str:hotel>/Evenements', event, name='evenements'),
    path('<str:hotel>/Covid', covid, name='covid_fr'),
    path('Sitemap/', sitemap, name='sitemap'),
    path('<str:hotel>/Icons/',icons,name="icons"),


]