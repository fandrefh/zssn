from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Item(models.Model):
    name = models.CharField(_('Item'), max_length=150)
    points = models.PositiveIntegerField(_('Pontos'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Itens')
        ordering = ['id']

    def __str__(self):
        return self.name


class Survivor(models.Model):
    GENDER_CHOICES = (
        ('M', _('Masculino')),
        ('F', _('Feminino')),
    )
    name = models.CharField(_('Nome'), max_length=200)
    age = models.PositiveIntegerField(_('Idade'))
    gender = models.CharField(_('Sexo'), max_length=1, choices=GENDER_CHOICES)
    longitude = models.FloatField(_('Longitude'))
    latitude = models.FloatField(_('Latitude'))
    infected = models.BooleanField(_('Infectado?'), default=False)

    class Meta:
        verbose_name = _('Sobrevivente')
        verbose_name_plural = _('Sobreviventes')
        ordering = ['id']

    def __str__(self):
        return self.name


class Inventory(models.Model):
    survivor = models.ForeignKey(Survivor, verbose_name=_('Sobrevivente'), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name=_('Item'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Quantidade'))

    class Meta:
        verbose_name = _('Inventário')
        verbose_name_plural = _('Inventários')
        ordering = ['id']

    def __str__(self):
        return self.survivor.name
