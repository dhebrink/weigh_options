from django.test import TestCase
from django.utils import timezone

from .models import Answer, Category, Prompt, SubCategory, Template, TemplateCopy
# Create your tests here.

class TestCategoryModel(TestCase):

    def test_str(self):
        cat = Category(name='Test Category')
        self.assertEquals(str(cat), cat.name)


class TestSubCategoryModel(TestCase):

    def test_str(self):
        sub_cat = SubCategory(name='A Sample Sub-Category')
        self.assertEquals(str(sub_cat), sub_cat.name)

    def test_category_delete_cascade(self):
        cat = Category(name='Category')
        cat.save()
        self.assertIsNotNone(cat.id)

        sub_cat = SubCategory(name='Sub-category', category=cat)
        sub_cat.save()
        self.assertIsNotNone(sub_cat.id)
        sub_id = sub_cat.id

        # Remove the Category, and our sub-category should be gone
        cat.delete()
        queried_sub_categories = SubCategory.objects.filter(pk=sub_id)
        self.assertEquals(list(queried_sub_categories), [])


class TestTemplateModel(TestCase):

    def test_str(self):
        template = Template(name='A Template')
        self.assertEquals(str(template), template.name)

    def test_mark_deleted(self):
        template= Template(name='The Template')
        template.save()
        self.assertIsNone(template.date_deleted)
        self.assertFalse(template.deleted)

        template.mark_deleted()
        today = timezone.now().date()
        self.assertTrue(template.deleted)
        self.assertIsNotNone(template.date_deleted)
        self.assertEquals(template.date_deleted.date(), today)


class TestPromptModel(TestCase):

    def setUp(self):
        template = Template()
        template.save()
        self.prompt = Prompt(template=template)

    def test_answer_type_selections(self):
        options = Prompt.ANSWER_TYPE_OPTIONS
        self.assertEquals(len(options), 4)
        opt_1, opt_2, opt_3, opt_4 = options

        self.assertEquals(opt_1[0], 'bool')
        self.assertEquals(opt_1[1], 'Yes / No')

        self.assertEquals(opt_2[0], 'free-form')
        self.assertEquals(opt_2[1], 'Free-Form Text Entry')

        self.assertEquals(opt_3[0], 'single-select')
        self.assertEquals(opt_3[1], 'Single Selection')

        self.assertEquals(opt_4[0], 'multi-select')
        self.assertEquals(opt_4[1], 'Multiple Selections')

    def test_mark_deleted(self):
        self.assertFalse(self.prompt.deleted)
        self.assertIsNone(self.prompt.date_deleted)

        self.prompt.mark_deleted()
        today = timezone.now().date()
        self.assertTrue(self.prompt.deleted)
        self.assertEquals(self.prompt.date_deleted.date(), today)

    def test_parsed_answer_options(self):
        choices = ['one', 'two', 'three', 'four']
        self.prompt.answer_options = '~'.join(choices)
        parsed_choices = self.prompt.answer_options_parsed
        self.assertEquals(parsed_choices, choices)

    def test_parsed_answer_options_with_spaces_are_stripped(self):
        choices = ['one', '  two', 'three  ', '  four  ']
        self.prompt.answer_options = '~'.join(choices)
        parsed_choices = self.prompt.answer_options_parsed

        stripped_choices = [c.strip() for c in choices]
        self.assertEquals(parsed_choices, stripped_choices)


class TestTemplateCopyModel(TestCase):

    def setUp(self):
        template = Template()
        template.save()
        self.copy = TemplateCopy(template=template)
        self.copy.save()

    def test_mark_deleted(self):
        self.assertFalse(self.copy.deleted)
        self.assertIsNone(self.copy.date_deleted)

        self.copy.mark_deleted()
        today = timezone.now().date()
        self.assertTrue(self.copy.deleted)
        self.assertEquals(self.copy.date_deleted.date(), today)


class TestAnswerModel(TestCase):

    def setUp(self):
        template = Template()
        template.save()
        copy = TemplateCopy(template=template)
        copy.save()
        prompt = Prompt(template=template)
        prompt.save()
        self.answer = Answer(template_copy=copy, prompt=prompt)
        self.answer.save()

    def test_mark_deleted(self):
        self.assertIsNone(self.answer.date_added)
        self.assertIsNone(self.answer.response)

        response_is = 'A selection'
        today = timezone.now().date()
        self.answer.store_value(response_is)
        self.assertEquals(self.answer.response, response_is)
        self.assertEquals(self.answer.date_added.date(), today)
