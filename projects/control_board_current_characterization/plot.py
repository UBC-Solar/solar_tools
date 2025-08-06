import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys

# 

# Run in terminal with `python plot.py <filename>` or `python plot.py all` to process all files

# Files:
# TEK0008.CSV = First run recording startup, 5 second total time
# TEK0012.CSV = Startup with 100 ms div size, for 1s total recording time
# TEK0015.CSV = Full startup sequence with 1s div size for 10s total recording time

# Files that show the capacitor current spike: 12 and 17
# TEK0012: 0.0440 to 0.0512 s
# TEK0017: 0.0292 to 0.0400 s

VOLTAGE_OFFSET = 1.67 # Internal voltage offset of the TMCS1108A3U current sensor, derived from csv data

def smooth_data(data, window_size=11):
    """
    Apply moving average smoothing to data to reduce noise.
    
    Args:
        data (array): Input data to smooth
        window_size (int): Size of the smoothing window
    
    Returns:
        array: Smoothed data
    """
    if len(data) < window_size:
        return data
    
    # Pad the data at the edges to handle boundary effects
    pad_width = window_size // 2
    padded_data = np.pad(data, pad_width, mode='edge')
    
    # Apply moving average filter, 11 points
    smoothed = np.convolve(padded_data, np.ones(window_size)/window_size, mode='same')
    
    # Remove padding
    return smoothed[pad_width:-pad_width]

def read_tek_csv(filename):
    """
    Read a Tektronix CSV file and extract time and voltage data.
    
    Args:
        filename (str): Path to the CSV file
        
    Returns:
        tuple: (time_data, voltage_data) as numpy arrays
    """
    # Read the CSV file, skipping the header information
    # The actual data starts after the metadata rows
    data = []
    time_data = []
    voltage_data = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    # Find where the actual data starts (rows with time and voltage values)
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 5:
            try:
                # Try to parse the 4th and 5th columns as time and voltage
                time_val = float(parts[3])
                voltage_val = float(parts[4])
                time_data.append(time_val)
                voltage_data.append(voltage_val)
            except (ValueError, IndexError):
                # Skip rows that can't be parsed (metadata rows)
                continue
    
    return np.array(time_data), np.array(voltage_data)

