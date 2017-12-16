from django.contrib import admin
from sv.models import Trainer, TSV, Report, Latest, Nonreddit
# Register your models here.


class TSVInline(admin.TabularInline):
    model = TSV


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('username', 'flair_class', 'flair_text', 'activity')
    search_fields = ('username',)
    inlines = [TSVInline,]


class TSVAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'tsv', 'gen', 'sub_id', 'completed', 'created', 'archived', 'last_seen', 'pending')
    search_fields = ('tsv',)
    actions = ['make_archived']

    def make_archived(modeladmin, request, queryset):
        queryset.update(completed=True, archived=True)
    make_archived.short_description = 'Mark selected TSVs as archived'


class NonredditAdmin(admin.ModelAdmin):
    list_display = ('tsv', 'username', 'ign', 'url', 'fc', 'timestamp', 'language', 'source')
    search_fields = ('username', 'tsv', 'ign', 'fc')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('url', 'status', 'handled', 'info', 'created')
    search_fields = ('info',)
    actions = ['make_handled']

    def make_handled(modeladmin, request, queryset):
        queryset.update(handled=True)
    make_handled.short_description = 'Mark selected reports as handled'


admin.site.register(Trainer, TrainerAdmin)
admin.site.register(TSV, TSVAdmin)
admin.site.register(Nonreddit, NonredditAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Latest)
