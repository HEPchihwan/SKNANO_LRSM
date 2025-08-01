#!/usr/bin/env python3

data_directory = "/gv0/Users/achihwan/SKNanoRunlog/out/TTbar_test/2022"

import ROOT
import cmsstyle as CMS
import os
import glob
from array import array
import gc

# Prevent ROOT from owning Python objects
ROOT.SetOwnership(ROOT.gROOT, False)

# Colors for plotting
DATA_COLOR = ROOT.kBlack
MC_COLOR = ROOT.TColor.GetColor("#5790fc")  # Blue for MC

class DataMCCanvas():
    def __init__(self, combined_data_hist, mc_hist, config):
        super().__init__()
        
        self.data_hist = combined_data_hist
        self.mc_hist = mc_hist
        self.config = config
        
        # Keep references to prevent garbage collection
        self._objects_to_keep = []
        
        # Style the histograms
        self._style_histograms()
        
        # Create ratio histogram (Data vs MC)
        self.ratio = None
        if self.data_hist and self.mc_hist:
            self.ratio = self.data_hist.Clone("data_mc_ratio")
            self.ratio.SetDirectory(0)
            self.ratio.SetStats(0)
            self.ratio.Divide(self.mc_hist)
            self._objects_to_keep.append(self.ratio)
        
        # Set up canvas
        self._setup_canvas()
    
    def _style_histograms(self):
        """Apply styling to data and MC histograms"""
        if self.data_hist:
            # Data: black points with error bars
            self.data_hist.SetMarkerStyle(20)
            self.data_hist.SetMarkerSize(1.0)
            self.data_hist.SetMarkerColor(DATA_COLOR)
            self.data_hist.SetLineColor(DATA_COLOR)
            self.data_hist.SetLineWidth(2)
            self.data_hist.SetStats(0)
            if not self.data_hist.GetSumw2N():
                self.data_hist.Sumw2()
        
        if self.mc_hist:
            # MC: filled histogram with blue color
            self.mc_hist.SetFillColor(MC_COLOR)
            self.mc_hist.SetLineColor(MC_COLOR)
            self.mc_hist.SetLineWidth(2)
            self.mc_hist.SetFillStyle(1001)  # Solid fill
            self.mc_hist.SetStats(0)
            if not self.mc_hist.GetSumw2N():
                self.mc_hist.Sumw2()
    
    def _setup_canvas(self):
        """Setup the canvas with two pads for main plot and ratio"""
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        
        # Calculate y-axis range
        if "ymax" in self.config.keys() and self.config["ymax"] is not None:
            ymax = self.config["ymax"]
        else:
            data_max = self.data_hist.GetMaximum() if self.data_hist else 0
            mc_max = self.mc_hist.GetMaximum() if self.mc_hist else 0
            ymax = max(data_max, mc_max) * 1.5
            if ymax <= 0:
                ymax = 1000  # Default fallback
        
        ymin = self.config.get("ymin", 0.1 if self.config.get("logy", False) else 0.)
        
        # Apply log scale defaults
        if self.config.get('logy', False):
            if "ymin" not in self.config.keys():
                ymin = 1e-1
            if ymax < 1000:
                ymax = 1000
        
        # Debug information
        print(f"Y-axis range: [{ymin}, {ymax}]")
        if self.data_hist:
            print(f"Combined Data histogram max: {self.data_hist.GetMaximum()}")
        if self.mc_hist:
            print(f"MC histogram max: {self.mc_hist.GetMaximum()}")
        
        # Set CMS style
        CMS.SetEnergy(13.6)
        CMS.SetLumi("7.9104 fb^{-1}")
        CMS.SetExtraText("Preliminary")
        
        # Create canvas
        canvas_name = f"canvas_{id(self)}"
        self.canv = ROOT.TCanvas(canvas_name, canvas_name, 800, 800)
        ROOT.SetOwnership(self.canv, False)
        self._objects_to_keep.append(self.canv)
        
        # Create pads
        pad1_name = f"pad1_{id(self)}"
        pad2_name = f"pad2_{id(self)}"
        
        # Upper pad for main plot
        pad1 = ROOT.TPad(pad1_name, pad1_name, 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0.02)
        pad1.SetTopMargin(0.08)
        pad1.SetLeftMargin(0.12)
        pad1.SetRightMargin(0.05)
        ROOT.SetOwnership(pad1, False)
        self._objects_to_keep.append(pad1)
        
        # Lower pad for ratio
        pad2 = ROOT.TPad(pad2_name, pad2_name, 0, 0.0, 1, 0.3)
        pad2.SetTopMargin(0.02)
        pad2.SetBottomMargin(0.35)
        pad2.SetLeftMargin(0.12)
        pad2.SetRightMargin(0.05)
        ROOT.SetOwnership(pad2, False)
        self._objects_to_keep.append(pad2)
        
        # Apply log scale if needed
        if self.config.get('logy', False):
            pad1.SetLogy()
        
        pad1.Draw()
        pad2.Draw()
        
        self.pad1 = pad1
        self.pad2 = pad2
        
        # Store axis ranges
        self.xmin = self.config["xRange"][0]
        self.xmax = self.config["xRange"][-1]
        self.ymin = ymin
        self.ymax = ymax
        self.ratio_ymin = self.config["yRange"][0]
        self.ratio_ymax = self.config["yRange"][1]
        
        # Create legend (for 2 entries: Data + MC)
        self.leg = ROOT.TLegend(0.65, 0.75, 0.92, 0.9)
        self.leg.SetTextSize(0.035)
        self.leg.SetBorderSize(0)
        self.leg.SetFillStyle(0)
        ROOT.SetOwnership(self.leg, False)
        self._objects_to_keep.append(self.leg)
    
    def draw(self):
        """Draw the data vs MC comparison"""
        
        # =====================================
        # Upper pad - Main plot
        # =====================================
        self.pad1.cd()
        
        # Draw MC histogram first (as filled histogram)
        first_drawn = False
        if self.mc_hist:
            self.mc_hist.SetMinimum(self.ymin)
            self.mc_hist.SetMaximum(self.ymax)
            self.mc_hist.Draw("HIST")
            first_drawn = True
            
            # Set axis properties
            self.mc_hist.GetYaxis().SetTitle(self.config["yTitle"])
            self.mc_hist.GetYaxis().SetTitleSize(0.05)
            self.mc_hist.GetYaxis().SetTitleOffset(1.2)
            self.mc_hist.GetYaxis().SetLabelSize(0.04)
            self.mc_hist.GetXaxis().SetLabelSize(0)  # Hide x-axis labels on upper pad
            self.mc_hist.GetXaxis().SetTickLength(0.03)
            
            # Draw MC statistical error band (crosshatch)
            mc_error = self.mc_hist.Clone("mc_error")
            mc_error.SetFillColor(ROOT.kBlack)
            mc_error.SetFillStyle(3013)  # Crosshatch pattern (no border)
            mc_error.SetMarkerSize(0)
            ROOT.SetOwnership(mc_error, False)
            self._objects_to_keep.append(mc_error)
            mc_error.Draw("E2 SAME")
        
        # Draw combined data histogram (as points with error bars)
        if self.data_hist:
            if not first_drawn:
                self.data_hist.SetMinimum(self.ymin)
                self.data_hist.SetMaximum(self.ymax)
                self.data_hist.GetYaxis().SetTitle(self.config["yTitle"])
                self.data_hist.GetYaxis().SetTitleSize(0.05)
                self.data_hist.GetYaxis().SetTitleOffset(1.2)
                self.data_hist.GetYaxis().SetLabelSize(0.04)
                self.data_hist.GetXaxis().SetLabelSize(0)
                self.data_hist.Draw("E1")
            else:
                self.data_hist.Draw("E1 SAME")
        
        # Add legend entries
        if self.data_hist:
            self.leg.AddEntry(self.data_hist, "Data", "PE")
        if self.mc_hist:
            self.leg.AddEntry(self.mc_hist, "T#bar{T}LJ MC", "F")
            # Add MC statistical error entry
            if hasattr(self, '_mc_error_entry'):
                mc_error = getattr(self, '_mc_error_entry')
            else:
                mc_error = self.mc_hist.Clone("mc_error_legend")
                mc_error.SetFillColor(ROOT.kBlack)  
                mc_error.SetFillStyle(3013)
                ROOT.SetOwnership(mc_error, False)
                self._objects_to_keep.append(mc_error)
                self._mc_error_entry = mc_error
            self.leg.AddEntry(mc_error, "MC statistical error", "F")
        
        self.leg.Draw()
        
        # Add CMS labels
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.045)
        latex.SetTextFont(62)
        latex.DrawLatex(0.12, 0.93, "CMS")
        
        latex.SetTextSize(0.035)
        latex.SetTextFont(52)
        latex.DrawLatex(0.20, 0.93, "Preliminary")
        
        latex.SetTextFont(42)
        latex.DrawLatex(0.73, 0.93, "7.9104 fb^{-1} (13.6 TeV)")
        
        ROOT.SetOwnership(latex, False)
        self._objects_to_keep.append(latex)
        
        # Redraw axis
        self.pad1.RedrawAxis()
        
        # =====================================
        # Lower pad - Ratio plot
        # =====================================
        self.pad2.cd()
        
        if self.ratio:
            # Create dummy histogram for ratio pad axis
            nb = self.mc_hist.GetNbinsX() if self.mc_hist else 100
            ratio_dummy = ROOT.TH1F(f"ratio_dummy_{id(self)}", "", nb, self.xmin, self.xmax)
            ratio_dummy.SetMinimum(self.ratio_ymin)
            ratio_dummy.SetMaximum(self.ratio_ymax)
            ratio_dummy.GetXaxis().SetTitle(self.config["xTitle"])
            ratio_dummy.GetYaxis().SetTitle("Data / MC")
            
            # Adjust font sizes for ratio pad
            ratio_dummy.GetXaxis().SetTitleSize(0.12)
            ratio_dummy.GetXaxis().SetTitleOffset(1.0)
            ratio_dummy.GetXaxis().SetLabelSize(0.10)
            ratio_dummy.GetYaxis().SetTitleSize(0.08)
            ratio_dummy.GetYaxis().SetTitleOffset(0.5)
            ratio_dummy.GetYaxis().SetLabelSize(0.08)
            ratio_dummy.GetYaxis().SetNdivisions(505)
            ratio_dummy.SetDirectory(0)
            
            ROOT.SetOwnership(ratio_dummy, False)
            self._objects_to_keep.append(ratio_dummy)
            ratio_dummy.Draw()
            
            # Create MC error band for ratio (uncertainty = 1/MC * sqrt(MC))
            mc_ratio_error = ROOT.TH1F(f"mc_ratio_error_{id(self)}", "", nb, self.xmin, self.xmax)
            for i in range(1, nb + 1):
                mc_content = self.mc_hist.GetBinContent(i)
                mc_error = self.mc_hist.GetBinError(i)
                if mc_content > 0:
                    ratio_error = mc_error / mc_content  # Relative error
                    mc_ratio_error.SetBinContent(i, 1.0)
                    mc_ratio_error.SetBinError(i, ratio_error)
                else:
                    mc_ratio_error.SetBinContent(i, 1.0)
                    mc_ratio_error.SetBinError(i, 0.0)
            
            mc_ratio_error.SetFillColor(ROOT.kBlack)
            mc_ratio_error.SetFillStyle(3013)  # Crosshatch pattern
            mc_ratio_error.SetMarkerSize(0)
            ROOT.SetOwnership(mc_ratio_error, False)
            self._objects_to_keep.append(mc_ratio_error)
            mc_ratio_error.Draw("E2 SAME")
            
            # Draw horizontal line at y=1
            line = ROOT.TLine(self.xmin, 1., self.xmax, 1.)
            line.SetLineStyle(2)
            line.SetLineColor(ROOT.kBlack)
            line.SetLineWidth(1)
            ROOT.SetOwnership(line, False)
            self._objects_to_keep.append(line)
            line.Draw()
            
            # Draw combined data ratio histogram
            self.ratio.SetLineColor(DATA_COLOR)
            self.ratio.SetLineWidth(2)
            self.ratio.SetMarkerStyle(20)
            self.ratio.SetMarkerSize(0.8)
            self.ratio.SetMarkerColor(DATA_COLOR)
            self.ratio.Draw("E1 SAME")
            
            # Redraw axis for ratio pad
            self.pad2.RedrawAxis()
        
        # Update canvas
        self.canv.Update()
    
    def save_as(self, filename):
        """Save the plot"""
        self.canv.SaveAs(filename)
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'canv') and self.canv:
            self.canv.Close()
        self._objects_to_keep.clear()
        gc.collect()
    
    def __del__(self):
        """Destructor"""
        try:
            self.close()
        except:
            pass

