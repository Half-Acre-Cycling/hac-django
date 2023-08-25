# Half Acre Cycling Django App
### Introduction
This is a full-fledged django app that can serve any backend needs that the team needs.
At present, this is solely used for the HAC CXE (Cyclocross Eliminator), which is a special race format
that takes a long time organizationally if it is done by pen and paper. 

### CXE Bracket Bot General outline
The Django app handles race imports via CSV from a bikereg output format.
Upon initial import, it sorts racers into seed rounds automatically, which can then be scored.
The general URL structure matches the race format, which is to say:
Category>Round>Race
EG: Juniors>Seed Round>Seed Round Heat 1

To see more information about how the race is actually run, check out [this document](eliminator.md)

### Installation
- install pipenv
- invoke a pipenv shell inside this workspace with `pipenv shell`
- install dependencies with `pipenv install`
- `cd hac` to get into the django root directory (ensure your are still in your pipenv)
- set up the initial database structure by `python manage.py makemigrations` and `python manage.py migrate`
- create yourself a superuser by running `python manage.py createsuperuser`
- collect static assets by running `python manage.py collectstatic`, this generates the initial CSS files from sass.
- run your server by running `python manage.py runserver`. This _should_ auto-compile Sass, but if for some reason your changes are not appearing,
you can always halt the server and collect static again, and run again.
- if changes are made to the database model, you will likely need to create another migration file and perform that migration.
- The django admin panel can be accessed at `/admin/`

### Next Steps / Tasks
- basic mobile-first front end
- drag racers from one heat to another
- drag and drop file uploading for CSV data
- results view
- unauthenticated racer views
- auto-play presentation view (in case Jean wants to bring his TV, lol)
- add approximate start times to races
- schedule view
- additional validation for scoring submissions
- additional validation for next round generation
- add FAQ as a single page (see third item from documentation on the [eliminator docs](eliminator.md))
- add individual FAQ elements as tooltips
- add "bracket" view (oy this hurts my head)
