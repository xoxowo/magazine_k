from django.test import Client, TestCase

from .models import Review
from users.models import User
from products.models import Category,Product,ProductImage

class ReviewTest(TestCase):
    def setUp(self):
        
        User.objects.create(
            id = 1,
            username = 'user1',
            password = 'cnstlr!',
            name = '춘식',
            zip_code = 12345,
            address_line_1 = '서울광역시 강남구',
            address_line_2 = 'aaa빌딩',
            phone_number = '010',
            email = 'aaa@kakao.com',
            # point = 100000
        )
        
        Category.objects.create(
            id =1,
            name = "book",
        )
        
        Product.objects.create(
            id = 1,
            title = "죠르디 24시",
            price = 22000,
            language = "KOREAN",
            size = "155 x 155 mm",
            pages = 860,
            published_date = "2020.09.25",
            isbn="979-11-6036-118-6",
            description = "죠르디의 일상을 담은 숏툰집 <죠르디 24시>는 카카오 페이지릍 통해 \
                            연재된 숏툰과 죠르디 회사 생활에 대한 스핀오프 내용을 담은 책이다.",
            issue_number=2,
            product_image_url="www.ccc.fef",
            main_category_id = 1,
        )
        
        Product.objects.create(
            id = 2,
            title = "TEA",
            price = 18000,
            language = "KOREAN",
            size = "170 x 240 mm",
            pages = 168,
            published_date = "2023.03.06",
            isbn="979-11-9810-853-1",
            description = "뜨거운 물에 차나무잎을 우려낸 음료인 차(茶)는  \
                            수천 년 역사를 기반으로 지역과 시대의 문화를 반영하며 독자적 기호 식품으로 발달해왔습니다.",
            issue_number=2,
            product_image_url="www.ccc.ffff",
            main_category_id = 1,
        )
        
        Review.objects.create(
            id = 1,
            user_id = 1,
            product_id =1,
            content="구매한 책 아주 마음에 들어요.",
            rating=5
        )
        
        Review.objects.create(
            id = 2,
            user_id = 1,
            product_id =2,
            content="책의 내용이 아주 흥미로워요",
            rating=4
        )
    
    
    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Review.objects.all().delete()
        
    
    def test_product_review_view(self):
        client = Client()
        response = client.get('/products/<int:product_id>/reviews')
        
        self.assertEqual(response.json(),
                        {
                            'Results': 
                                {
                                'review'  : 1,
                                'username': "user1",
                                'content' : "구매한 책 아주 마음에 들어요.",
                                'rating'  : 5,
                                }
  
                        }
                        )
        self.assertEqual(response.status_code, 200)