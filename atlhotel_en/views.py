from django.shortcuts import render
from django.http import HttpResponse
from atlhotel.models import Contact, Hotel, Page, PicturePage, SousPage, PictureSousPage, TextSousPage, TextPage, Group, Reservation, RoomsPrice
from .models import TextPageEn, TextSousPageEn
from django.core.mail import send_mail, BadHeaderError
from atlantis.settings import EMAIL_HOST_USER
from django.contrib import messages
from datetime import datetime, timedelta, date


# Create your views here.


def main_en (request):#the group page:
	#Atlantis group:
	group = Group.objects.get(name = 'Atlantis')
	#all the hotels of the database
	hotel = Hotel.objects.all()
	#the home page of the group:
	page = Page.objects.get(page_name = "accueil group")
	#image and description of the group
	groupImg= PicturePage.objects.get(page = page, etiquette = "group img")
	groupText = TextPageEn.objects.get(page = page)
	#images of the hotels:
	imgHotels = PicturePage.objects.filter(page = page, etiquette = 'hotels')
	#tuple of imgHotels and hotel
	hotels = zip(imgHotels, hotel)

	context = {
	'hotel':hotel,
	'group':group,
	'page':page,
	'groupImg':groupImg,
	'groupText':groupText,
	'hotels':hotels,
	}
	return render (request,'atlhotel_en/hotels.html',context)


