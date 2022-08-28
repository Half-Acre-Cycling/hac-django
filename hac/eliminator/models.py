from django.db import models
from django.forms.models import model_to_dict

class Athlete(models.Model):
    usac_number = models.TextField(blank=True, default="")
    bib_number = models.TextField()
    name = models.TextField()
    category_name = models.TextField()
    year = models.TextField(default="2022")

    def __str__(self):
        return self.bib_number

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)

class Category(models.Model):
    athletes = models.ManyToManyField(Athlete, blank=True)
    title = models.TextField()
    year = models.TextField(default="2022")

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
        return self.title

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

    def __str__(self):
        return self.place

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)

class Race(models.Model):
    title = models.TextField()
    year = models.TextField(default="2022")
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    athletes = models.ManyToManyField(Athlete, blank=True)
    places = models.ManyToManyField(RaceResult, blank=True)

    def __str__(self):
        return self.title

    def serialize(self):
        return model_to_dict(self)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)