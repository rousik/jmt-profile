# JMT Profile Generator

A tool to generate elevation profiles from GPX files, particularly useful for visualizing multi-day hikes like the John Muir Trail.

## Installation

1. Make sure you have [Poetry](https://python-poetry.org/) installed
2. Clone this repository
3. Install dependencies:
```bash
poetry install
```

## Usage

The tool can be used to generate elevation profiles from one or more GPX files. Each GPX file should represent one day of hiking.

Basic usage:
```bash
poetry run python -m jmt_profile.cli day1.gpx day2.gpx day3.gpx
```

To save the plot to a file:
```bash
poetry run python -m jmt_profile.cli day1.gpx day2.gpx day3.gpx -o profile.png
```

The generated plot will show:
- X-axis: Cumulative distance in miles
- Y-axis: Elevation in feet
- Different colors for each day's segment
- A legend identifying each day
- Grid lines for better readability

## Requirements

- Python 3.11 or higher
- GPX files from your hike (one per day)
