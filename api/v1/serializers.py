from time import time

from django.contrib.auth.models import User
from rest_framework import serializers

from pipeline import models

from . import utils


class PlaylistSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="public_id", read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ("id", "name", "owner")
        model = models.Playlist


class ProcessingStateSerializer(serializers.ModelSerializer):
    started_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        fields = ("status", "progress", "started_at")
        model = models.ProcessingState


class SubtitleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="public_id", read_only=True)
    video_id = serializers.CharField(source="video__id", read_only=True)
    url = serializers.CharField(read_only=True)

    class Meta:
        fields = ("id", "language", "video_id", "url")
        model = models.Subtitle


class VideoUploadUrlSerializer(serializers.ModelSerializer):
    class RelatedPlaylistField(serializers.SlugRelatedField):
        def get_queryset(self):
            return models.Playlist.objects.filter(owner=self.context["request"].user)

    id = serializers.CharField(source="public_video_id", read_only=True)
    expires_at = serializers.IntegerField(read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    playlist = RelatedPlaylistField(slug_field="public_id", required=False)

    class Meta:
        fields = ("id", "expires_at", "owner", "origin", "playlist")
        model = models.VideoUploadUrl

    def create(self, validated_data):
        """
        Overloads the create method in order to set a valid "expires_at" value
        before saving to database.
        """

        validated_data["expires_at"] = (
            time() + models.VideoUploadUrl.objects.EXPIRE_DELAY
        )
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, default=utils.random_password)
    token = serializers.CharField(read_only=True, source="auth_token.key")
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        fields = ("username", "password", "token", "is_staff")
        model = User

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data["username"], password=validated_data["password"]
        )


class VideoFormatSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)
    bitrate = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            "name",
            "url",
            "bitrate",
            "width",
            "height",
            "duration_millis",
            "file_size",
            "frame_rate",
        )
        model = models.VideoFormat


class VideoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="public_id", read_only=True)
    processing = ProcessingStateSerializer(source="processing_state", read_only=True)
    subtitles = SubtitleSerializer(many=True, read_only=True)
    formats = VideoFormatSerializer(many=True, read_only=True)
    thumbnail = serializers.CharField(source="thumbnail_url", read_only=True)

    class Meta:
        fields = ("id", "title", "processing", "subtitles", "formats", "thumbnail")
        model = models.Video
