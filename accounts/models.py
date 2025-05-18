from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('ユーザーはメールアドレスを持つ必要があります')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.is_staff = True  # フィールド名を変更
        user.save(using=self._db)
        EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.is_staff = True  # フィールド名を変更
        user.is_superuser = True  # フィールド名を変更
        user.save(using=self._db)
        EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255, verbose_name='メールアドレス')
    first_name = models.CharField(max_length=30, verbose_name='名')
    last_name = models.CharField(max_length=30, verbose_name='姓')
    is_active = models.BooleanField(default=True, verbose_name='アクティブ')
    is_staff = models.BooleanField(default=False, verbose_name='スタッフ')
    is_superuser = models.BooleanField(default=False, verbose_name='管理者')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='登録日')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
    def __str__(self):
        return self.email

    def add_email_address(self, request, new_email):
        # ユーザーの新しいメールアドレスを追加し、メール確認を送信します。
        # 新しいメールアドレスが確認されるまで、古いメールアドレスはプライマリのままです。
        return EmailAddress.objects.add_email(request, self.user, new_email, confirm=True)
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = User.objects.get(pk=self.pk)
            if orig.email != self.email:
                if User.objects.filter(email=self.email).exists():
                    raise ValidationError('このメールアドレスはすでに使用されています。')
        super(User, self).save(*args, **kwargs)
        
@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # メールアドレスが確認されたら、新しいメールアドレスをプライマリに設定
    email_address.set_as_primary()
    # 古いメールアドレスを削除
    stale_addresses = EmailAddress.objects.filter(
        user=email_address.user).exclude(primary=True).delete()