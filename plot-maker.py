#!/usr/bin/env python3
"""
Trade-off Analysis Plots for ABR Streaming

This module creates visualization of performance trade-offs between
different segment lengths and smoothing window configurations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Brand colors and complementary colors
PRIMARY_RED = '#E50914'
PRIMARY_BLACK = '#141414'
DARK_GRAY = '#1F1F1F'
LIGHT_GRAY = '#808080'

# Custom color palette for different segment lengths
# Using primary red and complementary colors that work well together
COLORS = [
    PRIMARY_RED,     # Primary red
    '#1A75FF',       # Complementary blue
    '#00B300'        # Complementary green
]


def load_data(csv_file="sweep_results.csv"):
    """
    Load data from sweep results CSV file.
    
    Args:
        csv_file: Path to the CSV file containing sweep results
        
    Returns:
        pandas.DataFrame: DataFrame with sweep results
    """
    try:
        return pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"File {csv_file} not found. Creating sample data.")
        # Create sample data if file not found
        segment_lengths = [2.0, 4.0, 6.0]
        smooth_windows = [1, 3, 5, 7]
        
        # Create empty dataframe with the same structure
        columns = ["segment_length", "smooth_window", 
                   "mean_bitrate", "sd_bitrate", 
                   "mean_stall", "sd_stall"]
        df = pd.DataFrame(columns=columns)
        
        # Fill with sample data
        for i, seg_len in enumerate(segment_lengths):
            for j, window in enumerate(smooth_windows):
                row = {
                    "segment_length": seg_len,
                    "smooth_window": window,
                    "mean_bitrate": 1000 + i*200 - j*50,
                    "sd_bitrate": 70 + np.random.uniform(-10, 10),
                    "mean_stall": 0 if window == 1 else (j*10 + i*20),
                    "sd_stall": 0 if window == 1 else (j*5 + i*2)
                }
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        
        return df


def create_tradeoff_plots(df, output_file="tradeoff_analysis.png"):
    """
    Create trade-off analysis plots for streaming performance metrics.
    
    Args:
        df: DataFrame with sweep results
        output_file: Path to save the output image
        
    Returns:
        tuple: (figure, axes)
    """
    # Set the style
    plt.style.use('default')

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor('white')

    # Overlay rebuffer curves
    for i, seg_len in enumerate(sorted(df.segment_length.unique())):
        sub = df[df.segment_length == seg_len]
        ax1.plot(sub.smooth_window,
                 sub.mean_stall,
                 marker="o",
                 color=COLORS[i % len(COLORS)],
                 linewidth=2.5,
                 markersize=8,
                 label=f"{seg_len}s segments")

    ax1.set_title("Mean Rebuffer Time vs. Smoothing Window", 
                  color=PRIMARY_BLACK, 
                  fontsize=14, 
                  pad=20)
    ax1.set_xlabel("Smoothing Window (segments)", 
                   color=PRIMARY_BLACK, 
                   fontsize=12)
    ax1.set_ylabel("Mean Rebuffer Time (s)", 
                   color=PRIMARY_BLACK, 
                   fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.3, color=LIGHT_GRAY)
    ax1.legend(title="Segment Length", 
              facecolor='white', 
              edgecolor=LIGHT_GRAY,
              title_fontsize=12,
              fontsize=11)
    for text in ax1.get_legend().get_texts():
        text.set_color(PRIMARY_BLACK)
    ax1.tick_params(colors=PRIMARY_BLACK)

    # Overlay bitrate curves
    for i, seg_len in enumerate(sorted(df.segment_length.unique())):
        sub = df[df.segment_length == seg_len]
        ax2.plot(sub.smooth_window,
                 sub.mean_bitrate,
                 marker="o",
                 color=COLORS[i % len(COLORS)],
                 linewidth=2.5,
                 markersize=8,
                 label=f"{seg_len}s segments")

    ax2.set_title("Mean Chosen Bitrate vs. Smoothing Window", 
                  color=PRIMARY_BLACK, 
                  fontsize=14, 
                  pad=20)
    ax2.set_xlabel("Smoothing Window (segments)", 
                   color=PRIMARY_BLACK, 
                   fontsize=12)
    ax2.set_ylabel("Mean Bitrate (kbps)", 
                   color=PRIMARY_BLACK, 
                   fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.3, color=LIGHT_GRAY)
    ax2.legend(title="Segment Length", 
              facecolor='white', 
              edgecolor=LIGHT_GRAY,
              title_fontsize=12,
              fontsize=11)
    for text in ax2.get_legend().get_texts():
        text.set_color(PRIMARY_BLACK)
    ax2.tick_params(colors=PRIMARY_BLACK)

    # Add styled borders
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_color(LIGHT_GRAY)
            spine.set_linewidth(1.5)

    # Add main title
    fig.suptitle('L × N Trade-off Analysis', 
                 color=PRIMARY_BLACK, 
                 fontsize=16, 
                 y=1.05)

    plt.tight_layout()

    # Save with high DPI for quality
    plt.savefig(output_file, 
                dpi=300, 
                bbox_inches='tight', 
                facecolor='white')
    print(f"Saved trade-off analysis to {output_file}")
    
    return fig, (ax1, ax2)


def main():
    """Main function to create the trade-off analysis plots"""
    df = load_data()
    fig, axes = create_tradeoff_plots(df)
    plt.show()


if __name__ == "__main__":
    main()
