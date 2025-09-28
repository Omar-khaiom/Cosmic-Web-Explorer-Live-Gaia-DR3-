/**
 * FPS Benchmark for Galaxy Visualization
 * Measures rendering performance across different scenarios
 */

class FPSBenchmark {
    constructor() {
        this.results = [];
        this.isRunning = false;
        this.currentTest = null;
        this.frameCount = 0;
        this.startTime = 0;
        this.frameTimes = [];
    }
    
    /**
     * Run a comprehensive benchmark suite
     */
    async runBenchmarkSuite() {
        console.log('Starting FPS benchmark suite...');
        
        const testCases = [
            { name: 'LOD 0 - High Detail', lodLevel: 0, pointCount: 100000 },
            { name: 'LOD 1 - Medium Detail', lodLevel: 1, pointCount: 50000 },
            { name: 'LOD 2 - Low Detail', lodLevel: 2, pointCount: 25000 },
            { name: 'Zoom In Test', lodLevel: 0, zoom: 0.1 },
            { name: 'Zoom Out Test', lodLevel: 2, zoom: 10.0 },
            { name: 'Rotation Test', lodLevel: 1, rotation: true }
        ];
        
        for (const testCase of testCases) {
            const result = await this.runSingleTest(testCase);
            this.results.push(result);
            
            // Wait between tests
            await this.sleep(1000);
        }
        
        this.generateReport();
    }
    
    /**
     * Run a single benchmark test
     */
    async runSingleTest(testConfig, duration = 5000) {
        console.log(`Running test: ${testConfig.name}`);
        
        this.currentTest = testConfig;
        this.frameCount = 0;
        this.frameTimes = [];
        this.startTime = performance.now();
        
        // Configure the test environment
        this.configureTest(testConfig);
        
        // Run the test
        return new Promise((resolve) => {
            this.isRunning = true;
            
            const measureFrame = () => {
                if (!this.isRunning) return;
                
                const frameStart = performance.now();
                
                // Simulate rendering work
                this.simulateRender();
                
                const frameEnd = performance.now();
                const frameTime = frameEnd - frameStart;
                
                this.frameTimes.push(frameTime);
                this.frameCount++;
                
                if (frameEnd - this.startTime >= duration) {
                    this.isRunning = false;
                    resolve(this.calculateResults());
                } else {
                    requestAnimationFrame(measureFrame);
                }
            };
            
            requestAnimationFrame(measureFrame);
        });
    }
    
    /**
     * Configure test environment
     */
    configureTest(config) {
        // This would interact with the actual galaxy viewer
        // For now, just log the configuration
        console.log('Test configuration:', config);
        
        // Set LOD level
        if (config.lodLevel !== undefined) {
            console.log(`Setting LOD level to ${config.lodLevel}`);
        }
        
        // Set zoom level
        if (config.zoom !== undefined) {
            console.log(`Setting zoom to ${config.zoom}`);
        }
        
        // Enable rotation
        if (config.rotation) {
            console.log('Enabling rotation animation');
        }
    }
    
    /**
     * Simulate rendering work
     */
    simulateRender() {
        // Simulate some computational work
        const pointCount = this.currentTest.pointCount || 50000;
        
        // Simulate matrix calculations
        for (let i = 0; i < pointCount / 1000; i++) {
            Math.sin(Math.random() * Math.PI * 2);
            Math.cos(Math.random() * Math.PI * 2);
        }
    }
    
    /**
     * Calculate test results
     */
    calculateResults() {
        const totalTime = performance.now() - this.startTime;
        const avgFPS = (this.frameCount / totalTime) * 1000;
        const avgFrameTime = totalTime / this.frameCount;
        
        const sortedFrameTimes = [...this.frameTimes].sort((a, b) => a - b);
        const p95FrameTime = sortedFrameTimes[Math.floor(sortedFrameTimes.length * 0.95)];
        const p99FrameTime = sortedFrameTimes[Math.floor(sortedFrameTimes.length * 0.99)];
        
        return {
            testName: this.currentTest.name,
            totalFrames: this.frameCount,
            totalTime: totalTime,
            avgFPS: avgFPS,
            avgFrameTime: avgFrameTime,
            minFrameTime: Math.min(...this.frameTimes),
            maxFrameTime: Math.max(...this.frameTimes),
            p95FrameTime: p95FrameTime,
            p99FrameTime: p99FrameTime,
            config: this.currentTest
        };
    }
    
    /**
     * Generate benchmark report
     */
    generateReport() {
        console.log('\n=== FPS Benchmark Report ===');
        console.log('=' * 40);
        
        this.results.forEach((result, index) => {
            console.log(`\nTest ${index + 1}: ${result.testName}`);
            console.log(`Average FPS: ${result.avgFPS.toFixed(2)}`);
            console.log(`Average Frame Time: ${result.avgFrameTime.toFixed(2)}ms`);
            console.log(`Min Frame Time: ${result.minFrameTime.toFixed(2)}ms`);
            console.log(`Max Frame Time: ${result.maxFrameTime.toFixed(2)}ms`);
            console.log(`95th Percentile: ${result.p95FrameTime.toFixed(2)}ms`);
            console.log(`99th Percentile: ${result.p99FrameTime.toFixed(2)}ms`);
        });
        
        // Export results as JSON
        this.exportResults();
    }
    
    /**
     * Export results to JSON file
     */
    exportResults() {
        const jsonData = JSON.stringify({
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            results: this.results
        }, null, 2);
        
        // In a real implementation, this would save to a file
        console.log('\nBenchmark results (JSON):');
        console.log(jsonData);
        
        // Create downloadable file
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `fps_benchmark_${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    /**
     * Utility function to sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Usage example
if (typeof window !== 'undefined') {
    // Browser environment
    window.FPSBenchmark = FPSBenchmark;
    
    // Auto-start benchmark when page loads
    window.addEventListener('DOMContentLoaded', () => {
        const benchmark = new FPSBenchmark();
        
        // Add button to start benchmark
        const button = document.createElement('button');
        button.textContent = 'Run FPS Benchmark';
        button.style.position = 'fixed';
        button.style.top = '10px';
        button.style.right = '10px';
        button.style.zIndex = '1000';
        button.onclick = () => benchmark.runBenchmarkSuite();
        document.body.appendChild(button);
    });
} else {
    // Node.js environment
    module.exports = FPSBenchmark;
}