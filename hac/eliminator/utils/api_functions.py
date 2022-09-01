from eliminator.models import Category, Athlete, Round, Race, RaceResult

def update_athlete(id, *args, **kwargs):
    try:
        Athlete.objects.filter(id=id).update(**kwargs)
    except Exception as e:
        print(e)
    return Athlete.objects.get(id=id).serialize()