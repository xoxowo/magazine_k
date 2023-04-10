import json
import jwt

from django.test import Client, TestCase, TransactionTestCase
from unittest.mock import patch

from .models import Review
from users.models import User
from products.models import Category,Product,ProductImage

from my_settings import ALGORITHM,SECRET_KEY;

class ReviewTest(TransactionTestCase):
    def setUp(self):
        
        User.objects.create(
            id = 1,
            username = 'ddd',
            password = '123Qwe!!',
            name = 'aa',
            email = 'aaa@kakao.com'
            # point = 100000
        )
        
        Category.objects.create(
            id =1,
            name = "book",
        )
        
        Product.objects.create(
            id = 1,
            title = "job",
            price = 22000,
            language = "KOREAN",
            size = "155 x 155 mm",
            pages = 860,
            published_date = "2020.09.25",
            isbn="979-11-6036-118-6",
            description = "how can I use this?",
            issue_number=2,
            product_image_url="www.ccc.fef",
            main_category_id = 1,
        )
        
        Review.objects.create(
            id = 1,
            user_id = 1,
            product_id =1,
            content="this is very nice",
            rating=5.0
        )
    
    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Review.objects.all().delete()
    
    def test_product_review_view(self):
        client = Client()
        
        response = client.get('/products/1/reviews')
        
        self.assertEqual(response.json(), 
                       {'Results': [{'content': 'this is very nice',
                                     'rating': '5.0',
                                     'review': 1,
                                     'username': 'ddd'}]})
        self.assertEqual(response.status_code, 200)
        
    def test_fali_product_review_post_view(self):

        payload = {'id' : User.objects.get(id=1).id}
        token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        client  = Client()
        header  = {'HTTP_Authorization' : token}
        
        body = {
                "content":"dfsee",
                "rating" :"3.0"
                }

        response = client.post('/products/1/reviews', json.dumps(body), content_type='application/json', **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'Message': 'Invalid_Request'})
    