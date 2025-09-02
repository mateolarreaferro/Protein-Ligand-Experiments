#!/usr/bin/env python3
"""
CPU-only version of Boltz runner for memory-constrained systems
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

# Force CPU usage to avoid memory issues
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

def run_prediction(yaml_file, use_msa_server=True):
    """Run Boltz-2 prediction for a given YAML file on CPU"""
    
    if not Path(yaml_file).exists():
        print(f"Error: {yaml_file} not found")
        return False
    
    base_name = Path(yaml_file).stem
    output_dir = f"boltz_results_{base_name}"
    
    # Build command with CPU-friendly settings
    # Use the venv's boltz command
    boltz_cmd = './venv/bin/boltz'
    if not Path(boltz_cmd).exists():
        boltz_cmd = 'boltz'  # Fallback to system boltz
    
    cmd = [boltz_cmd, 'predict', yaml_file]
    
    if use_msa_server:
        cmd.append('--use_msa_server')
    
    # Add memory-saving options
    cmd.extend([
        '--recycling_steps', '1',  # Reduce recycling steps
        '--devices', '1',           # Use single device
        '--accelerator', 'cpu'      # Force CPU
    ])
    
    print(f"\n{'='*60}")
    print(f"Running CPU prediction for: {yaml_file}")
    print(f"Command: {' '.join(cmd)}")
    print(f"Output will be in: {output_dir}/")
    print("⚠️  Note: CPU prediction will be slower but avoids memory issues")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print(f"\n✅ Successfully completed: {yaml_file}")
        
        # Check output
        pred_dir = Path(output_dir) / "predictions" / base_name
        if pred_dir.exists():
            cif_files = list(pred_dir.glob("*.cif"))
            if cif_files:
                print(f"\n🎯 Generated {len(cif_files)} structure(s):")
                for cif in cif_files:
                    print(f"  - {cif.name}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        
        # Provide troubleshooting
        print("\n💡 Troubleshooting tips:")
        print("1. Try reducing the protein size (use a truncated version)")
        print("2. Close other applications to free memory")
        print("3. Consider using the Rowan cloud service directly")
        print("4. Try with a smaller test case first")
        
        return False

def main():
    """Run predictions on CPU"""
    
    print("🧬 Boltz-2 CPU Mode (Memory-Safe)")
    print(f"API Key: {ROWAN_API_KEY[:15]}...")
    
    predictions = [
        ('htr2a_psilocin.yaml', 'Psilocin'),
        ('htr2a_serotonin.yaml', 'Serotonin'),
        ('htr2a_ketanserin.yaml', 'Ketanserin')
    ]
    
    for yaml_file, description in predictions:
        print(f"\n📊 Processing: {description}")
        success = run_prediction(yaml_file)
        if not success:
            print("Stopping due to error")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_prediction(sys.argv[1])
    else:
        main()