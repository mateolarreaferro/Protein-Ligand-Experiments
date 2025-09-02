#!/usr/bin/env python3
"""
Visualize Boltz prediction results and analyze binding
"""

import json
import os
from pathlib import Path
import numpy as np

def analyze_prediction(base_name):
    """Analyze a single prediction result"""
    
    results_dir = f"boltz_results_{base_name}"
    pred_dir = Path(results_dir) / "predictions" / base_name
    
    if not pred_dir.exists():
        print(f"❌ No predictions found for {base_name}")
        return None
    
    # Find confidence file
    conf_files = list(pred_dir.glob("confidence_*.json"))
    if not conf_files:
        print(f"❌ No confidence files found for {base_name}")
        return None
    
    # Read confidence scores
    with open(conf_files[0], 'r') as f:
        conf_data = json.load(f)
    
    # Extract key metrics
    result = {
        'name': base_name,
        'confidence_score': conf_data['confidence_score'],
        'ligand_iptm': conf_data.get('ligand_iptm', 0),
        'complex_plddt': conf_data['complex_plddt'],
        'complex_ipde': conf_data['complex_ipde'],
        'structure_file': str(list(pred_dir.glob("*.cif"))[0]) if list(pred_dir.glob("*.cif")) else None
    }
    
    return result

def main():
    """Analyze all predictions"""
    
    print("🔬 Boltz-2 Prediction Analysis")
    print("="*60)
    
    # List of predictions to analyze
    predictions = [
        'htr2a_pocket_psilocin',
        'htr2a_psilocin',
        'htr2a_serotonin', 
        'htr2a_ketanserin'
    ]
    
    results = []
    
    for pred_name in predictions:
        result = analyze_prediction(pred_name)
        if result:
            results.append(result)
    
    if not results:
        print("No results to analyze")
        return
    
    # Display results
    print("\n📊 Binding Affinity Predictions:")
    print("-"*60)
    print(f"{'Compound':<25} {'Confidence':<12} {'Ligand iPTM':<12} {'Complex pLDDT':<12}")
    print("-"*60)
    
    for r in sorted(results, key=lambda x: x['ligand_iptm'], reverse=True):
        name = r['name'].replace('htr2a_', '').replace('htr2a_pocket_', '')
        print(f"{name:<25} {r['confidence_score']:<12.3f} {r['ligand_iptm']:<12.3f} {r['complex_plddt']:<12.3f}")
    
    print("\n📈 Interpretation:")
    print("-"*60)
    print("• Confidence Score: Overall model confidence (0-1, higher is better)")
    print("• Ligand iPTM: Interface confidence for ligand binding (0-1, higher = stronger binding)")
    print("• Complex pLDDT: Per-residue confidence (0-100, >70 is good)")
    print("• Complex iPDE: Interface predicted distance error (lower is better)")
    
    # Hypothesis test
    print("\n🧪 Hypothesis Test:")
    print("-"*60)
    
    # Find results for comparison
    psilocin = next((r for r in results if 'psilocin' in r['name']), None)
    serotonin = next((r for r in results if 'serotonin' in r['name']), None)
    ketanserin = next((r for r in results if 'ketanserin' in r['name']), None)
    
    if psilocin:
        print(f"✓ Psilocin binding score: {psilocin['ligand_iptm']:.3f}")
        if psilocin['ligand_iptm'] > 0.1:
            print("  → Shows binding affinity to HTR2A")
    
    if serotonin:
        print(f"✓ Serotonin binding score: {serotonin['ligand_iptm']:.3f}")
    
    if ketanserin:
        print(f"✓ Ketanserin binding score: {ketanserin['ligand_iptm']:.3f}")
        print("  → Antagonist control")
    
    # Visualization commands
    print("\n🖼️ To visualize structures:")
    print("-"*60)
    for r in results:
        if r['structure_file']:
            print(f"• {r['name']}:")
            print(f"  pymol {r['structure_file']}")
    
    print("\n💡 Or open in ChimeraX:")
    for r in results:
        if r['structure_file']:
            print(f"  open {r['structure_file']}")

if __name__ == "__main__":
    main()