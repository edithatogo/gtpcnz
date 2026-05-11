import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_parameter_registry(registry_path="docs/calibration/parameter-tiering-v1.7.2.csv"):
    """Loads the main parameter registry."""
    if not os.path.exists(registry_path):
        logging.error(f"Parameter registry not found at {registry_path}")
        raise FileNotFoundError(f"Missing {registry_path}")
    return pd.read_csv(registry_path)

def save_parameter_registry(df, registry_path="docs/calibration/parameter-tiering-v1.7.2.csv"):
    """Saves the updated parameter registry."""
    df.to_csv(registry_path, index=False)
    logging.info(f"Successfully updated parameter registry at {registry_path}")

def ingest_acc_ffs_data(oia_csv_path, registry_df):
    """
    Ingests ACC fee-for-service response data and updates related parameters.
    Expected to address F08 (acc_activity_strength) and S08 (scope_substitution_rate).
    """
    logging.info(f"Attempting to ingest ACC OIA data from {oia_csv_path}")
    
    if not os.path.exists(oia_csv_path):
        logging.warning(f"ACC OIA response not yet available at {oia_csv_path}. Skipping.")
        return registry_df
        
    try:
        acc_data = pd.read_csv(oia_csv_path)
        
        # Placeholder logic: Calculate GP vs Non-GP proportion
        if 'provider_type' in acc_data.columns and 'claim_volume' in acc_data.columns:
            total_vol = acc_data['claim_volume'].sum()
            non_gp_vol = acc_data[acc_data['provider_type'] != 'General Practitioner']['claim_volume'].sum()
            
            estimated_substitution_rate = non_gp_vol / total_vol if total_vol > 0 else 0
            
            # Update registry
            idx = registry_df.index[registry_df['parameter_id'] == 'S08'].tolist()
            if idx:
                registry_df.loc[idx[0], 'current_value'] = round(estimated_substitution_rate, 3)
                registry_df.loc[idx[0], 'source_status'] = 'OIA-2026-002 (Empirical)'
                logging.info(f"Updated S08 (scope_substitution_rate) to {estimated_substitution_rate:.3f}")
                
        # Update F08 based on total volume relative to a benchmark (placeholder logic)
        # This requires more complex logic once actual data schema is known.
        
    except Exception as e:
        logging.error(f"Error parsing ACC OIA data: {e}")
        
    return registry_df

def ingest_moh_capitation_data(oia_csv_path, registry_df):
    """
    Ingests MOH Capitation formula data.
    Expected to address F01, F02, D01.
    """
    logging.info(f"Attempting to ingest MOH OIA data from {oia_csv_path}")
    if not os.path.exists(oia_csv_path):
        logging.warning(f"MOH OIA response not yet available at {oia_csv_path}. Skipping.")
        return registry_df
    # Ingestion logic to be implemented when schema is known.
    return registry_df

def ingest_ambulance_disposition_data(oia_csv_path, registry_df):
    """
    Ingests St John ambulance disposition data.
    Expected to address H04, H05.
    """
    logging.info(f"Attempting to ingest Ambulance OIA data from {oia_csv_path}")
    if not os.path.exists(oia_csv_path):
        logging.warning(f"Ambulance OIA response not yet available at {oia_csv_path}. Skipping.")
        return registry_df
    # Ingestion logic to be implemented when schema is known.
    return registry_df

def main():
    logging.info("Starting OIA Data Ingestion Pipeline...")
    
    try:
        registry = load_parameter_registry()
        
        # Define expected paths for responses
        oia_dir = "docs/audit/oia_responses"
        acc_path = os.path.join(oia_dir, "OIA-2026-002-ACC.csv")
        moh_path = os.path.join(oia_dir, "OIA-2026-001-MOH.csv")
        stjohn_path = os.path.join(oia_dir, "OIA-2026-003-StJohn.csv")
        
        # Process each source
        registry = ingest_acc_ffs_data(acc_path, registry)
        registry = ingest_moh_capitation_data(moh_path, registry)
        registry = ingest_ambulance_disposition_data(stjohn_path, registry)
        
        save_parameter_registry(registry)
        
    except Exception as e:
        logging.error(f"Ingestion pipeline failed: {e}")

if __name__ == "__main__":
    main()
