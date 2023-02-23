import catalog.models

import core.models

from django.contrib import admin


class CatalogCommonAdmin(admin.ModelAdmin):
    list_display = (
        core.models.CatalogCommon.name.field.name,
        core.models.CatalogCommon.is_published.field.name,
    )
    list_editable = (core.models.CatalogCommon.is_published.field.name,)
    list_display_links = (core.models.CatalogCommon.name.field.name,)


admin.site.register(catalog.models.Category, CatalogCommonAdmin)
admin.site.register(catalog.models.Tag, CatalogCommonAdmin)


@admin.register(catalog.models.Item)
class ItemAdmin(CatalogCommonAdmin):
    filter_horizontal = (catalog.models.Item.tags.field.name,)
