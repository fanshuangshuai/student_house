from django.test import TestCase, Client

# Create your tests here.
from .models import Student


class StudentTestCase(TestCase):
    def setUp(self):
        '''setUp()创建一条测试数据'''
        Student.objects.create(
            name='the5fire',
            sex=1,
            email='test@qq.com',
            profession='coder',
            qq='333',
            phone='222',
        )

    # Model层测试
    def test_create_and_sex_show(self):
        '''测试数据创建以及sex的展示'''
        student = Student.objects.create(
            name='huyang',
            sex=1,
            email='qq@qq.com',
            profession='coder',
            qq='333',
            phone='222',
        )
        self.assertEqual(student.sex_show, '男', '性别字段跟内容不一致！')

    def test_filter(self):
        '''测试查询是否可用'''
        student = Student.objects.create(
            name='huyang',
            sex=1,
            email='qq@qq.com',
            profession='coder',
            qq='333',
            phone='222',
        )
        name='the5fire'
        student = Student.objects.filter(name=name)
        self.assertEqual(student.count(), 1, '应该只存在一个名称为{}的记录'.format(name))

    def test_get_index(self):
        '''GET测试首页的可用性'''
        client = Client()
        response = client.get('/student/')
        self.assertEqual(response.status_code, 200, 'status code must be 200!')

    def test_for_student(self):
        '''提交数据，然后请求首页，检查数据是否存在'''
        client = Client()
        data = dict(
            name='test_for_post',
            sex=1,
            email='333@qq.com',
            profession='coder',
            qq='333',
            phone='222',
        )
        response = client.post('/student/', data)
        self.assertEqual(response.status_code, 302, 'status code must be 302!')

        response = client.get('/student/')
        self.assertTrue(b'test_for_post' in response.content,
                        'response content must contain `test_for_post`')