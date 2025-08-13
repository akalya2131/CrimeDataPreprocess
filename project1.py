import pandas as pd
import numpy as np

# Path to your raw dataset
file_path = r"C:\Users\akaly\OneDrive\Desktop\PythonforDS\crime.csv"
df = pd.read_csv(file_path)

# 1. Handle Missing Values
num_cols = df.select_dtypes(include=[np.number]).columns
df[num_cols] = df[num_cols].apply(lambda col: col.fillna(col.mean()))

cat_cols = df.select_dtypes(exclude=[np.number]).columns
df[cat_cols] = df[cat_cols].apply(lambda col: col.fillna(col.mode()[0] if not col.mode().empty else col))

# 2. Remove Duplicates
df.drop_duplicates(inplace=True)

# 3. Outlier Removal using IQR
for col in num_cols:
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    df = df[(df[col] >= lower) & (df[col] <= upper)]

# Save cleaned data in chunks
cleaned_path = r"C:\Users\akaly\OneDrive\Desktop\PythonforDS\crime_cleaned.csv"
chunk_size = 100000
with open(cleaned_path, 'w', newline='', encoding='utf-8') as f:
    for i in range(0, len(df), chunk_size):
        df.iloc[i:i+chunk_size].to_csv(f, header=(i == 0), index=False)

print("Cleaned file saved at:", cleaned_path)
