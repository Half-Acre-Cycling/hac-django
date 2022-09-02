from django.contrib.auth.models import User, Group
from rest_framework import serializers
from eliminator.models import Athlete, Category, Race, Round, RaceResult

# class AthleteSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     usac_number = serializers.CharField(required=False, allow_blank=True)
#     bib_number = serializers.CharField(required=False, allow_blank=True)
#     name = serializers.CharField(required=False, allow_blank=True)
#     team = serializers.CharField(required=False, allow_blank=True)
#     year = serializers.CharField(required=False, allow_blank=True)

#     def create(self, validated_data):
#         """
#         Create and return a new `Athlete` instance, given the validated data.
#         """
#         return Athlete.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Athlete` instance, given the validated data.
#         """
#         instance.usac_number = validated_data.get('usac_number', instance.usac_number)
#         instance.bib_number = validated_data.get('bib_number', instance.bib_number)
#         instance.name = validated_data.get('name', instance.name)
#         instance.team = validated_data.get('team', instance.team)
#         instance.year = validated_data.get('year', instance.year)
#         instance.save()
#         return instance
class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = [
            'id',
            'usac_number',
            'bib_number',
            'name',
            'team',
            'year'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'athletes',
            'year'
        ]

class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = [
            'id',
            'title',
            'year',
            'category'
        ]

class RaceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult
        fields = [
            'id',
            'athlete',
            'place'
        ]

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult
        fields = [
            'id',
            'title',
            'year',
            'round',
            'athletes',
            'places'
        ]