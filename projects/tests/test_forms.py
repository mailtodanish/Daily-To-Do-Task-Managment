from django.test import TestCase
from projects.forms import LovCreateForm

class LovCreateFormTest(TestCase):
    def test_LovCreateForm_name_field_label(self):
        form = LovCreateForm()
        self.assertTrue(form.fields['Name'].label == 'Name')

    def test_LovCreateForm_name_field_required(self):
        form = LovCreateForm(data={'Name': '','Description':'test'})
        self.assertFalse(form.is_valid())
    
    def test_LovCreateForm_Description_field_required(self):
        form = LovCreateForm(data={'Name': 'Test','Description':''})
        self.assertFalse(form.is_valid())