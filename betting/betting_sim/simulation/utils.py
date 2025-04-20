"""
Utility functions for the simulation app.
"""
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from typing import List, Dict, Any, Optional, Tuple, Union
import pandas as pd

from .engine import (
    Simulator, SimulationConfig, OutcomeConfig, BettingStrategy,
    FixedFractionStrategy, KellyCriterionStrategy, MartingaleStrategy, CustomStrategy
)
from .models import Simulation, Outcome, SimulationResult


def create_simulator_from_model(simulation: Simulation) -> Tuple[Simulator, BettingStrategy]:
    """
    Create a Simulator instance from a Simulation model.
    
    Args:
        simulation: The Simulation model instance
        
    Returns:
        tuple: (simulator, strategy) instances
    """
    # Create outcome configs
    outcome_configs = []
    for outcome in simulation.outcomes.all():
        outcome_configs.append(OutcomeConfig(
            name=outcome.name,
            probability=outcome.probability,
            multiplier=outcome.multiplier
        ))
    
    # Create simulation config
    config = SimulationConfig(
        initial_bankroll=simulation.initial_bankroll,
        num_rounds=simulation.num_rounds,
        num_simulations=simulation.num_simulations,
        outcomes=outcome_configs
    )
    
    # Create strategy
    strategy = None
    if simulation.strategy == 'fixed_fraction':
        strategy = FixedFractionStrategy(fraction=simulation.bet_fraction)
    elif simulation.strategy == 'kelly_criterion':
        outcomes_list = [
            {'probability': o.probability, 'multiplier': o.multiplier}
            for o in simulation.outcomes.all()
        ]
        strategy = KellyCriterionStrategy(outcomes_list, fraction_limit=simulation.bet_fraction)
    elif simulation.strategy == 'martingale':
        strategy = MartingaleStrategy(base_fraction=simulation.bet_fraction / 10, max_fraction=simulation.bet_fraction)
    elif simulation.strategy == 'custom' and simulation.custom_strategy:
        strategy = CustomStrategy(simulation.custom_strategy.file.path)
    else:
        # Fallback to fixed fraction if something is wrong
        strategy = FixedFractionStrategy(fraction=simulation.bet_fraction)
    
    # Create simulator
    simulator = Simulator(config, strategy)
    
    return simulator, strategy


def generate_plots(result: SimulationResult) -> Dict[str, str]:
    """
    Generate and encode plots as base64 strings.
    
    Args:
        result: The SimulationResult instance
        
    Returns:
        dict: Dictionary of plot names to base64-encoded HTML/image strings
    """
    detailed_results = result.get_detailed_results()
    plots = {}
    
    # Generate Plotly plots
    plots['bankroll_trajectory'] = plot_bankroll_trajectory_plotly(detailed_results)
    plots['bankroll_histogram'] = plot_bankroll_histogram_plotly(detailed_results)
    plots['outcome_distribution'] = plot_outcome_distribution_plotly(detailed_results)
    
    return plots


def plot_bankroll_trajectory_plotly(results: Dict[str, Any]) -> str:
    """
    Generate a Plotly plot of bankroll trajectories.
    
    Args:
        results: Simulation results dictionary
        
    Returns:
        str: HTML representation of the plot
    """
    fig = go.Figure()
    
    # Add mean trajectory
    fig.add_trace(go.Scatter(
        x=list(range(len(results['mean_trajectory']))),
        y=results['mean_trajectory'],
        mode='lines',
        name='Mean',
        line=dict(color='blue', width=2)
    ))
    
    # Add percentile bounds
    fig.add_trace(go.Scatter(
        x=list(range(len(results['percentile_10']))),
        y=results['percentile_10'],
        mode='lines',
        name='10th Percentile',
        line=dict(color='red', width=1, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=list(range(len(results['percentile_90']))),
        y=results['percentile_90'],
        mode='lines',
        name='90th Percentile',
        line=dict(color='green', width=1, dash='dash')
    ))
    
    # Add sample trajectories (first 5)
    for i, result in enumerate(results['individual_results'][:5]):
        fig.add_trace(go.Scatter(
            x=list(range(len(result['bankroll_over_time']))),
            y=result['bankroll_over_time'],
            mode='lines',
            name=f'Sample {i+1}',
            opacity=0.5,
            line=dict(width=1)
        ))
    
    # Update layout
    fig.update_layout(
        title='Bankroll Trajectory Over Rounds',
        xaxis_title='Round',
        yaxis_title='Bankroll',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig.to_html(include_plotlyjs='cdn', full_html=False)


def plot_bankroll_histogram_plotly(results: Dict[str, Any]) -> str:
    """
    Generate a Plotly histogram of final bankrolls.
    
    Args:
        results: Simulation results dictionary
        
    Returns:
        str: HTML representation of the plot
    """
    # Extract all final bankrolls
    final_bankrolls = [r['final_bankroll'] for r in results['individual_results']]
    
    # Create histogram figure
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=final_bankrolls,
        nbinsx=20,
        name='Final Bankroll',
        marker_color='blue',
        opacity=0.7
    ))
    
    # Add vertical lines for statistics
    fig.add_vline(
        x=results['mean_final_bankroll'], 
        line_dash='dash', 
        line_color='red',
        annotation_text=f"Mean: {results['mean_final_bankroll']:.2f}",
        annotation_position="top right"
    )
    
    fig.add_vline(
        x=results['median_final_bankroll'], 
        line_dash='dash', 
        line_color='green',
        annotation_text=f"Median: {results['median_final_bankroll']:.2f}",
        annotation_position="top left"
    )
    
    # Update layout
    fig.update_layout(
        title='Distribution of Final Bankrolls',
        xaxis_title='Final Bankroll',
        yaxis_title='Frequency',
        template='plotly_white',
        bargap=0.1
    )
    
    return fig.to_html(include_plotlyjs='cdn', full_html=False)


