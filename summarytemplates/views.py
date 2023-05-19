import json
import os

import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import Response


def current(request):
    if request.method == 'GET':
        return current_get(request)
    elif request.method == 'POST':
        return current_post(request)


def current_get(request):
    template = make_api_get_request('/admin/summary-templates/current')
    return render(request, 'summarytemplates/current.html', {
        'system_prompt': template['systemPrompt'],
        'data_template': template['dataTemplate'],
        'prompt_template': template['promptTemplate'],
    })


def current_post(request):
    messages.success(request, 'Template saved successfully.')
    if request.headers.get('HX-Request') == 'true':
        response = HttpResponse()
        response['HX-Redirect'] = '/summarytemplates'
        return response
    return redirect('/summarytemplates')


def validate_and_preview_post(request):
    data = parse_request_post(request.POST)
    body = {
        'systemPrompt': data['systemPrompt'],
        'dataTemplate': data['dataTemplate'],
        'promptTemplate': data['promptTemplate'],
    }
    answer = make_api_post_request('/admin/summary-templates/validate', body)
    return render(request, 'summarytemplates/current_templatecontrols.html', {
        'validated': True,
        'valid': answer['isValid'],
        'error_message': answer['errorMessage'],
        'preview': answer['preview'],
    })


def make_api_get_request(uri: str):
    headers = {
        'Accept': 'application/json',
    }
    response = requests.get(os.environ.get('API_BASE_URL') + uri, headers=headers)
    answer = json.loads(response.content.decode('utf-8'))
    return answer


def make_api_post_request(uri: str, body):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.post(
        os.environ.get('API_BASE_URL') + uri,
        data=json.dumps(body),
        headers=headers)
    if response.content:
        answer = json.loads(response.content.decode('utf-8'))
        return answer


def make_api_put_request(uri: str, body):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.put(
        os.environ.get('API_BASE_URL') + uri,
        data=json.dumps(body),
        headers=headers)
    return response


def parse_request_post(request_post):
    # create a new copy of the request.POST data
    parsed_post = request_post.copy()

    # loop through the keys in the request.POST data
    for key in request_post:
        # check if the key contains an array index
        if '[' in key and ']' in key:
            # extract the key prefix and index from the key name
            key_prefix, index = key.split('[', 1)
            index = index.split(']', 1)[0]
            # create a dictionary for the message
            message = {k.split('.')[1]: v for k, v in request_post.items() if k.startswith(f'{key_prefix}[{index}].')}
            # add the message to the parsed_post dictionary
            parsed_post[key_prefix] = parsed_post.get(key_prefix, []) + [message]

    # remove duplicates from lists in the parsed_post dictionary
    for key, value in parsed_post.items():
        if isinstance(value, list):
            unique_value = []
            for item in value:
                if item not in unique_value:
                    unique_value.append(item)
            parsed_post[key] = unique_value

    return parsed_post