def load_histogram(file_path, hist_name, systematic="Central", silent=False):
    """Load histogram from ROOT file"""
    root_file = ROOT.TFile.Open(file_path)
    if not root_file or root_file.IsZombie():
        if not silent:
            print(f"Error: Cannot open file {file_path}")
        return None
    
    # Navigate to systematic directory
    directory = root_file.Get(systematic)
    if not directory:
        if not silent:
            print(f"Error: Cannot find directory {systematic} in {file_path}")
        root_file.Close()
        return None
    
    hist = directory.Get(hist_name)
    if not hist:
        if not silent:
            print(f"Error: Cannot find histogram {hist_name} in {file_path}:{systematic}")
        root_file.Close()
        return None
    
    # Clone to avoid issues when file is closed
    hist_clone = hist.Clone(f"{os.path.basename(file_path)}_{hist_name}")
    hist_clone.SetDirectory(0)
    ROOT.SetOwnership(hist_clone, False)
    root_file.Close()
    
    return hist_clone

def combine_muon_data(data_dir, hist_name, systematic="Central"):
    """Load and combine Muon C and D data histograms (excluding E)"""
    muon_c_path = os.path.join(data_dir, "Muon_C.root")
    muon_d_path = os.path.join(data_dir, "Muon_D.root")
    
    # Load histograms
    hist_c = load_histogram(muon_c_path, hist_name, systematic)
    hist_d = load_histogram(muon_d_path, hist_name, systematic)
    
    # Track individual contributions
    events_c = hist_c.Integral() if hist_c else 0
    events_d = hist_d.Integral() if hist_d else 0
    
    # Create combined histogram
    combined_hist = None
    
    # Start with the first available histogram
    if hist_c:
        combined_hist = hist_c.Clone("Combined_Muon_Data")
        combined_hist.SetDirectory(0)
        print(f"Loaded Muon C: {events_c:.1f} events")
    elif hist_d:
        combined_hist = hist_d.Clone("Combined_Muon_Data")
        combined_hist.SetDirectory(0)
        print(f"Loaded Muon D: {events_d:.1f} events")
    
    # Add the remaining histogram
    if combined_hist and hist_d and combined_hist != hist_d:
        combined_hist.Add(hist_d)
        print(f"Added Muon D: {events_d:.1f} events")
    elif combined_hist and hist_c and combined_hist != hist_c:
        combined_hist.Add(hist_c)
        print(f"Added Muon C: {events_c:.1f} events")
    
    if combined_hist:
        ROOT.SetOwnership(combined_hist, False)
        total_events = combined_hist.Integral()
        print(f"Combined Data Total (C+D): {total_events:.1f} events")
    else:
        print("Warning: Could not load any muon data histograms")
    
    return combined_hist

