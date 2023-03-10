from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as dj_filters
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated

from soteria.api.fields import TimeZoneSerializerField
from soteria.api.pagination import DefaultPageNumberPagination, PaginatedListAPIViewMixin
from soteria.api.views import MethodSerializerMixin, TenantAPIView
from soteria.atms.models import Asset, Form, Job, JobType
from soteria.atms.serializers.assets import AssetDetailSerializer
from soteria.atms.services.job import create_job
from soteria.orgs.models import Location, OrganizationMember


class JobListCreateAPI(
    PaginatedListAPIViewMixin,
    MethodSerializerMixin,
    TenantAPIView,
):
    class OutputSerializer(serializers.ModelSerializer):
        asset = AssetDetailSerializer()
        weekdays_abbr = serializers.SerializerMethodField()

        class Meta:
            model = Job
            fields = (
                "id",
                "name",
                "asset",
                "weekdays",
                "weekdays_abbr",
                "assign_to",
                "location",
                "time_ranges",
                "duration",
                "job_type",
                "job_created_at",
                "created_at",
                "updated_at",
                "time_scale",
                "start_at",
                "end_at",
            )

        def get_weekdays_abbr(self, obj: Job):
            return obj.get_weekdays_abbr

    class InputSerializer(serializers.ModelSerializer):
        time_scale_choices = (
            ("daily", "Daily"),
            ("monthly", "Monthly"),
            ("quaterly", "Quaterly"),
        )
        name = serializers.CharField(max_length=200)
        description = serializers.CharField(max_length=300)
        job_type = serializers.PrimaryKeyRelatedField(
            queryset=JobType.objects.all(), required=False
        )
        asset = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all())
        assign_to = serializers.PrimaryKeyRelatedField(queryset=OrganizationMember.objects.all())
        location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
        form = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all())
        time_ranges = serializers.ListField(child=serializers.TimeField())
        duration = serializers.CharField()
        weekdays = serializers.ListField(required=False)
        timezone = TimeZoneSerializerField(required=False)
        time_scale = serializers.ChoiceField(choices=time_scale_choices)
        start_at = serializers.DateTimeField()
        end_at = serializers.DateTimeField()

        class Meta:
            model = Job
            fields = (
                "name",
                "description",
                "job_type",
                "asset",
                "assign_to",
                "form",
                "location",
                "weekdays",
                "time_ranges",
                "duration",
                "timezone",
                "time_scale",
                "start_at",
                "end_at",
            )

        def validate_weekdays(self, value):
            for day in value:
                if day not in range(1, 8):
                    raise serializers.ValidationError(
                        _(
                            "Invalid weekday number, should be in range 1 to 7, where "
                            "Mon=1... Sun=7"
                        )
                    )

            return value

    class ListFilterSet(dj_filters.FilterSet):
        name = dj_filters.CharFilter(field_name="name", lookup_expr="contains")
        location = dj_filters.ModelChoiceFilter(queryset=Location.objects.all())
        asset = dj_filters.ModelChoiceFilter(queryset=Asset.objects.all())
        date = dj_filters.DateFilter(method="filter_for_date")
        job_type = dj_filters.ModelChoiceFilter(queryset=JobType.objects.all())
        form_type = dj_filters.ModelChoiceFilter(queryset=Form.objects.all())
        duration = dj_filters.NumberFilter(field_name="duration")
        time_scale = dj_filters.ChoiceFilter(choices=Job.TimeScale.choices)
        time_ranges = dj_filters.BaseInFilter(
            method="fiter_for_time_ranges", lookup_expr="icontains"
        )

        class Meta:
            model = Job
            fields = ["assign_to"]

        def filter_for_date(self, queryset, name, value):
            return queryset.filter(created_at__date=value)

        def fiter_for_time_ranges(self, queryset, name, value):
            try:
                resp = queryset.filter(time_ranges__contains=value)
            except ValidationError:
                raise serializers.ValidationError(
                    _("Invalid time format. It must be in HH:MM[:ss[.uuuuuu]] format.'")
                )
            return resp

    class ListPagination(DefaultPageNumberPagination):
        pass

    ListOutputSerializer = OutputSerializer

    method_serializer_classes = {
        ("GET",): ListOutputSerializer,
        ("POST",): InputSerializer,
    }
    pagination_class = ListPagination
    queryset = Job.objects.all().order_by("-created_at")
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        dj_filters.DjangoFilterBackend,
    ]
    filter_class = ListFilterSet

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        job = create_job(
            asset=data["asset"],
            assign_to=data["assign_to"],
            location=data["location"],
            form=data["form"],
            weekdays=data.get("weekdays"),
            time_ranges=data["time_ranges"],
            duration=data["duration"],
            job_type=data.get("job_type"),
            name=data.get("name"),
            description=data.get("description"),
            timezone=data.get("timezone"),
            time_scale=data.get("time_scale"),
            start_at=data.get("start_at"),
            end_at=data.get("end_at"),
        )
        resp_data = self.OutputSerializer(job).data
        return self.success_response(data=resp_data, status=status.HTTP_201_CREATED)
