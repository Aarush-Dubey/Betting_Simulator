from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Simulation, Outcome
from strategies.models import Strategy


class OutcomeForm(forms.ModelForm):
    """Form for individual outcome within a simulation"""
    class Meta:
        model = Outcome
        fields = ['name', 'probability', 'multiplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'probability': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'multiplier': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class BaseOutcomeFormSet(forms.BaseInlineFormSet):
    """Base formset for outcomes to ensure probabilities sum to 1"""
    def clean(self):
        super().clean()
        
        # Check if any forms have been marked for deletion
        if any(self.deleted_forms):
            return
            
        # Ensure we have at least two outcomes
        valid_forms = [form for form in self.forms if form.is_valid() and not form.cleaned_data.get('DELETE')]
        if len(valid_forms) < 2:
            raise forms.ValidationError("You must have at least two outcomes.")
            
        # Check that probabilities sum to 1
        total_probability = sum(form.cleaned_data.get('probability', 0) for form in valid_forms)
        if not (0.99 <= total_probability <= 1.01):  # Allow small rounding errors
            raise forms.ValidationError(f"The sum of probabilities must be 1.0 (currently {total_probability:.2f}).")


OutcomeFormSet = forms.inlineformset_factory(
    Simulation, Outcome, form=OutcomeForm,
    formset=BaseOutcomeFormSet, extra=2, min_num=2, validate_min=True
)


class SimulationForm(forms.ModelForm):
    """Form for creating or updating a simulation"""
    class Meta:
        model = Simulation
        fields = [
            'name', 'description', 'initial_bankroll', 'num_rounds',
            'bet_fraction', 'num_simulations', 'strategy', 'custom_strategy',
            'is_parameter_sweep', 'sweep_parameter', 'sweep_start', 'sweep_end', 'sweep_steps'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'initial_bankroll': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'num_rounds': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10000'}),
            'bet_fraction': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'num_simulations': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10000'}),
            'strategy': forms.Select(attrs={'class': 'form-select', 'id': 'strategy-select'}),
            'custom_strategy': forms.Select(attrs={'class': 'form-select', 'id': 'custom-strategy-select'}),
            'is_parameter_sweep': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is-parameter-sweep'}),
            'sweep_parameter': forms.Select(attrs={'class': 'form-select', 'id': 'sweep-parameter'}),
            'sweep_start': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sweep_end': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sweep_steps': forms.NumberInput(attrs={'class': 'form-control', 'min': '2', 'max': '100'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Setup sweep_parameter choices
        self.fields['sweep_parameter'].choices = [
            ('', '-- Select Parameter --'),
            ('bet_fraction', 'Bet Fraction'),
            ('initial_bankroll', 'Initial Bankroll'),
        ]
        
        # Filter custom strategies by user if user is provided
        if user and not user.is_anonymous:
            self.fields['custom_strategy'].queryset = Strategy.objects.filter(user=user)
        else:
            self.fields['custom_strategy'].queryset = Strategy.objects.none()
    
    def clean(self):
        cleaned_data = super().clean()
        strategy = cleaned_data.get('strategy')
        custom_strategy = cleaned_data.get('custom_strategy')
        is_parameter_sweep = cleaned_data.get('is_parameter_sweep')
        
        # Custom strategy is required if strategy is 'custom'
        if strategy == 'custom' and not custom_strategy:
            self.add_error('custom_strategy', 'A custom strategy must be selected.')
        
        # Validate parameter sweep values if enabled
        if is_parameter_sweep:
            sweep_parameter = cleaned_data.get('sweep_parameter')
            sweep_start = cleaned_data.get('sweep_start')
            sweep_end = cleaned_data.get('sweep_end')
            sweep_steps = cleaned_data.get('sweep_steps')
            
            if not sweep_parameter:
                self.add_error('sweep_parameter', 'Parameter to sweep is required.')
            
            if sweep_start is None:
                self.add_error('sweep_start', 'Start value is required.')
            
            if sweep_end is None:
                self.add_error('sweep_end', 'End value is required.')
            
            if sweep_steps is None:
                self.add_error('sweep_steps', 'Number of steps is required.')
            
            if sweep_start is not None and sweep_end is not None and sweep_start >= sweep_end:
                self.add_error('sweep_end', 'End value must be greater than start value.')
        
        return cleaned_data 