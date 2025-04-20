from django import forms
from django.conf import settings
from .models import Strategy
import os
import re


class StrategyForm(forms.ModelForm):
    """
    Form for uploading and validating custom strategy files.
    """
    class Meta:
        model = Strategy
        fields = ['name', 'description', 'file']
    
    def clean_file(self):
        """
        Validate the uploaded strategy file:
        1. Check file extension
        2. Check file size
        3. Check if it contains required function
        """
        file = self.cleaned_data.get('file')
        
        if not file:
            raise forms.ValidationError("Please upload a strategy file.")
        
        # Check file extension
        name, ext = os.path.splitext(file.name)
        if ext.lower() != '.py':
            raise forms.ValidationError("Only Python (.py) files are allowed.")
        
        # Check file size
        if file.size > settings.MAX_STRATEGY_SIZE:
            max_size_kb = settings.MAX_STRATEGY_SIZE / 1024
            raise forms.ValidationError(f"File size must be under {max_size_kb} KB.")
        
        # Check for bet_fraction function
        file_content = file.read().decode('utf-8')
        file.seek(0)  # Reset file pointer
        
        # Simple pattern matching to check for function definition
        function_pattern = r'def\s+bet_fraction\s*\(\s*bankroll\s*,\s*round_idx\s*,\s*history\s*\)'
        if not re.search(function_pattern, file_content):
            raise forms.ValidationError(
                "The file must contain a 'bet_fraction(bankroll, round_idx, history)' function."
            )
        
        return file 