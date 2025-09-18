import os
import pandas as pd
import matplotlib.pyplot as plt
from pipelines.fred.ingestion import fetch_series

# Get series from input (manual or GitHub Actions)
series_input = input("Enter comma-separated FRED series IDs (e.g., UMCSENT,GDPC1,CPIAUCSL): ")
series_list = [s.strip() for s in series_input.split(",")]

# Use environment variable if available, otherwise hardcode public key
api_key = os.getenv("FRED_API_KEY", "a6bd75c0ecd1b95bfdc5c3b9f5a97f6e")

# Create output folders
os.makedirs("outputs/excel", exist_ok=True)
os.makedirs("outputs/plots", exist_ok=True)

for series_id in series_list:
    df = fetch_series(
        series_id=series_id,
        start_date="2020-01-01",
        end_date="2023-12-31",
        frequency='M',
        api_key=api_key
    )

    # Save Excel
    excel_path = f"outputs/excel/{series_id}.xlsx"
    df.to_excel(excel_path, index=False)

    # Plot
    plt.figure(figsize=(10,5))
    plt.plot(df["date"], df[series_id], marker='o')
    plt.title(f"{series_id} from FRED")
    plt.xlabel("Date")
    plt.ylabel(series_id)
    plt.grid(True)
    plt.tight_layout()
    
    plot_path = f"outputs/plots/{series_id}.png"
    plt.savefig(plot_path)
    plt.close()
    
    print(f"✅ {series_id} Excel and plot generated successfully!")
