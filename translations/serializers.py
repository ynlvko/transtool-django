from rest_framework import serializers

from .models import Language, Project, Record, RecordValue, Section


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'languages']


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']


class SectionSerializer(serializers.ModelSerializer):
    record_count = serializers.SerializerMethodField()

    def get_record_count(self, obj):
        return obj.record_set.count()

    class Meta:
        model = Section
        fields = ['id', 'project', 'name', 'record_count']


class SectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['name']


class RecordValueSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = RecordValue
        fields = ['id', 'value', 'language', 'record']


class RecordSerializer(serializers.ModelSerializer):
    values = RecordValueSerializer(many=True, read_only=True)

    class Meta:
        model = Record
        fields = ['id', 'key', 'values']
