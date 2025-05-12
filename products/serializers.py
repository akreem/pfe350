from django.db.models.aggregates import Avg
from rest_framework import serializers
from taggit.serializers import TagListSerializerField , TaggitSerializer
from .models import ProductImage, Product
from django.core.files import File
from django.conf import settings
import os
from django.core.files.base import ContentFile


from .models import Product , Brand , Review


class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'



class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ProductListSerializers(serializers.ModelSerializer):
    # brand = BrandListSerializers()  # Show all data off brand
    brand = serializers.StringRelatedField()   # show name of brand this product
    avg_rate = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
    
    def get_avg_rate(self, product):
        avg = product.review_product.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            return 0
        return avg['rate_avg']
    
    def get_review_count(self, product:Product):
        review = product.review_product.all().count()
        return review



class ProductDetailSerializers(TaggitSerializer,serializers.ModelSerializer):
    brand = BrandListSerializers()
    avg_rate = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    review = ReviewSerializers(source='review_product',many=True)
    tags = TagListSerializerField() 

    class Meta:
        model = Product
        fields = '__all__'
    
    def get_avg_rate(self, product):
        avg = product.review_product.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            return 0
        return avg['rate_avg']
    
    def get_review_count(self, product:Product):
        review = product.review_product.all().count()
        return review



class BrandDetailSerializers(serializers.ModelSerializer):
    products = ProductListSerializers(source='product_name', many=True)
    class Meta:
        model = Brand
        fields = '__all__'



class ProductCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','image','price']






class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    product_image = serializers.ListField(write_only=True)
    image = serializers.CharField(write_only=True)  # 👈 allow image path via API

    class Meta:
        model = Product
        exclude = []  # include everything else

    def create(self, validated_data):
        images_data = validated_data.pop('product_image', [])
        image_path = validated_data.pop('image', None)

        if not image_path:
            raise serializers.ValidationError({'image': 'This field is required.'})

        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
        if os.path.exists(full_image_path):
            with open(full_image_path, 'rb') as f:
                content = f.read()
            image_file = ContentFile(content, name=os.path.basename(full_image_path))
            validated_data['image'] = image_file
        else:
            raise serializers.ValidationError({'image': f"Image not found at {full_image_path}"})

        product = Product.objects.create(**validated_data)

        for img in images_data:
            rel_path = img.get('image')
            full_path = os.path.join(settings.MEDIA_ROOT, rel_path)

            if os.path.exists(full_path):
                with open(full_path, 'rb') as f:
                    content = f.read()
                file_obj = ContentFile(content, name=os.path.basename(full_path))
                ProductImage.objects.create(product=product, image=file_obj)
            else:
                raise serializers.ValidationError({'product_image': f"File not found: {rel_path}"})

        return product

