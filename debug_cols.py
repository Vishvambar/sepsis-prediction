import pandas as pd

df = pd.read_csv(r'c:\Users\Admin\Desktop\mimic-iv-clinical-database-demo-2.2\Dataset.csv', nrows=5)
print("Columns:", df.columns.tolist())
for col in df.columns:
    print(f"'{col}'")
