# Synthetic Data Generation App

The Synthetic Data Generation App is a Streamlit web application that allows users to upload a sample CSV file and generate synthetic data based on that sample. The app uses the Synthetic Data Vault (SDV) library, specifically the GaussianCopula model, to learn the statistical properties of the sample data and create synthetic data that closely resembles the original data.


## How to Use the App

1. **Upload Sample Data**: To get started, click on the "Upload Sample Data CSV" button and select a CSV file containing your sample data. The app will then display the columns from the sample data in a table.

2. **Select Locale**: Choose the locale for generating fake data using the drop-down menu. The available locales are "en_US," "en_GB," "es_ES," "fr_FR," "de_DE," and "en_IN."

3. **Select Primary Keys**: Select one or more columns from your sample data to be used as primary keys. These columns will be used to maintain relationships between rows in the synthetic data.

4. **Select Columns for Fake Data Generation**: Choose one or more columns from your sample data for which you want to generate fake data. The app will use the Faker library to generate fake data based on the selected locale.

5. **Generate Synthetic Data**: After making your selections, the app will fit the GaussianCopula model on the sample data and generate synthetic data. Specify the number of rows you want in the synthetic data using the number input.

6. **View and Download Synthetic Data**: The app will display the generated synthetic data in a table. You can download the synthetic data as a CSV file by clicking on the "Click here to download the synthetic data" link.

## Requirements

- Python 3.7 or higher
- Streamlit
- Pandas
- SDV (Synthetic Data Vault)
- Faker

You can install the required packages using the following command:

## How to Run the App

1. Clone this repository to your local machine:
2. Install the required packages (if you haven't already) using the command mentioned in the Requirements section, use command "pip install -r requirements.txt".

3. Run the Streamlit app or from terminal execute command "streamlit run main.py"

4. The app should open in your default web browser. If it doesn't, look for the URL displayed in the terminal after running the previous command, and open it in your web browser manually.

## Note

- This application is intended for educational and testing purposes only (You can use this to generate data set for Performance test as well). Do not use the generated synthetic data for real-world scenarios or any sensitive data.

## License

This project is licensed under the [License](LICENSE).
