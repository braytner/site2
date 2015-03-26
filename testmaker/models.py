# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

class Test(models.Model):
    name = models.CharField(verbose_name=u"Тест",max_length=600)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    def get_url(self):

        first_question = Question.objects.filter(test=self)[:1]
        if first_question.count():
            return reverse('detail', args=(first_question[0].id,))
        else:
            return reverse('index')
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Тест"

class TestResultOption(models.Model):
    test = models.ForeignKey('Test')
    low_score = models.IntegerField()
    high_score = models.IntegerField()
    description = models.CharField(max_length = 600)  

    class Meta:
        ordering = ['high_score']


class Question(models.Model):
    test = models.ForeignKey('Test')
    text = models.CharField(verbose_name=u"Запитання",max_length=600)
    order = models.IntegerField()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Запитання"

class Answer(models.Model):
    question = models.ForeignKey('Question')
    text = models.CharField(verbose_name=u"Відповідь",max_length=200)
    score = models.IntegerField(default=0) 
    order = models.IntegerField()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Відповідь"

class TestUser(models.Model):
    name = models.CharField(verbose_name=u"Прізвище, Ім'я, По батькові", max_length=600)
    group = models.CharField(verbose_name=u"Група",max_length=100)

    class Meta:
         verbose_name_plural = "Студенти"

    cont = 'cont'
    exp = 'exp'
    group_type_choices = (
        (cont, u'Контрольна'),
        (exp, u'Експериментальна'),
    )
    group_type = models.CharField(verbose_name=u"Тип групи",max_length=10, choices=group_type_choices)

    begin = 'begin'
    end = 'end'    
    test_type_choices = (
        (begin, u'Початок'),
        (end, u'Кінець'),
    )
    test_type = models.CharField(verbose_name=u"Тип тестування",max_length=10, choices=test_type_choices)      

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('set_user', kwargs={'user_id':self.id})

    
class UserAnswer(models.Model):
    user = models.ForeignKey('TestUser')
    question = models.ForeignKey('Question')
    answer = models.ForeignKey('Answer')

    def __unicode__(self):
        return unicode(self.user) + ' - ' + unicode(self.question) + ' - ' + unicode(self.answer)

    class Meta:
        unique_together = ("user", "answer", "question")
        verbose_name_plural = "Відповіді студентів"