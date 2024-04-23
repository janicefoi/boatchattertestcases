class Boat(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='jsh/product_images/')
    category = models.CharField(max_length=50, choices=[
        ('fishing', 'Fishing Boats'),
        ('sail', 'Sail Boats'),
        ('yacht', 'Yachts'),
    ])
    brand = models.CharField(max_length=255, default='JSH')
    availability = models.BooleanField(default=True)
    accommodation = models.PositiveIntegerField(default=1)
    booking_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def is_available_on_date(self, selected_date):
        return self.availability and (self.booking_date is None or self.booking_date != selected_date)
