from django.urls import path

from .views import (LanguageList, ProjectLanguagesView, ProjectList,
                    ProjectSectionsView, RecordValuesView, SectionRecordsView)

urlpatterns = [
    path('languages/', LanguageList.as_view(), name='language-list'),
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<int:project_id>/languages/',
         ProjectLanguagesView.as_view(), name='project-languages'),
    path('projects/<int:project_id>/sections/',
         ProjectSectionsView.as_view(), name='project-sections'),
    path('sections/<int:section_id>/records/',
         SectionRecordsView.as_view(), name='section-records'),
    path('records/<int:record_id>/values/',
         RecordValuesView.as_view(), name='record-values'),
]
