from django.utils.html import strip_tags

from rest_framework import serializers

from main.models import Experience, Project


class _PortfolioStarMixin(serializers.Serializer):
    """Field hasil perhitungan star yang dipakai bersama Project & Experience."""

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class _DateRangeValidationMixin:
    """Selesai tidak boleh lebih awal dari mulai — padanan DateRangeFormMixin."""

    def validate(self, attrs):
        started_at = attrs.get("started_at")
        ended_at = attrs.get("ended_at")
        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {"ended_at": "Tanggal selesai tidak boleh lebih awal dari tanggal mulai."}
            )
        return attrs


class ProjectSerializer(_DateRangeValidationMixin, _PortfolioStarMixin,
                        serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField()
    is_ongoing = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "category", "category_display", "description",
            "technologies", "repository_url", "report_url", "deployment_url",
            "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_technologies(self, value):
        return strip_tags(value)

    def get_category_display(self, obj):
        return obj.get_category_display()

    def get_is_ongoing(self, obj):
        return obj.is_ongoing


class ExperienceSerializer(_DateRangeValidationMixin, _PortfolioStarMixin,
                           serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField()
    is_ongoing = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "role", "organization", "description",
            "category", "category_display", "thumbnail", "organization_url",
            "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Judul experience tidak boleh hanya berisi tag HTML.")
        return value

    def validate_role(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Peran tidak boleh hanya berisi tag HTML.")
        return value

    def validate_organization(self, value):
        return strip_tags(value)

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Deskripsi experience tidak boleh hanya berisi tag HTML.")
        return value

    def get_category_display(self, obj):
        return obj.get_category_display()

    def get_is_ongoing(self, obj):
        return obj.is_ongoing
