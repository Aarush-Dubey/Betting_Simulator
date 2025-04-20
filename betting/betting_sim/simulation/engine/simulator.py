"""
Core simulation engine for betting simulations.
"""
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Callable, Union, Tuple
import random
import time
from abc import ABC, abstractmethod


@dataclass
class OutcomeConfig:
    """Configuration for a single outcome in a betting simulation."""
    name: str
    probability: float
    multiplier: float


@dataclass
class SimulationConfig:
    """Configuration for a betting simulation."""
    initial_bankroll: float = 100.0
    num_rounds: int = 100
    num_simulations: int = 1000
    outcomes: List[OutcomeConfig] = None
    
    def __post_init__(self):
        if self.outcomes is None:
            self.outcomes = []
            
        # Validate probabilities sum to 1
        total_prob = sum(outcome.probability for outcome in self.outcomes)
        if not (0.99 <= total_prob <= 1.01):  # Allow for slight rounding errors
            raise ValueError(f"Outcome probabilities must sum to 1 (currently {total_prob})")


class BettingStrategy(ABC):
    """Abstract base class for betting strategies."""
    
    @abstractmethod
    def get_bet_fraction(self, bankroll: float, round_idx: int, history: List[Dict[str, Any]]) -> float:
        """
        Calculate the fraction of the bankroll to bet.
        
        Args:
            bankroll: Current bankroll amount
            round_idx: Current round index (0-based)
            history: List of dictionaries with past results
                    Each dict has:
                    - 'bankroll': bankroll after the round
                    - 'bet_amount': amount bet
                    - 'outcome_idx': index of the outcome that occurred
                    - 'multiplier': the multiplier applied
                    
        Returns:
            float: Fraction of bankroll to bet (0.0 to 1.0)
        """
        pass


