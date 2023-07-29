import base64
import pandas as pd
import streamlit as st
from sdv.tabular import GaussianCopula
from faker import Faker
from sdv.metadata import SingleTableMetadata

# Helper function to create metadata with appropriate transformers
def create_metadata(sample_data):
    metadata = SingleTableMetadata()

    for column in sample_data.columns:
        if sample_data[column].dtype == "int64":
            metadata.add_column(column, type='integer')
        elif sample_data[column].dtype == "float64":
            metadata.add_column(column, type='float')
        else:
            metadata.add_column(column, type='categorical')

    return metadata

# Helper function to generate fake data using Faker
def generate_fake_data(provider, num_rows):
    faker = Faker()
    return [getattr(faker, provider)() for _ in range(num_rows)]

# Streamlit web application
def main():
    st.title("Synthetic Data Generation App")
    st.markdown("---")

    st.subheader("Upload Sample Data")
    st.write("Please upload a CSV file as your sample data.")

    # File upload widget
    uploaded_file = st.file_uploader("Upload Sample Data CSV", type=["csv"])

    if uploaded_file is not None:
        # Load the sample data
        sample_data = pd.read_csv(uploaded_file, encoding='latin-1')

        # Show the columns from the sample data in a table
        st.subheader("Sample Data Columns:")
        st.dataframe(sample_data.columns)

        # Get user's choice for primary keys
        primary_keys = st.multiselect("Select primary keys:", sample_data.columns)

        # Create metadata with appropriate transformers
        metadata = create_metadata(sample_data)

        # Initialize and fit the SDV model
        sdv = GaussianCopula(metadata=metadata, primary_key=primary_keys)
        sdv.fit(sample_data)

        # Generate synthetic data
        num_rows = st.number_input("Enter the number of rows for data generation:", min_value=1, step=1, value=10)

        # Create a synthetic data DataFrame
        synthetic_data = sdv.sample(num_rows)

        # Replace selected columns with fake data
        for column in sample_data.columns:
            if column not in primary_keys and column in metadata and metadata[column]["type"] == "categorical":
                provider = column.replace(" ", "_").lower()
                fake_data = generate_fake_data(provider, num_rows)
                synthetic_data[column] = fake_data

        # Show generated data
        st.markdown("---")
        st.subheader("Generated Synthetic Data:")
        st.dataframe(synthetic_data)

        # Download link for the generated data
        st.markdown("---")
        st.subheader("Download Generated Data:")
        csv_download_link(synthetic_data, "generated_data.csv", "Click here to download the synthetic data")

# Helper function to create a download link for the DataFrame as CSV
def csv_download_link(df, filename, link_text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
