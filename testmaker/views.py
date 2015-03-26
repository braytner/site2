# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import redirect
from models import Test, Question, Answer, TestUser, UserAnswer
from django.db.models import Sum

class IndexView(generic.ListView):
    template_name = 'tests.html'
    context_object_name = 'tests'

    def get_queryset(self):
        
        return Test.objects.all()


def question_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user_id = request.session["user_id"]
    user = get_object_or_404(TestUser, pk=user_id)

    def redirect_to_next():
        next_question = Question.objects.filter(test=question.test, order__gt=question.order).exclude(useranswer__user=user_id)[:1]

        if next_question.count():
            return HttpResponseRedirect(reverse('detail', args=(next_question[0].id,)))
        else:
            return HttpResponseRedirect(reverse('test_result', args=(question.test_id,)))

    if UserAnswer.objects.filter(user=user_id, question=pk).count():
        return redirect_to_next()
    
    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer'])    
    except (KeyError, Answer.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question
        })
    else:

        UserAnswer.objects.create(user=user, question=question, answer=selected_answer)

        return redirect_to_next()

       
def set_user(reqeust, user_id):
    reqeust.session['user_id'] = user_id
    return HttpResponseRedirect(reverse('index'))

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return HttpResponseRedirect(reverse('user_add'))    



class UserCreate(generic.CreateView):
    template_name = 'user.html'
    model = TestUser
    fields = ['name', 'group', 'group_type', 'test_type']

def need_login(func):
    def as_view(request, *args, **kwargs):
        if not 'user_id' in request.session:
            return redirect('/signup')
        return func(request, *args, **kwargs)
    return as_view

def test_result(request, pk):
    user_id = request.session["user_id"]
    test = get_object_or_404(Test, pk=pk)
    user = get_object_or_404(TestUser, pk=user_id)

    result = get_test_result(user, test)

    return render(request, 'result.html', {
        'result': result['result'],
        'user': user,
        'test': test,
        'score': result['score']
    })

def report(request):

    if not request.user.is_superuser:
        return redirect('/admin')

    users = TestUser.objects.all()
    tests = Test.objects.all()

    result_users = []

    for user in users:
        u = user.__dict__
        u['kind'] = user.get_group_type_display() + ' - ' + user.get_test_type_display()

        u['tests'] = []

        for test in tests:
            result = get_test_result(user, test)
            if not result['score'] is None:
                t = {
                    'name': test.name,
                    'result': result
                }
                u['tests'].append(t)

        result_users.append(u)

    return render(request, 'report.html', {
        'users': result_users
    })

def get_test_result(user, test):

    score = UserAnswer.objects.filter(user=user, question__test=test).aggregate(Sum('answer__score'))['answer__score__sum']

    result = u'невідомий'

    for option in test.testresultoption_set.all():
        if score >= option.low_score and score <= option.high_score:
            result = option.description

    return {
        'score': score,
        'result': result
    }


    

    

