from django.db import models
# Create your models here.
class Group(models.Model):
	name = models.CharField(max_length=300, default="Atlantis", verbose_name="Nom du groupe")
	name_ar = models.CharField(max_length=300, default="اتلانتس" , verbose_name="Nom du groupe en arabe" )
	address= models.CharField(max_length=300,  verbose_name="Adresse")
	address_ar= models.CharField(max_length=300,null=True, blank=True, verbose_name="Adresse en arabe")
	address_en= models.CharField(max_length=300, null=True, blank=True, verbose_name="Adresse en anglais")
	tel= models.PositiveIntegerField(verbose_name="Numéro de téléphone")
	mail = models.EmailField(max_length=254, verbose_name="Adresse électronique")


	class Meta:
		verbose_name = 'Groupe'
		verbose_name_plural = 'Groupes'


	def __str__(self):
		return self.name

class Hotel(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="groupe")
	name = models.CharField(max_length=250, verbose_name="Nom de l'hôtel")
	name_ar = models.CharField(max_length=300, null=True, blank=True, verbose_name="Nom de l'hôtel en arabe" )
	adress= models.CharField(max_length=300, verbose_name="Adresse")
	adress_ar = models.CharField(max_length=300, null=True, blank=True, verbose_name="Adresse en arabe")
	adress_en = models.CharField(max_length=300, null=True, blank=True, verbose_name="Adresse en anglais")
	tel= models.PositiveIntegerField(verbose_name="Numéro de téléphone")
	mail = models.EmailField(max_length=254, verbose_name="Adresse électronique")
	region = models.CharField(max_length=200, null=True, blank=True,verbose_name="Nom de la région" ) 
	region_ar = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom de la région en arabe") 
	region_en = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom de la région en anglais") 
	n_star = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nombre d'étoiles de l'hôtel")
	coming_soon = models.BooleanField(default=False)
	logo = models.ImageField(null=True, blank=True)
	facebook_url = models.CharField(max_length=500, null=True, blank=True, verbose_name="Lien Facebook de l'hôtel")
	instagram_url = models.CharField(max_length=500, null=True, blank=True, verbose_name="Lien Instagram de l'hôtel")
	tripadvisor_url = models.CharField(max_length=500, null=True, blank=True, verbose_name="Lien Tripadvisor de l'hôtel")
	youtube_url = models.CharField(max_length=500, null=True, blank=True, verbose_name="Lien Youtube de l'hôtel")
	

	class Meta:
		verbose_name = 'Hôtel'
		verbose_name_plural = 'Hôtels'


	def __str__(self):
		return self.name

class Page (models.Model):
	 hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Hôtel")
	 page_name = models.CharField(max_length = 300, verbose_name="Nom de la page")
	 page_name_en = models.CharField(max_length = 300, null=True, blank=True, verbose_name="Nom de l'url la page en anglais")
	 page_name_fr = models.CharField(max_length = 300, null=True, blank=True, verbose_name="Nom de l'url de la page en français") 
	 page_name_ar = models.CharField(max_length = 300, null=True, blank=True, verbose_name="Nom de la page en arabe")  
	 def __str__(self):
	 	return self.page_name+" "+ str(self.hotel)

class SousPage(models.Model):
	name_spage = models.CharField(max_length = 300, null=True, blank=True, verbose_name="Nom de la sous page")
	name_spage_en = models.CharField(max_length = 300, null=True, blank=True, verbose_name="Nom de la sous page en anglais")
	name_spage_ar =  models.CharField(max_length = 300, null=True, blank=True, verbose_name="Nom de la sous page en arabe")
	page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)


	class Meta:
		verbose_name = 'Sous page'
		verbose_name_plural = 'Sous pages'


	def __str__(self):
		return str(self.page)+" "+ str(self.name_spage)
	

class PicturePage(models.Model):
	page = models.ForeignKey(Page, on_delete=models.CASCADE)
	pic = models.ImageField(verbose_name="Image")
	etiquette = models.CharField(max_length = 300)
	position = models.PositiveIntegerField()
	desc = models.CharField(max_length=300, blank= True, null=True, verbose_name="Description")

	class Meta:
		verbose_name = 'Image des pages'
		verbose_name_plural = 'Images des pages'


	def __str__(self):
		return str(self.page)+" "+self.etiquette + " p" + str(self.position)

