import pandas as pd

# Read CSV file
df = pd.read_csv("WAQI dataset - Sheet1.csv")  # Use read_excel("your_file.xlsx") for Excel

# Display the first 10 records
print(df.dtypes)
print(df.describe())
print(df.shape)
df.columns = ["Timestamp", "Continent", "Country", "City", "AQI", "PM2.5", "PM10", "NO2"]
print(df.head(10))  # Check if it worked

print(df.isnull().sum())  # Count missing values per column
