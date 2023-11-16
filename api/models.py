'''Contains the definition of the models used in the appCRUD application'''
from django.db import models


class User(models.Model):
    '''Definition of User model'''
    user = models.CharField(verbose_name="User", max_length=50) 
    last_name = models.CharField(verbose_name="Last Name", max_length=50)
    password = models.CharField(verbose_name="Password", max_length=50)

    def __str__(self):
        return f"Id: {self.id} User: {self.user}"

    class Meta:
        '''Metadata for Persona model'''
        db_table = "User"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["id"]


class Auth(models.Model):
    """ Definition of Auth model """
    is_disabled = models.BooleanField(default=False)
    token = models.TextField("Token", max_length=10)

    class Meta:  
        """ Metadata for Auth model """
        db_table = "Auth"
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

        indexes = [
            models.Index(
                fields=["token"], name="auth_token_idx"
            )
        ]

    def __str__(self):
        return str(self.token)
