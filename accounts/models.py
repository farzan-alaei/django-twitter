from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,**extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields,
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser=True
        
        user.save(using=self._db)
        return user        
    
class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(_('username'),max_length=150,unique=True)
    first_name = models.CharField (_("firstname"),max_length=150,blank=True)
    last_name = models.CharField (_("lastname"),max_length=150,blank=True)
    email=models.EmailField(_("email"),unique=True)
    mobile=models.CharField(_("mobile"),max_length=11,unique=True,blank=True,null=True)
    is_staff=models.BooleanField(_("staff status"),default=False,help_text=_('show that user can login to panel admin or not'))
    is_active=models.BooleanField(_('active'),default=False,help_text=_('show that user can log in to website or not!'))
    date_joined=models.DateTimeField(_("date_joined"),default=timezone.now)
    image=models.ImageField(_('image'),blank=True)
    followers = models.ManyToManyField('self',related_name='follow',blank=True,symmetrical=False)
    following = models.ManyToManyField('self', related_name='fellow',blank=True,symmetrical=False)
    
    objects=MyUserManager()
    
    EMAIL_FIELD='email'
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def get_absolute_url(self):
        return reverse("accounts:update", kwargs={"pk": self.pk})
    

class UserFollowing(models.Model):
    
    
    user_id=models.ForeignKey(User,verbose_name=_("followings"),related_name='f',on_delete=models.CASCADE)
    
    following_user_id = models.ForeignKey("User",related_name='p',on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
