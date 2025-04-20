from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, FileResponse
from django.contrib import messages

from .models import Strategy
from .forms import StrategyForm


class StrategyListView(ListView):
    """View for listing strategies."""
    model = Strategy
    template_name = 'strategies/strategy_list.html'
    context_object_name = 'strategies'
    
    def get_queryset(self):
        """Filter by user if authenticated."""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset.none()  # Don't show strategies to unauthenticated users
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Strategies'
        return context


class StrategyDetailView(LoginRequiredMixin, DetailView):
    """View for displaying a single strategy."""
    model = Strategy
    template_name = 'strategies/strategy_detail.html'
    context_object_name = 'strategy'
    
    def get_queryset(self):
        """Filter by user."""
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = f'Strategy: {self.object.name}'
        
        # Read the file contents
        try:
            with self.object.file.open('r') as f:
                context['file_contents'] = f.read()
        except Exception:
            context['file_contents'] = "Error reading file."
            
        return context


class StrategyCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new strategy."""
    model = Strategy
    form_class = StrategyForm
    template_name = 'strategies/strategy_form.html'
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Upload New Strategy'
        return context
    
    def form_valid(self, form):
        """Set the user before saving."""
        form.instance.user = self.request.user
        messages.success(self.request, "Strategy uploaded successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the strategy detail page."""
        return reverse('strategies:detail', kwargs={'pk': self.object.pk})


class StrategyUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating a strategy."""
    model = Strategy
    form_class = StrategyForm
    template_name = 'strategies/strategy_form.html'
    
    def get_queryset(self):
        """Filter by user."""
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Strategy'
        return context
    
    def form_valid(self, form):
        """Set success message."""
        messages.success(self.request, "Strategy updated successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the strategy detail page."""
        return reverse('strategies:detail', kwargs={'pk': self.object.pk})


class StrategyDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a strategy."""
    model = Strategy
    template_name = 'strategies/strategy_confirm_delete.html'
    success_url = reverse_lazy('strategies:list')
    
    def get_queryset(self):
        """Filter by user."""
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Strategy'
        return context
    
    def delete(self, request, *args, **kwargs):
        """Set success message."""
        messages.success(request, "Strategy deleted successfully.")
        return super().delete(request, *args, **kwargs)


class StrategyDownloadView(LoginRequiredMixin, View):
    """View for downloading strategy files."""
    
    def get(self, request, pk):
        """Download the strategy file."""
        strategy = get_object_or_404(Strategy, pk=pk, user=request.user)
        
        # Create the file response
        response = FileResponse(strategy.file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{strategy.file_name}"'
        
        return response


class StrategyTemplateView(View):
    """View for downloading template strategy file."""
    
    def get(self, request):
        """Download the template strategy file."""
        template_content = '''"""
Example betting strategy template
"""

def bet_fraction(bankroll, round_idx, history):
    """
    Calculate the fraction of bankroll to bet.
    
    Args:
        bankroll (float): Current bankroll amount
        round_idx (int): Current round index (0-based)
        history (list): List of dictionaries with past results
                        Each dict has:
                        - 'bankroll': bankroll after the round
                        - 'bet_amount': amount bet
                        - 'outcome_idx': index of the outcome that occurred
                        - 'multiplier': the multiplier applied
                        
    Returns:
        float: Fraction of bankroll to bet (0.0 to 1.0)
    """
    # Example: always bet 10% of bankroll
    return 0.1
    
    # Example: increase bet over time (up to 20%)
    # return min(0.1 + (round_idx / 1000), 0.2)
    
    # Example: adjust bet based on recent outcomes
    # if len(history) > 0:
    #     last_outcome = history[-1]
    #     if last_outcome['multiplier'] > 1.0:
    #         # Won last round, increase bet slightly
    #         return min(0.15, 0.1 + 0.01 * len(history))
    #     else:
    #         # Lost last round, decrease bet slightly
    #         return max(0.05, 0.1 - 0.01 * len(history))
    # return 0.1  # Default for first round
'''
        
        # Create the response
        response = HttpResponse(template_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="strategy_template.py"'
        
        return response 