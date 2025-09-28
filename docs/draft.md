# Galaxy Visualization System

## Draft Documentation

### Overview

This project implements a large-scale galaxy visualization system designed to render millions of astronomical objects with adaptive Level of Detail (LOD) techniques for optimal performance.

### System Architecture

The system consists of several key components:

#### Data Pipeline

- **Raw Data Processing**: Preprocessing SDSS galaxy survey data
- **Voxel Tiling**: Spatial partitioning for efficient data access
- **LOD Generation**: Multi-resolution data structures for adaptive rendering

#### Visualization Engine

- **WebGL Renderer**: Hardware-accelerated 3D rendering
- **Adaptive LOD**: Dynamic quality adjustment based on viewing distance
- **Point Cloud Rendering**: Efficient galaxy point visualization with custom shaders

#### Performance Evaluation

- **Metrics Collection**: FPS monitoring and performance analysis
- **Benchmark Suite**: Automated testing across different scenarios
- **Quality Assessment**: Visual and quantitative evaluation tools

### Key Features

1. **Scalable Rendering**: Handles datasets with millions of galaxies
2. **Interactive Navigation**: Smooth camera controls with zoom and rotation
3. **Adaptive Quality**: Automatic LOD selection for optimal performance
4. **Real-time Performance**: Target 60 FPS on modern hardware
5. **Scientific Accuracy**: Preserves astronomical data integrity

### Technical Specifications

#### Data Format

- Input: CSV files with galaxy coordinates, magnitudes, and colors
- Processing: Binary tile format for efficient GPU transfer
- LOD Levels: 3 levels (high, medium, low detail)

#### Rendering Pipeline

- Vertex Shader: Position transformation and point size calculation
- Fragment Shader: Galaxy appearance with brightness and color
- Culling: Frustum and distance-based visibility optimization

#### Performance Targets

- **High Detail (LOD 0)**: >30 FPS with 100K+ points
- **Medium Detail (LOD 1)**: >45 FPS with 50K+ points
- **Low Detail (LOD 2)**: >60 FPS with 25K+ points

### Directory Structure

```
/data/               # Galaxy datasets and processed tiles
  galaxies_raw.csv   # Raw SDSS data
  galaxies_final.csv # Processed data ready for visualization
  /tiles/            # Spatial tile data
    /lod0/*.bin      # High detail binary tiles
    /lod1/*.bin      # Medium detail binary tiles
    /lod2/*.bin      # Low detail binary tiles

/scripts/            # Data processing and build tools
  preprocess_sdss.py # Raw data cleaning and formatting
  build_voxel_tiles.py # Spatial partitioning implementation
  build_lod_sets.py  # Multi-resolution data generation

/viewer/             # WebGL visualization application
  index.html         # Main application interface
  main.js           # Core visualization logic
  /shaders/         # GLSL shader programs
    points.vert.glsl # Vertex shader for galaxy points
    points.frag.glsl # Fragment shader for galaxy appearance

/eval/              # Performance evaluation and metrics
  graph_metrics.py  # Performance analysis tools
  fps_bench.js     # Automated benchmark suite
  metrics.ipynb    # Interactive analysis notebook

/docs/              # Documentation and research materials
  draft.md         # Project documentation (this file)
  /figures/        # Visualizations and diagrams
```

### Development Roadmap

#### Phase 1: Core Implementation ✓

- [x] Basic data structures and file organization
- [x] Initial WebGL renderer with basic point rendering
- [x] Simple camera controls and navigation

#### Phase 2: Performance Optimization

- [ ] Implement adaptive LOD system
- [ ] Add frustum culling and occlusion
- [ ] Optimize GPU buffer management
- [ ] Add performance profiling tools

#### Phase 3: Visual Enhancement

- [ ] Improve galaxy appearance with realistic colors
- [ ] Add star formation regions and nebulae
- [ ] Implement smooth transitions between LOD levels
- [ ] Add visual effects for stellar phenomena

#### Phase 4: Scientific Features

- [ ] Add galaxy classification and filtering
- [ ] Implement redshift visualization
- [ ] Add astronomical coordinate systems
- [ ] Include observational metadata display

### Research Questions

1. **Scalability**: How does performance scale with galaxy count?
2. **Visual Quality**: What LOD transition strategies maintain visual continuity?
3. **Scientific Utility**: How can we preserve astronomical accuracy while optimizing performance?
4. **User Experience**: What navigation paradigms work best for 3D cosmic data?

### References

- SDSS Data Release Documentation
- WebGL 2.0 Specification
- Astronomical Visualization Best Practices
- Real-time Rendering Techniques for Large Datasets

## How to Run the Galaxy Visualization System

### Prerequisites

1. **Python Environment**

   - Python 3.8 or higher
   - Required packages: `pandas`, `numpy`, `matplotlib`, `jupyter`

