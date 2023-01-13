import os

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Product, Category
from .views import CategoryViewSet, ProductViewSet
from django.contrib.auth import get_user_model
User = get_user_model()


class CategoryTest(APITestCase):
    """
    testing category
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.user = self.setup_user()

    @staticmethod
    def setup_category():
        list_of_category = [Category('category1'), Category('category2'), Category('category3')]
        Category.objects.bulk_create(list_of_category)

    @staticmethod
    def setup_user():
        return User.objects.create_user('test@gmail.com', '1', is_active=True)

    def test_get_category(self):
        request = self.factory.get('/api/v1/product/category/')
        view = CategoryViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200
        assert Category.objects.count() == 3
        assert Category.objects.first().title == 'category1'

    def test_post_category(self):
        data = {'title': 'test'}
        request = self.factory.post('/api/v1/product/category/', data)
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == 201


class ProductTest(APITestCase):
    """
    testing product
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.user = self.setup_user()
        self.setup_product()
        self.access_token = self.setup_user_token()

    @staticmethod
    def setup_category():
        Category.objects.create(title='test_product')

    @staticmethod
    def setup_user():
        return User.objects.create_user('test@gmail.com', '1', is_active=True)

    def setup_user_token(self):
        data = {
            'email': 'test@gmail.com',
            'password': '1'
        }
        request = self.factory.post('/api/v1/account/login/', data)
        view = TokenObtainPairView.as_view()
        response = view(request)
        return response.data['access']

    def setup_product(self):
        products = [Product(owner=self.user, category=Category.objects.first(), price=20, image='test', title='test'),
                    Product(owner=self.user, category=Category.objects.first(), price=20, image='test', title='test')]
        Product.objects.bulk_create(products)

    def test_get_product(self):
        request = self.factory.get('/api/v1/product/')
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200

    def test_post_product(self):
        import os
        image = open('media/images/22.png', 'rb')
        data = {'owner': self.user.id,
                'category': Category.objects.first().title,
                'title': 'test_product',
                'price': 20,
                'image': image
                }
        request = self.factory.post('/api/v1/product/product/', data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        view = ProductViewSet.as_view({'post': 'create'})
        response = view(request)
        image.close()
        remove_image = response.data.get('image').split('/')[-1]
        path = os.path.join(os.path.abspath(os.path.dirname('/home/hello/Desktop/makers/Django/last_project/media/images/')), f'{remove_image}')
        os.remove(path)
        assert response.status_code == 201