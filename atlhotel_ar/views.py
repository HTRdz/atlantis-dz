from django.shortcuts import render
from atlhotel.models import Contact, Hotel, Page, PicturePage, SousPage, PictureSousPage, TextSousPage, TextPage, Group, Reservation, RoomsPrice
from .models import TextPageAr, TextSousPageAr
from django.core.mail import send_mail, BadHeaderError
from atlantis.settings import EMAIL_HOST_USER
from django.contrib import messages
from datetime import datetime, timedelta, date

# Create your views here.
def main_ar(request):
	group = Group.objects.get(name ='Atlantis')
	hotel = Hotel.objects.all()
	page = Page.objects.get(page_name = "accueil group")
	groupImg = PicturePage.objects.get(page = page, etiquette = "group img")
	groupText = TextPageAr.objects.get(page = page)
	imgHotels = PicturePage.objects.filter(page = page, etiquette = 'hotels')
	hotels = zip(imgHotels, hotel)
	context = {
	'hotel':hotel,
	'group':group,
	'page':page,
	'groupImg':groupImg,
	'groupText':groupText,
	'hotels':hotels,
	}
	return render (request,'atlhotel_ar/hotels.html',context)


def home(request, hotel):
	
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")
	if h.coming_soon == False:
		page = Page.objects.get(hotel = h, page_name = "accueil hotel")
		picsBanner =  PicturePage.objects.filter(page = page, etiquette = "banner")
		videoDesc =  TextPage.objects.get(page = page, etiquette = "url youtube")
		textDesc = TextPageAr.objects.get(page = page, etiquette = "description hotel")
		picsCaroussel =  PicturePage.objects.filter(page = page, etiquette = "caroussel")
		textCarousel = TextPageAr.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"), etiquette = None)
		zipped = zip(picsCaroussel,textCarousel)
		#price of rooms
		price = RoomsPrice.objects.filter(hotel = h)

		picScroll = PicturePage.objects.get(page = page, etiquette = "banner scroll")
		textScroll = TextPageAr.objects.get(page = page, etiquette = "banner scroll")

		picCovid = PicturePage.objects.get(page = page, etiquette = "covid")
		textCovid = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "covid"))

		picinsta = PicturePage.objects.filter(page = Page.objects.get(hotel = h, page_name = "galerie"), etiquette = "galerie")
		#links to restaurants
		restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
		#footer
		hotels = Hotel.objects.all()
		#chambres:
		chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
		maps = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))
		d = date.today() + timedelta(days = 3)
		if d.day < 10:
			day = '0' + str(d.day)
		else:
			day = str(d.day)
		if d.month < 10:
			month = '0' + str(d.month)
		else:
			month = str(d.month)

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
Langue: Arabe.
"""
			#adresse mail de réception
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			#message de succès 
			messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")
		context = {
			'h':h,
			'page': page,
			'banners': picsBanner,
			'pics': picinsta, 
			'scroll': picScroll,
			'covid': picCovid,
			'restos': restos,
			'hotels':hotels,
			'textDesc':textDesc,
			'zipped':zipped,
			'textScroll':textScroll,
			'textCovid' :textCovid,
			'n':range(h.n_star),
			'videoDesc':videoDesc,
			'price':price,
			'chambres':chambres,
			'year':d.year,
			'month': month,
			'day' : day,
			'map':maps,
		}
		return render(request, 'atlhotel_ar/home.html',context)
	else:
		group = Group.objects.get(name = 'Atlantis')
		return render(request, 'atlhotel_ar/coming soon.html',{'group':group,})


def covid(request,hotel):
	
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")
	page = Page.objects.get(hotel = h, page_name = "covid") 
	pics = PicturePage.objects.filter(page = page)
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	text = TextPageAr.objects.get(page = page)
	context = {
		'h': h,
		'page': page,
		'pics': pics,
		'restos': restos,
		'hotels':hotels,
		'text': text,
	}
	return render(request,'atlhotel_ar/covid.html', context)


def rooms(request, hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")

	page = Page.objects.get(hotel = h, page_name = "chambres")
	chambres = SousPage.objects.filter(page = page)
	picsCaroussel = PicturePage.objects.filter(page = page, etiquette = "caroussel")

	picsChambres = PicturePage.objects.filter(page = page, etiquette = 'chambres')
	texts = TextPageAr.objects.filter(page = page, etiquette = None)

	zipped = zip(picsChambres, texts)

	price = RoomsPrice.objects.filter(hotel = h)
	hotels = Hotel.objects.all()
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	maps = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)

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
Langue: Arabe.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")

	context = {
	'h':h,
	'page':page,
	'chambres':chambres,
	'picsCaroussel':picsCaroussel,
	'zipped':zipped, 
	'restos': restos,
	'hotels':hotels,
	'price':price,
	'year':d.year,
	'month': month,
	'day' : day,
	'map':maps,
	}
	return render (request, 'atlhotel_ar/rooms.html',context)



def room_type(request, hotel, room_type):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")

	page = Page.objects.get(hotel = h, page_name = "chambres")

	sousPage = SousPage.objects.get(page = page, name_spage_en = room_type)

	price = RoomsPrice.objects.get(hotel = h, room_type = room_type)

	text = TextPageAr.objects.get(page = page, description = room_type)
	picsCarousel = PictureSousPage.objects.filter(SousPage = sousPage)

	#amenities=TextSousPageAr.objects.get(sous_page=sousPage, etiquette="Amenities")
	houseRules = TextPageAr.objects.filter(page = page,  etiquette = "house rules")
	annulation = TextPageAr.objects.get(page = page, etiquette = "Annulation")

	picsChambres = PicturePage.objects.filter(page = page, etiquette = 'chambres').exclude(desc = sousPage.name_spage)
	textChambres = TextPageAr.objects.filter(page = page, etiquette = None).exclude(description = room_type)
	zipped = zip(picsChambres,textChambres)

	prices = RoomsPrice.objects.filter(hotel = h).exclude(hotel = h, room_type = room_type)

	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel= h, page_name = "chambres"))
	maps = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
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
Langue: Arabe.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")


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
	'chambres':chambres,
	'year':d.year,
	'month': month,
	'day' : day,
	'map':maps,
	}
	return render (request, 'atlhotel_ar/room_type.html',context)


def gallery (request,hotel):
	h = Hotel.objects.get(name = hotel)
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")
	page= Page.objects.get(hotel = h, page_name = "galerie") 
	picCover = PicturePage.objects.get(page = page, etiquette = "cover")
	pics = PicturePage.objects.filter(page = page, etiquette = "galerie")
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel= h, page_name = "chambres"))
	maps = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
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
Langue: Arabe.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")
	context = {
	'h':h,
	'page':page,
	'pics': pics,
	'restos': restos,
	'hotels':hotels,
	'picCover': picCover,
	'chambres':chambres,
	'year':d.year,
	'month': month,
	'day' : day,
	'map':maps,
	}
	return render (request,'atlhotel_ar/gallery.html',context)


def resto (request, hotel, nom_resto):
	h = Hotel.objects.get(name = hotel)
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")
	page = Page.objects.get(hotel = h, page_name = "restaurants")
	restos = SousPage.objects.filter(page = page)
	sousPage = SousPage.objects.get(page = page, name_spage = nom_resto)
	pics = PictureSousPage.objects.filter(SousPage = sousPage, etiquette = "caroussel")
	menu= TextSousPageAr.objects.filter(sous_page = sousPage)
	hotels = Hotel.objects.all()
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel= h, page_name = "chambres"))
	maps = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)

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
Langue: Arabe.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")


	context = {
	'h':h,
	'page':page,
	'sousPage':sousPage,
	'restos': restos,
	'pics':pics,
	'hotels':hotels,
	'menu':menu,
	'chambres':chambres,
	'year':d.year,
	'month': month,
	'day' : day,
	'map':maps,
	}
	return render (request, 'atlhotel_ar/restaurant.html',context)


def event(request, hotel):
	h = Hotel.objects.get(name = hotel)
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")
	page = Page.objects.get(hotel = h, page_name = "evenements") 
	pics = PicturePage.objects.filter(page = page)
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	texts = TextPageAr.objects.filter(page = page)
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel= h, page_name = "chambres"))
	maps = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
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
Langue: Arabe.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")


	context = {
	'h':h,
	'page': page,
	'pics':pics,
	'restos': restos,
	'hotels':hotels,
	'texts':texts,
	'chambres':chambres,
	'year':d.year,
	'month': month,
	'day' : day,
	'map':maps,
	}
	return render(request,'atlhotel_ar/events.html', context)


def area(request,hotel, area):
	hotels = Hotel.objects.all()
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")
	h = Hotel.objects.get(name = hotel)
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	page = Page.objects.get(page_name = "Region")
	region =SousPage.objects.get(page = page,name_spage = area) 
	pics = PictureSousPage.objects.filter(SousPage = region, etiquette = "img")
	video = PictureSousPage.objects.get(SousPage = region, etiquette = "video")
	textVideo = TextSousPageAr.objects.get(sous_page = region, etiquette = "video")
	text = TextSousPageAr.objects.filter(sous_page = region, etiquette = None)
	zipped = zip(pics, text)
	banner = PictureSousPage.objects.get(SousPage = region, etiquette = "banner")
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel= h, page_name = "chambres"))
	maps = TextPageAr.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)
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
Langue: Arabe.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		#message de succès 
		messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")

	context = {
	'h':h,
	'page': page,
	'sousPage':region,
	'restos': restos,
	'hotels':hotels,
	'zipped':zipped,
	'video': video,
	'banner':banner,
	'textVideo':textVideo,
	'chambres':chambres,
	'year':d.year,
	'month': month,
	'day' : day,
	'map':maps,
	}
	return render (request,'atlhotel_ar/area.html', context)


def contact (request, hotel):
	h = Hotel.objects.get(name = hotel)
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("this hotel doesn't exist")
	page = Page.objects.get(hotel = h, page_name = "Contact")
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	maps = TextPageAr.objects.get(page = page)
	picCover = PicturePage.objects.get(page = page, etiquette = "cover")
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel= h, page_name = "chambres"))

	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)

	if request.method == 'POST':
		new_name = request.POST.get('name')
		new_mail = request.POST.get('mail_user')
		new_phone = request.POST.get('phone')
		new_subject = request.POST.get ('subject')
		new_request = request.POST.get('request')
		new_mail1 = request.POST.get("mail_r")
		new_phone1 = request.POST.get('phone_r')
		new_name1 = request.POST.get('name_r')
		new_room_type1 = request.POST.get('room_type')
		new_np1 = request.POST.get('np')
		new_date_arrival1 = request.POST.get('date_a')
		new_date_departure1 =  request.POST.get('date_d')
		
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
Langue: Arabe.
"""
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			messages.add_message(request, messages.INFO, "شكرا لك على تقديم طلب الحجز")
		else:
			Contact.objects.create(hotel = h,name = new_name, mail_user = new_mail, phone = new_phone, subject = new_subject, request = new_request, langue = "Ar")
			#mail reclamation contact:
			subject = 'Réclamation du site d\''  + str(h.group.name) + ' ' + str(h.name) + ' ' + str(new_name)
			message = f""" 
Contenu de la réclamation:

Hôtel : {str(h.group.name)} {str(h.name)}.
Nom complet: {new_name}.
Numéro de téléphone : {str(new_phone)}. 
Adresse électronique : {str(new_mail)}.
Requête: {new_subject}.
Message: {new_request}
Langue: Arabe.
"""
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			messages.add_message(request, messages.INFO, "شكرا لك على تقديم شكوى")	
	context = {
		'h':h,
		'page':page,
		'restos': restos,
		'hotels':hotels,
		'map':maps,
		'picCover': picCover,
		'chambres':chambres,
		'year':d.year,
		'month': month,
		'day' : day,
	}
	return render (request,'atlhotel_ar/contact.html',context)


def sitemap(request):
	pages = Page.objects.all()
	pages_ar=[]
	pages_use =[]
	for p in pages:
		pages_ar.append(str(p.page_name_en)+"_ar")
		pages_use.append(p)
	zipped = zip(pages_ar,pages_use)
	
	context = {
	'group':Group.objects.get(name="Atlantis"),
	'hotels': Hotel.objects.all(),
	'pages':pages,
	'zipped':zipped,
	'sps':SousPage.objects.all(),
	}
	return render (request,'atlhotel_ar/sitemap.html', context)


def icons(request):
	return render (request,'atlhotel_ar/icons index.html',{})