import pandas as pd
from datetime import date
from eliminator.models import Category, Athlete, Round, Race
import json
import random

def setup_initial_round(category_obj):
    """given a category, create initial seed rounds"""
    round_obj = Round.objects.create(**{
        "title": "Seed",
        "year": date.today().year,
        "category": category_obj
    })

    # Determine number of races in the seed round
    athlete_count = category_obj.athletes.all().count()
    count_of_division_operations = 0
    athlete_dividend = athlete_count
    while athlete_dividend > 8:
        # divide athlete count by two. If still over the maximum rider count,
        # divide again
        athlete_dividend /= 2
        # Keep track of the number of division operations, our seed race count will be 2^nth
        count_of_division_operations += 1
    seed_race_quantity = 2 ** count_of_division_operations
    min_athletes_per_round = int(athlete_dividend)
    count_of_modulus_athletes = athlete_count % seed_race_quantity

    # randomize order of athletes in this category
    athletes = list(category_obj.athletes.all())
    random.shuffle(athletes)
    
    athlete_index = 0
    for race_number in range(seed_race_quantity):
        race_number_pretty = str(race_number + 1)
        this_race_obj = Race.objects.create(**{
            'title': race_number_pretty,
            'year': date.today().year,
            'round': round_obj
        })

        # determine number of athletes in this race by taking the minimum
        # and adding an extra (if applicable)
        this_race_athlete_count = min_athletes_per_round
        # If there's extra athletes
        if count_of_modulus_athletes > 0:
            # take one of the extra athletes
            count_of_modulus_athletes -= 1
            # add it to this race
            this_race_athlete_count += 1

        for this_race_athlete_index in range(this_race_athlete_count):
            # get the athlete and add it to this race
            this_athlete_obj = athletes[athlete_index]
            this_race_obj.athletes.add(this_athlete_obj)

            # increment athlete index as it is not done automatically
            athlete_index += 1

def create_data_from_csv(file, category_name):
    # Create a new Category
    category_obj = Category.objects.create(**{
        "year": date.today().year,
        "title": category_name
    })

    # Read in rider data
    df = pd.read_csv(file)
    df.fillna('', inplace=True)
    for index, row in df.iterrows():
        # Create a new Athlete
        athlete_obj = Athlete.objects.create(**{
            "usac_number": row['USAC Category CROSS'],
            "bib_number": row['Bib'],
            "name": ' '.join([row['First Name'], row['Last Name']]),
            "team": row["Team"],
            "year": date.today().year
        })
        # Add it to our new category
        category_obj.athletes.add(athlete_obj)
    setup_initial_round(category_obj)