from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Contact, Hotel, Page, PicturePage, SousPage, PictureSousPage, TextSousPage, TextPage, Group, Reservation, RoomsPrice
from django.core.mail import send_mail, BadHeaderError
from atlantis.settings import EMAIL_HOST_USER
from django.contrib import messages
from datetime import datetime, timedelta, date

# Create your views here.


def main(request):
	# groupe atlantis:
	group = Group.objects.get(name = 'Atlantis')
	# tous les hotels de la base de données (ils sont tous affiliées au group Atlantis)
	hotel = Hotel.objects.all()
	# page d'accueil du groupe atlantis:
	page = Page.objects.get(page_name = "accueil group")
	# image et desription du groupe:
	groupImg= PicturePage.objects.get(page = page, etiquette = "group img")
	groupText = TextPage.objects.get(page = page, etiquette = "group desc")
	# images des hotels:
	imgHotels = PicturePage.objects.filter(page = page, etiquette = 'hotels')
	# tuple d'imageHotels et hotel
	hotels = zip(imgHotels, hotel)

	context = {
		'hotel':hotel,
		'group':group,
		'page':page,
		'groupImg':groupImg,
		'groupText':groupText,
		'hotels':hotels,
	}
	return render (request,'atlhotel/hotels.html',context)


def home(request, hotel):#Page d'accueil des hotels
	#Erreur 404:
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	# coming_soon == False => ne pas load la page de coming soon
	if h.coming_soon == False:
		page = Page.objects.get(hotel = h, page_name = "accueil hotel")
		# images du banner:
		picsBanner=  PicturePage.objects.filter(page = page, etiquette = "banner")
		# le liens de la video:
		videoDesc =  TextPage.objects.get(page = page, etiquette = "url youtube")
		# la description de l'hotel:
		textDesc = TextPage.objects.get(page = page, etiquette = "description hotel")
		# images + Dsecription des chambres:
		picsCaroussel =  PicturePage.objects.filter(page = page, etiquette = "caroussel")
		textCarousel = TextPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"), etiquette = None)
		# tuple des images et du texte
		zipped = zip(picsCaroussel,textCarousel)
		# prix des chambres
		price = RoomsPrice.objects.filter(hotel = h)
		# le Banner scrollable et son texte:
		picScroll = PicturePage.objects.get(page = page, etiquette = "banner scroll")
		textScroll = TextPage.objects.get(page = page, etiquette = "banner scroll")
		# Image et texte mesure sanitaire:
		picCovid = PicturePage.objects.get(page = page, etiquette = "covid")
		textCovid = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "covid"))
		# image avant le footer:
		picinsta = PicturePage.objects.filter(page = Page.objects.get(hotel = h, page_name = "galerie"), etiquette = "galerie")
		# liens restaurants du header:
		restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
		# les hotels dans le footer footer:
		hotels = Hotel.objects.all()
		# chambres:
		chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
		#texte contenant la balise de la map:
		maps = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))
		# date d'aujourd'hui + 3 jours pour le min de l'input type = date en html:
		d = date.today() + timedelta(days = 3)
		# rajouter un zéro avant le jour ou le moi si ils sont inferieurs à 10 pour l'html:
		if d.day < 10:
			day = '0' + str(d.day)
		else:
			day = str(d.day)
		if d.month < 10:
			month = '0' + str(d.month)
		else:
			month = str(d.month)
		# formulaire réservation
		if request.method == 'POST':
			# récupération des paramètres:
			new_mail = request.POST.get("mail_r") #e-mail
			new_phone = request.POST.get('phone_r') #numéro de téléphone
			new_name = request.POST.get('name_r') #nom et prénom
			new_room_type = request.POST.get('room_type') #type de chambres
			new_np = request.POST.get('np') #nombre de personnes
			new_date_arrival = request.POST.get('date_a') #date d'arrivée
			new_date_departure =  request.POST.get('date_d') #date du départ
			# creation d'une instance de la classe Reservation:
			r = Reservation.objects.create(hotel = h, name = new_name, mail = new_mail, phone = new_phone, langue = "Fr", np = new_np, room_type = new_room_type, date_arrival = new_date_arrival, date_departure = new_date_departure)
			# les paramètres du mail de réservation:
			subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
			message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Type de chambre : {new_room_type}.
