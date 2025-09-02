#!/usr/bin/env python3
"""
Wrapper script to run Boltz-2 predictions with Rowan API key
"""

import os
import sys
import subprocess
from pathlib import Path

# Import API key from settings
try:
    from settings import ROWAN_API_KEY
except ImportError:
    print("Error: settings.py not found. Please create it with your ROWAN_API_KEY.")
    sys.exit(1)

# Set the API key as environment variable
os.environ['ROWAN_API_KEY'] = ROWAN_API_KEY

def run_prediction(yaml_file, use_msa_server=True):
    """Run Boltz-2 prediction for a given YAML file"""
    
    if not Path(yaml_file).exists():
        print(f"Error: {yaml_file} not found")
        return False
    
    cmd = ['boltz', 'predict', yaml_file]
    if use_msa_server:
        cmd.append('--use_msa_server')
    
    print(f"\n{'='*60}")
    print(f"Running prediction for: {yaml_file}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print(f"✅ Successfully completed: {yaml_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running prediction for {yaml_file}: {e}")
        return False
    except FileNotFoundError:
        print("❌ Error: 'boltz' command not found. Please install it with: pip install boltz")
        return False

def main():
    """Run all predictions"""
    
    print("🧬 Starting Boltz-2 Protein-Ligand Binding Predictions")
    print(f"API Key configured: {ROWAN_API_KEY[:15]}...")
    
    # List of prediction files
    predictions = [
        ('htr2a_psilocin.yaml', 'Psilocin (psychedelic agonist)'),
        ('htr2a_serotonin.yaml', 'Serotonin (endogenous agonist)'),
        ('htr2a_ketanserin.yaml', 'Ketanserin (antagonist control)')
    ]
    
    results = []
    
    for yaml_file, description in predictions:
        print(f"\n📊 {description}")
        success = run_prediction(yaml_file)
        results.append((yaml_file, description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📈 SUMMARY")
    print(f"{'='*60}")
    
    for yaml_file, description, success in results:
        status = "✅ Complete" if success else "❌ Failed"
        print(f"{status} - {description} ({yaml_file})")
    
    print(f"\n💡 Results saved in: output/predictions/")
    print("🔬 Compare IC50 values and binder probabilities to test the hypothesis")

if __name__ == "__main__":
    # Check if specific file provided as argument
    if len(sys.argv) > 1:
        for yaml_file in sys.argv[1:]:
            run_prediction(yaml_file)
    else:
        # Run all predictions
        main()