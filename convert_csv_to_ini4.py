import pandas as pd

# Read the CSV file
df = pd.read_csv('SwitchInventory.csv')

# Print the column names
print(df.columns)

# Open the output file
with open('inventory.ini', 'w') as f:
    # Write the inventory groups and hosts
    for group in df['DeviceType'].unique():
        f.write(f'[{group}]\n')
        for host in df[df['DeviceType'] == group]['IP']:
            f.write(f'{host}\n')