def load_mc_histogram(data_dir, hist_name, systematic="Central"):
    """Load MC histogram from TTLJ file"""
    ttlj_path = os.path.join(data_dir, "TTLJ_powheg.root")
    
    mc_hist = load_histogram(ttlj_path, hist_name, systematic)
    if mc_hist:
        print(f"Loaded TTbar MC: {mc_hist.Integral():.1f} events")
    
    return mc_hist

def plot_data_mc_comparison(data_dir, hist_name, config, output_name="data_mc_comparison", systematic="Central"):
    """Create Data vs MC comparison plot"""
    
    print(f"Creating Data vs MC comparison for histogram: {hist_name}")
    print(f"Data directory: {data_dir}")
    
    # Load and combine muon data (C and D only, excluding E)
    combined_data_hist = combine_muon_data(data_dir, hist_name, systematic)
    
    # Load MC histogram
    mc_hist = load_mc_histogram(data_dir, hist_name, systematic)
    
    if not combined_data_hist and not mc_hist:
        print("Error: No histograms could be loaded!")
        return None
    
    if not combined_data_hist:
        print("Warning: No data histograms found!")
    if not mc_hist:
        print("Warning: No MC histogram found!")
    
    # Apply rebinning if requested
    if "rebin" in config and config["rebin"] > 1:
        if combined_data_hist:
            combined_data_hist.Rebin(config["rebin"])
        if mc_hist:
            mc_hist.Rebin(config["rebin"])
    
    # Create and draw the plot
    canvas = None
    try:
        canvas = DataMCCanvas(combined_data_hist, mc_hist, config)
        canvas.draw()
        
        # Save the plot
        canvas.save_as(f"{output_name}.png")
        canvas.save_as(f"{output_name}.pdf")
        
        print(f"Plot saved as {output_name}.png and {output_name}.pdf")
        
        return canvas
        
    except Exception as e:
        print(f"Error creating plot: {e}")
        if canvas:
            canvas.close()
        return None

