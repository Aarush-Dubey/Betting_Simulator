# Betting Simulation Platform

A Django-based web application for designing and running generalized betting simulations with configurable parameters and visualization capabilities.

![Betting Simulation Platform](https://via.placeholder.com/800x400?text=Betting+Simulation+Platform)

## Features

- 📊 Configure simulation parameters (bankroll, rounds, etc.)
- 🎯 Set up multiple outcomes with probabilities and multipliers
- 📈 Choose from various betting strategies (Fixed Fraction, Kelly Criterion, Martingale)
- 🧰 Upload custom betting strategies using Python
- 📉 Visualize simulation results with interactive charts
- 🔄 Parameter sweep capability for strategy optimization
- 📋 Dashboard to compare and analyze results

## Technology Stack

- **Backend**: Django 4.2.7, Python 3.x
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Visualization**: Plotly, Matplotlib
- **Database**: SQLite (default), extensible to other databases

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Aarush-Dubey/Betting_Simulator.git
   cd Betting_Simulator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Setup environment variables:
   ```bash
   cp .env.example .env
   ```

5. Run migrations:
   ```bash
   cd betting_sim
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the server:
   ```bash
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser

## Application Structure

The application is organized into the following Django apps:

- **core**: Base templates, user authentication, and homepage
- **simulation**: Models, forms, and views for creating and running simulations
- **strategies**: Custom strategy management (upload, validation)
- **dashboard**: Data visualization and result analysis

## Usage Guide

### Creating a Simulation

1. Navigate to "New Simulation"
2. Enter basic information (name, description)
3. Set simulation parameters:
   - Initial bankroll amount
   - Number of rounds
   - Number of simulations to run
4. Define betting outcomes:
   - Add outcome names (e.g., "Win", "Loss")
   - Set probabilities (must sum to 1.0)
   - Define multipliers for each outcome
5. Choose a betting strategy
6. Save the simulation

### Running a Simulation

1. Go to your saved simulation
2. Click "Run Simulation"
3. View results once processing is complete

### Analyzing Results

- View bankroll trajectory charts
- Analyze outcome distribution
- Compare different strategies
- Export data to CSV for further analysis

## Built-in Strategies

### Fixed Fraction
Bet a fixed percentage of your bankroll each round.

### Kelly Criterion
Optimize bet size to maximize expected logarithmic growth of wealth.

### Martingale
Double your bet after each loss, reset after a win.

## Custom Strategies

You can create and upload your own betting strategies in Python. Example:

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

## Screenshots

- Homepage
- Simulation creation
- Results dashboard
- Strategy comparison

## License

MIT

## Contact

[Your Contact Information]

## Acknowledgments

- [List any libraries, resources or inspirations] 