class Simulator:
    """Main simulation engine class."""
    
    def __init__(self, config: SimulationConfig, strategy: BettingStrategy):
        """
        Initialize the simulator with a configuration and strategy.
        
        Args:
            config: Simulation configuration
            strategy: Betting strategy to use
        """
        self.config = config
        self.strategy = strategy
        
        # Validate configuration
        if not config.outcomes:
            raise ValueError("At least one outcome must be specified")
        
        # Pre-calculate cumulative probabilities for efficient sampling
        self.cum_probs = np.cumsum([o.multiplier for o in config.outcomes])
        self.cum_probs /= self.cum_probs[-1]  # Normalize
        
    def _sample_outcome(self) -> Tuple[int, float]:
        """
        Sample a random outcome based on configured probabilities.
        
        Returns:
            tuple: (outcome_index, multiplier)
        """
        r = random.random()
        cum_probs = [0] + [o.probability for o in self.config.outcomes]
        for i in range(len(cum_probs) - 1):
            cum_probs[i + 1] += cum_probs[i]
            
        for i, (lower, upper) in enumerate(zip(cum_probs, cum_probs[1:])):
            if lower <= r < upper:
                return i, self.config.outcomes[i].multiplier
                
        # Fallback for floating point errors
        return len(self.config.outcomes) - 1, self.config.outcomes[-1].multiplier
        
    def run_single_simulation(self) -> Dict[str, Any]:
        """
        Run a single simulation.
        
        Returns:
            dict: Results of the simulation
        """
        bankroll = self.config.initial_bankroll
        history = []
        
        # Track min bankroll for drawdown calculation
        max_bankroll = bankroll
        min_bankroll_after_max = bankroll
        max_drawdown = 0.0
        
        # Track bankroll over time
        bankroll_over_time = [bankroll]
        
        for round_idx in range(self.config.num_rounds):
            # Stop if bankroll reaches zero or very close to zero
            if bankroll <= 0.01:
                # Fill remaining rounds with zero
                bankroll_over_time.extend([0] * (self.config.num_rounds - round_idx))
                break
                
            # Get bet fraction from strategy
            bet_fraction = self.strategy.get_bet_fraction(bankroll, round_idx, history)
            bet_fraction = max(0.0, min(1.0, bet_fraction))  # Clamp to [0, 1]
            
            # Calculate bet amount
            bet_amount = bankroll * bet_fraction
            
            # Sample outcome
            outcome_idx, multiplier = self._sample_outcome()
            
            # Update bankroll
            new_bankroll = bankroll - bet_amount + (bet_amount * multiplier)
            new_bankroll = max(0, new_bankroll)  # Ensure non-negative
            
            # Update history
            history.append({
                'round': round_idx,
                'bankroll_before': bankroll,
                'bet_amount': bet_amount,
                'bet_fraction': bet_fraction,
                'outcome_idx': outcome_idx,
                'multiplier': multiplier,
                'bankroll': new_bankroll,
            })
            
            # Update drawdown tracking
            if new_bankroll > max_bankroll:
                max_bankroll = new_bankroll
                min_bankroll_after_max = new_bankroll
            elif new_bankroll < min_bankroll_after_max:
                min_bankroll_after_max = new_bankroll
                current_drawdown = (max_bankroll - min_bankroll_after_max) / max_bankroll
                max_drawdown = max(max_drawdown, current_drawdown)
            
            # Update bankroll and record
            bankroll = new_bankroll
            bankroll_over_time.append(bankroll)
        
        return {
            'initial_bankroll': self.config.initial_bankroll,
            'final_bankroll': bankroll,
            'max_bankroll': max_bankroll,
            'max_drawdown': max_drawdown,
            'bankrupt': bankroll <= 0.01,
            'history': history,
            'bankroll_over_time': bankroll_over_time,
        }
    
    def run_multiple_simulations(self, progress_callback=None) -> Dict[str, Any]:
        """
        Run multiple simulations and compute aggregate statistics.
        
        Args:
            progress_callback: Optional callback function to report progress (receives value 0.0-1.0)
            
        Returns:
            dict: Aggregated simulation results
        """
        results = []
        bankrolls = []
        bankroll_trajectories = []
        num_bankrupt = 0
        max_drawdowns = []
        
        start_time = time.time()
        
        for i in range(self.config.num_simulations):
            result = self.run_single_simulation()
            results.append(result)
            bankrolls.append(result['final_bankroll'])
            bankroll_trajectories.append(result['bankroll_over_time'])
            
            if result['bankrupt']:
                num_bankrupt += 1
                
            max_drawdowns.append(result['max_drawdown'])
            
            if progress_callback and i % max(1, self.config.num_simulations // 100) == 0:
                progress_callback(i / self.config.num_simulations)
        
        # Calculate statistics
        bankrolls = np.array(bankrolls)
        mean_bankroll = float(np.mean(bankrolls))
        median_bankroll = float(np.median(bankrolls))
        std_bankroll = float(np.std(bankrolls))
        min_bankroll = float(np.min(bankrolls))
        max_bankroll = float(np.max(bankrolls))
        
        # Calculate bankroll trajectories statistics
        bankroll_trajectories = np.array(bankroll_trajectories)
        mean_trajectory = np.mean(bankroll_trajectories, axis=0).tolist()
        percentile_10 = np.percentile(bankroll_trajectories, 10, axis=0).tolist()
        percentile_90 = np.percentile(bankroll_trajectories, 90, axis=0).tolist()
        
        # Calculate max drawdown statistics
        mean_max_drawdown = float(np.mean(max_drawdowns))
        median_max_drawdown = float(np.median(max_drawdowns))
        max_max_drawdown = float(np.max(max_drawdowns))
        
        # Prepare results
        return {
            'num_simulations': self.config.num_simulations,
            'mean_final_bankroll': mean_bankroll,
            'median_final_bankroll': median_bankroll,
            'std_final_bankroll': std_bankroll,
            'min_final_bankroll': min_bankroll,
            'max_final_bankroll': max_bankroll,
            'probability_of_ruin': num_bankrupt / self.config.num_simulations,
            'mean_max_drawdown': mean_max_drawdown,
            'median_max_drawdown': median_max_drawdown,
            'max_max_drawdown': max_max_drawdown,
            'mean_trajectory': mean_trajectory,
            'percentile_10': percentile_10,
            'percentile_90': percentile_90,
            'individual_results': results[:10],  # Include first 10 individual simulations
            'elapsed_time': time.time() - start_time,
        } 