from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from .forms import HayulGrowthForm
from .models import HayulGrowth

# Create your views here.


def index(request: HttpRequest):
    return render(request, 'chart/index.html')


# @login_required(login_url='common:login')
# def show_chart(request: HttpRequest):
#     return render(request, 'chart/show_chart.html')


class ChartView(TemplateView):
    template_name = 'chart/show_chart.html'
    # 템플릿으로 차트 이름을 context로 넘겨주면 좋을 듯.


@login_required(login_url='common:login')
def get_data(request):
    objects = HayulGrowth.objects.all()
    data = {
        'result': [
            {'year_month': obj.year_month, 'height': obj.height, 'weight': obj.weight} for obj in objects
        ]
    }

    return JsonResponse(data)


class HayulGrowthListView(ListView):
    model = HayulGrowth


# FormView를 활용할 수도 있는데, 아래와 같이 CreateView가 더욱 간결함.
# 다만 템플릿 이름은 '모델명_form.html'
# class HayulGrowthFormView(FormView):
#     form_class = HayulGrowthForm
#     template_name = "chart/post_form.html"
#     success_url = reverse_lazy("chart:show_chart")

#     def get(self, request):
#         form = self.form_class
#         return render(request, self.template_name, {"form": form})

#     def form_valid(self, form) -> HttpResponse:
#         return super().form_valid(form)


class HayulGrowthCreateView(CreateView):
    model = HayulGrowth
    fields = ['year_month', 'height', 'weight']
    success_url = reverse_lazy("chart:growth_chart")


class HayulGrowthUpdateView(UpdateView):
    model = HayulGrowth
    fields = ['year_month', 'height', 'weight']
    success_url = reverse_lazy("chart:growth_chart")


class HayulGrowthDeleteView(DeleteView):
    model = HayulGrowth
    fields = ['year_month', 'height', 'weight']
    success_url = reverse_lazy("chart:growth_list")
