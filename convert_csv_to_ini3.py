import pandas as pd

# Read the CSV file
df = pd.read_csv('exportNetworkDeviceType4901084913444327266.csv')

# Print the column names
print(df.columns)

# Open the output file
with open('inventory.ini', 'w') as f:
    # Write the inventory groups and hosts
    for group in df['Profile:String(128):Required'].unique():
        f.write(f'[{group}]\n')
        for host in df[df['Profile:String(128):Required'] == group]['IP Address:Subnets(a.b.c.d/m#....):Required']:
            ip = host.split('/')[0]  # Split the IP address and subnet mask, and take only the IP address
            f.write(f'{ip}\n')
