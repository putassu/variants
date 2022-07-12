from django.db import models
from django.urls import reverse, reverse_lazy
import uuid
import datetime
from django.contrib.auth.models import User
from django.utils.html import format_html
from django import forms
app_name = 'varbase'
class Case(models.Model):
    """
    Model representing a patient
    """
    id = models.AutoField(primary_key=True,help_text="ID")
    IID = models.CharField("Внутренний ID образца",max_length=25)
    Lab_ID = models.CharField("Лабораторный номер",max_length=25)
    Composition = models.CharField("Состав исследования", max_length=200)
    Method = models.CharField("Метод исследования", max_length=200)
    Pathology = models.CharField("Патологические мутации", max_length=100)
    Platform = models.CharField("Платформа", max_length=170)
    Result = models.TextField("Результат", max_length=500)
    status = models.BooleanField("Статус")
    date = models.DateField("Дата изменения", default=datetime.date.today)
    class Meta:
        ordering = ["IID"]
        verbose_name_plural = 'Случаи'
        verbose_name = 'случай'
    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s %s (%s) г.р.' % (self.Lab_ID,self.status, self.date)


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('varbase:case-detail', args=[str(self.id)])


class Variant(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """

    id = models.AutoField(primary_key=True, help_text="ID варианта")
    id_с = models.ForeignKey('Case',verbose_name="ID случая",on_delete=models.SET_NULL, null=True)
    locus = models.ForeignKey('Locus',verbose_name="Локус", null=True, help_text="Выберите локус",on_delete=models.SET_NULL)
    alleles = models.ForeignKey('Alleles',verbose_name="Аллели", null=True, help_text="Выберите пару REF-ALT",on_delete=models.SET_NULL)
    ZIG=[(0,'0/1'),(1,'1/1'),(2,'1/2'),(3,'0/2'),(4,'0/0'),(5,'0/3'),(6,'2/3'),(7,'1/3'),(8,'0/4'),(9,'1/4'),(10,'3/4')]
    zig = models.CharField('Зиготность',max_length=3, choices=ZIG, blank=True, help_text='Выберите зиготность')
    VUS = [(0,'Pathogenic'),(1,'Likely pathogenic'),(2,'Uncertain significance'),(3,'Likely benign'),(4,'Benign')]
    vus = models.CharField('Variants of Uncertain Significance',max_length=50, choices=VUS, blank=True, help_text='Оценка патологичности варианта')
    user_id = models.ForeignKey(User,verbose_name="Пользователь", on_delete=models.SET_NULL, null=True, help_text="Имя пользователя")
    date = models.DateField(("Дата изменения"), default=datetime.date.today)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = 'Варианты'
        verbose_name = 'вариант'

    def __str__(self):
        """
        String for representing the Model object
        """
        try:
            fn = self.id_с.Lab_ID
        except:
            fn = 'Здесь ничего нет'
        return '%s (%s) ' % (self.date,fn)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        # print(reverse('catalog:case-detail', args=[str(self.id)]))
        return f'/{app_name}/variant-{self.id}/'


class Alleles(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.AutoField(primary_key=True, help_text="ID варианта")
    allele = models.CharField('REF-ALT',max_length=150, blank=True, help_text='["REF","ALT"]')
    user_id = models.ForeignKey(User,verbose_name="Пользователь", on_delete=models.SET_NULL, null=True, help_text="Имя пользователя")
    date = models.DateField(("Дата изменения"), default=datetime.date.today)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = 'REF-ALT'
        verbose_name = 'REF-ALT'

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.date, self.allele)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        # print(reverse('catalog:case-detail', args=[str(self.id)]))
        return f'/{app_name}/allele-{self.id}/'


class Locus(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.AutoField(primary_key=True, help_text="ID варианта")
    locus = models.CharField('Локус',max_length=25, blank=True, help_text='chr:position')
    user_id = models.ForeignKey(User,verbose_name="Пользователь", on_delete=models.SET_NULL, null=True, help_text="Имя пользователя")
    date = models.DateField("Дата изменения", default=datetime.date.today)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = 'Локусы'
        verbose_name = 'Локус'

    def __str__(self):
        """
        String for representing the Model object
        """
        try:
            fn = self.id
        except:
            fn = 'Здесь ничего нет'
        return '%s (%s) %' % (self.date,fn,self.locus)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        # print(reverse('catalog:case-detail', args=[str(self.id)]))
        return f'/{app_name}/locus-{self.id}/'