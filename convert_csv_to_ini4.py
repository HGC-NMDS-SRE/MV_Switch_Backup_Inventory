import pandas as pd

# Read the CSV file
df = pd.read_csv('SwitchInventory.csv')

# Print the column names
print(df.columns)

# Open the output file
with open('inventory.ini', 'w') as f:
    # Write all hosts without grouping
    for host in df['IP']:
        f.write(f'{host}\n')
