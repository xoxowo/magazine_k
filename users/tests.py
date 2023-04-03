import json

from django.test import Client, TestCase

from users.models import User

class JoinViewTest(TestCase):
    def setUp(self):
        client = Client()
        
        User.objects.create(
            id = 1,
            username = 'd',
            password = 'cnstlr!',
            name = 'aa',
            email = 'aaa@kakao.com'
            # point = 100000
        )
        
    def tearDown(self):
        User.objects.all().delete()

    def test_success_login_user(self):
        client = Client()
        
        user = {
            'username' : 'dddd',
            'password' : '123Qwe!!',
            'name' :'dddd',
            'phone_number' : 8210123456,
            'email':'aaa@a.net',
        }
        
        response = client.post('/member/join', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESS'})
        self.assertEqual(response.status_code, 201)        

    def test_fail_login_user(self):
        client = Client()

        user1 = {
            'username' : 'dddd',
            'password' : '123Qwe',
            'name' :'dd',
            'phone_number' : 8210123456,
            'email':'a@a.net',
        }
        
        response = client.post('/member/join',  json.dumps(user1), content_type='application/json')
        
        self.assertEqual(response.json(),{'MESSAGE':'Invalid password format'})
        self.assertEqual(response.status_code, 400)