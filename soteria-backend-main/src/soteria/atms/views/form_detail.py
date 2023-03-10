from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.views import TenantAPIView
from soteria.atms.customform import CustomFormSchemaJSONField
from soteria.atms.models import Form
from soteria.atms.services.form import deactivate_form, update_form_detail


class FormSchemaGetUpdateDeleteAPI(TenantAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Form
            fields = (
                "id",
                "name",
                "schema",
            )

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(max_length=200, required=False)
        schema = CustomFormSchemaJSONField()

        class Meta:
            model = Form
            fields = (
                "name",
                "schema",
            )

    UpdateOutputSerializer = OutputSerializer
    lookup_url_kwarg = "form_id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Form.objects.all()
        qs = qs.filter(id=self.kwargs["form_id"])
        return qs

    def get(self, request, *args, **kwargs):
        form = self.get_object()
        resp_data = self.OutputSerializer(form).data
        return self.success_response(resp_data)

    def put(self, request, *args, **kwargs):
        form = self.get_object()
        serializer = self.InputSerializer(instance=form, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        form = update_form_detail(form, data)
        resp_data = self.UpdateOutputSerializer(form).data
        return self.success_response(resp_data)

    def delete(self, request, *args, **kwargs):
        form = self.get_object()
        deactivate_form(form)
        return self.success_response(
            data={"message": _("Form is deactivated successfully")},
            status=status.HTTP_200_OK,
        )
