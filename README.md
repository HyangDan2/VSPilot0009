# Moiré Pattern Viewer

A PySide6-based visual tool to generate, analyze, and save Moiré pattern images, including FFT-based heatmaps and intensity tracking.

## Features

- Two-pattern moiré generation with adjustable parameters
- Live FFT heatmap visualization
- Moiré intensity tracking and chart
- Parameter persistence with JSON
- Save All functionality with timestamped experiment logs
- ML-ready for classification (planned)

## Directory Structure

- `moire_viewer/`: core GUI and logic
- `config/`: saved parameters
- `logs/`: auto-generated experiment logs
- `models/`: future ML classifier
- `ui/`: optional QtDesigner files
