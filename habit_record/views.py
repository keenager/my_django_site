from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpRequest
from django.utils import timezone
from dotenv import load_dotenv
import requests
import os
# Create your views here.

load_dotenv('../.env')

pixela_endpoint = 'https://pixe.la/v1/users'
PIXELA_TOKEN = os.getenv('PIXELA_TOKEN')
USER_NAME = 'redtraining'
# GRAPH_ID = 'test1'
# TODAY = timezone.localdate().strftime('%Y%m%d')

headers = {
    'X-USER-TOKEN': PIXELA_TOKEN}


def index(request: HttpRequest):
    try:
        res = requests.get(
            f'{pixela_endpoint}/{USER_NAME}/graphs', headers=headers)
        graph_list: list = res.json()['graphs']
    except:
        graph_list = []
        graph_id = ''
        make_messages(request, res)
    graph_id = request.GET.get('graph_id')
    context = {
        'graph_list': graph_list,
        'graph_id': graph_id if graph_id else graph_list[0]['id'] if graph_list else '',
        'today': timezone.localdate().strftime('%Y-%m-%d'),
    }
    return render(request, 'habit_tracker/index.html', context)


def create_graph(request: HttpRequest):
    if request.method == 'POST':
        req_body = {
            'id': request.POST.get('graph_id'),
            'name': request.POST.get('graph_name'),
            'unit': request.POST.get('unit'),
            'type': request.POST.get('type'),
            'color': request.POST.get('color'),
            'timezone': 'Asia/Seoul',
        }
        res = requests.post(
            f'{pixela_endpoint}/{USER_NAME}/graphs',
            headers=headers,
            json=req_body,
        )
        make_messages(request, res)
        return redirect(reverse('habit:index') + '?graph_id=' + req_body['id'])

    colors = {
        'green': 'shibafu',
        'red': 'momiji',
        'blue': 'sora',
        'yellow': 'ichou',
        'purple': 'ajisai',
        'black': 'kuro',
    }

    return render(request, 'habit_tracker/create_graph.html', {'colors': colors})


def add_pixel(request: HttpRequest):
    graph_id = request.POST.get('graph_id')
    date = ''.join(request.POST.get('date').split('-'))
    quantity = request.POST.get('quantity')

    post_value = {
        'date': date,
        'quantity': quantity,
    }
    res = requests.post(
        f'{pixela_endpoint}/{USER_NAME}/graphs/{graph_id}',
        headers=headers,
        json=post_value,
    )
    make_messages(request, res)

    return redirect(reverse('habit:index') + '?graph_id=' + graph_id)


def delete_pixel(request: HttpRequest):
    graph_id = request.POST.get('graph_id')
    date = ''.join(request.POST.get('date').split('-'))
    print(date)
    res = requests.delete(
        f'{pixela_endpoint}/{USER_NAME}/graphs/{graph_id}/{date}',
        headers=headers,
    )
    print('res : ' + res.text)
    make_messages(request, res)

    return redirect(reverse('habit:index') + '?graph_id=' + graph_id)


def delete_graph(request: HttpRequest):
    graph_id = request.POST.get('graph_id')
    res = requests.delete(
        f'{pixela_endpoint}/{USER_NAME}/graphs/{graph_id}',
        headers=headers,
    )
    make_messages(request, res)

    return redirect('habit:index')


def make_messages(request: HttpRequest, res: requests.Response):
    res_data = res.json()
    isSuccess = res_data['isSuccess']
    if isSuccess:
        messages.add_message(request, messages.SUCCESS, res_data['message'])
    else:
        messages.add_message(request, messages.ERROR, res_data['message'])