Nombre de personnes : {new_np}.
Date d'arrivée : {new_date_arrival}.
Date du départ : {new_date_departure}.
Langue: français.
"""
			# adresse mail de réception
			recepient = 'webdev@htr-services-dz.com'
			# envoie du mail:
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			# message de succès 
			messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")

		context = {
			'h':h,
			'page': page,
			'banners': picsBanner,
			'scroll': picScroll,
			'covid': picCovid,
			'restos': restos,
			'hotels':hotels,
			'textDesc':textDesc,
			'zipped':zipped,
			'textScroll':textScroll,
			'textCovid' :textCovid,
			'ar': page.page_name_en + '_ar',
			'pics': picinsta, 
			'n':range(h.n_star),
			'videoDesc':videoDesc,
			'price':price,
			'chambres':chambres,
			'year':d.year,
			'month': month,
			'day' : day,
			'map':maps,
		}
		return render(request, 'atlhotel/main.html',context)
	#affichage de la page coming soon
	else:
		group = Group.objects.get(name = 'Atlantis')
		return render(request, 'atlhotel/coming soon.html',{'group':group,})


def chambres(request, hotel): # page d'accueil des chambres
	#erreur 404
	try:
		h=Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	# page d'accueil des chambres:
	page = Page.objects.get(hotel = h, page_name = "chambres")
	# les chambres:
	chambres = SousPage.objects.filter(page = page)
	# images des chambres dans le carrousel:
	picsCaroussel = PicturePage.objects.filter(page = page, etiquette = "caroussel")
	# images des chambres et leurs textes descriptifs:
	picsChambres = PicturePage.objects.filter(page = page, etiquette = 'chambres')
	texts = TextPage.objects.filter(page = page, etiquette = None)
	# tuple picsChambres et texts:
	zipped = zip(picsChambres, texts)
	# prix des chambres:
	price = RoomsPrice.objects.filter(hotel = h)
	# restaurants pour le header: 
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	# les hotels pour le footer:
	hotels = Hotel.objects.all()
	#texte contenant la balise de la map:
	maps = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))
	# rajouter un zéro avant le jour ou le moi si ils sont inferieurs à 10 pour l'html:
	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
	# le formulaire de réservation:
	if request.method == 'POST':
		#récupération des paramètres:
		new_mail = request.POST.get("mail_r")
		new_phone = request.POST.get('phone_r')
		new_name = request.POST.get('name_r')
		new_room_type = request.POST.get('room_type')
		new_np = request.POST.get('np')
		new_date_arrival = request.POST.get('date_a')
		new_date_departure =  request.POST.get('date_d')
		# creation d'une instance de la classe:
		r = Reservation.objects.create(hotel = h, name = new_name, mail = new_mail, phone = new_phone, langue = "Fr", np = new_np, room_type = new_room_type, date_arrival = new_date_arrival, date_departure = new_date_departure)
		# mail de réservation:
		subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
		message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Type de chambre : {new_room_type}.
Nombre de personnes : {new_np}.
Date d'arrivée : {new_date_arrival}.
Date du départ : {new_date_departure}.
Langue: français.
"""
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		# message de succès 
		messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")
	context = {
		'h':h,
		'page':page,
		'chambres':chambres,
		'picsCaroussel':picsCaroussel,
		'zipped':zipped, 
		'restos': restos,
		'hotels':hotels,
		'ar': page.page_name_en + '_ar',
		'price':price,
		'year':d.year,
		'month': month,
		'day' : day,
		'map':maps,
	}
	return render (request, 'atlhotel/chambres.html',context)

# page detail des chambres:
def chambre_details(request, hotel, type_chambre):
	# erreur 404:
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")

	#page d'accueil des chambres
	page = Page.objects.get(hotel = h, page_name = "chambres")
	#chambres:
	chambres = SousPage.objects.filter(page = page)
	# sous page de la chambre souhaitée
	sousPage = SousPage.objects.get(page = page, name_spage = type_chambre)
	# texte descriptif de la chambre:
	text = TextPage.objects.get(page = page, description = type_chambre)
	# prix de la chambre:
	price = RoomsPrice.objects.get(hotel = h, room_type_fr = type_chambre)
	#print(price)
	# images du carrousel de la chambre:
	picsCarousel = PictureSousPage.objects.filter(SousPage = sousPage)
	#images et descriptions des chambres a l'exclusion de celle qui est déjà affichée:
	picsChambres = PicturePage.objects.filter(page = page, etiquette = 'chambres').exclude(desc = type_chambre)
	textChambres = TextPage.objects.filter(page = page, etiquette = None).exclude(description = sousPage.name_spage)
	#tuple de picsChambres et textChambres
	zipped = zip(picsChambres,textChambres)
	#prix des chambres a l'exclusion de celle qui est déjà affichée:
	prices = RoomsPrice.objects.filter(hotel = h).exclude(hotel = h,room_type_fr = type_chambre)
	
	#amenties
	#amenities=TextSousPage.objects.get(sous_page=sousPage, etiquette="Amenities") #pour le moment statique
	#regles à respecter de l'hotel
	houseRules = TextPage.objects.filter(page = page,  etiquette = "house rules")
	#condition d'annulation
	annulation = TextPage.objects.get(page = page,  etiquette = "Annulation")
	#les restaurants du header:
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	#les hotels du footer:
	hotels = Hotel.objects.all()
	#texte contenant la balise de la map:
	maps = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
	# formulaire de réservation
	if request.method == 'POST':
		#récupération des paramètres:
		new_mail = request.POST.get("mail_r")
		new_phone = request.POST.get('phone_r')
		new_name = request.POST.get('name_r')
		new_room_type = request.POST.get('room_type')
		new_np = request.POST.get('np')
		new_date_arrival = request.POST.get('date_a')
		new_date_departure =  request.POST.get('date_d')
		# creation d'une instance de la classe:
		r = Reservation.objects.create(hotel = h, name = new_name, mail = new_mail, phone = new_phone, langue = "Fr", np = new_np, room_type = new_room_type, date_arrival = new_date_arrival, date_departure = new_date_departure)
		# mail de réservation:
		subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
		message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Type de chambre : {new_room_type}.
