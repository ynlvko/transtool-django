from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    languages = models.ManyToManyField('Language', through='ProjectLanguage')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Record(models.Model):
    key = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.key


class RecordValue(models.Model):
    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        related_name='values',
    )
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return f"{self.record} - {self.language}: {self.value}"

    class Meta:
        unique_together = ('record', 'language')


class ProjectLanguage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.name} - {self.language.name}"
