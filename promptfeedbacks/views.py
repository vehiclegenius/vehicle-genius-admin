from django.shortcuts import render

from summarytemplates.views import make_api_get_request, make_api_post_request


def index_get(request):
    state: str = request.GET.get('state', 'unresolved').lower()
    is_resolved = state == 'resolved'
    feedbacks = make_api_get_request('/admin/prompt-feedback?isResolved=' + str(is_resolved).lower())
    return render(request, 'promptfeedbacks/index.html', {'resolved': is_resolved, 'feedbacks': feedbacks})


def resolve_post(request, pk):
    make_api_post_request('/admin/prompt-feedback/' + pk + '/resolve', {})
    return render(request, 'promptfeedbacks/resolved_success.html')
