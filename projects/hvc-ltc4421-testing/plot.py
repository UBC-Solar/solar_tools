import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('output', exist_ok=True)
csv_files = sorted({f.upper(): f for f in glob.glob('*.CSV') + glob.glob('*.csv')}.values())

for path in csv_files:
    df = pd.read_csv(path, header=None, usecols=[3, 4])
    df.columns = ['time', 'voltage']
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    df['voltage'] = pd.to_numeric(df['voltage'], errors='coerce')
    df = df.dropna()

    plt.figure(figsize=(10, 5))
    plt.scatter(df['time'], df['voltage'], s=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title(path)
    plt.grid(True)
    plt.tight_layout()

    out = os.path.join('output', path.rsplit('.', 1)[0] + '.png')
    plt.savefig(out, dpi=150)
    plt.close()
    print(f'Saved {out}')
