from django.contrib import admin
from .models import  TextPageEn, TextSousPageEn
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.
admin.site.site_header = 'Platform d\'administration Atlantis'


class TextPageEnAtlantis(ImportExportActionModelAdmin):
	list_filter = ('page',)
	
	text_readonly_fields = ('page',)

	text_fieldsets = (
		('Page', {
			'fields' : ('page',)
			}),
		('Texte en anglais', {
			'fields' : ('title','texte',)
			}),
		)

	fieldsets = (
		('page', {
			'fields' : ('page',)
			}),
		('Texte en anglais', {
			'fields' : ('title','texte',)
			}),
		('Sa position dans la page', {
			'fields' : ('etiquette', 'description',)
			}),
		)


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.text_readonly_fields
		else:
			return super(TextPageEnAtlantis, self).get_readonly_fields(request, obj=obj)


	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.text_fieldsets
	 	else:
	 		return super(TextPageEnAtlantis, self).get_fieldsets(request, obj=obj)


class TextSousPageEnAtlantis(ImportExportActionModelAdmin):
	list_filter = ('sous_page',)

	text_readonly_fields = ('sous_page',)

	text_fieldsets = (
		('Sous page', {
			'fields' : ('sous_page',)
			}),
		('Texte en anglais', {
			'fields' : ('title','texte',)
			}),
		)
	fieldsets = (
		('Sous page', {
			'fields' : ('sous_page',)
			}),
		('Texte en anglais', {
			'fields' : ('title','texte',)
			}),
		('Sa position dans la page', {
			'fields' : ('etiquette', 'position',)
			}),
		)


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.text_readonly_fields
		else:
			return super(TextSousPageEnAtlantis, self).get_readonly_fields(request, obj=obj)


	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.text_fieldsets
	 	else:
	 		return super(TextSousPageEnAtlantis, self).get_fieldsets(request, obj=obj)


admin.site.register(TextPageEn, TextPageEnAtlantis)
admin.site.register(TextSousPageEn, TextSousPageEnAtlantis)
