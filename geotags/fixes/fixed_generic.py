from django.contrib.contenttypes import generic as real_generic


class GenericInlineModelAdmin(real_generic.GenericInlineModelAdmin):
    """
    Django 1.0 GenericStackedInline ignores max_num and exclude.
    See http://code.djangoproject.com/ticket/9122
    """
    def get_formset(self, request, obj=None, **kwargs):
        if self.declared_fieldsets:
            fields = real_generic.flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        defaults = {
            "ct_field": self.ct_field,
            "fk_field": self.ct_fk_field,
            "form": self.form,
            "formfield_callback": self.formfield_for_dbfield,
            "formset": self.formset,
            "extra": self.extra,
            "can_delete": True,
            "can_order": True,
            "fields": fields,
            "max_num": self.max_num,
            "exclude": self.exclude,
        }
        defaults.update(kwargs)
        return real_generic.generic_inlineformset_factory(self.model, **defaults)


class GenericStackedInline(GenericInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class GenericTabularInline(GenericInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'