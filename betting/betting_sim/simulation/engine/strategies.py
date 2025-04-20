"""
Implementation of various betting strategies.
"""
import importlib.util
import sys
import os
import inspect
from typing import List, Dict, Any, Callable, Optional
from .simulator import BettingStrategy


class FixedFractionStrategy(BettingStrategy):
    """
    Bet a fixed fraction of the bankroll each round.
    """
    
    def __init__(self, fraction: float = 0.1):
        """
        Initialize with the fixed fraction to bet.
        
        Args:
            fraction: Fraction of bankroll to bet (0.0 to 1.0)
        """
        self.fraction = max(0.0, min(1.0, fraction))
    
    def get_bet_fraction(self, bankroll: float, round_idx: int, history: List[Dict[str, Any]]) -> float:
        """
        Return the fixed fraction.
        
        Args:
            bankroll: Current bankroll amount
            round_idx: Current round index (0-based)
            history: List of dictionaries with past results
            
        Returns:
            float: Fraction of bankroll to bet (0.0 to 1.0)
        """
        return self.fraction


class KellyCriterionStrategy(BettingStrategy):
    """
    Kelly Criterion strategy that maximizes expected logarithmic growth.
    """
    
    def __init__(self, outcomes_config: List[Dict[str, float]], fraction_limit: float = 1.0):
        """
        Initialize with the outcome configuration.
        
        Args:
            outcomes_config: List of outcome configurations with probabilities and multipliers
            fraction_limit: Upper limit on the bet fraction (0.0 to 1.0)
        """
        self.outcomes = outcomes_config
        self.fraction_limit = max(0.0, min(1.0, fraction_limit))
    
    def get_bet_fraction(self, bankroll: float, round_idx: int, history: List[Dict[str, Any]]) -> float:
        """
        Calculate the Kelly Criterion bet fraction.
        
        Args:
            bankroll: Current bankroll amount
            round_idx: Current round index (0-based)
            history: List of dictionaries with past results
            
        Returns:
            float: Fraction of bankroll to bet (0.0 to 1.0)
        """
        # Calculate expected value
        expected_value = sum(o['probability'] * o['multiplier'] for o in self.outcomes)
        
        # If EV <= 1, don't bet
        if expected_value <= 1.0:
            return 0.0
        
        # Calculate variance
        variance = sum(o['probability'] * (o['multiplier'] - expected_value) ** 2 for o in self.outcomes)
        
        # Calculate Kelly bet fraction: f* = (EV - 1) / variance
        kelly_fraction = (expected_value - 1) / variance if variance > 0 else 0.0
        
        # Apply fraction limit
        return min(kelly_fraction, self.fraction_limit)


class MartingaleStrategy(BettingStrategy):
    """
    Martingale strategy that doubles the bet after each loss.
    """
    
    def __init__(self, base_fraction: float = 0.01, max_fraction: float = 1.0):
        """
        Initialize with base and maximum fractions.
        
        Args:
            base_fraction: The starting bet fraction
            max_fraction: Maximum fraction of bankroll to bet
        """
        self.base_fraction = max(0.0, min(1.0, base_fraction))
        self.max_fraction = max(self.base_fraction, min(1.0, max_fraction))
        self.consecutive_losses = 0
        self.initial_bankroll = None
    
    def get_bet_fraction(self, bankroll: float, round_idx: int, history: List[Dict[str, Any]]) -> float:
        """
        Calculate the Martingale bet fraction.
        
        Args:
            bankroll: Current bankroll amount
            round_idx: Current round index (0-based)
            history: List of dictionaries with past results
            
        Returns:
            float: Fraction of bankroll to bet (0.0 to 1.0)
        """
        # Store initial bankroll on first round
        if round_idx == 0:
            self.initial_bankroll = bankroll
            self.consecutive_losses = 0
            return self.base_fraction
        
        # Check if last round was a win or loss
        last_round = history[-1]
        last_bankroll_before = last_round['bankroll_before']
        current_bankroll = bankroll
        
        # If bankroll increased, reset to base bet
        if current_bankroll > last_bankroll_before:
            self.consecutive_losses = 0
            return self.base_fraction
        
        # Otherwise, double the bet
        self.consecutive_losses += 1
        fraction = self.base_fraction * (2 ** self.consecutive_losses)
        
        # Cap at max fraction
        return min(fraction, self.max_fraction)


class CustomStrategy(BettingStrategy):
    """
    Custom strategy that loads a user-defined bet_fraction function from a Python file.
    """
    
    def __init__(self, strategy_path: str):
        """
        Initialize by loading the custom strategy.
        
        Args:
            strategy_path: Path to the Python file containing the strategy
        """
        self.strategy_path = strategy_path
        self.bet_fraction_func = self._load_strategy(strategy_path)
    
    def _load_strategy(self, file_path: str) -> Callable:
        """
        Load a Python module from file path and extract the bet_fraction function.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            callable: The bet_fraction function from the module
        """
        try:
            # Generate a module name based on the file path
            module_name = os.path.basename(file_path).replace('.py', '')
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                raise ImportError(f"Could not load module from {file_path}")
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if bet_fraction function exists
            if not hasattr(module, 'bet_fraction'):
                raise AttributeError("Module does not contain a 'bet_fraction' function")
                
            # Get the function
            bet_fraction_func = getattr(module, 'bet_fraction')
            
            # Validate function signature
            sig = inspect.signature(bet_fraction_func)
            if len(sig.parameters) != 3:
                raise ValueError(
                    f"bet_fraction function must take exactly 3 parameters: "
                    f"bankroll, round_idx, and history (found {len(sig.parameters)})"
                )
            
            return bet_fraction_func
            
        except Exception as e:
            # If anything goes wrong, fallback to a safe default strategy
            import logging
            logging.error(f"Error loading custom strategy: {e}")
            return lambda bankroll, round_idx, history: 0.01  # Safe default: bet 1%
    
    def get_bet_fraction(self, bankroll: float, round_idx: int, history: List[Dict[str, Any]]) -> float:
        """
        Call the user-defined bet_fraction function.
        
        Args:
            bankroll: Current bankroll amount
            round_idx: Current round index (0-based)
            history: List of dictionaries with past results
            
        Returns:
            float: Fraction of bankroll to bet (0.0 to 1.0)
        """
        try:
            # Call the custom function and clamp the result
            fraction = self.bet_fraction_func(bankroll, round_idx, history)
            return max(0.0, min(1.0, fraction))
        except Exception as e:
            # If the function raises an exception, log it and return a safe bet
            import logging
            logging.error(f"Error in custom bet_fraction function: {e}")
            return 0.01  # Safe default: bet 1% 