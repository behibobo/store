from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField


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

    def __str__(self):
        return self.user.username

class Upload(models.Model):
    file_path = models.ImageField(blank=True)

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
    title = models.CharField(max_length=150, blank=True, null=True)
    keywords = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    extra = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title

class Brand(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    image = models.CharField(max_length=300)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    order = models.IntegerField(default=1)
    image = models.CharField(max_length=300 ,blank=True, null=True,)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="children")
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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
    slug = models.SlugField()
    description = models.TextField()

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_variations = models.ManyToManyField(ItemVariation)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{} of {}".format(self.quantity, self.item.name)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
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
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class Province(models.Model):
    name = models.CharField(max_length=200)

class City(models.Model):
    province = models.ForeignKey(Province,
                             on_delete=models.CASCADE)    
    name = models.CharField(max_length=200)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
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

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.pk


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
