#!/usr/bin/env python3
"""
Trade-off Analysis Plots for ABR Streaming

This module creates visualization of performance trade-offs between
different segment lengths and smoothing window configurations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from visualization_styles import (
    PRIMARY_RED, TEXT_BLACK, LIGHT_GRAY, SEGMENT_COLORS,
    apply_style, style_legend, set_styled_labels
)


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
    
    # Apply styling
    apply_style(fig, [ax1, ax2])

    # Overlay rebuffer curves
    for i, seg_len in enumerate(sorted(df.segment_length.unique())):
        sub = df[df.segment_length == seg_len]
        ax1.plot(sub.smooth_window,
                 sub.mean_stall,
                 marker="o",
                 color=SEGMENT_COLORS[i % len(SEGMENT_COLORS)],
                 linewidth=2.5,
                 markersize=8,
                 label=f"{seg_len}s segments")

    # Set labels for first plot
    set_styled_labels(
        ax1,
        title="Mean Rebuffer Time vs. Smoothing Window",
        xlabel="Smoothing Window (segments)",
        ylabel="Mean Rebuffer Time (s)"
    )

    # Create and style legend for first plot
    legend1 = ax1.legend(title="Segment Length")
    style_legend(legend1)
    legend1.get_title().set_color(TEXT_BLACK)

    # Overlay bitrate curves
    for i, seg_len in enumerate(sorted(df.segment_length.unique())):
        sub = df[df.segment_length == seg_len]
        ax2.plot(sub.smooth_window,
                 sub.mean_bitrate,
                 marker="o",
                 color=SEGMENT_COLORS[i % len(SEGMENT_COLORS)],
                 linewidth=2.5,
                 markersize=8,
                 label=f"{seg_len}s segments")

    # Set labels for second plot
    set_styled_labels(
        ax2,
        title="Mean Chosen Bitrate vs. Smoothing Window",
        xlabel="Smoothing Window (segments)",
        ylabel="Mean Bitrate (kbps)"
    )

    # Create and style legend for second plot
    legend2 = ax2.legend(title="Segment Length")
    style_legend(legend2)
    legend2.get_title().set_color(TEXT_BLACK)

    # Add main title
    fig.suptitle('L × N Trade-off Analysis', 
                 color=TEXT_BLACK, 
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
