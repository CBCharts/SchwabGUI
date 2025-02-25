#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# ----------------------------
# Define project paths
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "outputs" / "vol_oi"
OUTPUT_DIR = PROJECT_ROOT / "visualization" / "vol_oi" / "tryouts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Define file patterns to process
# ----------------------------
patterns = ["0DTE*.csv", "1DTE*.csv", "EoM*.csv", "EoW*.csv"]
csv_files = [f for pattern in patterns for f in INPUT_DIR.glob(pattern)]

if not csv_files:
    print("No CSV files found matching the specified patterns.")
else:
    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        
        # =========================
        # 1) LOAD & PREP THE DATA
        # =========================
        df_raw = pd.read_csv(csv_file)
        
        # Extract spotPrice from the first row (all rows have the same value)
        spot_price = df_raw["spotPrice"].iloc[0]
        
        # Convert expirationDate to datetime.date
        df_raw["expirationDate"] = pd.to_datetime(df_raw["expirationDate"], errors="coerce").dt.date
        
        # Wide-to-long conversion for calls and puts
        call_data = df_raw[["strike", "expirationDate", "call vol", "call oi"]].copy()
        call_data["OptionType"] = "Call"
        call_data.rename(columns={
            "strike": "Strike",
            "expirationDate": "Expiration",
            "call vol": "Volume",
            "call oi": "OpenInterest"
        }, inplace=True)
        
        put_data = df_raw[["strike", "expirationDate", "put vol", "put oi"]].copy()
        put_data["OptionType"] = "Put"
        put_data.rename(columns={
            "strike": "Strike",
            "expirationDate": "Expiration",
            "put vol": "Volume",
            "put oi": "OpenInterest"
        }, inplace=True)
        
        df = pd.concat([call_data, put_data], ignore_index=True)
        
        # =========================
        # 2) IDENTIFY TODAY & NEXT EXPIRATION
        # =========================
        system_today = datetime.date.today()
        unique_dates = sorted(df["Expiration"].dropna().unique())
        
        if not unique_dates:
            today_date = None
            next_date = None
        else:
            today_date = next((d for d in unique_dates if d >= system_today), unique_dates[-1])
            next_date = next((d for d in unique_dates if d > today_date), None)
        
        # Precompute next-date volumes per (Strike, OptionType) for the 50% rule
        next_vol_dict = {}
        if next_date:
            df_next = df[df["Expiration"] == next_date]
            grouped_next = df_next.groupby(["Strike", "OptionType"])["Volume"].sum().reset_index()
            for _, row in grouped_next.iterrows():
                next_vol_dict[(row["Strike"], row["OptionType"])] = row["Volume"]
        
        # =========================
        # 3) ASSIGN LEGEND CATEGORIES
        # =========================
        def get_legend_category(row):
            exp = row["Expiration"]
            opt_type = row["OptionType"]
            vol = row["Volume"]
            strike = row["Strike"]
            
            if exp == today_date:
                return "0DTE Calls" if opt_type == "Call" else "0DTE Puts"
            elif exp == next_date:
                return "1DTE"
            else:
                ref_vol = next_vol_dict.get((strike, opt_type), 0)
                if ref_vol > 0 and vol > 0.5 * ref_vol:
                    return "1DTE < ; +50% >1DTE Volume"
                else:
                    return "Remainder"
        
        df["LegendCategory"] = df.apply(get_legend_category, axis=1)
        
        # For the horizontal bar chart, convert puts to negative volumes
        df["VolumePlot"] = df.apply(lambda row: row["Volume"] if row["OptionType"] == "Call" else -row["Volume"], axis=1)
        
        # Define color mapping for the legend categories
        color_map = {
            "0DTE Calls": "blue",
            "0DTE Puts": "red",
            "1DTE": "yellow",
            "1DTE < ; +50% >1DTE Volume": "green",
            "Remainder": "white"
        }
        
        # =========================
        # 4) VISUALIZATION 1: HORIZONTAL BAR CHART
        # =========================
        fig1 = px.bar(
            df.sort_values("Strike"),
            x="VolumePlot",
            y="Strike",
            orientation="h",
            color="LegendCategory",
            color_discrete_map=color_map,
            hover_data=["Expiration", "Volume", "OpenInterest", "Strike", "OptionType"],
            template="plotly_dark",
            title="Visualization 1: Horizontal Bar (Puts Left, Calls Right)"
        )
        fig1.update_layout(
            xaxis=dict(zeroline=True, zerolinewidth=1, zerolinecolor='white')
        )
        
        # Add a dashed grey horizontal line at y = spot_price
        fig1.add_shape(
            type="line",
            xref="paper",  # span the entire x-axis
            x0=0,
            x1=1,
            yref="y",
            y0=spot_price,
            y1=spot_price,
            line=dict(dash="dash", color="grey")
        )
        
        # =========================
        # 5) VISUALIZATION 4: SCATTER PLOT WITH LEGEND
        # =========================
        fig4 = px.scatter(
            df,
            x="Strike",
            y="Volume",
            size="OpenInterest",
            color="LegendCategory",
            color_discrete_map=color_map,
            hover_data=["Expiration", "Volume", "OpenInterest", "Strike", "OptionType"],
            template="plotly_dark",
            title="Visualization 4: Scatter Plot with Unified Legend"
        )
        max_volume = df["Volume"].max()
        # Add a dashed grey vertical line at x = spot_price
        fig4.add_shape(
            type="line",
            xref="x",
            x0=spot_price,
            x1=spot_price,
            yref="y",
            y0=0,
            y1=max_volume,
            line=dict(dash="dash", color="grey")
        )
        
        # =========================
        # 6) SAVE THE VISUALIZATIONS AS HTML FILES
        # =========================
        # Dynamically name the output files based on the input filename
        output_file1 = OUTPUT_DIR / f"{csv_file.stem}_visualization1.html"
        output_file4 = OUTPUT_DIR / f"{csv_file.stem}_visualization4.html"
        
        fig1.write_html(str(output_file1))
        fig4.write_html(str(output_file4))
        
        print(f"Saved:\n  {output_file1}\n  {output_file4}")
