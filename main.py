import base64
import pandas as pd
import streamlit as st
from sdv.tabular import GaussianCopula

# Helper function to get unique column names with checkboxes
def get_unique_column_selection(all_columns):
    unique_columns = st.multiselect("Select columns for unique data generation:", all_columns)
    return unique_columns

# Function to generate unique value for a column
def generate_unique_value(column_data, unique_values):
    while True:
        value = column_data.sample(n=1).values[0]
        if value not in unique_values:
            unique_values.add(value)
            return value

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

        # Get unique column selection using checkboxes
        unique_columns = get_unique_column_selection(sample_data.columns.tolist())

        if len(unique_columns) > 0:
            # Initialize and fit the SDV model
            sdv = GaussianCopula()
            sdv.fit(sample_data)

            # Generate synthetic data
            num_rows = st.number_input("Enter the number of rows for data generation:", min_value=1, step=1, value=10)

            # Create a synthetic data DataFrame
            synthetic_data = sdv.sample(num_rows)

            # Generate unique values for selected columns
            unique_values_dict = {column: set() for column in unique_columns}

            for column in unique_columns:
                column_data = sample_data[column]
                unique_values = unique_values_dict[column]
                for i in range(num_rows):
                    synthetic_data.at[i, column] = generate_unique_value(column_data, unique_values)

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