Nombre de personnes : {new_np}.
Date d'arrivée : {new_date_arrival}.
Date du départ : {new_date_departure}.
Langue: français.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")

	context = {
		'h':h,
		'page':page,
		'sousPage': sousPage,
		'picsCarousel': picsCarousel,
		'restos': restos,
		'hotels':hotels,
		'text':text,
		'hr':houseRules,
		'annul':annulation,
		'zipped':zipped,
		#'a':amenities,
		'price':price,
		'prices':prices,
		'ar': page.page_name_en + '_ar',
		'chambres' :chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map':maps,
	}
	return render (request, 'atlhotel/chambreD.html',context)


def gallery (request,hotel):
	#erreur 404:
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	#page de la galerie:
	page = Page.objects.get(hotel = h, page_name = "galerie")
	#chambres:
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	#image en tête de page:
	picCover = PicturePage.objects.get(page = page, etiquette = "cover") 
	#images de la galerie:
	pics = PicturePage.objects.filter(page = page, etiquette = "galerie")
	# restaurant du header:
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	# hotels du footer:
	hotels = Hotel.objects.all()
	#texte contenant la balise de la map:
	maps = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
	#formulaire de reservation
	if request.method == 'POST':
		#récupération des paramètres:
		new_mail = request.POST.get("mail_r")
		new_phone = request.POST.get('phone_r')
		new_name = request.POST.get('name_r')
		new_room_type = request.POST.get('room_type')
		new_np = request.POST.get('np')
		new_date_arrival = request.POST.get('date_a')
		new_date_departure =  request.POST.get('date_d')
		# creation d'une instance de la classe:
		r = Reservation.objects.create(hotel = h, name = new_name, mail = new_mail, phone = new_phone, langue = "Fr", np = new_np, room_type = new_room_type, date_arrival = new_date_arrival, date_departure = new_date_departure)
		#mail de réservation:
		subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
		message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Type de chambre : {new_room_type}.
Nombre de personnes : {new_np}.
Date d'arrivée : {new_date_arrival}.
Date du départ : {new_date_departure}.
Langue: français.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")
	context = {
		'h':h,
		'page':page,
		'pics': pics,
		'restos': restos,
		'hotels':hotels,
		'ar': page.page_name_en + '_ar',
		'picCover': picCover,
		'chambres':chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map':maps,
	}
	return render (request,'atlhotel/gallery.html',context)


def contact (request, hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	#page contact
	page = Page.objects.get(hotel = h, page_name = "Contact")
	#chambres:
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel= h, page_name = "chambres"))
	#restaurants du header:
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	#hotels du footer:
	hotels = Hotel.objects.all()
	#texte contenant la balise de la map:
	maps = TextPage.objects.get(page = page)
	#image en tête de page:
	picCover = PicturePage.objects.get(page = page, etiquette = "cover")

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
	#formulaire de réservation et de réclamation:
	if request.method == 'POST':
		#informations relatives aux réclamtions:
		new_mail = request.POST.get("mail_user") # e-mail
		new_phone = request.POST.get('phone') #numéro de téléphone
		new_name = request.POST.get('name') #nom et prénom
		new_subject = request.POST.get ('subject') #l'objet de la requete
		new_request = request.POST.get('request') #le message de réclamation
		#information relatives aux réservations:
		new_mail1 = request.POST.get("mail_r") #e-mail
		new_phone1 = request.POST.get('phone_r') #numéro de téléphone
		new_name1 = request.POST.get('name_r') #nom et prénom
		new_room_type1 = request.POST.get('room_type') #type de chambre
		new_np1 = request.POST.get('np') #nombre de personnes
		new_date_arrival1 = request.POST.get('date_a') #date d'arrivée
		new_date_departure1 =  request.POST.get('date_d') #date du départ
		# la réservation:
		if new_mail1 and new_phone1:
			r = Reservation.objects.create(hotel = h, name = new_name1, mail = new_mail1, phone = new_phone1, langue = "Fr", np = new_np1, room_type = new_room_type1, date_arrival = new_date_arrival1, date_departure = new_date_departure1)
			#mail de réservation:
			subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
			message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name1}.
