from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Vi_Dictionary(models.Model):
    vi_text = models.CharField(max_length=200, blank=False, default='')
    kanji_text = models.CharField(max_length=200, blank=True, default='')
    hiragana_text = models.CharField(max_length=200, blank=True, default='')
    katakana_text = models.CharField(max_length=200, blank=True, default='')
    example = models.CharField(max_length=200, blank=True, default='')
    description = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vi_text
    
    class Meta:
        db_table = 'dsvn_dictionary_vi_dictionary'

class Ja_Dictionary(models.Model):
    hiragana_text = models.CharField(max_length=200, blank=True, default='')
    kanji_text = models.CharField(max_length=200, blank=True, default='')
    katakana_text = models.CharField(max_length=200, blank=True, default='')
    vi_text = models.CharField(max_length=200, blank=True, default='')
    example = models.CharField(max_length=200, blank=True, default='')
    description = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hiragana_text

    class Meta:
        db_table = 'dsvn_dictionary_ja_dictionary'

class User(AbstractUser):
    # Delete not use field
    username = models.CharField(max_length=200, blank=True, default='')
    last_login = models.CharField(max_length=200, blank=True, default='')
    is_staff = models.CharField(max_length=200, blank=True, default='')
    is_superuser = models.CharField(max_length=200, blank=True, default='')

    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'auth_user'

class DsvnDictionary(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title