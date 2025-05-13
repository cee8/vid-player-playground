#!/usr/bin/env python3
"""
Common Visualization Styles for ABR Streaming Simulation

This module provides consistent styling and color schemes
for all visualizations in the ABR streaming simulation project.
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Brand colors
PRIMARY_RED = '#E50914'
TEXT_BLACK = '#141414'
DARK_GRAY = '#1F1F1F'
LIGHT_GRAY = '#808080'

# Color palette for different segment lengths
SEGMENT_COLORS = [
    PRIMARY_RED,     # Primary red
    '#1A75FF',       # Complementary blue
    '#00B300'        # Complementary green
]


def apply_style(fig, axes):
    """
    Apply consistent styling to figure and axes.
    
    Args:
        fig: Matplotlib figure object
        axes: List of axes objects (or single axis)
    """
    # Convert single axis to list for consistent handling
    if not isinstance(axes, list) and not isinstance(axes, tuple):
        axes = [axes]
    
    # Set figure background to white
    fig.patch.set_facecolor('white')
    
    for ax in axes:
        # Set axis background to white
        ax.set_facecolor('white')
        
        # Apply styled borders
        for spine in ax.spines.values():
            spine.set_color(LIGHT_GRAY)
            spine.set_linewidth(1.5)
        
        # Style tick labels
        ax.tick_params(colors=TEXT_BLACK)
        
        # Style grid
        ax.grid(True, linestyle='--', alpha=0.3, color=LIGHT_GRAY)


def style_legend(legend):
    """
    Apply styling to a legend.
    
    Args:
        legend: Matplotlib legend object
    """
    legend.set_facecolor('white')
    legend.set_edgecolor(LIGHT_GRAY)
    
    for text in legend.get_texts():
        text.set_color(TEXT_BLACK)


def get_primary_cmap():
    """
    Create a primary-colored colormap.
    
    Returns:
        matplotlib.colors.LinearSegmentedColormap: Brand-styled colormap
    """
    return LinearSegmentedColormap.from_list('primary_red', 
                                            ['#FFFFFF', PRIMARY_RED])


def set_styled_labels(ax, title="", xlabel="", ylabel="", fontsize_title=14, fontsize_labels=12):
    """
    Set styled labels on an axis.
    
    Args:
        ax: Matplotlib axis object
        title: Title text
        xlabel: X-axis label text
        ylabel: Y-axis label text
        fontsize_title: Font size for title
        fontsize_labels: Font size for axis labels
    """
    if title:
        ax.set_title(title, color=TEXT_BLACK, fontsize=fontsize_title, pad=20)
    if xlabel:
        ax.set_xlabel(xlabel, color=TEXT_BLACK, fontsize=fontsize_labels)
    if ylabel:
        ax.set_ylabel(ylabel, color=TEXT_BLACK, fontsize=fontsize_labels)


def init_styled_plot(figsize=(12, 7)):
    """
    Initialize a figure and axis with consistent styling.
    
    Args:
        figsize: Figure size as (width, height) tuple
        
    Returns:
        tuple: (figure, axis)
    """
    # Set the default style
    plt.style.use('default')
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Apply styling
    apply_style(fig, ax)
    
    return fig, ax 