from django.contrib import admin
from models import Test, Question, Answer, TestUser, UserAnswer, TestResultOption

class TestResultOptionInline(admin.StackedInline):
    model = TestResultOption
    extra = 4

class TestAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    inlines = [TestResultOptionInline]

admin.site.register(Test, TestAdmin)

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = [ 'order', 'text' ]
    list_display_links = ('text',)
    list_filter = ('test',)
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)

class TestUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'group_type', 'test_type']
    list_filter = ('group',)  

admin.site.register(TestUser, TestUserAdmin)

admin.site.register(UserAnswer)