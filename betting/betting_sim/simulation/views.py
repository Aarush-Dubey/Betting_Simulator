"""
Views for the simulation app.
"""
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View, TemplateView
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect

import json

from .models import Simulation, Outcome, SimulationResult
from .forms import SimulationForm, OutcomeFormSet
from .utils import (
    create_simulator_from_model, generate_plots, 
    run_parameter_sweep, export_results_to_csv
)


class SimulationListView(ListView):
    """View for listing all simulations."""
    model = Simulation
    template_name = 'simulation/simulation_list.html'
    context_object_name = 'simulations'
    paginate_by = 10
    
    def get_queryset(self):
        """Filter by user if authenticated."""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset.filter(user=None)
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Simulations'
        return context


class SimulationDetailView(DetailView):
    """View for displaying a single simulation."""
    model = Simulation
    template_name = 'simulation/simulation_detail.html'
    context_object_name = 'simulation'
    
    def get_context_data(self, **kwargs):
        """Add page title and latest result to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = f'Simulation: {self.object.name}'
        
        # Get latest result if exists
        latest_result = self.object.results.order_by('-run_date').first()
        context['latest_result'] = latest_result
        
        return context


class SimulationCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new simulation."""
    model = Simulation
    form_class = SimulationForm
    template_name = 'simulation/simulation_form.html'
    
    def get_form_kwargs(self):
        """Add user to form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Add outcome formset to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Simulation'
        
        if self.request.POST:
            context['outcome_formset'] = OutcomeFormSet(self.request.POST)
        else:
            context['outcome_formset'] = OutcomeFormSet()
        
        return context
    
    def form_valid(self, form):
        """Process form and outcome formset if both are valid."""
        context = self.get_context_data()
        outcome_formset = context['outcome_formset']
        
        with transaction.atomic():
            # Set the user
            form.instance.user = self.request.user
            
            # Save the form to create the simulation instance
            self.object = form.save()
            
            # Save the outcome formset
            if outcome_formset.is_valid():
                outcome_formset.instance = self.object
                outcome_formset.save()
            else:
                return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the simulation detail page."""
        return reverse('simulation:detail', kwargs={'pk': self.object.pk})


class SimulationUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating an existing simulation."""
    model = Simulation
    form_class = SimulationForm
    template_name = 'simulation/simulation_form.html'
    
    def get_form_kwargs(self):
        """Add user to form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Add outcome formset to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Simulation'
        
        if self.request.POST:
            context['outcome_formset'] = OutcomeFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context['outcome_formset'] = OutcomeFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        """Process form and outcome formset if both are valid."""
        context = self.get_context_data()
        outcome_formset = context['outcome_formset']
        
        with transaction.atomic():
            # Save the form
            self.object = form.save()
            
            # Save the outcome formset
            if outcome_formset.is_valid():
                outcome_formset.instance = self.object
                outcome_formset.save()
            else:
                return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the simulation detail page."""
        return reverse('simulation:detail', kwargs={'pk': self.object.pk})


class SimulationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a simulation."""
    model = Simulation
    template_name = 'simulation/simulation_confirm_delete.html'
    success_url = reverse_lazy('simulation:list')
    
    def get_context_data(self, **kwargs):
        """Add page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Simulation'
        return context


class RunSimulationView(View):
    """View for running a simulation."""
    
    def get(self, request, pk):
        """Show confirmation page."""
        simulation = get_object_or_404(Simulation, pk=pk)
        return render(request, 'simulation/run_simulation.html', {
            'simulation': simulation,
            'title': 'Run Simulation'
        })
    
    def post(self, request, pk):
        """Run the simulation and store results."""
        simulation = get_object_or_404(Simulation, pk=pk)
        
        try:
            if simulation.is_parameter_sweep:
                # Run parameter sweep
                sweep_results = run_parameter_sweep(simulation)
                
                # Save the sweep results (simplified for now)
                result = SimulationResult(
                    simulation=simulation,
                    mean_final_bankroll=0.0,  # Placeholder
                    median_final_bankroll=0.0,  # Placeholder
                    std_final_bankroll=0.0,  # Placeholder
                    min_final_bankroll=0.0,  # Placeholder
                    max_final_bankroll=0.0,  # Placeholder
                    probability_of_ruin=0.0,  # Placeholder
                    max_drawdown=0.0  # Placeholder
                )
                
                # Serialize sweep results to JSON
                result.set_detailed_results(sweep_results)
                result.save()
                
            else:
                # Create simulator from the model
                simulator, _ = create_simulator_from_model(simulation)
                
                # Run the simulation
                results = simulator.run_multiple_simulations()
                
                # Save the results
                result = SimulationResult(
                    simulation=simulation,
                    mean_final_bankroll=results['mean_final_bankroll'],
                    median_final_bankroll=results['median_final_bankroll'],
                    std_final_bankroll=results['std_final_bankroll'],
                    min_final_bankroll=results['min_final_bankroll'],
                    max_final_bankroll=results['max_final_bankroll'],
                    probability_of_ruin=results['probability_of_ruin'],
                    max_drawdown=results['mean_max_drawdown']
                )
                
                # Serialize detailed results to JSON
                result.set_detailed_results(results)
                result.save()
            
            messages.success(request, "Simulation completed successfully!")
            return redirect('simulation:result', pk=result.pk)
            
        except Exception as e:
            messages.error(request, f"Error running simulation: {str(e)}")
            return redirect('simulation:detail', pk=simulation.pk)


class SimulationResultView(DetailView):
    """View for displaying simulation results."""
    model = SimulationResult
    template_name = 'simulation/simulation_result.html'
    context_object_name = 'result'
    
    def get_context_data(self, **kwargs):
        """Add plots and page title to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = f'Results: {self.object.simulation.name}'
        
        # Generate plots
        plots = generate_plots(self.object)
        context['plots'] = plots
        
        return context


class ExportResultView(View):
    """View for exporting simulation results to CSV."""
    
    def get(self, request, pk):
        """Generate and return CSV file."""
        result = get_object_or_404(SimulationResult, pk=pk)
        
        # Generate CSV
        csv_content = export_results_to_csv(result)
        
        # Create the HTTP response
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{result.simulation.name}_results.csv"'
        
        return response 