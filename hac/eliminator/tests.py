import os, json
from unicodedata import category
from django.test import TestCase
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from eliminator.models import Category, Athlete, Round, Race
from django.conf import settings
from eliminator.utils.data_utils import create_data_from_csv

TEST_CATEGORY_DATA_FILE_PATH = os.path.join(settings.BASE_DIR.parent, "eliminator_sample_data.csv")
test_category_data = open(TEST_CATEGORY_DATA_FILE_PATH)

"""
Some tests to perform:
- Model race placing. Does each rider get a minimum of three races? 
    i.e. any Athlete object with zero dns or dnf RaceResult related records
    should have at least 3 RaceResult related records.
- can an authenticated staff user change a bib number for an Athlete?
- can an authenticated staff user move an Athlete from one Race to another Race
    (within the same Round)
- can an authenticated staff user place a rider in their RaceResult record?
"""
class SetupData(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Athletes for one category, as well as the category they go in
        create_data_from_csv(test_category_data, 'test_category')
        
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_anonymous_cannot_upload(self):
        print("test to ensure that an anonymous user gets redirected away from staff pages")
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 302)

    def test_admin_can_log_in(self):
        print("test whether a staff user can log in and get to the upload page")
        User = get_user_model()
        User.objects.create_user('my-user-name', email='foo@bar.com', password='password', is_staff=True)
        self.assertTrue(self.client.login(username='my-user-name', password='password'))
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/upload/')
        self.assertEqual(response.status_code, 200)
        
    def test_admin_can_upload(self):
        print('test whether a staff user can upload a category')
        User = get_user_model()
        User.objects.create_user('my-user-name', email='foo@bar.com', password='password', is_staff=True)
        self.assertTrue(self.client.login(username='my-user-name', password='password'))
        response = self.client.post('/upload/', {'category_name': 'test_upload_category', 'file': test_category_data})
        self.assertEqual(response.status_code, 200)


    def test_new_category_has_riders(self):
        print('test to ensure that our test category has riders assigned to it')
        test_category = Category.objects.get(title='test_category')
        self.assertGreater(test_category.athletes.all().count(), 0)

    def test_athletes_assigned_to_seed_round(self):
        test_category = Category.objects.get(title='test_category')
        seed_round = Round.objects.get(title='Seed', category=test_category)
        seed_races = Race.objects.filter(round=seed_round)
        print('Test to ensure that category generation resulted in at least one seed race')
        self.assertGreater(seed_races.count(), 0)
        athlete_count_from_category = test_category.athletes.all().count()
        athlete_count_from_races = 0
        for race in seed_races:
            this_race_athlete_count = race.athletes.all().count()
            athlete_count_from_races += this_race_athlete_count
        print('Test to ensure that number of athletes in seed race matches number of athletes in category')
        self.assertEqual(athlete_count_from_category, athlete_count_from_races)
        print('Test to ensure each athlete only exists once in each seed race')
        athlete_ids = []
        for race in seed_races:
            for athlete in race.athletes.all():
                athlete_id = athlete.serialize()['id']
                self.assertFalse(athlete_id in athlete_ids)
                athlete_ids.append(athlete_id)

    def test_update_athlete(self):
        User = get_user_model()
        bad_response = self.client.post('/athletes/1', {'bib_number': '123456'})
        self.assertEqual(bad_response.status_code, 302)
        User.objects.create_user('my-user-name', email='foo@bar.com', password='password', is_staff=True)
        self.assertTrue(self.client.login(username='my-user-name', password='password'))
        get_response = self.client.get('/athletes/1')
        test_athlete_usac_number = json.loads(get_response.content)['usac_number']
        self.assertEqual(test_athlete_usac_number, '5')
        new_value = '987654'
        update_response = self.client.put('/athletes/1', {'bib_number': new_value}, content_type='application/json')
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(new_value, Athlete.objects.get(id=1).serialize()['bib_number'])