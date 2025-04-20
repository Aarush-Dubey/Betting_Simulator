from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
import os
import sys
import platform


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Betting Simulations Platform'
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About'
        return context


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


class RegisterView(CreateView):
    template_name = 'core/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('core:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


def welcome(request):
    """
    A simple welcome view that doesn't rely on database access.
    This helps diagnose deployment issues.
    """
    debug_info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'env_vars': {k: v for k, v in os.environ.items() if k in [
            'VERCEL', 'VERCEL_REGION', 'DJANGO_SETTINGS_MODULE', 'DEBUG'
        ]},
        'sys_path': sys.path,
        'current_dir': os.getcwd(),
    }
    
    html = f"""
    <html>
    <head>
        <title>Betting Simulator - Welcome</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .success {{ background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 4px; }}
            .debug {{ background-color: #f8f9fa; padding: 15px; border-radius: 4px; overflow: auto; margin-top: 20px; }}
            h1 {{ color: #333; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Betting Simulator</h1>
            <div class="success">
                <p><strong>Success!</strong> Your Django application is running on Vercel.</p>
            </div>
            
            <h2>Debug Information:</h2>
            <div class="debug">
                <h3>Python Version:</h3>
                <pre>{debug_info['python_version']}</pre>
                
                <h3>Platform:</h3>
                <pre>{debug_info['platform']}</pre>
                
                <h3>Environment Variables:</h3>
                <pre>{debug_info['env_vars']}</pre>
                
                <h3>Python Path:</h3>
                <pre>{debug_info['sys_path']}</pre>
                
                <h3>Current Directory:</h3>
                <pre>{debug_info['current_dir']}</pre>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html) 