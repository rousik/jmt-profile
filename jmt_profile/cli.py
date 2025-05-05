import argparse
import gpxpy
from pathlib import Path
from typing import Dict, List, NamedTuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class ElevationPoint(NamedTuple):
    """Represents single point of a hike."""
    day: int
    distance: float
    elevation: float


def parse_gpx_files(gpx_files: List[Path], use_imperial: bool = False) -> List[ElevationPoint]:
    """Parse a GPX files and extract points.
    
    Args:
        gpx_file: Path to the GPX file
        use_imperial: if True, units are in miles/feet
        
    Returns:
        Tuple of (distances, elevations) where:
        - distances: List of cumulative distances in miles
        - elevations: List of corresponding elevations in feet
    """

    elevation_points: List[ElevationPoint] = []
    total_distance = 0.0
    prev_point = None
    
    for (day, gpx_file) in enumerate(gpx_files):
        with open(gpx_file, 'r') as f:
            gpx = gpxpy.parse(f)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    elevation = point.elevation
                    if prev_point:
                        # Convert from meters to kilometers
                        total_distance += point.distance_2d(prev_point) / 1000.0
                    prev_point = point
                    elevation_points.append(ElevationPoint(day=day, distance=total_distance, elevation=elevation))
    
    return elevation_points


def main():
    parser = argparse.ArgumentParser(description='Generate elevation profile from GPX files')
    parser.add_argument('gpx_files', nargs='+', type=Path, help='GPX files to process (one per day)')
    parser.add_argument('--output', '-o', type=Path, help='Output file for the plot (e.g., profile.png)')
    parser.add_argument('--imperial', action='store_true', help='Use imperial units (miles/feet) instead of metric (km/m)')
    parser.add_argument('--colormap', '-c', type=str, default='viridis',
                       choices=['viridis', 'plasma', 'inferno', 'magma', 'hsv', 'nipy_spectral', 'jet', 'gist_rainbow'],
                       help='Colormap to use for the plot')
    
    args = parser.parse_args()
    
    # Verify all GPX files exist
    for gpx_file in args.gpx_files:
        if not gpx_file.exists():
            print(f"Error: File {gpx_file} does not exist")
            return 1
        
    epoints = parse_gpx_files(args.gpx_files, use_imperial=args.imperial)

    # To plot this, we need to transpose the data into list of x-points, y-points; each of these also need
    # to be keyed by the day.

    daily_points: Dict[int, List[ElevationPoint]] = {}
    for ept in epoints:
        if ept.day not in daily_points:
            daily_points[ept.day] = []
        daily_points[ept.day].append(ept)

    # Plot this.
    plt.figure(figsize=(12, 6))
    # Use the selected colormap
    colors = cm.get_cmap(args.colormap, len(daily_points))
    
    # Set font family to a serif font
    plt.rcParams['font.family'] = 'serif'
    
    for day in sorted(daily_points.keys()):
        x_points = [ept.distance for ept in daily_points[day]]
        y_points = [ept.elevation for ept in daily_points[day]]
        if args.imperial:
            x_points = [x * 0.621371 for x in x_points]
            y_points = [y * 3.28084 for y in y_points]
        plt.plot(x_points, y_points, color = colors(day))
        plt.fill_between(x_points, y_points, color=colors(day), alpha=0.3)
        # Add day number at the start of each segment
        plt.text(x_points[0], 0.0, str(day), 
                ha='left', va='bottom',
                fontsize=20)

    if args.imperial:
        plt.xlabel("Distance (mi)")
        plt.ylabel("Elevation (ft)")
    else:
        plt.xlabel("Distance (km)")
        plt.ylabel("Elevation (m)")
    plt.title("Elevation Profile by Day")
    plt.tight_layout()
    plt.show()
    return 0


if __name__ == '__main__':
    exit(main()) 