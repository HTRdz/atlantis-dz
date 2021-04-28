from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Hotel, Contact, Page, PicturePage, TextPage, Group, SousPage, PictureSousPage,TextSousPage, Reservation, RoomsPrice
from django.utils.translation import gettext_lazy as _
# Register your models here.

admin.site.site_header = 'Platform d\'administration Atlantis'


class GroupAtlantis(admin.ModelAdmin):
	group_readonly_fields =('name','name_ar',)

	fieldsets = (
        ('Information sur le groupe Atlantis', {
            'fields': ('name','name_ar','address', 'address_ar','address_en', 'tel', 'mail', )
        }),
        )


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.group_readonly_fields
		else:
			return super(GroupAtlantis, self).get_readonly_fields(request, obj=obj)

	
class HotelAtlantis(admin.ModelAdmin):
	list_filter = ('name',)
	fieldsets = (
        ('Information Hotel', {
            'fields': ('group','name','name_ar','adress', 'adress_ar','adress_en', 'tel', 'mail','n_star', )
        }),
        ('Region', {
            'fields': ('region', 'region_ar', 'region_en')
        }),
        ('Prochainement', {
            'fields': ('coming_soon',)
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
        ('Media sociaux',{
        	'fields': ('facebook_url', 'instagram_url', 'tripadvisor_url','youtube_url',)
        	}),
        )

	hotel_readonly_fields = ('group','name','name_ar', 'region', 'n_star','coming_soon','region', 'region_ar', 'region_en')

	hotel_fields = ('adress', 'adress_ar','adress_en', 'tel', 'mail', 'logo', 'facebook_url', 'instagram_url', 'tripadvisor_url','youtube_url',)

	hotel_fieldsets = (
        ('Information Hotel', {
            'fields': ('group','name','adress', 'adress_ar','adress_en', 'tel', 'mail','n_star', 'region')
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
        ('Media sociaux',{
        	'fields': ('facebook_url', 'instagram_url', 'tripadvisor_url','youtube_url',)
        	}),
        )


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.hotel_readonly_fields
		else:
			return super(HotelAtlantis, self).get_readonly_fields(request, obj=obj)


	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.hotel_fieldsets
	 	else:
	 		return super(HotelAtlantis, self).get_fieldsets(request, obj=obj)


class RoomsPriceAtlantis(admin.ModelAdmin):
	list_filter = ('hotel', 'room_type_fr',)
	price_readonly_fields = ('hotel','room_type_fr',)

	price_fieldsets = (
		('Prix des chambres:', {
            'fields': ('hotel','room_type_fr','room_price',)
        }),
        )

	fieldsets = (
        ('Prix des chambres:', {
            'fields': ('hotel', 'room_type_fr', 'room_type', 'room_price', )
        }),
        )


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.price_readonly_fields
		else:
			return super(RoomsPriceAtlantis, self).get_readonly_fields(request, obj=obj)


	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.price_fieldsets
	 	else:
	 		return super(RoomsPriceAtlantis, self).get_fieldsets(request, obj=obj)


class PicturePageAtlantis(admin.ModelAdmin):
	list_filter = ('page',)
	pic_readonly_fields = ('page',)

	pic_fieldsets = (
		('Page', {
			'fields' : ('page',)
			}),
		('Image', {
			'fields' : ('pic',)
			}),
		)

	fieldsets = (
		('Page', {
			'fields' : ('page',)
			}),
		('Image', {
			'fields' : ('pic',)
			}),
		('Sa position dans la page', {
			'fields' : ('etiquette', 'position', 'desc',)
			}),
		)


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.pic_readonly_fields
		else:
			return super(PicturePageAtlantis, self).get_readonly_fields(request, obj=obj)


	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.pic_fieldsets
	 	else:
	 		return super(PicturePageAtlantis, self).get_fieldsets(request, obj=obj)




class PictureSousPageAtlantis(admin.ModelAdmin):

	list_filter = ('SousPage',)

	pic_readonly_fields = ('SousPage',)

	pic_fieldsets = (
		('Sous page', {
			'fields' : ('SousPage',)
			}),
		('Image', {
			'fields' : ('pic',)
			}),
		)

	fieldsets = (
		('Sous page', {
			'fields' : ('SousPage',)
			}),
		('Image', {
			'fields' : ('pic',)
			}),
		('Sa position dans la page', {
			'fields' : ('etiquette', 'position',)
			}),
		)


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.pic_readonly_fields
		else:
			return super(PictureSousPageAtlantis, self).get_readonly_fields(request, obj=obj)


	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.pic_fieldsets
	 	else:
	 		return super(PictureSousPageAtlantis, self).get_fieldsets(request, obj=obj)


class TextPageAtlantis(admin.ModelAdmin):
	title = _('Texte de la page en français')
	parameter_name = 'page'
	list_filter = ('page',)

	text_readonly_fields = ('page',)

	text_fieldsets = (
		('Page', {
			'fields' : ('page',)
			}),
		('Texte', {
			'fields' : ('Titre','texte',)
			}),
		)

	fieldsets = (
		('page', {
			'fields' : ('page',)
			}),
		('Texte', {
			'fields' : ('Titre','texte',)
			}),
		('Sa position dans la page', {
			'fields' : ('etiquette', 'position', 'description',)
			}),
		)


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.text_readonly_fields
		else:
			return super(TextPageAtlantis, self).get_readonly_fields(request, obj=obj)


	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.text_fieldsets
	 	else:
	 		return super(TextPageAtlantis, self).get_fieldsets(request, obj=obj)
	def queryset(self, request, queryset):
		if request.user.groups.filter(name='admin-hotel').exists():
			return queryset.filter(page="Contact Bejaia")


class TextSousPageAtlantis(admin.ModelAdmin):
	list_filter = ('sous_page',)

	text_readonly_fields = ('sous_page',)

	text_fieldsets = (
		('Sous page', {
			'fields' : ('sous_page',)
			}),
		('Texte', {
			'fields' : ('Titre','texte',)
			}),
		)
	fieldsets = (
		('Sous page', {
			'fields' : ('sous_page',)
			}),
		('Texte', {
			'fields' : ('Titre','texte',)
			}),
		('Sa position dans la page', {
			'fields' : ('etiquette', 'position',)
			}),
		)


	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='admin-hotel').exists():
			return self.text_readonly_fields
		else:
			return super(TextSousPageAtlantis, self).get_readonly_fields(request, obj=obj)

	def get_fieldsets(self, request, obj=None):
	 	if request.user.groups.filter(name='admin-hotel').exists():
	 		return self.text_fieldsets
	 	else:
	 		return super(TextSousPageAtlantis, self).get_fieldsets(request, obj=obj)


admin.site.register(Group, GroupAtlantis)
admin.site.register(Hotel,HotelAtlantis)
admin.site.register(Page)
admin.site.register(SousPage)
admin.site.register(PicturePage, PicturePageAtlantis)
admin.site.register(TextPage,TextPageAtlantis)
admin.site.register(Contact)
admin.site.register(PictureSousPage, PictureSousPageAtlantis)
admin.site.register(TextSousPage, TextSousPageAtlantis)
admin.site.register(Reservation)
admin.site.register(RoomsPrice, RoomsPriceAtlantis)




