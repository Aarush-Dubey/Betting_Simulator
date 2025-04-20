from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from simulation.models import Simulation, SimulationResult


class DashboardView(LoginRequiredMixin, TemplateView):
    """View for the main dashboard."""
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        """Add dashboard data to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        
        user = self.request.user
        
        # Get user's simulations and results
        simulations = Simulation.objects.filter(user=user).order_by('-created_at')
        results = SimulationResult.objects.filter(simulation__user=user).order_by('-run_date')
        
        context['simulations'] = simulations[:10]  # Latest 10 simulations
        context['results'] = results[:10]  # Latest 10 results
        
        # Generate summary statistics
        context['simulation_count'] = simulations.count()
        context['result_count'] = results.count()
        
        # Get best and worst performers
        if results.exists():
            best_result = results.order_by('-mean_final_bankroll').first()
            worst_result = results.order_by('mean_final_bankroll').first()
            context['best_result'] = best_result
            context['worst_result'] = worst_result
        
        return context


class CompareResultsView(LoginRequiredMixin, View):
    """View for comparing two simulation results."""
    template_name = 'dashboard/compare_results.html'
    
    def get(self, request, pk1, pk2):
        """Handle GET request."""
        user = request.user
        
        # Get the two results
        result1 = get_object_or_404(SimulationResult, pk=pk1, simulation__user=user)
        result2 = get_object_or_404(SimulationResult, pk=pk2, simulation__user=user)
        
        # Generate comparison plots
        comparison_plots = self.generate_comparison_plots(result1, result2)
        
        context = {
            'title': 'Compare Results',
            'result1': result1,
            'result2': result2,
            'plots': comparison_plots
        }
        
        return render(request, self.template_name, context)
    
    def generate_comparison_plots(self, result1, result2):
        """Generate comparison plots for two results."""
        plots = {}
        
        # Get detailed results
        data1 = result1.get_detailed_results()
        data2 = result2.get_detailed_results()
        
        # Generate bankroll trajectory comparison
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        # Add mean trajectories for both results
        fig.add_trace(
            go.Scatter(
                x=list(range(len(data1['mean_trajectory']))),
                y=data1['mean_trajectory'],
                mode='lines',
                name=f'{result1.simulation.name} (Mean)',
                line=dict(color='blue', width=2)
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=list(range(len(data2['mean_trajectory']))),
                y=data2['mean_trajectory'],
                mode='lines',
                name=f'{result2.simulation.name} (Mean)',
                line=dict(color='red', width=2)
            )
        )
        
        # Add percentile bounds for both
        fig.add_trace(
            go.Scatter(
                x=list(range(len(data1['percentile_10']))),
                y=data1['percentile_10'],
                mode='lines',
                name=f'{result1.simulation.name} (10th)',
                line=dict(color='blue', width=1, dash='dash'),
                opacity=0.5
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=list(range(len(data1['percentile_90']))),
                y=data1['percentile_90'],
                mode='lines',
                name=f'{result1.simulation.name} (90th)',
                line=dict(color='blue', width=1, dash='dash'),
                opacity=0.5
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=list(range(len(data2['percentile_10']))),
                y=data2['percentile_10'],
                mode='lines',
                name=f'{result2.simulation.name} (10th)',
                line=dict(color='red', width=1, dash='dash'),
                opacity=0.5
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=list(range(len(data2['percentile_90']))),
                y=data2['percentile_90'],
                mode='lines',
                name=f'{result2.simulation.name} (90th)',
                line=dict(color='red', width=1, dash='dash'),
                opacity=0.5
            )
        )
        
        # Update layout
        fig.update_layout(
            title='Bankroll Trajectory Comparison',
            xaxis_title='Round',
            yaxis_title='Bankroll',
            legend_title='Simulations',
            template='plotly_white',
            hovermode='x unified'
        )
        
        plots['trajectory_comparison'] = fig.to_html(include_plotlyjs='cdn', full_html=False)
        
        # Create histogram comparison
        fig = go.Figure()
        
        # Extract final bankrolls
        bankrolls1 = [r['final_bankroll'] for r in data1.get('individual_results', [])]
        bankrolls2 = [r['final_bankroll'] for r in data2.get('individual_results', [])]
        
        # Create histogram traces
        fig.add_trace(go.Histogram(
            x=bankrolls1,
            opacity=0.7,
            name=result1.simulation.name,
            marker_color='blue',
            nbinsx=20
        ))
        
        fig.add_trace(go.Histogram(
            x=bankrolls2,
            opacity=0.7,
            name=result2.simulation.name,
            marker_color='red',
            nbinsx=20
        ))
        
        # Overlay both histograms
        fig.update_layout(
            barmode='overlay',
            title='Final Bankroll Distribution Comparison',
            xaxis_title='Final Bankroll',
            yaxis_title='Count',
            legend_title='Simulations',
            template='plotly_white'
        )
        
        plots['histogram_comparison'] = fig.to_html(include_plotlyjs='cdn', full_html=False)
        
        return plots 