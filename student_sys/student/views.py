from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from .forms import StudentForm
from .models import Student


def index(request):
    # students = Student.objects.all()
    students = Student.get_all()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = StudentForm()
    context = {
        'students': students,
    }
    return render(request, 'student/index.html', context=context)


class IndexView(View):
    template_name = 'student/index.html'

    def get_context(self):
        students = Student.get_all()
        context = {
            'students': students,
        }
        return context

    def get(self, request):
        context = self.get_context()
        form = StudentForm()
        context.update({        # 根据字典更新context
            'form': form
        })
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('student:index'))
        context = self.get_context()
        context.update({        # 根据字典更新context
            'form': form
        })
        return render(request, self.template_name, context=context)
