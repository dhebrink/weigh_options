from django.db.models import (
    BooleanField, CASCADE, CharField, DateTimeField, ForeignKey,
    Model, SET_NULL
)
from django.utils import timezone

CHAR_LARGE = 512
CHAR_MED = 200
CHAR_SMALL = 50


class Category(Model):
    name = CharField(max_length=CHAR_MED)

    def __str__(self):
        return self.name


class SubCategory(Model):
    category = ForeignKey(Category, on_delete=CASCADE)
    name = CharField(max_length=CHAR_MED)

    def __str__(self):
        return self.name


class Template(Model):
    sub_category = ForeignKey(SubCategory, on_delete=SET_NULL, null=True)
    name = CharField(max_length=CHAR_MED)
    date_added = DateTimeField(auto_now_add=True)
    deleted = BooleanField(default=False)
    date_deleted = DateTimeField(null=True)

    def __str__(self):
        return self.name

    def mark_deleted(self):
        self.deleted = True
        self.date_deleted = timezone.now()
        self.save()


class Prompt(Model):
    ANSWER_TYPE_OPTIONS = [
        ('bool', 'Yes / No'),
        ('free-form', 'Free-Form Text Entry'),
        ('single-select', 'Single Selection'),
        ('multi-select', 'Multiple Selections'),
    ]

    template = ForeignKey(Template, on_delete=CASCADE)
    text = CharField(max_length=CHAR_MED)
    description = CharField(max_length=CHAR_LARGE)
    answer_type = CharField(max_length=CHAR_SMALL, choices=ANSWER_TYPE_OPTIONS)
    # In case 'single-select' or 'multi-select' answer_type, store the selection options.
    # This value will be expected in a tilde-delimited string. (not commas, in case options contain them)
    answer_options = CharField(max_length=CHAR_LARGE, null=True, default=None)
    date_added = DateTimeField(auto_now_add=True)
    deleted = BooleanField(default=False)
    date_deleted = DateTimeField(null=True)

    def mark_deleted(self):
        self.deleted = True
        self.date_deleted = timezone.now()
        self.save()

    @property
    def answer_options_parsed(self):
        options_str = self.answer_options or ''
        options = options_str.split('~')
        return [o.strip() for o in options]


class TemplateCopy(Model):
    template = ForeignKey(Template, on_delete=CASCADE)
    label = CharField(max_length=CHAR_MED, null=True)
    date_added = DateTimeField(auto_now_add=True)
    deleted = BooleanField(default=False)
    date_deleted = DateTimeField(null=True)

    def mark_deleted(self):
        self.deleted = True
        self.date_deleted = timezone.now()
        self.save()


class Answer(Model):
    template_copy = ForeignKey(TemplateCopy, on_delete=CASCADE)
    prompt = ForeignKey(Prompt, on_delete=CASCADE)
    response = CharField(max_length=CHAR_LARGE, null=True)
    comments = CharField(max_length=CHAR_LARGE, null=True)
    date_added = DateTimeField(null=True)

    def store_value(self, the_response):
        self.response = the_response
        self.date_added = timezone.now()
        self.save()