def plot_voltage_and_current(filename, sensitivity_mv_per_a=200, time_min=None, time_max=None, output_filename=None, show_smoothed=True):
    """
    Create time vs voltage and time vs current plots for a given CSV file.
    
    Args:
        filename (str): Path to the CSV file
        sensitivity_mv_per_a (float): Sensitivity in mV/A (default: 200)
        time_min (float): Minimum time to display on x-axis (default: None, uses data min)
        time_max (float): Maximum time to display on x-axis (default: None, uses data max)
        output_filename (str): Custom base filename for output files (default: None, uses CSV base filename)
        show_smoothed (bool): Whether to display smoothed data (default: True)
    """
    # Read the data
    time, voltage = read_tek_csv(filename)
    
    # For plot 12, use higher offset (0.08V higher than standard)
    # Next time, manually note down the default voltage for 0 A so this isn't an issue (for every test)
    if os.path.splitext(os.path.basename(filename))[0] in ['TEK0012']: voltage_offset = VOLTAGE_OFFSET - 0.08
    else: voltage_offset = VOLTAGE_OFFSET
    
    # Apply voltage offset
    voltage = voltage - voltage_offset
    
    # Set any negative voltage values to the default 0 V
    voltage[voltage < -0.1] = 0
    
    # Apply smoothing to reduce noise
    voltage_smooth = smooth_data(voltage, window_size=11)
    
    # Convert sensitivity from mV/A to V/A
    sensitivity_v_per_a = sensitivity_mv_per_a / 1000
    
    # Calculate current using I = V / sensitivity (using smoothed voltage)
    current = voltage / sensitivity_v_per_a
    
    # Apply smoothing to current as well
    current_smooth = smooth_data(current, window_size=11)
    
    # Get base filename for saving
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    if output_filename is not None:
        base_filename = output_filename
    
    # Extract test number from filename (e.g., "0012" from "TEK0012.CSV")
    test_number = os.path.splitext(os.path.basename(filename))[0].replace('TEK', '')
    
    # Create voltage plot
    fig1, ax1 = plt.subplots(1, 1, figsize=(12, 6))
    if show_smoothed:
        ax1.plot(time, voltage_smooth, 'b-', linewidth=1, label='Smoothed')
    ax1.plot(time, voltage, 'b-', linewidth=0.3 if show_smoothed else 1, alpha=0.7 if show_smoothed else 1, label='Raw')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title(f'Voltage vs Time - {os.path.basename(filename)} (Offset: -{voltage_offset:.2f}V)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Add test number in top left corner
    ax1.text(0.02, 0.98, f'Test {test_number}', transform=ax1.transAxes, 
             fontsize=12, fontweight='bold', verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Set time range if specified
    if time_min is not None or time_max is not None:
        ax1.set_xlim(time_min, time_max)
        # Set y-axis to match displayed data range
        time_mask = ((time_min is None) or (time >= time_min)) & ((time_max is None) or (time <= time_max))
        ax1.set_ylim(voltage[time_mask].min() * 0.95, voltage[time_mask].max() * 1.05)
    
    # Save voltage plot
    voltage_filename = f"{base_filename}_voltage.png"
    plt.tight_layout()
    plt.savefig(voltage_filename, dpi=300, bbox_inches='tight')
    print(f"Voltage plot saved as: {voltage_filename}")
    plt.close(fig1)
    
    # Create current plot
    fig2, ax2 = plt.subplots(1, 1, figsize=(12, 6))
    if show_smoothed:
        ax2.plot(time, current_smooth, 'r-', linewidth=1, label='Smoothed')
    ax2.plot(time, current, 'r-', linewidth=0.3 if show_smoothed else 1, alpha=0.7 if show_smoothed else 1, label='Raw')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Current (A)')
    smoothed_text = ', Smoothed' if show_smoothed else ''
    ax2.set_title(f'Current vs Time (Sensitivity: {sensitivity_mv_per_a} mV/A{smoothed_text})')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Add test number in top left corner
    ax2.text(0.02, 0.98, f'Test {test_number}', transform=ax2.transAxes, 
             fontsize=12, fontweight='bold', verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Set time range if specified
    if time_min is not None or time_max is not None:
        ax2.set_xlim(time_min, time_max)
        # Set y-axis to match displayed data range
        time_mask = ((time_min is None) or (time >= time_min)) & ((time_max is None) or (time <= time_max))
        ax2.set_ylim(current[time_mask].min() * 0.95, current[time_mask].max() * 1.05)
    
    # Save current plot
    current_filename = f"{base_filename}_current.png"
    plt.tight_layout()
    plt.savefig(current_filename, dpi=300, bbox_inches='tight')
    print(f"Current plot saved as: {current_filename}")
    plt.close(fig2)
    
    # Print some statistics
    print(f"\nFile: {filename}")
    print(f"Time range: {time.min():.6f} s to {time.max():.6f} s")
    print(f"Raw voltage range: {voltage.min():.4f} V to {voltage.max():.4f} V")
    print(f"Smoothed voltage range: {voltage_smooth.min():.4f} V to {voltage_smooth.max():.4f} V")
    print(f"Raw current range: {current.min():.4f} A to {current.max():.4f} A")
    print(f"Smoothed current range: {current_smooth.min():.4f} A to {current_smooth.max():.4f} A")
    print(f"Data points: {len(time)}")
    print(f"Smoothing window: 11 points")

def generate_all_plots(sensitivity_mv_per_a=200, time_min=None, time_max=None, output_filename=None, show_smoothed=True):
    """
    Generate plots for all CSV files in the Oscilloscope-Data folder.
    
    Args:
        sensitivity_mv_per_a (float): Sensitivity in mV/A (default: 200)
        time_min (float): Minimum time to display on x-axis (default: None, uses data min)
        time_max (float): Maximum time to display on x-axis (default: None, uses data max)
        output_filename (str): Custom base filename for output files (default: None, uses CSV base filename)
        show_smoothed (bool): Whether to display smoothed data (default: True)
    """
    oscilloscope_data_dir = os.path.join(os.path.dirname(__file__), 'Oscilloscope-Data')
    
    if not os.path.exists(oscilloscope_data_dir):
        print(f"Error: Oscilloscope-Data folder not found at {oscilloscope_data_dir}")
        return
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(oscilloscope_data_dir) if f.endswith('.CSV')]
    csv_files.sort()
    
    if not csv_files:
        print("No CSV files found in Oscilloscope-Data folder.")
        return
    
    print(f"Found {len(csv_files)} CSV files. Generating plots...")
    
    for i, csv_file in enumerate(csv_files):
        filename = os.path.join(oscilloscope_data_dir, csv_file)
        print(f"\nProcessing {i+1}/{len(csv_files)}: {csv_file}")
        
        try:
            plot_voltage_and_current(filename, sensitivity_mv_per_a, time_min, time_max, output_filename, show_smoothed)
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
            continue
    
    print(f"\nCompleted processing all {len(csv_files)} files.")

def main():
    """
    Main function to handle command line arguments and file selection.
    """
    if len(sys.argv) > 1:
        # Check if user wants to generate all plots
        if sys.argv[1].lower() == 'all':
            generate_all_plots()
            return
        
        # If filename is provided as command line argument
        filename = sys.argv[1] if sys.argv[1].endswith('.CSV') else sys.argv[1] + '.CSV'
        filename = os.path.join(os.path.dirname(__file__), 'Oscilloscope-Data', filename)
    else:
        # Interactive file selection
        oscilloscope_data_dir = os.path.join(os.path.dirname(__file__), 'Oscilloscope-Data')
        print("Available CSV files:")
        csv_files = [f for f in os.listdir(oscilloscope_data_dir) if f.endswith('.CSV')]
        csv_files.sort()
        
        for i, file in enumerate(csv_files):
            print(f"{i}: {file}")
        
        try:
            choice = int(input("\nEnter the number of the file to plot: "))
            filename = os.path.join(oscilloscope_data_dir, csv_files[choice])
        except (ValueError, IndexError):
            print("Invalid selection. Exiting.")
            return
    
    # Check if file exists (final check)
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return
    
    # Use fixed sensitivity of 200 mV/A
    sensitivity = 200
    
    # Create the plots
    plot_voltage_and_current(filename, sensitivity)

# Files that show the capacitor current spike: 12 and 17
# TEK0012: 0.0440 to 0.0512 s
# TEK0017: 0.0292 to 0.0400 s

plot_voltage_and_current("Oscilloscope-Data/TEK0012.CSV", sensitivity_mv_per_a=200, time_min=0.0440, time_max=0.0512, output_filename="TEK0012_capacitor_spike", show_smoothed=False)
plot_voltage_and_current("Oscilloscope-Data/TEK0017.CSV", sensitivity_mv_per_a=200, time_min=0.0292, time_max=0.0400, output_filename="TEK0017_capacitor_spike", show_smoothed=False)
plot_voltage_and_current("Oscilloscope-Data/TEK0017.CSV", sensitivity_mv_per_a=200, time_min=0.24, time_max=0.40, output_filename="TEK0017_pos_contactor", show_smoothed=True)


if __name__ == "__main__":
    main()