class PictureSousPage(models.Model):
	SousPage = models.ForeignKey(SousPage, on_delete=models.CASCADE, null=True, verbose_name="Sous page")
	pic = models.ImageField(verbose_name="Image")
	etiquette = models.CharField(max_length = 300)
	position = models.CharField(max_length=300)


	class Meta:
		verbose_name = 'Image des sous pages'
		verbose_name_plural = 'Images des sous pages'


	def __str__(self):
		return str(self.SousPage) + " p" + str(self.position)

class TextSousPage(models.Model):
	sous_page = models.ForeignKey(SousPage, on_delete=models.CASCADE)
	Titre = models.CharField(max_length = 300)
	texte = models.TextField(blank= True, null= True)
	etiquette = models.CharField(max_length = 300,blank= True, null= True)
	position = models.PositiveIntegerField()


	class Meta:
		verbose_name = 'Texte des sous pages en français'
		verbose_name_plural = 'Textes des sous pages en français'


	def __str__(self):
		return str(self.sous_page)+" "+self.Titre+ " "+ str(self.position)


class TextPage(models.Model):
	page = models.ForeignKey(Page, on_delete=models.CASCADE)
	Titre = models.CharField(max_length = 300)
	texte = models.TextField(blank= True, null= True)
	position = models.PositiveIntegerField()
	etiquette = models.CharField(max_length = 300, null=True, blank=True)
	description = models.CharField(max_length = 300, null=True, blank=True)


	class Meta:
		verbose_name = 'Texte des pages en français'
		verbose_name_plural = 'Textes des pages en français'


	def __str__(self):
		return str(self.page)+" "+self.Titre+ " "+ str(self.position)

class Contact(models.Model):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name="Hôtel")
	name = models.CharField(max_length=300, verbose_name="Nom complet de la personne")
	mail_user = models.CharField(max_length=300, verbose_name="Adresse éléctronique")
	phone = models.PositiveIntegerField(verbose_name="Numéro de téléphone")
	subject = models.CharField(max_length=300, verbose_name="Objet de la réclamation")
	request = models.TextField(verbose_name="Message")
	langue = models.CharField(max_length=10, null=True, blank=True )


	def __str__(self):
		return self.name 

class Reservation(models.Model):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name="Hôtel")
	name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Nom complet de la personne")
	#last_name = models.CharField(max_length= 50)
	mail = models. EmailField(verbose_name="Adresse éléctronique")
	#address = models.CharField(max_length = 250)
	phone = models.PositiveIntegerField(verbose_name="Numéro de téléphone")
	langue = models.CharField(max_length = 20, null = True)
	np = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nombre de personnes")
	#n_children = models.PositiveIntegerField()
	#n_room = models.PositiveIntegerField()
	room_type = models.CharField( max_length = 100, null=True, blank=True, verbose_name="Type de chambre")
	#price = models.PositiveIntegerField()
	date_arrival = models.DateField(null=True, blank=True, verbose_name="Date d'arrivée")
	date_departure = models.DateField(null=True, blank=True, verbose_name="Date du départ")

	class Meta:
		verbose_name = 'Réservation'
		verbose_name_plural = 'Réservations'


	def __str__(self):
		return self.mail

class RoomsPrice (models.Model):
	hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE, verbose_name="Hôtel")
	room_type_fr = models.CharField(max_length = 100, null = True, blank = True, verbose_name="Type de chambre")
	room_type = models.CharField(max_length = 100, verbose_name="Type de chambre en anglais")
	room_price = models.PositiveIntegerField(verbose_name="Prix de la chambre")	
	

	class Meta:
		verbose_name = 'Prix des chambres'
		verbose_name_plural = 'Prix des chambres'


	def __str__(self):
		return str(self.hotel) + " " +str(self.room_type) + " " + str(self.room_price) 	