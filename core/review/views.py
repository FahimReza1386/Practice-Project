# Django Imports

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
    

# Third Party

from review.models import ReviewModel
from .forms import CreateReviewForm, ReplyReviewForm

class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=ReviewModel
    http_method_names = "post"
    form_class=CreateReviewForm
    success_message= "مشتری گرامی نظر شما با موفقیت ثبت شد ."

    def get_success_url(self):
        return reverse_lazy("blog:blog-grid")
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model=ReviewModel
    http_method_names = "post"
    success_message="مشتری گرامی نظر شما با موفقیت حذف شد ."
    success_url = reverse_lazy("blog:blog-grid")



class ReviewReplyView(LoginRequiredMixin, SuccessMessageMixin, CreateView):  
    http_method_names="post"
    model=ReviewModel
    form_class=ReplyReviewForm
    success_message= "مشتری گرامی نظر شما با موفقیت ثبت شد ."

    def get_success_url(self):
        return reverse_lazy("blog:blog-grid")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        parent_id = self.request.POST.get("review_reply")
        if parent_id:
            form.instance.parent = ReviewModel.objects.get(pk=parent_id)
        return super().form_valid(form)
