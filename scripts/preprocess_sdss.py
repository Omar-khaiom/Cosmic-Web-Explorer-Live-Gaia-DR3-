#!/usr/bin/env python3
"""
Preprocess SDSS galaxy data
Cleans and formats raw galaxy observations for visualization
"""

import pandas as pd
import numpy as np

def preprocess_sdss_data(input_file, output_file):
    """Process raw SDSS data into clean format"""
    # Load raw data
    data = pd.read_csv(input_file)
    
    # TODO: Add preprocessing logic
    # - Remove outliers
    # - Normalize coordinates
    # - Filter by magnitude
    
    # Save processed data
    data.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

if __name__ == "__main__":
    preprocess_sdss_data("../data/galaxies_raw.csv", "../data/galaxies_final.csv")