# Betting Simulation Platform

A Django-based web application for designing and running generalized betting simulations with configurable parameters and visualization capabilities.

## Features

- Configure simulation parameters (bankroll, rounds, etc.)
- Set up multiple outcomes with probabilities and multipliers
- Choose from various betting strategies (Fixed Fraction, Kelly Criterion, Martingale)
- Upload custom betting strategies
- Visualize simulation results with interactive charts
- Parameter sweep capability for strategy optimization

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Setup environment variables:
   ```
   cp .env.example .env
   ```
5. Run migrations:
   ```
   cd betting_sim
   python manage.py migrate
   ```
6. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```
7. Run the server:
   ```
   python manage.py runserver
   ```
8. Visit http://127.0.0.1:8000/ in your browser

## Usage

1. Create a new simulation from the homepage
2. Configure your betting parameters
3. Select or upload a betting strategy
4. Run the simulation
5. View and analyze the results

## Strategies

The system supports the following betting strategies:

- **Fixed Fraction**: Bet a fixed percentage of your bankroll each round
- **Kelly Criterion**: Maximize expected logarithmic growth
- **Martingale**: Double your bet after each loss, reset after a win
- **Custom Strategy**: Upload your own Python script with a `bet_fraction()` function

## Custom Strategy Format

Create a Python file with the following function:

```python
def bet_fraction(bankroll, round_idx, history):
    """
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
    # Your strategy logic here
    return 0.1  # Example: always bet 10% of bankroll
```

## License

MIT 