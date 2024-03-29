from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

import catalog.models
import core.models


class CatalogCommonAdmin(admin.ModelAdmin):
    list_display = (
        core.models.CatalogCommon.name.field.name,
        core.models.CatalogCommon.is_published.field.name,
    )
    list_editable = (core.models.CatalogCommon.is_published.field.name,)
    list_display_links = (core.models.CatalogCommon.name.field.name,)


admin.site.register(catalog.models.Category, CatalogCommonAdmin)
admin.site.register(catalog.models.Tag, CatalogCommonAdmin)
admin.site.register(catalog.models.Preview)
admin.site.register(catalog.models.Gallery)


class InlinePreview(AdminImageMixin, admin.TabularInline):
    model = catalog.models.Preview


class InlineGallery(AdminImageMixin, admin.TabularInline):
    model = catalog.models.Gallery


@admin.register(catalog.models.Item)
class ItemAdmin(CatalogCommonAdmin):
    list_display = (
        core.models.CatalogCommon.name.field.name,
        core.models.CatalogCommon.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
        catalog.models.Item.image_tmb,
    )
    list_editable = (
        core.models.CatalogCommon.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = [InlinePreview, InlineGallery]
