import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = BASE_DIR + "/data/health_data.csv"

# Titles
APP_TITLE = "Farm Monitoring Dashboard"
WELCOME_MESSAGE = "Welcome, {username}!"
FARM_HEALTH_TITLE = "Overall Farm Health"
HEALTH_TREND_TITLE = "Farm Health Trend Over Time"
SHELF_OVERVIEW_TITLE = "Shelf Health Overview"

# Buttons & Labels
HEALTH_METRIC_LABEL = "Most Recent Health %"

# Error Messages
ERROR_NO_SHELF_SELECTED = "No shelf selected! Please go back to the dashboard."

# Styles
HOVER_TABLE_STYLE = """
<style>
    .hover-table-row:hover { background-color: #f0f0f0 !important; cursor: pointer; }
    .stDataFrame { border-radius: 10px; }
</style>
"""

