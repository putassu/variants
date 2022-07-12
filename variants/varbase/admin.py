from django.contrib import admin
from .models import Case, Variant, Alleles, Locus

admin.site.register(Case)
admin.site.register(Variant)
admin.site.register(Alleles)
admin.site.register(Locus)
