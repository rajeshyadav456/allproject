from rest_framework import serializers

from soteria.atms.models import Job
from soteria.atms.serializers.assets import AssetDetailSerializer
from soteria.orgs.serializers.organizatioin_member import OrganizationMemberDetailSerializer


class JobDetailOutputSerializer(serializers.ModelSerializer):
    asset = AssetDetailSerializer()
    weekdays_abbr = serializers.SerializerMethodField()
    assign_to = OrganizationMemberDetailSerializer()

    class Meta:
        model = Job
        fields = (
            "id",
            "name",
            "description",
            "asset",
            "weekdays",
            "weekdays_abbr",
            "assign_to",
            "location",
            "job_type",
            "form",
            "time_ranges",
            "duration",
            "time_scale",
            "start_at",
            "end_at",
            "created_at",
            "updated_at",
        )

    def get_weekdays_abbr(self, obj: Job):
        return obj.get_weekdays_abbr


class JobReporteSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source="location.name", allow_null=True, required=False)
    asset_name = serializers.CharField(source="asset.name", allow_null=True, required=False)
    assign_to = serializers.CharField(source="assign_to.email")
    form_name = serializers.CharField(source="form.name", allow_null=True, required=False)
    job_type_name = serializers.CharField(source="job_type.name", allow_null=True, required=False)

    class Meta:
        model = Job
        fields = (
            "id",
            "name",
            "description",
            "asset_name",
            "weekdays",
            "assign_to",
            "location_name",
            "job_type_name",
            "form_name",
            "time_ranges",
            "duration",
        )
