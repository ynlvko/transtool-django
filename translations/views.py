from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Language, Project, Record, RecordValue, Section
from .serializers import (LanguageSerializer, ProjectCreateSerializer,
                          ProjectSerializer, RecordSerializer,
                          RecordValueSerializer, SectionCreateSerializer,
                          SectionSerializer)


class LanguageList(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectLanguagesView(APIView):
    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def patch(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        project.languages.set(request.data.get('langs'))
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class ProjectSectionsView(APIView):
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        sections = Section.objects.filter(project=project)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        section_name = request.data.get('name')

        section = Section(name=section_name, project=project)
        section.save()

        serializer = SectionSerializer(section)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SectionRecordsView(APIView):
    def get(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)

        records = Record.objects.filter(section=section)
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)

        record_key = request.data.get('key')
        if not record_key:
            return Response({"error": "Record key is required"}, status=status.HTTP_400_BAD_REQUEST)

        record = Record(key=record_key, section=section)
        record.save()

        serializer = RecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecordValuesView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, record_id):
        try:
            record = Record.objects.get(id=record_id)
        except Record.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        record_values = RecordValue.objects.filter(record=record)
        serializer = RecordValueSerializer(record_values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, record_id, format=None):
        record = get_object_or_404(Record, pk=record_id)
        language = get_object_or_404(
            Language,
            pk=request.data.get('language_id')
        )
        value = request.data.get('value')

        record_value = RecordValue.objects.filter(
            record=record,
            language=language,
        ).first()
        if (record_value):
            record_value.value = value
            record_value.save()
        else:
            record_value = RecordValue.objects.create(
                record=record,
                language=language,
                value=value,
            )
        serializer = RecordValueSerializer(record_value)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
