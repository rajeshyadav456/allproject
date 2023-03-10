from typing import Dict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.atms.models import Form


def create_form_schema(form_name: str, schema: Dict):
    if Form.objects.filter(name=form_name).exists():
        raise serializers.ValidationError(_("Form with same name alreday exists."))

    form = Form.objects.create(name=form_name, schema=schema)

    return form


def update_form_detail(form: Form, data: Dict):
    update_fields = []
    for field, value in data.items():
        setattr(form, field, value)
        update_fields.append(field)

    if update_fields:
        form.save(update_fields=update_fields)

    return form


def deactivate_form(form: Form):
    Form.objects.filter(id=form.id).delete()
