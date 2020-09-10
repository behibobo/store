from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.db.models import Q
from autoslug import AutoSlugField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFill

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    credit_based_user = models.BooleanField(default=False)
    credit = models.IntegerField(null=True, blank=True)
    credit_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UploadFile(models.Model):
    file_path = models.FileField(blank=True)

class Upload(models.Model):
    file_path = models.ImageField(blank=True)
    thumbnail = ImageSpecField(source='file_path', processors=[ResizeToFill(128, 128)], format='PNG', options={'quality': 70})

    def __str__(self):
        return self.file_path

class Option(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Spec(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Seo(models.Model):
    item_id = models.PositiveIntegerField()
    item_type = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    keywords = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    extra = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title

class Brand(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=1000, unique=True)
    image = models.CharField(max_length=300, blank=True, null=True,)
    display = models.BooleanField(default=True)
    doc = models.CharField(max_length=300, blank=True, null=True,)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=1000, unique=True)
    order = models.IntegerField(default=1)
    image = models.CharField(max_length=300 ,blank=True, null=True,)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="children")
    display = models.BooleanField(default=True)
    svg_icon = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_all_children(self, include_self=True):
        children = Q(pk=0)
        if include_self:
            children |= Q(pk=self.pk)
        for u in self.children.all():
            _r = u.get_all_children(include_self=True)
            if _r:
                children |= _r
        return children

    def get_top_most_parent(self):
        parents = Category.objects.filter(parent__isnull=True)
        for item in parents:
            ids = list(Category.objects.filter(item.get_all_children()).values_list("id", flat=True))
            if self.id in ids:
                return item.id

class Article(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    image = models.CharField(max_length=300, blank=True, null=True,)
    slug = models.CharField(max_length=1000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class CategorySpec(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='specs')
    spec = models.CharField(max_length=200)
    order = models.IntegerField(default=1)

    def __str__(self):
        return "{} - {}".format(self.category.name, self.spec)



class Item(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products",)
    slug = models.CharField(max_length=1000, unique=True)
    doc = models.CharField(max_length=300, blank=True, null=True,)
    description = models.TextField(blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=300)
    thumbnail = models.CharField(max_length=300, null=True, blank=True,)
    alt = models.CharField(max_length=300, blank=True, null=True,)
    title = models.CharField(max_length=300, blank=True, null=True,)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.item.name

class ItemSpec(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='specs')
    spec = models.CharField(max_length=200,blank=True, null=True,)
    value = models.CharField(max_length=200,blank=True, null=True,)

    def __str__(self):
        return "{} - {}".format(self.item.name, self.spec)

class Variation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='variations')
    stock = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,)
    reduced_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,)
    option_one = models.CharField(max_length=150,blank=True, null=True,)
    value_one = models.CharField(max_length=150,blank=True, null=True,)
    option_two = models.CharField(max_length=150,blank=True, null=True,)
    value_two = models.CharField(max_length=150,blank=True, null=True,)
    option_three = models.CharField(max_length=150,blank=True, null=True,)
    value_three = models.CharField(max_length=150,blank=True, null=True,)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.item.name

class ItemOption(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=150,blank=True, null=True,)
    value = models.CharField(max_length=150,blank=True, null=True,)

    def __str__(self):
        return self.item.name

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items')



class ItemVariation(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=150)
    attachment = models.ImageField(blank=True)

    class Meta:
        unique_together = (
            ('variation', 'value')
        )

    def __str__(self):
        return self.value


class OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{} of {}".format(self.quantity, self.variation.item.name)

    def get_total_item_price(self):
        return self.quantity * self.variation.price

    def get_total_discount_item_price(self):
        return self.quantity * self.variation.reduced_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.variation.reduced_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address',on_delete=models.SET_NULL, blank=True, null=True)
    
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for item in self.order_items.all():
            total += item.get_final_price()
        return total

class Province(models.Model):
    name = models.CharField(max_length=200)
class City(models.Model):
    province = models.ForeignKey(Province,
                             on_delete=models.CASCADE)    
    name = models.CharField(max_length=200)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    default = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Slider(models.Model):
    image = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)
    order = models.IntegerField(default=1)
    display = models.BooleanField(default=True)
    start_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.code

class Setting(models.Model):
    logo = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    keywords = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    ArticleCount = models.IntegerField(default=6)
    ItemCount = models.IntegerField(default=6)

    def __str__(self):
        return self.title

class Page(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)
    slug = models.CharField(max_length=1000, unique=True)
    content = models.TextField()
    image = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

class Menu(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    display = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.pk


class Tag(models.Model):
    item_id = models.PositiveIntegerField()
    item_type = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.title


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