def plot_outcome_distribution_plotly(results: Dict[str, Any]) -> str:
    """
    Generate a Plotly pie chart of outcome distribution.
    
    Args:
        results: Simulation results dictionary
        
    Returns:
        str: HTML representation of the plot
    """
    # Count outcomes from individual results
    outcome_counts = {}
    
    for result in results['individual_results']:
        for round_data in result['history']:
            outcome_idx = round_data['outcome_idx']
            outcome_counts[outcome_idx] = outcome_counts.get(outcome_idx, 0) + 1
    
    # Create pie chart
    labels = [f'Outcome {idx}' for idx in outcome_counts.keys()]
    values = list(outcome_counts.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    
    # Update layout
    fig.update_layout(
        title='Distribution of Outcomes',
        template='plotly_white'
    )
    
    return fig.to_html(include_plotlyjs='cdn', full_html=False)


def run_parameter_sweep(simulation: Simulation) -> Dict[str, Any]:
    """
    Run a parameter sweep simulation.
    
    Args:
        simulation: The Simulation model instance
        
    Returns:
        dict: Results of the parameter sweep
    """
    if not simulation.is_parameter_sweep:
        raise ValueError("Simulation is not configured for parameter sweep")
    
    parameter = simulation.sweep_parameter
    start_value = simulation.sweep_start
    end_value = simulation.sweep_end
    num_steps = simulation.sweep_steps
    
    # Generate parameter values
    param_values = np.linspace(start_value, end_value, num_steps)
    
    # Store results for each parameter value
    sweep_results = []
    
    for param_value in param_values:
        # Create a copy of the simulation with the modified parameter
        temp_simulation = Simulation(
            name=simulation.name,
            description=simulation.description,
            initial_bankroll=simulation.initial_bankroll,
            num_rounds=simulation.num_rounds,
            bet_fraction=simulation.bet_fraction,
            num_simulations=simulation.num_simulations // num_steps,  # Divide simulations
            strategy=simulation.strategy,
            custom_strategy=simulation.custom_strategy
        )
        
        # Set the parameter being swept
        if parameter == 'bet_fraction':
            temp_simulation.bet_fraction = param_value
        elif parameter == 'initial_bankroll':
            temp_simulation.initial_bankroll = param_value
        
        # Create simulator and run
        simulator, _ = create_simulator_from_model(temp_simulation)
        results = simulator.run_multiple_simulations()
        
        # Store results with parameter value
        sweep_results.append({
            'param_value': param_value,
            'mean_final_bankroll': results['mean_final_bankroll'],
            'median_final_bankroll': results['median_final_bankroll'],
            'std_final_bankroll': results['std_final_bankroll'],
            'probability_of_ruin': results['probability_of_ruin'],
            'mean_max_drawdown': results['mean_max_drawdown']
        })
    
    return {
        'parameter': parameter,
        'sweep_results': sweep_results
    }


def export_results_to_csv(result: SimulationResult) -> str:
    """
    Export simulation results to CSV format.
    
    Args:
        result: The SimulationResult instance
        
    Returns:
        str: CSV content as a string
    """
    detailed_results = result.get_detailed_results()
    
    # Create a DataFrame for summary statistics
    summary_data = {
        'Metric': [
            'Initial Bankroll', 'Mean Final Bankroll', 'Median Final Bankroll',
            'Min Final Bankroll', 'Max Final Bankroll', 'Standard Deviation',
            'Probability of Ruin', 'Mean Max Drawdown', 'Number of Simulations'
        ],
        'Value': [
            detailed_results.get('initial_bankroll', 'N/A'),
            result.mean_final_bankroll,
            result.median_final_bankroll,
            result.min_final_bankroll,
            result.max_final_bankroll,
            result.std_final_bankroll,
            result.probability_of_ruin,
            result.max_drawdown,
            detailed_results.get('num_simulations', 'N/A')
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_csv = summary_df.to_csv(index=False)
    
    # If we have individual simulation data, create a section for that
    if 'individual_results' in detailed_results:
        individual_data = []
        for i, sim in enumerate(detailed_results['individual_results']):
            individual_data.append({
                'Simulation': i + 1,
                'Final Bankroll': sim['final_bankroll'],
                'Max Bankroll': sim['max_bankroll'],
                'Max Drawdown': sim['max_drawdown'],
                'Went Bankrupt': sim['bankrupt']
            })
        
        individual_df = pd.DataFrame(individual_data)
        individual_csv = individual_df.to_csv(index=False)
        
        # Combine the sections
        csv_content = f"# Summary Statistics\n{summary_csv}\n\n# Individual Simulation Results\n{individual_csv}"
    else:
        csv_content = f"# Summary Statistics\n{summary_csv}"
    
    return csv_content 