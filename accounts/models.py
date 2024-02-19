from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def _create_user(self,email,password,**others_fields):
        if not email : 
            raise ValueError("Users must have an email")
        user=self.model(
            email=self.normalize_email(email),**others_fields)
        user.set_password(password)
        others_fields.setdefault("is_staff", False)
        others_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None,**others_fields):
        others_fields.setdefault("is_staff", False)
        others_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **others_fields)

    def create_superuser(self,  email, password=None, **others_fields):
        others_fields.setdefault("is_staff", True)
        others_fields.setdefault("is_superuser", True)
        if others_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if others_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **others_fields)
        
    
class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField (_("firstname"),max_length=150,Blank=True)
    last_name = models.CharField (_("lastname"),max_length=150,Blank=True)
    email=models.EmailField(_("email"),unique=True)
    mobile=models.CharField(_("mobile"),unique=True,blank=True,null=True)
    is_staff=models.BooleanField(_("staff status"),default=False,help_text=_('show that user can login to panel admin or not'))
    is_active=models.BooleanField(_('active'),default=False,help_text=_('show that user can log in to website or not!'))
    date_joined=models.DateTimeField(_("date_joined"),default=timezone.now())
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