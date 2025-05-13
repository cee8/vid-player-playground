#!/usr/bin/env python3
"""
Markov Chain-based Adaptive Bitrate Streaming Simulator

This module simulates network conditions and ABR streaming playback
using a Markov chain model to generate realistic bandwidth patterns.
"""

import random
import statistics
import csv
import yaml


def simulate_throughput(num_steps, P, states):
    """
    Simulates a Markov chain to generate throughput samples.
    
    Args:
        num_steps: Number of segments to simulate
        P: Transition probability matrix
        states: List of throughput states (kbps)
        
    Returns:
        List of throughput samples
    """
    current = 0
    trace = []
    for _ in range(num_steps):
        trace.append(states[current])
        r = random.random()
        cum = 0
        for j, p in enumerate(P[current]):
            cum += p
            if r < cum:
                current = j
                break
    return trace


def get_smoothed_throughput(trace, idx, window):
    """
    Computes moving average of throughput over specified window.
    
    Args:
        trace: List of throughput samples
        idx: Current index
        window: Number of samples to include in moving average
        
    Returns:
        Average throughput over the window
    """
    start = max(0, idx - window + 1)
    return statistics.mean(trace[start : idx + 1])


def simulate_playback(trace, segment_length=2.0, smooth_window=3):
    """
    Simulates ABR playback with buffer management.
    
    Args:
        trace: List of throughput samples
        segment_length: Length of each segment in seconds
        smooth_window: Number of samples for throughput smoothing
        
    Returns:
        Tuple of (average bitrate, total rebuffer time)
    """
    buffer_sec = segment_length * smooth_window
    total_stall = 0.0

    for i, bw in enumerate(trace):
        quality = get_smoothed_throughput(trace, i, smooth_window)
        download_time = quality * segment_length / bw

        if buffer_sec >= download_time:
            buffer_sec -= download_time
        else:
            stall = download_time - buffer_sec
            total_stall += stall
            buffer_sec = 0.0

        buffer_sec += segment_length

    avg_bitrate = statistics.mean(
        get_smoothed_throughput(trace, i, smooth_window)
        for i in range(len(trace))
    )
    return avg_bitrate, total_stall


def monte_carlo(P, states, num_steps=150,
                segment_length=2.0, smooth_window=3,
                runs=100):
    """
    Runs Monte Carlo simulation to estimate ABR performance.
    
    Args:
        P: Transition probability matrix
        states: List of throughput states (kbps)
        num_steps: Number of segments to simulate
        segment_length: Length of each segment in seconds
        smooth_window: Number of samples for throughput smoothing
        runs: Number of Monte Carlo trials
        
    Returns:
        List of (average bitrate, total stall time) tuples for each run
    """
    results = []
    for _ in range(runs):
        trace = simulate_throughput(num_steps, P, states)
        avg_q, total_stall = simulate_playback(
            trace,
            segment_length=segment_length,
            smooth_window=smooth_window
        )
        results.append((avg_q, total_stall))
    return results


def parameter_sweep(P, states,
                    num_steps=150,
                    segment_lengths=(2.0, 4.0, 6.0),
                    smooth_windows=(1, 3, 5, 7),
                    runs=100):
    """
    Performs parameter sweep over segment lengths and smoothing windows.
    Writes results to CSV file with mean and standard deviation metrics.
    
    Args:
        P: Transition probability matrix
        states: List of throughput states (kbps)
        num_steps: Number of segments to simulate
        segment_lengths: List of segment lengths to test
        smooth_windows: List of smoothing windows to test
        runs: Number of Monte Carlo trials for each parameter combination
    """
    with open("sweep_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "segment_length", "smooth_window",
            "mean_bitrate", "sd_bitrate",
            "mean_stall", "sd_stall"
        ])
        for seg_len in segment_lengths:
            for w in smooth_windows:
                data = monte_carlo(
                    P, states,
                    num_steps=num_steps,
                    segment_length=seg_len,
                    smooth_window=w,
                    runs=runs
                )
                qs = [d[0] for d in data]
                stl = [d[1] for d in data]
                writer.writerow([
                    seg_len, w,
                    statistics.mean(qs), statistics.stdev(qs),
                    statistics.mean(stl), statistics.stdev(stl)
                ])
    print("Wrote sweep_results.csv")


def load_config(config_file="config.yaml"):
    """
    Loads configuration from YAML file.
    
    Args:
        config_file: Path to YAML configuration file
        
    Returns:
        Dictionary with configuration parameters
    """
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def main():
    """Main function to run the simulation"""
    # Load configuration from YAML
    try:
        config = load_config()
        P = config["P"]
        states = config["states"]
        defaults = config["defaults"]
        
        # Extract parameters from config
        num_steps = defaults["num_steps"]
        segment_lengths = defaults["segment_lengths"]
        smooth_windows = defaults["smooth_windows"]
        runs = defaults["runs"]
    except FileNotFoundError:
        print("Config file not found. Using default parameters.")
        # Default parameters if config is not available
        P = [
            [0.7, 0.2, 0.1],
            [0.1, 0.8, 0.1],
            [0.1, 0.3, 0.6],
        ]
        states = [500, 1000, 2000]
        num_steps = 150
        segment_lengths = [2.0, 4.0, 6.0]
        smooth_windows = [1, 3, 5, 7]
        runs = 100

    # Run a single simulation to demonstrate functionality
    trace = simulate_throughput(num_steps, P, states)
    print("Throughput trace (first 20 steps):", trace[:20])

    # Run a single playback simulation
    avg_q, total_stall = simulate_playback(trace,
                                          segment_length=2.0,
                                          smooth_window=3)
    print(f"Average chosen bitrate: {avg_q:.1f} kbps")
    print(f"Total rebuffer time:   {total_stall:.1f} seconds")

    # Run Monte Carlo simulations
    data = monte_carlo(
        P, states,
        num_steps=num_steps,
        segment_length=2.0,
        smooth_window=3,
        runs=runs
    )

    # Compute summary statistics
    avg_qs = [r[0] for r in data]
    stalls = [r[1] for r in data]
    print("=== Monte Carlo summary (n=100) ===")
    print(f"Avg bitrate: {statistics.mean(avg_qs):.1f} ± {statistics.stdev(avg_qs):.1f} kbps")
    print(f"Rebuffer  : {statistics.mean(stalls):.1f} ± {statistics.stdev(stalls):.1f} sec")

    # Run parameter sweep
    print("Running parameter sweep...")
    parameter_sweep(
        P, states,
        num_steps=num_steps,
        segment_lengths=segment_lengths,
        smooth_windows=smooth_windows,
        runs=runs
    )


if __name__ == "__main__":
    main()