def home(request, hotel):#Home page:
	#Error 404:
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	#coming_soon == False => don't load the coming soon page
	if h.coming_soon == False:
		page= Page.objects.get(hotel = h, page_name = "accueil hotel")
		#Banner images:
		picsBanner=  PicturePage.objects.filter(page = page, etiquette = "banner")
		#youtube video link:
		videoDesc =  TextPage.objects.get(page = page, etiquette = "url youtube")
		#description of the hotel:
		textDesc = TextPageEn.objects.get(page = page, etiquette = "description hotel")
		#rooms on the home page:
		picsCaroussel =  PicturePage.objects.filter(page = page, etiquette = "caroussel")
		textCarousel = TextPageEn.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"), etiquette = None)
		#tuple of picsCaroussel and textCarousel:
		zipped = zip(picsCaroussel,textCarousel)
		#prices of rooms:
		price = RoomsPrice.objects.filter(hotel = h)
		#image and text of the scrolling banner
		picScroll = PicturePage.objects.get(page = page, etiquette = "banner scroll")
		textScroll = TextPageEn.objects.get(page = page, etiquette = "banner scroll")
		#image and text of covid prevention:
		picCovid = PicturePage.objects.get(page = page, etiquette = "covid")
		textCovid = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "covid"))
		#images before th footer:
		picinsta = PicturePage.objects.filter(page = Page.objects.get(hotel = h, page_name = "galerie"), etiquette = "galerie")
		#restaurents for the header:
		restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
		#hotels for the footer
		hotels = Hotel.objects.all()
		#chambres:
		chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
		maps = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))
		
		d = date.today() + timedelta(days = 3)
		if d.day < 10:
			day = '0' + str(d.day)
		else:
			day = str(d.day)
		if d.month < 10:
			month = '0' + str(d.month)
		else:
			month = str(d.month)

		# booking form:
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
Langue: Anglais.
"""
			#adresse mail de réception
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			messages.add_message(request, messages.INFO, "Thank you for making a reservation request")			

		context = {
			'h':h,
			'page': page,
			'banners': picsBanner,
			'videoDesc':videoDesc,
			'scroll': picScroll,
			'covid': picCovid,
			'restos': restos,
			'hotels':hotels,
			'textDesc':textDesc,
			'zipped':zipped,
			'textScroll':textScroll,
			'textCovid' :textCovid,
			'ar': page.page_name_en + '_ar',
			'n':range(h.n_star),
			'pics': picinsta,
			'price':price,
			'chambres' :chambres,
			'year':d.year,
			'month': month,
			'day' : day,
			'map': maps,
		}
		return render(request, 'atlhotel_en/home.html',context)
	#load the coming soon page:
	else:
		group = Group.objects.get(name = 'Atlantis')
		return render(request, 'atlhotel_en/coming soon.html',{'group':group,})


def rooms(request, hotel): #rooms page:
	#error 404:
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")

	page = Page.objects.get(hotel = h, page_name = "chambres")

	chambres = SousPage.objects.filter(page = page)

	picsCaroussel = PicturePage.objects.filter(page = page, etiquette = "caroussel")
	
	picsRooms = PicturePage.objects.filter(page = page, etiquette = 'chambres')
	texts = TextPageEn.objects.filter(page = page, etiquette = None)
	zipped = zip(picsRooms, texts)

	price = RoomsPrice.objects.filter(hotel = h)

	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	maps = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

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
Langue: Anglais.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		messages.add_message(request, messages.INFO, "Thank you for making a reservation request")

	context = {
		'h':h,
		'page': page,
		'chambres':chambres,
		'picsCaroussel':picsCaroussel,
		'restos': restos,
		'hotels':hotels,
		'zipped': zipped,
		'ar': page.page_name_en + '_ar',
		'price':price,
		'year':d.year,
		'month': month,
		'day' : day,
		'map': maps,
	}
	return render (request, 'atlhotel_en/Rooms.html',context)

def room_type(request, hotel,room_type):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	d = date.today() + timedelta(days = 3)
	if d.day < 10:
		day = '0' + str(d.day)
	else:
		day = str(d.day)
	if d.month < 10:
		month = '0' + str(d.month)
	else:
		month = str(d.month)

	page = Page.objects.get(hotel = h, page_name = "chambres")

	sousPage = SousPage.objects.get(page = page,name_spage_en = room_type)
	#chambres:
	chambres = SousPage.objects.filter(page = page)

	text = TextPageEn.objects.get(page = page, description = room_type)

	price = RoomsPrice.objects.get(hotel = h, room_type = room_type)

	picsCarousel = PictureSousPage.objects.filter(SousPage = sousPage)
	
	#amenities=TextSousPageEn.objects.get(sous_page=sousPage, etiquette="Amenities")
	houseRules = TextPageEn.objects.filter(page = page,  etiquette = "house rules")
	annulation = TextPageEn.objects.get(page = page,  etiquette = "Annulation")
	
	picsChambres = PicturePage.objects.filter(page = page, etiquette = 'chambres').exclude(desc = sousPage.name_spage)
	textChambres = TextPageEn.objects.filter(page = page, etiquette=None).exclude(description = sousPage.name_spage_en)
	zipped = zip(picsChambres,textChambres)
	prices = RoomsPrice.objects.filter(hotel = h).exclude(hotel = h,room_type = room_type)
	
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	maps = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

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
Langue: Anglais.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		messages.add_message(request, messages.INFO, "Thank you for making a reservation request")

	context = {
		'h':h,
		'page': page,
		'sousPage': sousPage,
		'picsCarousel': picsCarousel,
		'restos': restos,
		'hotels':hotels,
		'text':text,
		'hr':houseRules,
		'annul':annulation,
		'zipped':zipped,
		#'a':amenities,
		'ar': page.page_name_en + '_ar',
		'price':price,
		'prices':prices,
		'chambres' :chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map': maps,
	}
	return render (request, 'atlhotel_en/room_type.html',context)

def gallery (request,hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	page = Page.objects.get(hotel = h, page_name = "galerie") 
	#chambres:
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	pics = PicturePage.objects.filter(page = page, etiquette = "galerie")
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	picCover = PicturePage.objects.get(page = page, etiquette = "cover")
	maps = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

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
Langue: Anglais.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		messages.add_message(request, messages.INFO, "Thank you for making a reservation request")


	context = {
		'h':h,
		'page': page,
		'pics': pics,
		'restos': restos,
		'hotels':hotels,
		'ar': page.page_name_en + '_ar',
		'picCover': picCover,
		'chambres':chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map': maps,
	}
	return render (request,'atlhotel_en/gallery.html',context)

def event(request, hotel):
	try:
		h=Hotel.objects.get(name= hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	page= Page.objects.get(hotel=h, page_name="evenements") 
	pics = PicturePage.objects.filter(page=page)
	restos = SousPage.objects.filter(page=Page.objects.get(hotel=h, page_name="restaurants"))
	hotels = Hotel.objects.all()
	texts = TextPageEn.objects.filter(page=page)
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	maps = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

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
Langue: Anglais.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		messages.add_message(request, messages.INFO, "Thank you for making a reservation request")

	context = {
		'h':h,
		'page': page,
		'pics':pics,
		'restos': restos,
		'hotels':hotels,
		'texts':texts,
		'ar': page.page_name_en + '_ar',
		'chambres':chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map': maps,
	}
	return render(request,'atlhotel_en/events.html', context)

def area(request,hotel, area):
	hotels = Hotel.objects.all()
	try:
		h=Hotel.objects.get(name= hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	restos = SousPage.objects.filter(page=Page.objects.get(hotel=h, page_name="restaurants"))
	page = Page.objects.get(page_name="Region")
	region =SousPage.objects.get(page=page,name_spage_en=area) 
	pics = PictureSousPage.objects.filter(SousPage=region, etiquette="img")
	video = PictureSousPage.objects.get(SousPage=region, etiquette="video")
	textVideo = TextSousPageEn.objects.get(sous_page=region, etiquette="video")
	text = TextSousPageEn.objects.filter(sous_page=region, etiquette=None)
	zipped = zip(pics, text)
	banner = PictureSousPage.objects.get(SousPage=region, etiquette="banner")
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	maps = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

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
Langue: Anglais.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		messages.add_message(request, messages.INFO, "Thank you for making a reservation request")

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
		'ar': page.page_name_en + '_ar',
		'chambres':chambres,
		'year':d.year,
		'month': month,
		'day' : day,
		'map': maps,
	}
	return render (request,'atlhotel_en/area.html', context)

def contact (request, hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	page = Page.objects.get(hotel = h, page_name = "Contact")
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	maps = TextPageEn.objects.get(page = page)
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

	#chambres:
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
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
Langue: Anglais.
"""
			#adresse mail de réception
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			messages.add_message(request, messages.INFO, "Thank you for making a reservation request")
		else:
			Contact.objects.create(hotel = h,name = new_name, mail_user = new_mail, phone = new_phone, subject = new_subject, request = new_request, langue = "En")
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
Langue: Anglais.
"""
			recepient = 'webdev@htr-services-dz.com'
			send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
			messages.add_message(request, messages.INFO, "Thank you for making a complaint")
	context = {
		'h':h,
		'page': page,
		'restos': restos,
		'hotels':hotels,
		'ar': page.page_name_en + '_ar',
		'map': maps,
		'picCover': picCover,
		'chambres':chambres,
		'year':d.year,
		'month': month,
		'day' : day,
	}
	return render (request,'atlhotel_en/contact.html',context)

def covid(request, hotel):
	try:
		h = Hotel.objects.get(name = hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	page = Page.objects.get(hotel = h, page_name = "covid") 
	pics = PicturePage.objects.filter(page = page)
	restos = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "restaurants"))
	hotels = Hotel.objects.all()
	text = TextPageEn.objects.get(page = page)
	context = {
		'h':h,
		'page': page,
		'pics':pics,
		'restos': restos,
		'hotels':hotels,
		'text':text,
		'ar': page.page_name_en + '_ar',
	}
	return render(request,'atlhotel_en/covid.html', context)

def resto (request, hotel, nom_resto):
	try:
		h=Hotel.objects.get(name= hotel)
	except Hotel.DoesNotExist:
		raise Http404("This hotel doesn't exist")
	page= Page.objects.get(hotel=h, page_name="restaurants")
	restos = SousPage.objects.filter(page=page)
	sousPage = SousPage.objects.get(page=page, name_spage=nom_resto)
	pics = PictureSousPage.objects.filter(SousPage=sousPage, etiquette="caroussel")
	menu= TextSousPageEn.objects.filter(sous_page=sousPage)
	hotels = Hotel.objects.all()
	chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
	maps = TextPageEn.objects.get(page = Page.objects.get(hotel = h, page_name = "Contact"))

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
		new_name = request.POST.get('name_r')
		new_mail = request.POST.get("mail_r")
		new_phone = request.POST.get('phone_r')
		new_room_type = request.POST.get('room_type')
		new_np = request.POST.get('np')
		new_date_arrival = request.POST.get('date_a')
		new_date_departure =  request.POST.get('date_d')
		#chambres:
		chambres = SousPage.objects.filter(page = Page.objects.get(hotel = h, page_name = "chambres"))
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
Langue: Anglais.
"""
		#adresse mail de réception
		recepient = 'webdev@htr-services-dz.com'
		send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		messages.add_message(request, messages.INFO, "Thank you for making a reservation request")
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
		'map': maps,
	}
	return render (request, 'atlhotel_en/restaurant.html',context)
def sitemap(request):

	context = {
	'group':Group.objects.get(name="Atlantis"),
	'hotels' :Hotel.objects.all(),
	'ps': Page.objects.all(),
	'sps':SousPage.objects.all(),
	}
	return render (request,'atlhotel_en/sitemap.html', context)
def icons(request):
	# try:
	# 	h=Hotel.objects.get(name= hotel)
	# except Hotel.DoesNotExist:
	# 	raise Http404("This hotel doesn't exist")
	return render (request,'atlhotel_en/icons index.html',{})