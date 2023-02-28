from django.test import Client, TestCase

from users.models import User

class JoinViewTest(TestCase):
    def setUp(self):
        client = Client()
        
        User.objects.create(
            id = 1,
            username = 'user1',
            password = 'cnstlr!',
            name = '춘식',
            zip_code = 12345,
            address_line_1 = '서울광역시 강남구',
            address_line_2 = 'aaa빌딩',
            phone_number = '010',
            email = 'aaa@kakao.com'
            # point = 100000
        )
        
        User.objects.create(
            id = 2,
            username = 'user2',
            password = 'fkdldjs!',
            name = '라이언',            
            zip_code = 12345,
            address_line_1 = '서울광역시 강남구',
            address_line_2 = 'aaa빌딩',
            phone_number = '0101222',
            email = 'bbb@kakao.com'
            # point = '100000'
        )
    
    def tearDown(self) :
        User.objects.all().delete()
        
    def user_join_success_test(self):
        client = Client()
        response = client.get('/member/join')
        
        self.assertEqual(response.json(),
                         {
                            'MESSAGE':'SUCCESS'
                         }
                         
                         )
        self.assertEqual(response.status_code, 201)
        
    def user_join_fail_test(self):
        client = Client()
        response = client.get('/member/join')
        
        self.assertEqual(response.json(),
                         {
                            'MESSAGE':'Already_Registered_User'
                         })
        self.assertEqual(response.status_code, 400)
        

class LoginViewTest(TestCase):
    def setUp(self):
        client = Client()
        
        User.objects.create(
            id = 1,
            username = 'user1',
            password = 'cnstlr!',
            name = '춘식',
            zip_code = 12345,
            address_line_1 = '서울광역시 강남구',
            address_line_2 = 'aaa빌딩',
            phone_number = '010',
            email = 'aaa@kakao.com'
            # point = 100000
        )
        
        User.objects.create(
            id = 2,
            username = 'user2',
            password = 'fkdldjs!',
            name = '라이언',            
            zip_code = 12345,
            address_line_1 = '서울광역시 강남구',
            address_line_2 = 'aaa빌딩',
            phone_number = '0101222',
            email = 'bbb@kakao.com'
            # point = '100000'
        )
    
    def tearDown(self) :
        User.objects.all().delete()
        
    def user_login_success_test(self):
        client = Client()
        response = client.get('/member/login')
        
        self.assertEqual(response.json(),
                         {
                            'MESSAGE':'SUCCESS',
                            'AUTHORIZATION': 'access_token'
                         }                         
                         )
        self.assertEqual(response.status_code, 200)

    def user_login_fail_test(self):
        client = Client()
        response = client.get('/member/login')
        
        self.assertEqual(response.json(),
                         {
                            'MESSAGE':'INVALID_USER'
                         }
                         )
        self.assertEqual(response.status_code, 401)