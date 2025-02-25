import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from filelock import FileLock
from loguru import logger

# ---------------------------- Configuration ---------------------------- #

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = PROJECT_ROOT / "outputs" / "vol_oi" / "0DTE_vol_oi.csv"
OUTPUT_DIR = PROJECT_ROOT / "visualization" / "vol_oi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configure logger
LOG_DIR = PROJECT_ROOT / "logs" / "visuals"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    LOG_DIR / "vol_oi_zero_visual.log",
    rotation="1 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# ---------------------------- Utility Functions ---------------------------- #

def load_new_data(file_path):
    """Load the latest snapshot of vol/oi data with file locking."""
    try:
        lock = FileLock(f"{file_path}.lock")
        with lock:
            new_data = pd.read_csv(file_path)

        logger.info(f"CSV Columns: {new_data.columns.tolist()}")
        new_data['timestamp'] = pd.to_datetime(new_data['timestamp'])
        logger.info(f"Successfully loaded new data from {file_path}")
        return new_data
    except Exception as e:
        logger.error(f"Error loading new data from {file_path}: {e}")
        raise


def create_bar_chart(data, call_col, put_col, title, output_file, spot_price):
    """Generate and save a Plotly horizontal bar chart for put/call volume or open interest."""
    try:
        fig = go.Figure()

        # Convert put values to negative for left-side alignment
        put_data = -data[put_col]
        call_data = data[call_col]

        # Add Put data (red)
        fig.add_trace(go.Bar(
            y=data['strike'],
            x=put_data,
            orientation='h',
            name=f"Put {put_col.capitalize()}",
            marker_color='red'
        ))

        # Add Call data (blue)
        fig.add_trace(go.Bar(
            y=data['strike'],
            x=call_data,
            orientation='h',
            name=f"Call {call_col.capitalize()}",
            marker_color='blue'
        ))

        # Determine full width of the chart (most left to most right)
        max_x = max(call_data.max(), abs(put_data.min()))
        min_x = -max_x

        # Add SPX spot price horizontal line spanning entire chart width
        fig.add_shape(
            type="line",
            x0=min_x,  # Extend from the most left
            x1=max_x,  # Extend to the most right
            y0=spot_price,
            y1=spot_price,
            line=dict(color="yellow", width=4, dash="dash")
        )

        # Add spot price line to legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="yellow", width=4, dash="dash"),
            name=f"SPX Spot Price {spot_price}"
        ))

        # Hide negative signs by customizing tick labels
        tick_values = list(range(int(min_x), int(max_x) + 1, int(max_x // 5)))
        tick_labels = [str(abs(tick)) for tick in tick_values]

        fig.update_layout(
            title=title,
            barmode='relative',
            xaxis_title="Volume / Open Interest",
            yaxis_title="Strike Price",
            template="plotly_dark",  # Enforce dark mode
            xaxis=dict(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                tickvals=tick_values,
                ticktext=tick_labels  # Display absolute values without negative signs
            )
        )

        fig.write_html(output_file)
        logger.info(f"Saved chart to {output_file}")
    except Exception as e:
        logger.error(f"Error creating chart {title}: {e}")
        raise


def process_visualizations():
    """Process visualization of vol/oi data."""
    try:
        logger.info("Starting visualization processing...")

        # Load the latest data
        data = load_new_data(INPUT_FILE)
        spot_price = data['spotPrice'].iloc[0]

        # Generate charts for volume and open interest
        create_bar_chart(
            data,
            call_col='call vol',
            put_col='put vol',
            title="Put/Call Volume per Strike",
            output_file=OUTPUT_DIR / "put_call_volume.html",
            spot_price=spot_price
        )

        create_bar_chart(
            data,
            call_col='call oi',
            put_col='put oi',
            title="Put/Call Open Interest per Strike",
            output_file=OUTPUT_DIR / "put_call_oi.html",
            spot_price=spot_price
        )

        create_bar_chart_split_vol_oi(
            data,
            title="Put/Call Volume + Open Interest per Strike",
            output_file=OUTPUT_DIR / "put_call_vol_oi.html",
            spot_price=spot_price
        )

        logger.info("All visualizations successfully created.")

    except Exception as e:
        logger.critical(f"Critical error during visualization processing: {e}")


def create_bar_chart_split_vol_oi(data, title, output_file, spot_price):
    """Generate and save a Plotly horizontal bar chart with separate volume and open interest for puts and calls."""
    try:
        fig = go.Figure()

        # Convert put values to negative for left-side alignment
        put_oi = -data['put oi']
        put_vol = -data['put vol']
        call_oi = data['call oi']
        call_vol = data['call vol']

        # Add Put Open Interest (Red)
        fig.add_trace(go.Bar(
            y=data['strike'],
            x=put_oi,
            orientation='h',
            name="Put Open Interest",
            marker_color='red'
        ))

        # Add Put Volume (Light Red)
        fig.add_trace(go.Bar(
            y=data['strike'],
            x=put_vol,
            orientation='h',
            name="Put Volume",
            marker_color='lightcoral'
        ))

        # Add Call Open Interest (Blue)
        fig.add_trace(go.Bar(
            y=data['strike'],
            x=call_oi,
            orientation='h',
            name="Call Open Interest",
            marker_color='blue'
        ))

        # Add Call Volume (Light Blue)
        fig.add_trace(go.Bar(
            y=data['strike'],
            x=call_vol,
            orientation='h',
            name="Call Volume",
            marker_color='lightskyblue'
        ))

        # Determine full width of the chart (most left to most right)
        max_x = max(call_oi.max() + call_vol.max(), abs(put_oi.min() + put_vol.min()))
        min_x = -max_x

        # Add SPX spot price horizontal line spanning entire chart width
        fig.add_shape(
            type="line",
            x0=min_x,  # Extend from the most left
            x1=max_x,  # Extend to the most right
            y0=spot_price,
            y1=spot_price,
            line=dict(color="yellow", width=4, dash="dash")
        )

        # Add spot price line to legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="yellow", width=4, dash="dash"),
            name=f"SPX Spot Price {spot_price}"
        ))

        fig.update_layout(
            title=title,
            barmode='relative',
            xaxis_title="Volume / Open Interest",
            yaxis_title="Strike Price",
            template="plotly_dark",  # Enforce dark mode
        )

        fig.write_html(output_file)
        logger.info(f"Saved chart to {output_file}")
    except Exception as e:
        logger.error(f"Error creating chart {title}: {e}")
        raise

# ---------------------------- Main Execution ---------------------------- #

if __name__ == "__main__":
    process_visualizations()

