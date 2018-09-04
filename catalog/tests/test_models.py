from django.test import TestCase
from ..models import Author


class AuthorModelTest(TestCase):
    # 用于类级别设置，在测试运行开始的时侯，会调用一次。可以使用它来创建在任何测试方法中，都不会修改或更改的对象。
    @classmethod
    def setUpTestData(cls):
        # print('setUpTestData: Run once to set up non-modified data for all class method.')
        Author.objects.create(first_name='Big', last_name='Bang')

    # 在每个测试函数之前被调用，以设置可能被测试修改的任何对象（每个测试函数，都将获得这些对象的 “新” 版本）
    # def setUp(self):
    #     print('setUp: Run once for every method to set up clean data.')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '%s, %s'%(author.last_name, author.first_name)
        self.assertEqual(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')