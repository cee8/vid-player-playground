#!/usr/bin/env python3
"""
Heatmap Analysis for ABR Streaming Performance

This module creates heatmap visualizations of streaming performance metrics
across different segment lengths and smoothing window configurations.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from visualization_styles import (
    PRIMARY_RED, TEXT_BLACK, LIGHT_GRAY, DARK_GRAY,
    apply_style, get_primary_cmap
)


def load_data(csv_file="sweep_results.csv"):
    """
    Load data from sweep results CSV file.
    
    Args:
        csv_file: Path to the CSV file containing sweep results
        
    Returns:
        tuple: (segment_lengths, smoothing_windows, rebuffer_times, bitrates)
    """
    try:
        df = pd.read_csv(csv_file)
        
        # Extract unique values for segment lengths and smoothing windows
        segment_lengths = sorted(df.segment_length.unique())
        smoothing_windows = sorted(df.smooth_window.unique())
        
        # Create matrices for rebuffer times and bitrates
        rebuffer_times = np.zeros((len(segment_lengths), len(smoothing_windows)))
        bitrates = np.zeros((len(segment_lengths), len(smoothing_windows)))
        
        # Fill matrices with data from CSV
        for i, seg_len in enumerate(segment_lengths):
            for j, window in enumerate(smoothing_windows):
                row = df[(df.segment_length == seg_len) & (df.smooth_window == window)]
                if not row.empty:
                    rebuffer_times[i, j] = row.mean_stall.values[0]
                    bitrates[i, j] = row.mean_bitrate.values[0]
        
        return segment_lengths, smoothing_windows, rebuffer_times, bitrates
    
    except FileNotFoundError:
        print(f"File {csv_file} not found. Using sample data.")
        # Sample data as fallback
        segment_lengths = [2, 4, 6]  # seconds
        smoothing_windows = [1, 3, 5, 7]
        
        # Example data matrices
        rebuffer_times = np.array([
            [0.5, 0.3, 0.2, 0.1],  # L=2s
            [0.8, 0.4, 0.3, 0.2],  # L=4s
            [1.2, 0.6, 0.4, 0.3]   # L=6s
        ])
        
        bitrates = np.array([
            [1200, 1100, 1050, 1000],  # L=2s
            [1400, 1300, 1250, 1200],  # L=4s
            [1600, 1500, 1450, 1400]   # L=6s
        ])
        
        return segment_lengths, smoothing_windows, rebuffer_times, bitrates


def create_heatmap_analysis(segment_lengths, smoothing_windows, 
                           rebuffer_times, bitrates,
                           output_file="heatmap_analysis.png"):
    """
    Create heatmap visualization of streaming performance metrics.
    
    Args:
        segment_lengths: List of segment lengths
        smoothing_windows: List of smoothing windows
        rebuffer_times: Matrix of rebuffer times
        bitrates: Matrix of bitrates
        output_file: Path to save the output image
        
    Returns:
        tuple: (figure, axes)
    """
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor('white')
    
    # Apply styling to axes
    apply_style(fig, [ax1, ax2])

    # Get primary colormap
    primary_cmap = get_primary_cmap()

    # Plot 1: Rebuffer times with bitrate text overlay
    sns.heatmap(rebuffer_times, 
                annot=bitrates.astype(int),  # Overlay bitrate values
                fmt='d',
                cmap=primary_cmap,
                ax=ax1,
                cbar_kws={'label': 'Mean Rebuffer Time (s)'},
                xticklabels=[f'N={n}' for n in smoothing_windows],
                yticklabels=[f'L={l}s' for l in segment_lengths],
                annot_kws={'color': TEXT_BLACK, 'weight': 'bold'})

    # Plot 2: Bitrates
    sns.heatmap(bitrates,
                cmap=primary_cmap,
                ax=ax2,
                cbar_kws={'label': 'Mean Bitrate (kbps)'},
                xticklabels=[f'N={n}' for n in smoothing_windows],
                yticklabels=[f'L={l}s' for l in segment_lengths])

    # Customize plots
    ax1.set_title('Rebuffer Time (color) and\nDelivered Bitrate (text)', 
                  color=TEXT_BLACK, 
                  fontsize=14, 
                  pad=20)
    ax2.set_title('Mean Bitrate Distribution', 
                  color=TEXT_BLACK, 
                  fontsize=14, 
                  pad=20)

    # Add main title
    fig.suptitle('L × N Trade-off Analysis', 
                 color=TEXT_BLACK, 
                 fontsize=16, 
                 y=1.05)

    # Add explanatory text
    fig.text(0.5, 0.01, 
             'Left: Color intensity shows mean stall time; numbers show mean bitrate (kbps)\n'
             'Right: Color intensity shows mean bitrate distribution',
             ha='center', 
             fontsize=10,
             color=TEXT_BLACK)

    # Customize colorbar labels
    for ax in [ax1, ax2]:
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.label.set_color(TEXT_BLACK)
        cbar.ax.yaxis.set_label_coords(3.0, 0.5)  # Adjust label position
        cbar.ax.tick_params(colors=TEXT_BLACK)

    # Customize tick labels
    for ax in [ax1, ax2]:
        ax.tick_params(colors=TEXT_BLACK)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_color(TEXT_BLACK)

    plt.tight_layout()

    # Save with high DPI for quality
    plt.savefig(output_file, 
                dpi=300, 
                bbox_inches='tight', 
                facecolor='white')
    print(f"Saved heatmap analysis to {output_file}")
    
    return fig, [ax1, ax2]


def main():
    """Main function to create the heatmap analysis visualization"""
    segment_lengths, smoothing_windows, rebuffer_times, bitrates = load_data()
    fig, axes = create_heatmap_analysis(segment_lengths, smoothing_windows, 
                                        rebuffer_times, bitrates)
    plt.show()


if __name__ == "__main__":
    main() 