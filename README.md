# Adaptive Bitrate Streaming Simulation

A Markov chain-based Monte Carlo simulation framework for evaluating Quality of Experience (QoE) of adaptive bitrate streaming algorithms under variable network conditions.

## Project Structure

```
abr-sim/
├── markov-chain.py          # Core simulation framework
├── tradeoff_analysis.py     # Creates trade-off visualizations
├── heatmap_analysis.py      # Generates heatmap visualizations
├── buffer_dynamics.py       # Visualizes buffer behavior
├── visualization_styles.py  # Common styling for visualizations
├── config.yaml              # Configuration parameters
├── sweep_results.csv        # Results from parameter sweep
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

## Abstract

We present a Markov-chain + Monte Carlo simulation to evaluate QoE of simple ABR algorithms under variable network conditions. Key finding: a smoothing window of 1 segment with 2s segment length yields zero rebuffer and ~1057 kbps average bitrate.

## Installation

1. Clone the repository
2. Create a virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Full Simulation

To run the complete simulation with parameter sweep:

```bash
python markov-chain.py
```

This will:
1. Generate a network trace using the Markov chain model
2. Simulate ABR streaming with different parameters
3. Produce `sweep_results.csv` with metrics for all configurations

### Visualization Tools

Generate visualizations from the simulation results:

```bash
# Create trade-off analysis plots
python tradeoff_analysis.py

# Generate heatmap visualization
python heatmap_analysis.py

# Visualize buffer dynamics
python buffer_dynamics.py
```

## Methodology

### Network Model

- 3-state Markov chain (500/1000/2000 kbps)
- Transition matrix defined in `config.yaml`

### ABR Algorithm

- Throughput-based algorithm with configurable smoothing window
- Segment download & buffer dynamics simulation

### Monte Carlo Framework

- Parameter sweep over:
  - `segment_length` ∈ {2, 4, 6} seconds
  - `smooth_window` ∈ {1, 3, 5, 7} segments
- 100 runs per configuration

## Results

Analysis of the simulation results shows:

- Only configurations with `smooth_window=1` completely avoid rebuffering
- Larger segment lengths provide higher average bitrate but also increase rebuffering risk
- The 2s segment length with window=1 provides the best balance of quality and stability

## Performance Visualization

The framework generates three types of visualizations:

1. **Trade-off Analysis Plots**: Shows the relationship between smoothing window size, segment length, rebuffer time, and bitrate
2. **Heatmap Analysis**: Visualizes the trade-offs between different configurations
3. **Buffer Dynamics**: Illustrates buffer behavior during streaming

All visualizations use a consistent styling provided by the `visualization_styles.py` module.

## Configuration

Modify `config.yaml` to adjust simulation parameters:

```yaml
# Example configuration
states:
  - 500    # kbps
  - 1000   # kbps
  - 2000   # kbps
P:  # transition matrix
  - [0.7, 0.2, 0.1]
  - [0.1, 0.8, 0.1]
  - [0.1, 0.3, 0.6]
```

## Extending the Project

### Adding New Visualizations

To create new visualizations with consistent styling:

```python
from visualization_styles import init_styled_plot, set_styled_labels

# Initialize a styled plot
fig, ax = init_styled_plot()

# Add your visualization code here
# ...

# Set styled labels
set_styled_labels(ax, 
                  title="Your Title", 
                  xlabel="X-Axis Label", 
                  ylabel="Y-Axis Label")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Your Name - Initial work

## Acknowledgments

- Inspired by research on adaptive bitrate streaming algorithms
- Professional visualizations for intuitive representation of results