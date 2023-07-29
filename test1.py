import base64
import pandas as pd
import streamlit as st
from sdv.tabular import GaussianCopula
from faker import Faker


# Helper function to generate fake data using Faker
def generate_fake_data(column, num_rows, locale):
    faker = Faker(locale=locale)
    fake_data = [getattr(faker, column)() for _ in range(num_rows)]
    return fake_data


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

        # Locale selection
        locale = st.selectbox("Select Locale:", ["en_US", "en_GB", "es_ES", "fr_FR", "de_DE", "en_IN"])

        # Get user's choice for primary key (multiple selection allowed)
        primary_keys = st.multiselect("Select primary keys:", sample_data.columns)

        # Get user's choice for generating fake data for columns (multiple selection allowed)
        fake_data_columns = st.multiselect("Select columns for fake data generation:", sample_data.columns)

        # Initialize and fit the SDV model
        sdv = GaussianCopula(primary_key=primary_keys,
                             enforce_min_max_values=False,
                             anonymize_fields={'name': 'name'})
        sdv.fit(sample_data)

        # Generate synthetic data
        num_rows = st.number_input("Enter the number of rows for data generation:", min_value=1, step=1, value=10)

        # Create a synthetic data DataFrame
        synthetic_data = sdv.sample(num_rows)

        # Generate fake data for the selected columns
        for fake_data_column in fake_data_columns:
            if fake_data_column in sample_data.columns:
                fake_data = generate_fake_data(fake_data_column, num_rows, locale)
                synthetic_data[fake_data_column] = fake_data

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
