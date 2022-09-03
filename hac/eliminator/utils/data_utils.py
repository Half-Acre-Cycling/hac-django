from unicodedata import category
import pandas as pd
from datetime import date
from eliminator.models import Category, Athlete, RaceResult, Round, Race
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
            "usac_number": row['USAC License'],
            "bib_number": row['Bib'],
            "name": ' '.join([row['First Name'], row['Last Name']]),
            "team": row["Team"],
            "year": date.today().year,
            "rider_category": row['USAC Category CROSS']
        })
        # Add it to our new category
        category_obj.athletes.add(athlete_obj)
    setup_initial_round(category_obj)

def generate_first_elimination_rounds(category_obj):
    # get count of placing athletes from this category
    seed_round = Round.objects.get(category=category_obj, title="Seed", year= date.today().year)
    
    races = Race.objects.filter(round=seed_round)
    eligible_athlete_count = 0
    for race in races:
        race_results = RaceResult.objects.filter(race=race)
        for race_result_obj in race_results:
            race_result = race_result_obj.serialize()
            if race_result['is_placing']:
                eligible_athlete_count += 1
    if eligible_athlete_count > 16:
        """"""
        elim_round = Round.objects.create(**{
            "title": "Elimination 1",
            "year": date.today().year,
            "category": category_obj
        })
        elim_1_key = [
            {
                'race': '1',
                'athletes': [
                    {
                        'race': '1',
                        'place': '1'
                    },
                    {
                        'race': '1',
                        'place': '2'
                    },
                    {
                        'race': '1',
                        'place': '3'
                    },
                    {
                        'race': '1',
                        'place': '4'
                    },
                    {
                        'race': '2',
                        'place': '5'
                    },
                    {
                        'race': '2',
                        'place': '6'
                    },
                    {
                        'race': '2',
                        'place': '7'
                    },
                    {
                        'race': '2',
                        'place': '8'
                    },
                ]
            },
            {
                'race': '2',
                'athletes': [
                    {
                        'race': '2',
                        'place': '1'
                    },
                    {
                        'race': '2',
                        'place': '2'
                    },
                    {
                        'race': '2',
                        'place': '3'
                    },
                    {
                        'race': '2',
                        'place': '4'
                    },
                    {
                        'race': '3',
                        'place': '5'
                    },
                    {
                        'race': '3',
                        'place': '6'
                    },
                    {
                        'race': '3',
                        'place': '7'
                    },
                    {
                        'race': '3',
                        'place': '8'
                    },
                ]
            },
            {
                'race': '3',
                'athletes': [
                    {
                        'race': '3',
                        'place': '1'
                    },
                    {
                        'race': '3',
                        'place': '2'
                    },
                    {
                        'race': '3',
                        'place': '3'
                    },
                    {
                        'race': '3',
                        'place': '4'
                    },
                    {
                        'race': '4',
                        'place': '5'
                    },
                    {
                        'race': '4',
                        'place': '6'
                    },
                    {
                        'race': '4',
                        'place': '7'
                    },
                    {
                        'race': '4',
                        'place': '8'
                    },
                ]
            },
            {
                'race': '4',
                'athletes': [
                    {
                        'race': '4',
                        'place': '1'
                    },
                    {
                        'race': '4',
                        'place': '2'
                    },
                    {
                        'race': '4',
                        'place': '3'
                    },
                    {
                        'race': '4',
                        'place': '4'
                    },
                    {
                        'race': '1',
                        'place': '5'
                    },
                    {
                        'race': '1',
                        'place': '6'
                    },
                    {
                        'race': '1',
                        'place': '7'
                    },
                    {
                        'race': '1',
                        'place': '8'
                    },
                ]
            },
        ]
        for race_key in elim_1_key:
            this_race_obj = Race.objects.create(**{
                'title': race_key['race'],
                'year': date.today().year,
                'round': elim_round
            })
            for athlete_key in race_key['athletes']:
                # find the athlete to add by looking up the race result
                prev_race = Race.objects.get(round=seed_round, title=athlete_key['race'])
                try:
                    this_race_result = RaceResult.objects.get(place=athlete_key['place'], race=prev_race)
                    this_race_obj.athletes.add(this_race_result.athlete)
                except RaceResult.DoesNotExist:
                    pass
    else:
        elim_round = Round.objects.create(**{
            "title": "Elimination",
            "year": date.today().year,
            "category": category_obj
        })
        elim_1_key = [
            {
                'race': '1',
                'athletes': [
                    {
                        'race': '1',
                        'place': '1'
                    },
                    {
                        'race': '1',
                        'place': '2'
                    },
                    {
                        'race': '1',
                        'place': '3'
                    },
                    {
                        'race': '1',
                        'place': '4'
                    },
                    {
                        'race': '2',
                        'place': '5'
                    },
                    {
                        'race': '2',
                        'place': '6'
                    },
                    {
                        'race': '2',
                        'place': '7'
                    },
                    {
                        'race': '2',
                        'place': '8'
                    },
                ]
            },
            {
                'race': '2',
                'athletes': [
                    {
                        'race': '2',
                        'place': '1'
                    },
                    {
                        'race': '2',
                        'place': '2'
                    },
                    {
                        'race': '2',
                        'place': '3'
                    },
                    {
                        'race': '2',
                        'place': '4'
                    },
                    {
                        'race': '1',
                        'place': '5'
                    },
                    {
                        'race': '1',
                        'place': '6'
                    },
                    {
                        'race': '1',
                        'place': '7'
                    },
                    {
                        'race': '1',
                        'place': '8'
                    },
                ]
            }
        ]
        for race_key in elim_1_key:
            this_race_obj = Race.objects.create(**{
                'title': race_key['race'],
                'year': date.today().year,
                'round': elim_round
            })
            for athlete_key in race_key['athletes']:
                # find the athlete to add by looking up the race result
                prev_race = Race.objects.get(round=seed_round, title=athlete_key['race'])
                try:
                    this_race_result = RaceResult.objects.get(place=athlete_key['place'], race=prev_race)
                    this_race_obj.athletes.add(this_race_result.athlete)
                except RaceResult.DoesNotExist:
                    pass

