import os
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from faker import Faker
import requests
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

from apps.product.models import (
    Category, Product, ProductImage, Size, Color,
    ProductVariant, Review, Collection, Offer
)

fake = Faker(['ar_EG', 'ar_AA'])

class Command(BaseCommand):
    help = 'Generates test data for the product app'

    def add_arguments(self, parser):
        parser.add_argument('--products', type=int, default=50, help='Number of products to create')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before generating new data')

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('All product data cleared.'))

        self.create_categories()
        self.create_sizes()
        self.create_colors()
        
        num_products = options['products']
        for _ in range(num_products):
            product = self.create_product()
            self.create_product_images(product)
            self.create_product_variants(product)
            self.create_reviews(product)

        self.create_collections()
        self.create_offers()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_products} products and related data.'))

    def clear_data(self):
        """Clear all existing product data"""
        Review.objects.all().delete()
        ProductVariant.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Size.objects.all().delete()
        Color.objects.all().delete()
        Collection.objects.all().delete()
        Offer.objects.all().delete()

    def create_categories(self):
        """Create main categories and subcategories"""
        self.stdout.write('Creating categories...')
        
        # Main categories
        men_category = Category.objects.create(
            name='Men', 
            name_ar='رجالي',
            name_en='Men',
            slug='men',
            is_active=True
        )
        
        women_category = Category.objects.create(
            name='Women', 
            name_ar='نسائي',
            name_en='Women',
            slug='women',
            is_active=True
        )
        
        kids_category = Category.objects.create(
            name='Kids', 
            name_ar='أطفال',
            name_en='Kids',
            slug='kids',
            is_active=True
        )
        
        # Subcategories for Men
        men_subcategories = [
            ('Shirts', 'قمصان', 'shirts'),
            ('Pants', 'بناطيل', 'pants'),
            ('Shoes', 'أحذية', 'shoes'),
            ('Accessories', 'إكسسوارات', 'accessories'),
        ]
        
        for name_en, name_ar, slug in men_subcategories:
            Category.objects.create(
                name=name_en, 
                name_ar=name_ar,
                name_en=name_en,
                slug=slug,
                parent=men_category,
                is_active=True
            )
        
        # Subcategories for Women
        women_subcategories = [
            ('Dresses', 'فساتين', 'dresses'),
            ('Blouses', 'بلوزات', 'blouses'),
            ('Pants', 'بناطيل', 'women-pants'),
            ('Bags', 'حقائب', 'bags'),
        ]
        
        for name_en, name_ar, slug in women_subcategories:
            Category.objects.create(
                name=name_en, 
                name_ar=name_ar,
                name_en=name_en,
                slug=slug,
                parent=women_category,
                is_active=True
            )
        
        # Subcategories for Kids
        kids_subcategories = [
            ('Boys', 'ملابس أولاد', 'boys'),
            ('Girls', 'ملابس بنات', 'girls'),
            ('Shoes', 'أحذية أطفال', 'kids-shoes'),
        ]
        
        for name_en, name_ar, slug in kids_subcategories:
            Category.objects.create(
                name=name_en, 
                name_ar=name_ar,
                name_en=name_en,
                slug=slug,
                parent=kids_category,
                is_active=True
            )
        
        self.stdout.write(self.style.SUCCESS('Categories created successfully.'))

    def create_sizes(self):
        """Create sizes for products"""
        self.stdout.write('Creating sizes...')
        
        # Adult sizes
        adult_sizes = [
            ('XS', 'إكس إس'),
            ('S', 'إس'),
            ('M', 'إم'),
            ('L', 'إل'),
            ('XL', 'إكس إل'),
            ('XXL', 'إكس إكس إل'),
        ]
        
        for name, name_ar in adult_sizes:
            Size.objects.create(name=name, name_ar=name_ar)
        
        # Kids sizes
        kids_sizes = [
            ('2', '٢'),
            ('4', '٤'),
            ('6', '٦'),
            ('8', '٨'),
            ('10', '١٠'),
            ('12', '١٢'),
            ('14', '١٤'),
        ]
        
        for name, name_ar in kids_sizes:
            Size.objects.create(name=name, name_ar=name_ar)
        
        self.stdout.write(self.style.SUCCESS('Sizes created successfully.'))

    def create_colors(self):
        """Create colors for products"""
        self.stdout.write('Creating colors...')
        
        colors = [
            ('Black', 'أسود', '#000000'),
            ('White', 'أبيض', '#FFFFFF'),
            ('Red', 'أحمر', '#FF0000'),
            ('Blue', 'أزرق', '#0000FF'),
            ('Green', 'أخضر', '#008000'),
            ('Yellow', 'أصفر', '#FFFF00'),
            ('Brown', 'بني', '#A52A2A'),
            ('Grey', 'رمادي', '#808080'),
            ('Beige', 'بيج', '#F5F5DC'),
            ('Navy', 'كحلي', '#000080'),
        ]
        
        for name, name_ar, code in colors:
            Color.objects.create(name=name, name_ar=name_ar, code=code)
        
        self.stdout.write(self.style.SUCCESS('Colors created successfully.'))

    def get_random_image_url(self, category):
        """Get a random image URL based on category"""
        base_url = "https://source.unsplash.com/300x400/?"
        
        if category.slug in ['shirts', 'blouses']:
            return f"{base_url}shirt"
        elif category.slug in ['pants', 'women-pants']:
            return f"{base_url}pants"
        elif category.slug in ['shoes', 'kids-shoes']:
            return f"{base_url}shoes"
        elif category.slug == 'dresses':
            return f"{base_url}dress"
        elif category.slug == 'bags':
            return f"{base_url}bag"
        elif category.slug == 'accessories':
            return f"{base_url}accessory"
        elif category.slug in ['boys', 'girls']:
            return f"{base_url}kids+clothes"
        else:
            return f"{base_url}fashion"

    def download_image(self, url):
        """Download image from URL and convert to Django ContentFile"""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                return ContentFile(img_io.getvalue(), name=f"product_{random.randint(1000, 9999)}.jpg")
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error downloading image: {e}'))
            return None

    def create_product(self):
        """Create a random product"""
        # Get random category
        categories = Category.objects.filter(parent__isnull=False)
        category = random.choice(categories)
        
        # Determine product name based on category
        name_ar = fake.word()
        if category.parent.slug == 'men':
            name_ar = f"{name_ar} رجالي"
            name_en = f"Men's {fake.word().capitalize()}"
        elif category.parent.slug == 'women':
            name_ar = f"{name_ar} نسائي"
            name_en = f"Women's {fake.word().capitalize()}"
        elif category.parent.slug == 'kids':
            name_ar = f"{name_ar} أطفال"
            name_en = f"Kids' {fake.word().capitalize()}"
        
        # Generate price
        price = random.randint(100, 2000)
        
        # Determine if product has a discount
        has_discount = random.choice([True, False])
        old_price = None
        if has_discount:
            discount_percentage = random.choice([10, 15, 20, 25, 30, 40, 50])
            old_price = price + (price * discount_percentage / 100)
        
        # Create unique slug
        base_slug = slugify(name_en)
        unique_slug = f"{base_slug}-{random.randint(1000, 9999)}"
        
        # Create product
        product = Product.objects.create(
            name=name_en,
            name_ar=name_ar,
            name_en=name_en,
            slug=unique_slug,
            description=fake.paragraph(nb_sentences=3),
            description_ar=fake.paragraph(nb_sentences=3),
            description_en=fake.paragraph(nb_sentences=3),
            price=price,
            old_price=old_price,
            category=category,
            is_active=True,
            is_featured=random.choice([True, False]),
            is_new=random.choice([True, False]),
        )
        
        return product

    def create_product_images(self, product):
        """Create 1-4 images for a product"""
        num_images = random.randint(1, 4)
        
        for i in range(num_images):
            image_url = self.get_random_image_url(product.category)
            image_file = self.download_image(image_url)
            
            if image_file:
                ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    is_main=(i == 0)  # First image is the main image
                )

    def create_product_variants(self, product):
        """Create variants for a product"""
        try:
            # Get sizes based on category
            if product.category.parent.slug == 'kids':
                sizes = list(Size.objects.filter(name__in=['2', '4', '6', '8', '10', '12', '14']))
            else:
                sizes = list(Size.objects.filter(name__in=['S', 'M', 'L', 'XL']))
            
            # Limit to a random subset of sizes to avoid too many variants
            random.shuffle(sizes)
            selected_sizes = sizes[:random.randint(2, 3)]  # 2-3 sizes per product
            
            # Get random colors
            colors = list(Color.objects.all())
            random.shuffle(colors)
            variant_colors = colors[:random.randint(1, 3)]  # 1-3 colors per product
            
            # Create unique combinations of variants
            combinations = []
            for size in selected_sizes:
                for color in variant_colors:
                    combinations.append((size, color))
            
            # Shuffle and select a subset to ensure we don't hit unique constraints
            random.shuffle(combinations)
            selected_combinations = combinations[:random.randint(2, 4)]  # 2-4 variants per product
            
            # Create variants with unique combinations
            for size, color in selected_combinations:
                # Calculate variant price (may vary slightly from base product price)
                variant_price = product.price + random.randint(-50, 50)
                variant_price = max(10, variant_price)  # Ensure price is positive
                
                # Create variant with a unique SKU
                random_suffix = random.randint(1000, 9999)
                sku = f"{product.id}-{size.name}-{color.name}-{random_suffix}"
                
                # Check if this combination already exists
                if not ProductVariant.objects.filter(product=product, size=size, color=color).exists():
                    ProductVariant.objects.create(
                        product=product,
                        size=size,
                        color=color,
                        sku=sku,
                        price=variant_price,
                        stock=random.randint(0, 50),
                        is_active=True
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating variants for product {product.id}: {e}'))

    def create_reviews(self, product):
        """Create 0-5 reviews for a product"""
        num_reviews = random.randint(0, 5)
        
        for _ in range(num_reviews):
            Review.objects.create(
                product=product,
                name=fake.name(),
                email=fake.email(),
                rating=random.randint(1, 5),
                comment=fake.paragraph(nb_sentences=2),
                created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30)),
                is_approved=True
            )

    def create_collections(self):
        """Create collections and add products to them"""
        self.stdout.write('Creating collections...')
        
        collections_data = [
            ('Summer Collection', 'مجموعة الصيف', 'تشكيلة مميزة لصيف منعش', 'summer-collection'),
            ('Winter Essentials', 'أساسيات الشتاء', 'ملابس دافئة لفصل الشتاء', 'winter-essentials'),
            ('Formal Wear', 'ملابس رسمية', 'أناقة كلاسيكية للمناسبات الرسمية', 'formal-wear'),
            ('Casual Style', 'الأسلوب الكاجوال', 'أزياء مريحة للإطلالات اليومية', 'casual-style'),
        ]
        
        for name_en, name_ar, description_ar, slug in collections_data:
            # Create collection
            image_url = f"https://source.unsplash.com/800x600/?{slug.replace('-', '+')}"
            image_file = self.download_image(image_url)
            
            collection = Collection.objects.create(
                name=name_en,
                name_ar=name_ar,
                name_en=name_en,
                slug=slug,
                description=fake.paragraph(nb_sentences=2),
                description_ar=description_ar,
                description_en=fake.paragraph(nb_sentences=2),
                image=image_file,
                is_active=True
            )
            
            # Add random products to the collection
            products = list(Product.objects.all())
            random.shuffle(products)
            selected_products = products[:random.randint(5, 10)]
            
            collection.products.add(*selected_products)
        
        self.stdout.write(self.style.SUCCESS('Collections created successfully.'))

    def create_offers(self):
        """Create offers and add products to them"""
        self.stdout.write('Creating offers...')
        
        offers_data = [
            ('Summer Sale', 'تخفيضات الصيف', 'خصومات تصل إلى 50% على مجموعة مختارة من المنتجات', 30, 'summer-sale'),
            ('Special Discount', 'خصم خاص', 'عروض حصرية لفترة محدودة', 25, 'special-discount'),
            ('End of Season', 'نهاية الموسم', 'أسعار مخفضة على تشكيلة نهاية الموسم', 40, 'end-of-season'),
            ('Flash Sale', 'بيع سريع', 'عروض لمدة 24 ساعة فقط', 20, 'flash-sale'),
        ]
        
        # Define date ranges for offers
        now = timezone.now()
        
        for name_en, name_ar, description_ar, discount, slug in offers_data:
            # Create offer
            image_url = f"https://source.unsplash.com/800x600/?sale+{slug.replace('-', '+')}"
            image_file = self.download_image(image_url)
            
            start_date = now - timezone.timedelta(days=random.randint(1, 10))
            end_date = now + timezone.timedelta(days=random.randint(5, 30))
            
            offer = Offer.objects.create(
                title=name_en,
                title_ar=name_ar,
                title_en=name_en,
                slug=slug,
                description=fake.paragraph(nb_sentences=2),
                description_ar=description_ar,
                description_en=fake.paragraph(nb_sentences=2),
                discount_percentage=discount,
                image=image_file,
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )
            
            # Add products with discounts to the offer
            discounted_products = Product.objects.filter(old_price__isnull=False)
            if discounted_products.exists():
                random_products = random.sample(list(discounted_products), min(len(discounted_products), 10))
                offer.products.add(*random_products)
        
        self.stdout.write(self.style.SUCCESS('Offers created successfully.')) 