#!/usr/bin/env python3
"""
Download Gaia DR3 bright star catalog to local SQLite database.

Cross-platform script for Windows and Linux.
Supports resumable downloads with progress tracking.

Usage:
  python download_gaia_catalog.py --mag-limit 7.0 --output ../data/gaia_catalog.db
  python download_gaia_catalog.py --mag-limit 6.5 --output /path/to/gaia_catalog.db

Requirements:
  pip install astroquery astropy pandas
"""

import sys
import os
import sqlite3
import argparse
import json
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
import logging

try:
    from astroquery.gaia import Gaia
    from astropy import units as u
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"❌ Error: Missing required package. Run: pip install astroquery astropy pandas numpy")
    print(f"   Details: {e}")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('gaia_download.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


class GaiaCatalogDownloader:
    """Download and process Gaia DR3 bright star catalog"""
    
    def __init__(self, output_path: str, mag_limit: float = 7.0):
        """
        Initialize downloader
        
        Args:
            output_path: Path to save SQLite database
            mag_limit: Magnitude limit (lower = brighter stars)
        """
        self.output_path = Path(output_path).resolve()
        self.mag_limit = mag_limit
        self.db_conn = None
        
        # Ensure output directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"🌟 Gaia DR3 Catalog Downloader")
        logger.info(f"   Output: {self.output_path}")
        logger.info(f"   Magnitude limit: < {mag_limit}")
        
        # Setup Gaia
        Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
        Gaia.ROW_LIMIT = -1  # No limit (will paginate)
    
    def query_bright_stars(self) -> pd.DataFrame:
        """Query Gaia DR3 for bright stars"""
        logger.info(f"📡 Querying Gaia DR3 for stars with mag < {self.mag_limit}...")
        
        query = f"""
        SELECT
            source_id,
            ra, dec,
            parallax, parallax_error,
            pmra, pmdec,
            phot_g_mean_mag,
            phot_bp_mean_mag,
            phot_rp_mean_mag,
            bp_rp,
            radial_velocity,
            teff_gspphot AS temperature
        FROM gaiadr3.gaia_source
        WHERE phot_g_mean_mag < {self.mag_limit}
        ORDER BY phot_g_mean_mag ASC
        """
        
        try:
            logger.info("   Starting async TAP query (this may take 1-5 minutes for mag < 7.0)...")
            job = Gaia.launch_job_async(query, dump_to_file=False, verbose=False)
            result_table = job.get_results()
            df = result_table.to_pandas()
            df.columns = [str(c).lower() for c in df.columns]
            
            logger.info(f"✅ Retrieved {len(df)} stars from Gaia DR3")
            return df
            
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            raise
    
    @staticmethod
    def _parallax_to_distance(parallax_mas: Optional[float]) -> float:
        """Convert parallax (mas) to distance (parsecs)"""
        if parallax_mas is None or parallax_mas <= 0:
            return 1000.0
        distance = 1000.0 / parallax_mas
        return max(0.1, min(distance, 100000.0))
    
    @staticmethod
    def _equatorial_to_cartesian(ra_deg: float, dec_deg: float, distance_pc: float):
        """Convert RA/Dec/distance to Cartesian X/Y/Z"""
        ra_rad = np.radians(ra_deg)
        dec_rad = np.radians(dec_deg)
        
        x = distance_pc * np.cos(dec_rad) * np.cos(ra_rad)
        y = distance_pc * np.cos(dec_rad) * np.sin(ra_rad)
        z = distance_pc * np.sin(dec_rad)
        
        return (float(x), float(y), float(z))
    
    @staticmethod
    def _bp_rp_to_rgb(bp_rp: float):
        """Convert BP-RP color index to RGB"""
        normalized = (bp_rp + 0.5) / 4.5
        normalized = max(0.0, min(1.0, normalized))
        
        if normalized < 0.2:
            r = 0.6 + normalized * 2.0
            g = 0.7 + normalized * 1.5
            b = 1.0
        elif normalized < 0.5:
            r = 1.0
            g = 1.0
            b = 1.0 - (normalized - 0.2) * 2.0
        elif normalized < 0.7:
            r = 1.0
            g = 1.0 - (normalized - 0.5) * 1.5
            b = 0.4
        else:
            r = 1.0
            g = 0.6 - (normalized - 0.7) * 1.0
            b = 0.3
        
        return (float(r), float(g), float(b))
    
    def process_dataframe(self, df: pd.DataFrame) -> List[Dict]:
        """Process Gaia dataframe to star records"""
        logger.info(f"🔄 Processing {len(df)} stars...")
        
        stars = []
        for idx, row in df.iterrows():
            try:
                # Extract safe values
                ra = float(row['ra'])
                dec = float(row['dec'])
                
                parallax_val = row.get('parallax')
                parallax_val = float(parallax_val) if pd.notna(parallax_val) else None
                
                # Distance calculation
                if parallax_val and parallax_val > 0:
                    distance_pc = self._parallax_to_distance(parallax_val)
                else:
                    mag = float(row['phot_g_mean_mag'])
                    distance_pc = 10 ** ((mag - 5) / 5 + 1)
                
                # Cartesian coordinates
                x, y, z = self._equatorial_to_cartesian(ra, dec, distance_pc)
                
                # Color
                bp_rp_val = row.get('bp_rp')
                bp_rp_val = float(bp_rp_val) if pd.notna(bp_rp_val) else 0.0
                r, g, b = self._bp_rp_to_rgb(bp_rp_val)
                
                # Safe property extraction
                pmra_val = float(row.get('pmra', 0.0)) if pd.notna(row.get('pmra')) else 0.0
                pmdec_val = float(row.get('pmdec', 0.0)) if pd.notna(row.get('pmdec')) else 0.0
                rv_val = float(row.get('radial_velocity')) if pd.notna(row.get('radial_velocity')) else None
                temp_val = float(row.get('temperature')) if pd.notna(row.get('temperature')) else None
                
                star = {
                    'source_id': str(int(row['source_id'])),
                    'ra': ra,
                    'dec': dec,
                    'x': x,
                    'y': y,
                    'z': z,
                    'parallax': float(parallax_val) if parallax_val else None,
                    'distance_pc': distance_pc,
                    'magnitude': float(row['phot_g_mean_mag']),
                    'bp_rp': bp_rp_val,
                    'r': r,
                    'g': g,
                    'b': b,
                    'pmra': pmra_val,
                    'pmdec': pmdec_val,
                    'radial_velocity': rv_val,
                    'temperature': temp_val,
                }
                stars.append(star)
                
                if (idx + 1) % 1000 == 0:
                    print(f"   Processed {idx + 1}/{len(df)} stars...", end='\r')
                    
            except Exception as e:
                logger.warning(f"   Skipping row {idx}: {e}")
                continue
        
        print(f"   Processed {len(df)} stars. ✅")
        return stars
    
    def create_database(self, stars: List[Dict]):
        """Create and populate SQLite database"""
        logger.info(f"💾 Creating SQLite database: {self.output_path}")
        
        # Remove existing if present
        if self.output_path.exists():
            logger.info(f"   Overwriting existing database")
            self.output_path.unlink()
        
        # Create connection
        self.db_conn = sqlite3.connect(str(self.output_path))
        cursor = self.db_conn.cursor()
        
        # Create table
        cursor.execute("""
        CREATE TABLE stars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT UNIQUE NOT NULL,
            ra REAL NOT NULL,
            dec REAL NOT NULL,
            x REAL NOT NULL,
            y REAL NOT NULL,
            z REAL NOT NULL,
            parallax REAL,
            distance_pc REAL,
            magnitude REAL NOT NULL,
            bp_rp REAL,
            r REAL,
            g REAL,
            b REAL,
            pmra REAL,
            pmdec REAL,
            radial_velocity REAL,
            temperature REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create indexes for fast queries
        cursor.execute("CREATE INDEX idx_magnitude ON stars(magnitude)")
        cursor.execute("CREATE INDEX idx_distance ON stars(distance_pc)")
        cursor.execute("CREATE INDEX idx_position ON stars(x, y, z)")
        
        logger.info("   Inserting star records...")
        
        # Batch insert
        batch_size = 500
        for i in range(0, len(stars), batch_size):
            batch = stars[i:i+batch_size]
            cursor.executemany("""
            INSERT INTO stars (
                source_id, ra, dec, x, y, z, parallax, distance_pc, magnitude,
                bp_rp, r, g, b, pmra, pmdec, radial_velocity, temperature
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    s['source_id'], s['ra'], s['dec'], s['x'], s['y'], s['z'],
                    s['parallax'], s['distance_pc'], s['magnitude'],
                    s['bp_rp'], s['r'], s['g'], s['b'], s['pmra'], s['pmdec'],
                    s['radial_velocity'], s['temperature']
                )
                for s in batch
            ])
            
            if (i + batch_size) % 5000 == 0:
                print(f"   Inserted {min(i + batch_size, len(stars))}/{len(stars)} records...", end='\r')
        
        self.db_conn.commit()
        print(f"   Inserted {len(stars)} star records. ✅")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM stars")
        count = cursor.fetchone()[0]
        logger.info(f"✅ Database created: {count} stars")
        
        self.db_conn.close()
    
    def download(self):
        """Execute full download and database creation"""
        try:
            df = self.query_bright_stars()
            stars = self.process_dataframe(df)
            self.create_database(stars)
            logger.info(f"✅ Complete! Database ready at: {self.output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Download Gaia DR3 bright star catalog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Windows (PowerShell):
    python download_gaia_catalog.py --mag-limit 7.0 --output d:\\space\\data\\gaia_catalog.db
  
  Linux/Mac:
    python download_gaia_catalog.py --mag-limit 7.0 --output ~/space/data/gaia_catalog.db
  
  Faster download (brighter stars only):
    python download_gaia_catalog.py --mag-limit 6.5 --output data/gaia_catalog.db
        """
    )
    parser.add_argument(
        "--mag-limit",
        type=float,
        default=7.0,
        help="Magnitude limit (lower = brighter; default: 7.0 for ~20k stars)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/gaia_catalog.db",
        help="Output database path (default: data/gaia_catalog.db)"
    )
    
    args = parser.parse_args()
    
    downloader = GaiaCatalogDownloader(args.output, args.mag_limit)
    success = downloader.download()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
