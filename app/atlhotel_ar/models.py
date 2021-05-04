from django.db import models
from atlhotel.models import Hotel,Page, SousPage
# Create your models here.


class TextPageAr(models.Model):
	page = models.ForeignKey(Page, on_delete=models.CASCADE)
	title = models.CharField(max_length = 300)
	texte = models.TextField(blank= True, null= True)
	etiquette = models.CharField(max_length = 300, null=True, blank=True)
	description = models.CharField(max_length = 300, null=True, blank=True)

	class Meta:
		verbose_name = 'Texte des pages en arabe'
		verbose_name_plural = 'Textes des pages en arabe'


	def __str__(self):
		return str(self.page)+" "+self.title


class TextSousPageAr(models.Model):
	sous_page = models.ForeignKey(SousPage, on_delete=models.CASCADE)
	title = models.CharField(max_length = 300)
	texte = models.TextField(blank= True, null= True)
	etiquette = models.CharField(max_length = 300,blank= True, null= True)
	position = models.PositiveIntegerField(null=True, blank=True)

	class Meta:
		verbose_name = 'Texte des sous pages en arabe'
		verbose_name_plural = 'Textes des sous pages en arabe'


	def __str__(self):
		return str(self.sous_page)+" "+self.title