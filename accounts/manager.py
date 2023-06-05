from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None,   **extra_fields):
        if not email:
            raise ValueError('کاربر باید ادرس ایمیل داشته باشد')

        account = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        account.set_password(password)
        account.save(using=self._db)

        return account

    def create_superuser(self, email, username, password, **extra_fields):
        account = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            **extra_fields
        )

        account.is_admin = True
        account.save(using=self._db)

        return account
