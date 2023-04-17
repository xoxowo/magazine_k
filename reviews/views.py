import json
import boto3
import uuid

from enum                       import Enum

from django.views               import View
from django.http                import JsonResponse

from core.utils.login_decorator import login_decorator

from reviews.models             import Review
from products.models            import Product
from orders.models              import Order, OrderItem, OrderStatus

from my_settings                import *

class OrderStatusEnum(Enum):
    CART                   = 1
    BEFORE_DEPOSIT         = 2
    PREPARING_FOR_DELIVERY = 3
    SHIPPING               = 4
    DELIVERY_COMPLETED     = 5
    EXCHANGE               = 6
    RETURN                 = 7



class ReviewView(View):
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    
    @login_decorator
    def post(self, request, product_id):
        try:
            data     = request.POST
            user     = request.user
            content  = data['content']
            rating   = data['rating']
            filename = request.FILES.get('filename')
            url      = str(uuid.uuid4())
            orderd_products = OrderItem.objects.filter(order__user=user, order__order_status=OrderStatusEnum.DELIVERY_COMPLETED.value, product_id=product_id)

            if not orderd_products.exists():
                return JsonResponse({'Message':'Invalid_Request'}, status=401)
                
            Review.objects.create(
                user       = user,
                content    = content,
                rating     = rating,
                product_id = product_id,
                photo_url = "https://magazine-k.s3.ap-northeast-2.amazonaws.com/"+url
            )
            
            if filename != None :
                self.s3_client.upload_fileobj(
                    filename,
                    AWS_STORAGE_BUCKET_NAME,
                    url
                )
            
            return JsonResponse({'Message':'Success', 'filename':filename}, status=201)
        except KeyError:
            return JsonResponse({'Message':'Key_Error'}, status=400)

    def get(self, request, product_id):
        try:
            reviews = Review.objects.filter(product_id=product_id)

            results = [{
                        'review'  : review.id,
                        'username': review.user.username,
                        'content' : review.content,
                        'rating'  : review.rating,
                        'photo'   : review.photo_url,
                        }for review in reviews]
            return JsonResponse({'Results':results}, status=200) 
        
        except Product.DoesNotExist:
            return JsonResponse({'Message':'Invalid_Request'}, status=404)         

    @login_decorator
    def delete(self, request, product_id, review_id):
        try:
            user   = request.user
            review = Review.objects.get(id=review_id, user=user, product=product_id)

            review.delete()
            return JsonResponse({'Message':'Success'}, status=204)

        except Review.DoesNotExist:
            return JsonResponse({'Message':'Invalid_Review'}, status=401)