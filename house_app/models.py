import uuid
from datetime import datetime
from django.db import models


class Houses(models.Model):
    """
    Represents info about each House
    """
    house_id = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4)
    address = models.CharField(unique=True, max_length=100)
    build_year = models.PositiveSmallIntegerField(null=True)
    developer = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(
        default=datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z"))
    update_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.address

    class Meta:
        pass


class Flats(models.Model):
    """
    Represents info about each Flat
    """
    flat_id = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4)
    flat_number = models.PositiveSmallIntegerField(null=True)
    price = models.DecimalField(null=False, max_digits=12, decimal_places=2)
    rooms = models.PositiveSmallIntegerField()
    status = models.CharField()
    house = models.ForeignKey(Houses, verbose_name="Дом",
                              on_delete=models.CASCADE, related_name="related_house")

    def __str__(self):
        return f"This is flat #{self.flat_id}"

    class Meta:
        pass


class Users(models.Model):
    user_id = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4)
    email = models.EmailField()
    created_at = models.DateTimeField(
        default=datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z"))
    role = models.CharField(max_length=10)

    def __str__(self):
        return f"This is {self.email} user"

    class Meta:
        pass
