from django.db import models
from django.contrib.auth.models import User
import json


class Outcome(models.Model):
    """
    Represents a possible outcome in a betting simulation with its probability and multiplier.
    """
    name = models.CharField(max_length=100)
    probability = models.FloatField()
    multiplier = models.FloatField()
    simulation = models.ForeignKey('Simulation', on_delete=models.CASCADE, related_name='outcomes')
    
    def __str__(self):
        return f"{self.name} (Prob: {self.probability}, Mult: {self.multiplier}x)"


class Simulation(models.Model):
    """
    Represents a betting simulation configuration.
    """
    STRATEGY_CHOICES = [
        ('fixed_fraction', 'Fixed Fraction'),
        ('kelly_criterion', 'Kelly Criterion'),
        ('martingale', 'Martingale'),
        ('custom', 'Custom Strategy'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic parameters
    initial_bankroll = models.FloatField(default=100.0)
    num_rounds = models.IntegerField(default=100)
    bet_fraction = models.FloatField(default=0.1)
    num_simulations = models.IntegerField(default=1000)
    
    # Strategy
    strategy = models.CharField(max_length=50, choices=STRATEGY_CHOICES, default='fixed_fraction')
    custom_strategy = models.ForeignKey('strategies.Strategy', on_delete=models.SET_NULL, 
                                       null=True, blank=True, related_name='simulations')
    
    # Parameter sweeping
    is_parameter_sweep = models.BooleanField(default=False)
    sweep_parameter = models.CharField(max_length=50, blank=True)
    sweep_start = models.FloatField(null=True, blank=True)
    sweep_end = models.FloatField(null=True, blank=True)
    sweep_steps = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class SimulationResult(models.Model):
    """
    Stores the results of a simulation run.
    """
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='results')
    run_date = models.DateTimeField(auto_now_add=True)
    
    # Summary statistics
    mean_final_bankroll = models.FloatField()
    median_final_bankroll = models.FloatField()
    std_final_bankroll = models.FloatField()
    min_final_bankroll = models.FloatField()
    max_final_bankroll = models.FloatField()
    probability_of_ruin = models.FloatField()
    max_drawdown = models.FloatField()
    
    # Detailed results (stored as JSON)
    detailed_results = models.TextField()
    
    def get_detailed_results(self):
        """
        Deserializes the detailed_results JSON string into a Python object.
        """
        return json.loads(self.detailed_results)
    
    def set_detailed_results(self, results_dict):
        """
        Serializes the Python object into a JSON string for storage.
        """
        self.detailed_results = json.dumps(results_dict)
    
    def __str__(self):
        return f"Result for {self.simulation.name} (Run: {self.run_date})" 