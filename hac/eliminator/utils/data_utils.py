import pandas as pd
from datetime import date
from eliminator.models import Category, Athlete
import json

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