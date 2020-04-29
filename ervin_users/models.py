from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class ErvinUser(AbstractUser):
    verbose_name = 'user'

class ErvinGroup(Group):

    grp_order = models.IntegerField('Order Number', default=1, help_text='Where this group should appear on a list')

    class Meta:
        verbose_name='group'
        ordering = ['grp_order']


# vim: ai ts=4 sts=4 et sw=4
