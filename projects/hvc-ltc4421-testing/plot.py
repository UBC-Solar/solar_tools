import os
import glob
import re
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

    # Extract test number from filename (e.g. TEK0003.CSV -> 3)
    match = re.search(r'(\d+)', path)
    test_num = int(match.group(1)) if match else 0
    base = f'test{test_num}'

    plots = [
        ('scatter', 'Scatter Plot', lambda ax: ax.scatter(df['time'], df['voltage'], s=1)),
        ('line',    'Line Graph',   lambda ax: ax.plot(df['time'], df['voltage'], linewidth=0.8)),
    ]

    for suffix, label, draw in plots:
        fig, ax = plt.subplots(figsize=(10, 5))
        draw(ax)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Voltage (V)')
        ax.set_title(f'Test {test_num} - {label}')
        ax.grid(True)
        fig.tight_layout()

        out = os.path.join('output', f'{base}_{suffix}.png')
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f'Saved {out}')
