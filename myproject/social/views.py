from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView, DeleteView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from django.contrib import messages
from . import forms
from django.http import Http404

from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

# import AuthenticationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render,redirect

class PostList(ListView):
    model = Post
    template_name = 'social/index.html'
    context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'social/create_update_post.html'
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        # Set the user to the current logged-in user before saving
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Post Created Successfully")
        return super().form_valid(form)



# updateview

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'social/create_update_post.html'
    success_url = reverse_lazy('home')  
    
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        # Set the user to the current logged-in user before saving
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Post  updated Successfully")
        return super().form_valid(form)
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Check if the logged-in user is the owner or an admin
        if obj.user != self.request.user and not self.request.user.is_staff:
            return render(self.request, 'social/not_authorized.html')  # Render custom template
        return obj
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context

    

# deleteview

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')  # Redirect to the home page after successful post deletion
    template_name ='social/delete_post.html'  # Custom template for delete confirmation page
     
    pk_url_kwarg = 'id'

    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Check if the logged-in user is the owner or an admin
        if obj.user != self.request.user and not self.request.user.is_staff:
            return render(self.request, 'social/not_authorized.html')  # Render custom template
        return obj
    
    def delete(self,request,*args,**kwargs):
        messages.add_message(self.request, messages.SUCCESS, "Student deleted Successfully")
        return super().delete(request,*args,**kwargs)
    
    




def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"User Account created Successfully!")
            return redirect('home')
    else:
        form = forms.SignUpForm()



    return render(request,'social/auth_form.html',{'form':form})

def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.add_message(request,messages.SUCCESS,"Login Successfully.")
                return redirect('home')
            else :
                messages.add_message(request,messages.ERROR,'Invalid Credentials.')

    else:
        form = AuthenticationForm()
    return render(request,'social/login.html',{'form':form})

@login_required
def user_logout(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'Logout Successfully')
    return redirect('home')


@login_required
def user_profile(request):
    posts = Post.objects.filter(user = request.user)
    return render(request,'social/profile.html',{'posts':posts})




def post_detail(request, pk):
    # Retrieve the post based on the provided pk (primary key)
    post = get_object_or_404(Post, pk=pk)
    
    # Render the detail template with the post object
    return render(request, 'social/post_detail.html', {'post': post})