def main():
    """Main function to create TTbar Data vs MC plots"""
    
    print("TTbar Data vs MC Comparison Plotter")
    print("=" * 50)
    
    # Check if data directory exists
    if not os.path.exists(data_directory):
        print(f"Error: Data directory {data_directory} does not exist!")
        return
    
    # Configuration for the plot
    plot_config = {
        "xRange": [0, 2000],        # TTbar transverse mass range
        "yRange": [0.5, 2.0],       # Ratio plot range
        "xTitle": "m_{T}^{t#bar{t}} [GeV]",
        "yTitle": "Events / bin",
        "logy": True,               # Log scale
        "rebin": 5,                 # Rebin factor
        "ymax": 100000,             # Higher max for log scale
        "ymin": 0.1                 # Small positive value for log scale
    }
    
    # Create the plot
    hist_name = "TTbarTransverseMass_v2"
    output_name = "TTbar_DataMC_comparison_2022"
    
    try:
        canvas = plot_data_mc_comparison(
            data_directory, 
            hist_name, 
            plot_config, 
            output_name
        )
        
        if canvas:
            print("Plot creation successful!")
            # Keep the canvas alive for a moment to ensure saving completes
            input("Press Enter to exit...")
            canvas.close()
        else:
            print("Plot creation failed!")
            
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()