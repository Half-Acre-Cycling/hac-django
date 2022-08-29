import os
from django.test import TestCase
from django.conf import settings
from eliminator.utils.data_utils import create_data_from_csv

TEST_CATEGORY_DATA_FILE_PATH = os.path.join(settings.BASE_DIR.parent, "eliminator_sample_data.csv")
test_category_data = open(TEST_CATEGORY_DATA_FILE_PATH).read()

"""
Some tests to perform:
- can an authenticated staff user upload a category? Expect yes. Endpoint /upload/
- can an anonymous user upload a category? Expect no. Endpoint /upload/
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
    def setUpTestData(cls) -> None:
        # Create Athletes for one category, as well as the category they go in
        create_data_from_csv(test_category_data, 'test_category')

        return super().setUpTestData()

