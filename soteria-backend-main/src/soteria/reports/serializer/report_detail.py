from rest_framework import serializers

from soteria.models.report import Report


class ReportsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = (
            "id",
            "name",
            "organization",
            "column_mapping",
            "included_columns",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {**representation}
