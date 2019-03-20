from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings as site_settings

from django.db.models.signals import post_save


# TODO: all signals manipulations should store in separate file.
#  Move it if you want to use signals in this project.
def user_saved(sender=None, instance=None, **kwargs):
    pass


# connect all interesting user signals to this model like this:
post_save.connect(user_saved, sender=site_settings.AUTH_USER_MODEL)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, first_name, last_name, middle_name, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        user = self.model(username=username,
                          email=email,
                          first_name=self.model.normalize_name(first_name),
                          last_name=self.model.normalize_name(last_name),
                          middle_name=self.model.normalize_name(middle_name),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password, first_name, last_name, middle_name='', **extra_fields):
        extra_fields['is_staff'] = False
        extra_fields['is_superuser'] = False

        return self._create_user(username, email, password, first_name, last_name, middle_name, **extra_fields)

    def create_superuser(self, username, email, password, first_name='Site', last_name='Admin', middle_name='', **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(username, email, password, first_name, last_name, middle_name, **extra_fields)

    def check_username_existence(self, user_name):
        return self.filter(username=user_name).exists()

    def check_email_taken(self, email):
        return self.filter(email=email).exists()


class CustomUser(AbstractUser):
    # TODO: add image field for user))
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    middle_name = models.CharField(_("middle name"), max_length=50, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=False if site_settings.ENABLE_EMAIL_CONFIRMATION else True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = CustomUserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        if self.middle_name != '':
            full_name = '{} {}'.format(full_name, self.middle_name)

        return full_name.strip()

    def email_activation_code(self, **kwargs):
        # TODO: realize this functionality.
        pass
        # subject = "Активация вашего аккаунта на сайте {}.".format(site_settings.SITE_NAME)
        # self.send_mail(...)

    @classmethod
    def normalize_name(cls, name):
        if not isinstance(name, str):
            name = str(name)
        return name.strip().capitalize()
