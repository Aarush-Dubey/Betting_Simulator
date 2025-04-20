/**
 * Custom JavaScript for the Betting Simulation Platform
 */

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Strategy selector in simulation form
    const strategySelect = document.getElementById('strategy-select');
    const customStrategyContainer = document.getElementById('custom-strategy-container');
    
    if (strategySelect && customStrategyContainer) {
        function updateCustomStrategy() {
            if (strategySelect.value === 'custom') {
                customStrategyContainer.style.display = 'block';
            } else {
                customStrategyContainer.style.display = 'none';
            }
        }
        
        strategySelect.addEventListener('change', updateCustomStrategy);
        updateCustomStrategy(); // Initial state
    }
    
    // Parameter sweep logic in simulation form
    const parameterSweepCheckbox = document.getElementById('is-parameter-sweep');
    const parameterSweepContainer = document.getElementById('parameter-sweep-container');
    
    if (parameterSweepCheckbox && parameterSweepContainer) {
        function updateParameterSweep() {
            if (parameterSweepCheckbox.checked) {
                parameterSweepContainer.style.display = 'block';
            } else {
                parameterSweepContainer.style.display = 'none';
            }
        }
        
        parameterSweepCheckbox.addEventListener('change', updateParameterSweep);
        updateParameterSweep(); // Initial state
    }
    
    // Outcome formset logic
    const addOutcomeBtn = document.getElementById('add-outcome-btn');
    const outcomeFormset = document.getElementById('outcome-formset');
    const totalFormsInput = document.getElementById('id_outcomes-TOTAL_FORMS');
    
    if (addOutcomeBtn && outcomeFormset && totalFormsInput) {
        addOutcomeBtn.addEventListener('click', function() {
            const forms = outcomeFormset.getElementsByClassName('outcome-form');
            const formCount = forms.length;
            
            // Clone the first form
            const newForm = forms[0].cloneNode(true);
            
            // Update form index
            const inputs = newForm.getElementsByTagName('input');
            const selects = newForm.getElementsByTagName('select');
            const labels = newForm.getElementsByTagName('label');
            
            for (let i = 0; i < inputs.length; i++) {
                inputs[i].value = '';
                
                if (inputs[i].id) {
                    inputs[i].id = inputs[i].id.replace('-0-', '-' + formCount + '-');
                    inputs[i].name = inputs[i].name.replace('-0-', '-' + formCount + '-');
                }
            }
            
            for (let i = 0; i < selects.length; i++) {
                if (selects[i].id) {
                    selects[i].id = selects[i].id.replace('-0-', '-' + formCount + '-');
                    selects[i].name = selects[i].name.replace('-0-', '-' + formCount + '-');
                }
            }
            
            for (let i = 0; i < labels.length; i++) {
                if (labels[i].htmlFor) {
                    labels[i].htmlFor = labels[i].htmlFor.replace('-0-', '-' + formCount + '-');
                }
            }
            
            // Append new form with fade-in animation
            newForm.classList.add('fade-in');
            outcomeFormset.appendChild(newForm);
            
            // Update total forms
            totalFormsInput.value = formCount + 1;
        });
    }
    
    // Handle run simulation form submission
    const runForm = document.querySelector('form.run-simulation-form');
    const runSpinner = document.getElementById('run-spinner');
    
    if (runForm && runSpinner) {
        runForm.addEventListener('submit', function() {
            runSpinner.classList.remove('d-none');
            const button = runForm.querySelector('button[type="submit"]');
            button.disabled = true;
            button.textContent = 'Running...';
            button.prepend(runSpinner);
        });
    }
}); 