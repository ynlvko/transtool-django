from translations import models


def generate_file(project_id: int):
    project = models.Project.objects.get(project_id)
