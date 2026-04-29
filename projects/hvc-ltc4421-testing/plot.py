import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('output', exist_ok=True)
csv_files = sorted({f.upper(): f for f in glob.glob('*.CSV') + glob.glob('*.csv')}.values())


def load_csv(fname):
    df = pd.read_csv(fname, header=None, usecols=[3, 4])
    df.columns = ['time', 'voltage']
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    df['voltage'] = pd.to_numeric(df['voltage'], errors='coerce')
    return df.dropna()


def save_overlay(series, title, outname, xlim=None):
    """series: list of (fname, label, x_offset)"""
    fig, ax = plt.subplots(figsize=(10, 5))
    for fname, label, x_offset in series:
        df = load_csv(fname)
        ax.plot(df['time'] + x_offset, df['voltage'], linewidth=0.8, label=label)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    ax.set_title(title)
    if xlim:
        ax.set_xlim(*xlim)
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    out = os.path.join('output', outname)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'Saved {out}')


for path in csv_files:
    df = load_csv(path)
    match = re.search(r'(\d+)', path)
    test_num = int(match.group(1)) if match else 0
    base = f'test{test_num}'

    plots = [
        ('scatter', 'Scatter Plot', lambda ax, d=df: ax.scatter(d['time'], d['voltage'], s=1)),
        ('line',    'Line Graph',   lambda ax, d=df: ax.plot(d['time'], d['voltage'], linewidth=0.8)),
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


# --- Overlays ---
save_overlay(
    series=[
        ('TEK0010.CSV', 'Test 10', 0),
        ('TEK0020.CSV', 'Test 20', 0.00007),
    ],
    title='Test 10 & Test 20 - Overlay',
    outname='test10_test20_overlay_line.png',
    xlim=(-0.0002, 0.0007),
)

save_overlay(
    series=[
        ('TEK0009.CSV', 'Test 9',  0),
        ('TEK0022.CSV', 'Test 22', 0),
    ],
    title='Test 9 & Test 22 - Overlay',
    outname='test9_test22_overlay_line.png',
)

save_overlay(
    series=[
        ('TEK0023.CSV', 'Test 23', 0.000075),
        ('TEK0024.CSV', 'Test 24', 0.000045),
    ],
    title='Test 23 & Test 24 - Overlay',
    outname='test23_test24_overlay_line.png',
)
