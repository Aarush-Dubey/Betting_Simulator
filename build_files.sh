#!/bin/bash
# Simple build script for Vercel deployment
echo "Creating static files directory..."
mkdir -p betting/betting_sim/staticfiles/css betting/betting_sim/staticfiles/js
echo "Creating basic static files..."
echo "body { font-family: Arial, sans-serif; }" > betting/betting_sim/staticfiles/css/style.css
echo "console.log(\"Vercel deployment\");" > betting/betting_sim/staticfiles/js/main.js
echo "Build complete!"
