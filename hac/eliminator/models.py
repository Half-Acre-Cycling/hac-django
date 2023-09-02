from pickle import FALSE
from tkinter import CASCADE
from django.db import models
from django.forms.models import model_to_dict

class Athlete(models.Model):
    usac_number = models.TextField(blank=True, default="")
    bib_number = models.TextField(blank=True, default="")
    name = models.TextField(blank=True, default="")
    team = models.TextField(blank=True, default="")
    year = models.TextField(default="2022")
    rider_category = models.TextField(blank=True, default="")
    
    def __str__(self):
        return f'{self.bib_number} {self.name}'.strip()

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)

class Category(models.Model):
    athletes = models.ManyToManyField(Athlete, blank=True)
    title = models.TextField()
    year = models.TextField(default="2022")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)


class Round(models.Model):
    title = models.TextField()
    year = models.TextField(default="2022")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.title} {self.title}'

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
class Race(models.Model):
    time = models.TextField()
    is_past = models.BooleanField(default=False)
    title = models.TextField()
    year = models.TextField(default="2022")
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    athletes = models.ManyToManyField(Athlete, blank=True)

    def __str__(self):
        return f'{self.round} {self.title}'

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
class RaceResult(models.Model):
    places = {
        ("", "----"),
        ("dns", "Did Not Start"),
        ("dnf", "Did Not Finish"),
        ("dq", "Disqualified"),
        ("dnp", "Did Not Place"),
        ("1", "First"),
        ("2", "Second"),
        ("3", "Third"),
        ("4", "Fourth"),
        ("5", "Fifth"),
        ("6", "Sixth"),
        ("7", "Seventh"),
        ("8", "Eigth"),
        ("9", "Ninth"),
        ("10", "Tenth"),
        ("11", "Eleventh"),
        ("12", "Twelfth"),
        ("13", "Thirteenth"),
        ("14", "Fourteenth"),
        ("15", "Fifteenth"),
        ("16", "Sixteenth"),
        ("17", "Seventeenth"),
        ("18", "Eighteeenth"),
        ("19", "Nineteenth"),
        ("20", "Twentieth")
    }
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    place = models.TextField(default="", choices=places, blank=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    is_placing = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.athlete} {self.place}'

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
