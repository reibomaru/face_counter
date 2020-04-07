from django.shortcuts import redirect
from django.utils import timezone
from face_count.forms import CommentForm

def post_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_date = timezone.now()
        post.save()
    return redirect('usage')