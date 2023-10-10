from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError("Users must have an phone number")

        user = self.model( phone_number=phone_number,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone_number,
            password=password,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=" ادرس ایمیل",
        max_length=255,
        unique=True,
        null=True,blank=True
    )
    phone_number=models.CharField(max_length=12,verbose_name='شماره تلفن',unique=True,)
    username=models.CharField(max_length=30,verbose_name='نام کاربری',unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False,verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = "phone_number"


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'