import logging

import pandas as pd
from sdv.tabular import GaussianCopula


def load_sample_data(file_path):
    return pd.read_csv(file_path)  # Change the function based on your dataset type (e.g., Excel, JSON, etc.).


def create_metadata(sample_data):
    # Create a metadata dictionary from the column names and their data types
    metadata = {}
    for column in sample_data.columns:
        data_type = str(sample_data[column].dtype)
        metadata[column] = {'type': data_type}
    print(metadata)
    return metadata


def create_synthetic_data_gaussian_copula(file_path, num_rows_to_generate):
    # Step 1: Load sample data
    sample_data = load_sample_data(file_path)

    # Step 2: Create metadata from the sample data
    metadata = create_metadata(sample_data)

    # Step 3: Fit GaussianCopula to the sample data
    copula_model = GaussianCopula()
    copula_model.fit(sample_data)

    # Step 4: Generate synthetic data using the fitted model
    synthetic_data = copula_model.sample(num_rows_to_generate)

    return synthetic_data


# Example usage
sample_data_file = "organizations-100.csv"
num_rows_to_generate = 100

synthetic_data = create_synthetic_data_gaussian_copula(sample_data_file, num_rows_to_generate)

# Display the synthetic data
print(synthetic_data)
