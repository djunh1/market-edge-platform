from django.test import TestCase
from core.models.models_study import Study
from core.models.models_message import Message


class TestStudentContactForm(TestCase):
    def test_core_study_endpoint_GET_success(self):
        data = {
            "first_name": "Juliana",
            "last_name": " Crain",
            "message": "Would love to talk about Philip K. Dick",
        }

        response = self.client.get(f'/')
        self.assertEqual(response.status_code, 200)


    def test_core_study_endpoint_POST_success(self):
        pass

    def test_core_study_endpoint_POST_fail(self):
        pass

