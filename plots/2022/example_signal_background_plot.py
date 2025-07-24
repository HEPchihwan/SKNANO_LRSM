#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from signal_background_plotter import plot_signal_background, plot_individual_signals

def plot_individual_mass_points():
    """Create individual plots for each signal mass point"""
    
    # Path to your ROOT files
    data_directory = "/gv0/Users/achihwan/SKNanoRunlog/out/LRSM_TBChannel/2022"
    
    # Configuration for individual mass point plots
    plot_configs = {
        "WRMass_Central": {
            "xRange": [0, 8000],
            "yRange": [0.1, 100],
            "xTitle": "M_{W_{R}} [GeV]",
            "yTitle": "Events / 100 GeV",
            "logy": True,
            "rebin": 10,
            "canvas_width": 700,   # Even smaller size
            "canvas_height": 700
            ,"show_unity_line": True
        }
    }
    
    # Create individual plots for each histogram
    for hist_name, config in plot_configs.items():
        print(f"Creating individual signal plots for: {hist_name}")
        try:
            canvases = plot_individual_signals(data_directory, hist_name, config)
            print(f"Created {len(canvases)} individual plots for {hist_name}")
        except Exception as e:
            print(f"Error creating individual plots for {hist_name}: {e}")
    
    print("Finished creating individual signal mass point plots!")


if __name__ == "__main__":
    print("LRSM TBChannel Signal vs Background Plotter Example")
    print("=" * 60)
    
    # Check if data directory exists
    data_dir = "/gv0/Users/achihwan/SKNanoRunlog/out/LRSM_TBChannel/2022"
    if not os.path.exists(data_dir):
        print(f"Error: Data directory {data_dir} does not exist!")
        sys.exit(1)
    
    # Ask user which type of plots to create
    print("Choose plotting option:")
    print("1. Combined signal vs background plots (all signals together)")
    print("2. Individual signal mass point plots (separate plot for each mass)")
    print("3. Both")
    plot_individual_mass_points()
    
    