2. **Web Browser**

   - Modern browser with WebGL 2.0 support (Chrome, Firefox, Edge)
   - Hardware-accelerated graphics enabled

3. **Local Web Server**
   - Required for loading shader files and handling CORS policies

### Quick Start Guide

#### Step 1: Set up Python Environment

```powershell
# Navigate to project directory
cd d:\space

# Install Python dependencies
pip install pandas numpy matplotlib seaborn jupyter plotly

# Verify installation
python -c "import pandas, numpy, matplotlib; print('Dependencies installed successfully')"
```

#### Step 2: Process Galaxy Data (Optional for Demo)

```powershell
# Navigate to scripts directory
cd scripts

# Run data preprocessing
python preprocess_sdss.py

# Build voxel tiles
python build_voxel_tiles.py

# Generate LOD sets
python build_lod_sets.py
```

#### Step 3: Start the Visualization

**Option A: Using Python's built-in server**

```powershell
# Navigate to viewer directory
cd ..\viewer

# Start local server on port 8000
python -m http.server 8000

# Open browser and navigate to:
# http://localhost:8000
```

**Option B: Using Node.js (if available)**

```powershell
# Navigate to viewer directory
cd ..\viewer

# Install and run http-server
npx http-server -p 8000 -c-1

# Open browser and navigate to:
# http://localhost:8000
```

#### Step 4: Run Performance Analysis

```powershell
# Navigate to evaluation directory
cd ..\eval

# Run performance metrics
python graph_metrics.py

# Start Jupyter notebook for interactive analysis
jupyter notebook metrics.ipynb
```

### Detailed Usage Instructions

#### 1. Data Processing Pipeline

The data processing consists of three main steps:

**Preprocess SDSS Data:**

```powershell
cd d:\space\scripts
python preprocess_sdss.py
```

- Cleans raw galaxy survey data
- Normalizes coordinates and magnitudes
- Outputs processed CSV for visualization

**Build Voxel Tiles:**

```powershell
python build_voxel_tiles.py
```

- Partitions galaxy data into spatial tiles
- Creates efficient data structures for rendering
- Generates binary tile files

**Generate LOD Sets:**

```powershell
python build_lod_sets.py
```

- Creates multiple resolution levels
- Optimizes data for different viewing distances
- Outputs LOD-specific binary files

#### 2. Web Visualization

**Starting the Viewer:**

```powershell
cd d:\space\viewer
python -m http.server 8000
```

**Browser Controls:**

- **Mouse Drag**: Rotate camera around galaxies
- **Mouse Wheel**: Zoom in/out
- **LOD Level Dropdown**: Manually select detail level
- **Point Size Slider**: Adjust galaxy point sizes

**URL Parameters (Advanced):**

- `http://localhost:8000?lod=1` - Start with specific LOD level
- `http://localhost:8000?debug=1` - Enable performance overlay

#### 3. Performance Evaluation

**Automated Benchmarks:**

```powershell
cd d:\space\eval
python graph_metrics.py
```

**Interactive Analysis:**

```powershell
jupyter notebook metrics.ipynb
```

**Web-based FPS Testing:**

- Open the viewer in browser
- Press the "Run FPS Benchmark" button
- Results will be displayed and downloadable as JSON

### Troubleshooting

#### Common Issues

**1. CORS Errors when loading shaders:**

- **Solution**: Always use a local server, never open HTML files directly
- **Command**: `python -m http.server 8000` in the viewer directory

**2. WebGL not supported:**

- **Check**: Visit https://get.webgl.org/ to verify WebGL support
- **Solution**: Update graphics drivers or try a different browser

**3. Python module not found:**

- **Solution**: Install missing dependencies
- **Command**: `pip install pandas numpy matplotlib jupyter plotly seaborn`

**4. Poor performance:**

- **Check**: Ensure hardware acceleration is enabled in browser
- **Solution**: Try lower LOD levels or reduce point sizes

#### Performance Optimization

**For better performance:**

1. Use Chrome or Firefox with hardware acceleration
2. Start with LOD level 2 for initial testing
3. Reduce point size if frame rate is low
4. Close other browser tabs and applications

**For development:**

1. Use browser developer tools (F12) to monitor performance
2. Check WebGL errors in console
3. Use the built-in benchmark tools for systematic testing

### File Structure Summary

```
d:\space\
├── data\           # Raw and processed galaxy data
├── scripts\        # Python data processing tools
├── viewer\         # WebGL visualization application
├── eval\          # Performance analysis tools
└── docs\          # Documentation (this file)
```

### Next Steps

After running the system:

1. **Explore the Data**: Use mouse controls to navigate the galaxy visualization
2. **Test Performance**: Run benchmarks to understand system capabilities
3. **Analyze Results**: Use Jupyter notebooks for detailed performance analysis
4. **Customize**: Modify shaders and rendering parameters for different effects

---

_Last updated: September 28, 2025_
