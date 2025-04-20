"""
Vercel-specific settings and utilities for Django deployment.
"""

import os
from django.db.migrations.executor import MigrationExecutor


def apply_vercel_patches():
    """
    Apply necessary patches for Vercel deployment.
    
    This function applies patches that help Django work better in Vercel's
    serverless environment, such as bypassing database migrations.
    """
    if os.environ.get('VERCEL_REGION') or os.environ.get('VERCEL'):
        # Store the original migration plan method
        original_migration_plan = MigrationExecutor.migration_plan
        
        # Define a patched method that returns an empty list of migrations on Vercel
        def patched_migration_plan(self, targets, clean_start=False):
            if os.environ.get('VERCEL_REGION') or os.environ.get('VERCEL'):
                print("Bypassing migration plan on Vercel")
                return []
            return original_migration_plan(self, targets, clean_start)
        
        # Apply the patch
        MigrationExecutor.migration_plan = patched_migration_plan
        
        print("Vercel patches applied successfully")
    else:
        print("Not running on Vercel, skipping patches") 