Numéro de téléphone : {str(new_phone1)}. 
Adresse électronique : {str(new_mail1)}.
Type de chambre : {new_room_type1}.
Nombre de personnes : {new_np1}.
Date d'arrivée : {new_date_arrival1}.
Date du départ : {new_date_departure1}.
Langue: français.
"""
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")
		#la réclamation:
		else:
			Contact.objects.create(hotel = h,name = new_name, mail_user = new_mail, phone = new_phone, subject = new_subject, request = new_request, langue = "Fr")
			#mail reclamation contact:
			subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name) + ' ' + str(new_name)
			message = f""" 
Contenu de la réclamation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom complet: {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Requête: {new_subject}.
Message: {new_request}
Langue: français.
"""
			#adresse mail de réception
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			#message de succès 
			messages.add_message(request, messages.INFO, "Merci d'avoir effectué une réclamation")
	
	context = {
		'h':h,
		'page':page,
		'restos': restos,
		'hotels':hotels,
		'ar': page.page_name_en + '_ar',
		'map':maps,
		'picCover': picCover,
		'chambres': chambres,
		'year':d.year,
		'month': month,
		'day' : day,
	}
	return render (request,'atlhotel/contact.html',context)


def resto (request, hotel, nom_resto):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	# page des restaurants:
	page = Page.objects.get(hotel = h, page_name = "restaurants")
	# les chambres pour la réservation du header:
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	# les restaurants pour le header:
	restos = SousPage.objects.filter(page = page)
	# la page du restaurant souhaitée:
	sousPage = SousPage.objects.get(page = page, name_spage = nom_resto)
	# images du carrousel des platsdu restaurant:
	pics = PictureSousPage.objects.filter(SousPage = sousPage, etiquette = "caroussel")
	#le menu du restaurant:
	menu = TextSousPage.objects.filter(sous_page = sousPage)
	#pages des hotels pour le footer:
	hotels = Hotel.objects.all()
	#texte contenant la balise de la map:
	maps = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
	#les réservations:
	if request.method == 'POST':
		new_mail = request.POST.get("mail_r")
		new_phone = request.POST.get('phone_r')
		new_name = request.POST.get('name_r')
		new_room_type = request.POST.get('room_type')
		new_np = request.POST.get('np')
		new_date_arrival = request.POST.get('date_a')
		new_date_departure =  request.POST.get('date_d')
		# creation d'une instance de la classe:
		r = Reservation.objects.create(hotel = h, name = new_name, mail = new_mail, phone = new_phone, langue = "Fr", np = new_np, room_type = new_room_type, date_arrival = new_date_arrival, date_departure = new_date_departure)
		#envoie du mail de réservation:
		subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
		message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Type de chambre : {new_room_type}.
Nombre de personnes : {new_np}.
Date d'arrivée : {new_date_arrival}.
Date du départ : {new_date_departure}.
Langue: français.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")
	context = {
		'h':h,
		'page':page,
		'sousPage':sousPage,
		'restos': restos,
		'pics':pics,
		'hotels':hotels,
		'menu':menu,
		'ar': page.page_name_en + '_ar',
		'chambres':chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map':maps,
	}
	return render (request, 'atlhotel/Restaurant.html',context)


def event(request, hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	#page des evenements:
	page = Page.objects.get(hotel = h, page_name = "evenements")
	#images du caroussel de la page: 
	pics = PicturePage.objects.filter(page = page)
	#les restaurant du header:
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	#les hotels du footer:
	hotels = Hotel.objects.all()
	#texte de la page (la salle + sa capacité):
	texts = TextPage.objects.filter(page = page)
	#les chambres du header:
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	#texte contenant la balise de la map:
	maps = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))
	
	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
	#réservation:
	if request.method == 'POST':
		#récupération des paramètres:
		new_mail = request.POST.get("mail_r")
		new_phone = request.POST.get('phone_r')
		new_name = request.POST.get('name_r')
		new_room_type = request.POST.get('room_type')
		new_np = request.POST.get('np')
		new_date_arrival = request.POST.get('date_a')
		new_date_departure =  request.POST.get('date_d')
		# creation d'une instance de la classe:
		r = Reservation.objects.create(hotel = h, name = new_name, mail = new_mail, phone = new_phone, langue = "Fr", np = new_np, room_type = new_room_type, date_arrival = new_date_arrival, date_departure = new_date_departure)
		#mail de réservation:
		subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
		message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Type de chambre : {new_room_type}.
Nombre de personnes : {new_np}.
Date d'arrivée : {new_date_arrival}.
Date du départ : {new_date_departure}.
Langue: français.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")
	context = {
		'h':h,
		'page': page,
		'pics':pics,
		'restos': restos,
		'hotels':hotels,
		'texts':texts,
		'ar': page.page_name_en + '_ar',
		'chambres' : chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map':maps,
	}
	return render(request,'atlhotel/event.html', context)


def covid(request,hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	#page des mesures sanitaires:
	page= Page.objects.get(hotel = h, page_name = "covid")
	#images de la page: 
	pics = PicturePage.objects.filter(page = page)
	#les restaurants:
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	#hotels du footer:
	hotels = Hotel.objects.all()
	#texte de la page:
	text = TextPage.objects.get(page = page)

	context = {
		'h':h,
		'page': page,
		'pics':pics,
		'restos': restos,
		'hotels':hotels,
		'text':text,
		'ar': page.page_name_en + '_ar',
	}
	return render(request,'atlhotel/covid.html', context)


def region(request,hotel, region):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	# hotels du footer:	
	hotels = Hotel.objects.all()
	# les restaurants:
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	# page des région qui n'est affilié à aucun hotel vu qu'une région peut être commune a plusieurs hotels
	page = Page.objects.get(page_name = "Region")
	# la sous page de la région selon le str region indiqué dans le lien:
	region =SousPage.objects.get(page = page,name_spage = region) 
	# images de la pages:
	pics = PictureSousPage.objects.filter(SousPage = region, etiquette = "img")
	# texte associé aux images de la région:
	text = TextSousPage.objects.filter(sous_page = region, etiquette = None)
	zipped = zip(pics, text)
	# image qui sert de couverture à la vidéo:
	video = PictureSousPage.objects.get(SousPage = region, etiquette = "video")
	# texte associé à la vidéo:
	textVideo = TextSousPage.objects.get(sous_page = region, etiquette = "video")
	# image en tête de page:
	banner = PictureSousPage.objects.get(SousPage = region, etiquette = "banner")
	#les chambres:
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	#texte contenant la balise de la map:
	maps = TextPage.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
	# réservation:
	if request.method == 'POST':
		#récupération des paramètres:
		new_mail = request.POST.get("mail_r")
		new_phone = request.POST.get('phone_r')
		new_name = request.POST.get('name_r')
		new_room_type = request.POST.get('room_type')
		new_np = request.POST.get('np')
		new_date_arrival = request.POST.get('date_a')
		new_date_departure =  request.POST.get('date_d')
		# creation d'une instance de la classe:
		r = Reservation.objects.create(hotel = h, name = new_name, mail = new_mail, phone = new_phone, langue = "Fr", np = new_np, room_type = new_room_type, date_arrival = new_date_arrival, date_departure = new_date_departure)
		#mail de réservation:
		subject = 'Réservation du site d\'' + str(h.group.name) + ' ' + str(h.name)
		message = f""" 
Les informations personnelles de la personne ayant effectué une réservation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom et prénom : {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Type de chambre : {new_room_type}.
Nombre de personnes : {new_np}.
Date d'arrivée : {new_date_arrival}.
Date du départ : {new_date_departure}.
Langue: français.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "Merci d'avoir effectué une demande de réservation")
	context = {
		'h': h,
		'page': page,
		'sousPage': region,
		'restos': restos,
		'hotels': hotels,
		'zipped': zipped,
		'video':  video,
		'banner': banner,
		'textVideo': textVideo,
		'ar': page.page_name_en + '_ar',
		'chambres': chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map':maps,
	}
	return render (request,'atlhotel/region.html', context)


def sitemap(request):
	context = {
		'group' : Group.objects.get(name = "Atlantis"),
		'hotels' : Hotel.objects.all(),
		'ps': Page.objects.all(),
		'sps': SousPage.objects.all(),
	}
	return render (request,'atlhotel/sitemap.html', context)


def icons(request,hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("Cette hôtel n'existe pas")
	return render (request,'atlhotel/icons index.html',{'h':h,})