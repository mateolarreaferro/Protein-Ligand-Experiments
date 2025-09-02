# Psilocin vs Serotonin Binding at 5-HT2A: A Boltz-2 Computational Study

## 🎯 Project Overview

This experiment uses Boltz-2, a state-of-the-art protein-ligand structure prediction model, to investigate whether psilocin (the active metabolite of psilocybin) exhibits stronger predicted binding affinity than serotonin at the human 5-HT2A receptor.

## Scientific Background

### Why This Matters
The 5-HT2A receptor (HTR2A) is a key target for:
- **Psychedelics**: Psilocin (from magic mushrooms) acts as a potent agonist
- **Endogenous signaling**: Serotonin is the natural ligand
- **Therapeutics**: Understanding differential binding can inform drug development for depression, PTSD, and other conditions

### Why Psilocin, Not Psilocybin?
Psilocybin is a **prodrug** - it's dephosphorylated to psilocin in vivo. Psilocin is the actual psychoactive compound that crosses the blood-brain barrier and binds to serotonin receptors.

## Experimental Design

### Target
- **Protein**: Human 5-HT2A receptor (HTR2A)
- **UniProt ID**: P28223
- **Length**: 471 amino acids

### Ligands Tested

1. **Psilocin** (psychedelic agonist)
   - SMILES: `CN(C)CCC1=CNC2=C1C(=CC=C2)O`
   - Expected: Strong binding

2. **Serotonin** (endogenous agonist)
   - SMILES: `C1=CC2=C(C=C1O)C(=CN2)CCN`
   - Expected: Baseline binding

3. **Ketanserin** (antagonist control)
   - SMILES: `C1CN(CCC1C(=O)C2=CC=C(C=C2)F)CCN3C(=O)C4=CC=CC=C4NC3=O`
   - Expected: Strong binding (as antagonist)

## Setup Instructions

### 1. Environment Setup
```bash
# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Running Predictions

Run Boltz-2 for each ligand separately:

```bash
# Predict psilocin binding
boltz predict htr2a_psilocin.yaml --use_msa_server

# Predict serotonin binding
boltz predict htr2a_serotonin.yaml --use_msa_server

# Predict ketanserin binding (optional control)
boltz predict htr2a_ketanserin.yaml --use_msa_server
```

### 3. Analyzing Results

Results are saved in `output/predictions/<input-name>/affinity-*.json`

Key metrics to compare:
- **Binder probability**: Higher = stronger predicted binding
- **IC₅₀ (µM)**: Lower = stronger predicted potency
- **Binding pose**: Visual inspection of ligand positioning

## Expected Outcomes

### Hypothesis
Psilocin should show comparable or stronger predicted binding than serotonin at 5-HT2A, reflecting its known psychedelic potency.

### Rank Order (Expected)
1. Psilocin ≥ Serotonin (both agonists)
2. Ketanserin (strong antagonist binding)

## Important Considerations

### Model Limitations
- Boltz-2 predicts one ligand at a time (no competitive binding)
- GPCRs like 5-HT2A are highly flexible; predictions may vary
- No explicit modeling of water molecules or ions
- Results are screening-grade, not definitive

### Interpretation
- Use predictions for hypothesis generation
- Validate significant findings experimentally
- Consider conformational dynamics not captured in static structures

## Output Structure
```
output/
└── predictions/
    ├── htr2a_psilocin/
    │   ├── affinity-*.json  # Binding metrics
    │   └── *.pdb            # Predicted structure
    ├── htr2a_serotonin/
    │   ├── affinity-*.json
    │   └── *.pdb
    └── htr2a_ketanserin/
        ├── affinity-*.json
        └── *.pdb
```

## Visualization

After running predictions, you can:
1. Load PDB files in PyMOL or ChimeraX
2. Compare ligand binding poses
3. Analyze pocket interactions
4. Generate publication-quality figures

## Alternative: Web Interface

For zero-setup predictions, use Rowan's web interface:
1. Visit [Rowan's Protein-Ligand Co-Folding](https://rowansci.com/)
2. Paste HTR2A sequence + ligand SMILES
3. Submit and receive results in minutes

## References

- [Boltz-2 Documentation](https://github.com/rowancomputing/boltz)
- [HTR2A UniProt Entry](https://www.uniprot.org/uniprotkb/P28223)
- [Psilocin PubChem](https://pubchem.ncbi.nlm.nih.gov/)
- [5-HT2A Receptor Guide to Pharmacology](https://www.guidetopharmacology.org/)

## Citation

If you use this experimental setup in your research, please cite:
- Boltz-2 paper (when published)
- Relevant structural biology papers for 5-HT2A
- This repository for the experimental protocol