def generate_second_elimination_rounds(category_obj):
    first_elim_round = Round.objects.get(category=category_obj, title='Elimination 1', year=date.today().year)
    second_elim_round = Round.objects.create(**{
        "title": "Elimination 2",
        "year": date.today().year,
        "category": category_obj
    })
    elim_2_key = [
        {
            'race': '1',
            'athletes': [
                {
                    'race': '1',
                    'place': '1'
                },
                {
                    'race': '2',
                    'place': '1'
                },
                {
                    'race': '1',
                    'place': '2'
                },
                {
                    'race': '2',
                    'place': '2'
                },
                {
                    'race': '1',
                    'place': '3'
                },
                {
                    'race': '2',
                    'place': '3'
                },
                {
                    'race': '1',
                    'place': '4'
                },
                {
                    'race': '2',
                    'place': '4'
                },
            ]
        },
        {
            'race': '2',
            'athletes': [
                {
                    'race': '3',
                    'place': '1'
                },
                {
                    'race': '4',
                    'place': '1'
                },
                {
                    'race': '3',
                    'place': '2'
                },
                {
                    'race': '4',
                    'place': '2'
                },
                {
                    'race': '3',
                    'place': '3'
                },
                {
                    'race': '4',
                    'place': '3'
                },
                {
                    'race': '3',
                    'place': '4'
                },
                {
                    'race': '4',
                    'place': '4'
                },
            ]
        }
    ]
    for race_key in elim_2_key:
        this_race_obj = Race.objects.create(**{
            'title': race_key['race'],
            'year': date.today().year,
            'round': second_elim_round
        })
        for athlete_key in race_key['athletes']:
            # find the athlete to add by looking up the race result
            prev_race = Race.objects.get(round=first_elim_round, title=athlete_key['race'])
            try:
                this_race_result = RaceResult.objects.get(place=athlete_key['place'], race=prev_race)
                this_race_obj.athletes.add(this_race_result.athlete)
            except RaceResult.DoesNotExist:
                pass

