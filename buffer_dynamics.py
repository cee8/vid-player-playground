#!/usr/bin/env python3
"""
Buffer Dynamics Visualization for ABR Streaming

This module creates visualizations of buffer behavior during
adaptive bitrate streaming playback.
"""

import numpy as np
import matplotlib.pyplot as plt
from visualization_styles import (
    PRIMARY_RED, TEXT_BLACK, LIGHT_GRAY,
    init_styled_plot, apply_style, set_styled_labels
)


def create_buffer_dynamics_plot(initial_buffer=2.0, segment_length=2.0, 
                                download_time=3.0, empty_time=1.5,
                                output_file='buffer_dynamics.png'):
    """
    Creates a visualization of buffer dynamics during streaming.
    
    Args:
        initial_buffer: Initial buffer level in seconds
        segment_length: Length of each segment in seconds
        download_time: Time to download the segment in seconds
        empty_time: Time when the buffer becomes empty in seconds
        output_file: Path to save the output image
    """
    # Create time points
    t = np.array([0, empty_time, download_time, download_time + 0.1])
    buffer = np.array([initial_buffer, 0, 0, segment_length])

    # Initialize plot with styling
    fig, ax = init_styled_plot(figsize=(12, 7))

    # Plot the buffer level with primary red
    plt.plot(t, buffer, color=PRIMARY_RED, linewidth=3, label='Buffer Level')

    # Add shaded regions
    plt.fill_between(t[:2], buffer[:2], alpha=0.2, color=PRIMARY_RED, label='Normal Playback')
    if empty_time < download_time:
        plt.fill_between(t[1:3], buffer[1:3], alpha=0.2, color=LIGHT_GRAY, label='Stall')

    # Add annotations with styling
    plt.annotate('Download Start', xy=(0, initial_buffer), xytext=(0.2, initial_buffer + 0.3),
                arrowprops=dict(facecolor=PRIMARY_RED, shrink=0.05, width=2),
                color=TEXT_BLACK, fontsize=10)
    plt.annotate('Buffer Empty → Stall', xy=(empty_time, 0), xytext=(empty_time + 0.2, 0.3),
                arrowprops=dict(facecolor=PRIMARY_RED, shrink=0.05, width=2),
                color=TEXT_BLACK, fontsize=10)
    plt.annotate('Download Complete\n+L seconds added', xy=(download_time, segment_length),
                xytext=(download_time - 1, segment_length + 0.3),
                arrowprops=dict(facecolor=PRIMARY_RED, shrink=0.05, width=2),
                color=TEXT_BLACK, fontsize=10)

    # Set labels
    set_styled_labels(
        ax,
        title='Buffer Dynamics During Segment Download',
        xlabel='Time (seconds)',
        ylabel='Buffer Level (seconds)'
    )

    # Customize legend
    legend = plt.legend()
    legend.set_facecolor('white')
    legend.set_edgecolor(LIGHT_GRAY)
    for text in legend.get_texts():
        text.set_color(TEXT_BLACK)

    # Set axis limits
    plt.xlim(-0.5, download_time + 1)
    plt.ylim(-0.5, max(initial_buffer, segment_length) + 1)

    plt.tight_layout()

    # Save with high DPI for quality
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved buffer dynamics visualization to {output_file}")
    
    return fig, ax


def main():
    """Main function to create the buffer dynamics visualization"""
    fig, ax = create_buffer_dynamics_plot()
    plt.show()


if __name__ == "__main__":
    main() 