def generate_comeback_rounds(category_obj):
    first_elim_round = Round.objects.get(category=category_obj, title='Elimination 1', year=date.today().year)
    second_elim_round = Round.objects.get(category=category_obj, title='Elimination 2', year=date.today().year)
    comeback_round = Round.objects.create(**{
        "title": "Comeback",
        "year": date.today().year,
        "category": category_obj
    })
    comeback_key = [
        {
            'race': '1',
            'athletes': [
                {
                    'round': second_elim_round,
                    'race': '1',
                    'place': '5'
                },
                {
                    'round': second_elim_round,
                    'race': '1',
                    'place': '6'
                },
                {
                    'round': first_elim_round,
                    'race': '1',
                    'place': '5'
                },
                {
                    'round': first_elim_round,
                    'race': '1',
                    'place': '6'
                },
                {
                    'round': first_elim_round,
                    'race': '2',
                    'place': '7'
                },
                {
                    'round': first_elim_round,
                    'race': '2',
                    'place': '8'
                },
                {
                    'round': first_elim_round,
                    'race': '3',
                    'place': '5'
                },
                {
                    'round': first_elim_round,
                    'race': '3',
                    'place': '6'
                },
            ]
        },
        {
            'race': '2',
            'athletes': [
                {
                    'round': second_elim_round,
                    'race': '1',
                    'place': '7'
                },
                {
                    'round': second_elim_round,
                    'race': '1',
                    'place': '8'
                },
                {
                    'round': second_elim_round,
                    'race': '2',
                    'place': '7'
                },
                {
                    'round': second_elim_round,
                    'race': '2',
                    'place': '8'
                },
                {
                    'round': first_elim_round,
                    'race': '4',
                    'place': '7'
                },
                {
                    'round': first_elim_round,
                    'race': '4',
                    'place': '8'
                },
                {
                    'round': first_elim_round,
                    'race': '1',
                    'place': '7'
                },
                {
                    'round': first_elim_round,
                    'race': '1',
                    'place': '8'
                },
            ]
        },
        {
            'race': '3',
            'athletes': [
                {
                    'round': second_elim_round,
                    'race': '2',
                    'place': '5'
                },
                {
                    'round': second_elim_round,
                    'race': '2',
                    'place': '6'
                },
                {
                    'round': first_elim_round,
                    'race': '2',
                    'place': '5'
                },
                {
                    'round': first_elim_round,
                    'race': '2',
                    'place': '6'
                },
                {
                    'round': first_elim_round,
                    'race': '3',
                    'place': '7'
                },
                {
                    'round': first_elim_round,
                    'race': '3',
                    'place': '8'
                },
                {
                    'round': first_elim_round,
                    'race': '4',
                    'place': '5'
                },
                {
                    'round': first_elim_round,
                    'race': '4',
                    'place': '6'
                },
            ]
        }
    ]
    for race_key in comeback_key:
        this_race_obj = Race.objects.create(**{
            'title': race_key['race'],
            'year': date.today().year,
            'round': comeback_round
        })
        for athlete_key in race_key['athletes']:
            # find the athlete to add by looking up the race result
            
            try:
                prev_race = Race.objects.get(round=athlete_key['round'], title=athlete_key['race'])
                this_race_result = RaceResult.objects.get(place=athlete_key['place'], race=prev_race)
                this_race_obj.athletes.add(this_race_result.athlete)
            except Exception:
                pass

def generate_final(category_obj, elim_round):
    final_round = Round.objects.create(**{
        "title": "Final",
        "year": date.today().year,
        "category": category_obj
    })
    final_key = [
        {
            'race': 'Final',
            'athletes': [
                {
                    'race': '1',
                    'place': '1'
                },
                {
                    'race': '2',
                    'place': '1'
                },
                {
                    'race': '1',
                    'place': '2'
                },
                {
                    'race': '2',
                    'place': '2'
                },
                {
                    'race': '1',
                    'place': '3'
                },
                {
                    'race': '2',
                    'place': '3'
                },
                {
                    'race': '1',
                    'place': '4'
                },
                {
                    'race': '2',
                    'place': '4'
                },
            ]
        }
    ]
    for race_key in final_key:
        this_race_obj = Race.objects.create(**{
            'title': race_key['race'],
            'year': date.today().year,
            'round': final_round
        })
        for athlete_key in race_key['athletes']:
            # find the athlete to add by looking up the race result
            prev_race = Race.objects.get(round=elim_round, title=athlete_key['race'])
            try:
                this_race_result = RaceResult.objects.get(place=athlete_key['place'], race=prev_race)
                this_race_obj.athletes.add(this_race_result.athlete)
            except RaceResult.DoesNotExist:
                pass
    
def generate_final_32(category_obj):
    round = Round.objects.get(category=category_obj, title="Elimination 2", year=date.today().year)
    generate_final(category_obj, round)

def generate_final_16(category_obj):
    round = Round.objects.get(category=category_obj, title="Elimination", year=date.today().year)
    generate_final(category_obj, round)

def generate_petit_final_32(category_obj):
    comeback_round = Round.objects.get(category=category_obj, title="Comeback", year=date.today().year)
    petit_round = Round.objects.create(**{
        "title": "Small Final",
        "year": date.today().year,
        "category": category_obj
    })
    final_key = [
        {
            'race': 'Small Final',
            'athletes': [
                {
                    'race': '1',
                    'place': '1'
                },
                {
                    'race': '2',
                    'place': '1'
                },
                {
                    'race': '3',
                    'place': '1'
                },
                {
                    'race': '1',
                    'place': '2'
                },
                {
                    'race': '2',
                    'place': '2'
                },
                {
                    'race': '3',
                    'place': '2'
                }
            ]
        }
    ]
    for race_key in final_key:
        this_race_obj = Race.objects.create(**{
            'title': race_key['race'],
            'year': date.today().year,
            'round': petit_round
        })
        for athlete_key in race_key['athletes']:
            # find the athlete to add by looking up the race result
            prev_race = Race.objects.get(round=comeback_round, title=athlete_key['race'])
            try:
                this_race_result = RaceResult.objects.get(place=athlete_key['place'], race=prev_race)
                this_race_obj.athletes.add(this_race_result.athlete)
            except RaceResult.DoesNotExist:
                pass

def generate_petit_final_16(category_obj):
    elimination_round = Round.objects.get(categoy=category_obj, title="Elimination", year=date.today().year)
    petit_round = Round.objects.create(**{
        "title": "Small Final",
        "year": date.today().year,
        "category": category_obj
    })
    final_key = [
        {
            'race': 'Small Final',
            'athletes': [
                {
                    'race': '1',
                    'place': '5'
                },
                {
                    'race': '2',
                    'place': '5'
                },
                {
                    'race': '1',
                    'place': '6'
                },
                {
                    'race': '2',
                    'place': '6'
                },
                {
                    'race': '1',
                    'place': '7'
                },
                {
                    'race': '2',
                    'place': '7'
                },
                {
                    'race': '1',
                    'place': '8'
                },
                {
                    'race': '2',
                    'place': '8'
                }
            ]
        }
    ]
    for race_key in final_key:
        this_race_obj = Race.objects.create(**{
            'title': race_key['race'],
            'year': date.today().year,
            'round': petit_round
        })
        for athlete_key in race_key['athletes']:
            # find the athlete to add by looking up the race result
            prev_race = Race.objects.get(round=elimination_round, title=athlete_key['race'])
            try:
                this_race_result = RaceResult.objects.get(place=athlete_key['place'], race=prev_race)
                this_race_obj.athletes.add(this_race_result.athlete)
            except RaceResult.DoesNotExist:
                pass