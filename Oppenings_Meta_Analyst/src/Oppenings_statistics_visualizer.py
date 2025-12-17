import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
CSV_FILE = "Oppenings_stats.csv"

def generate_percentage_heatmap():
    print(f"Loading data from {CSV_FILE}...")
    
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"ERROR: {CSV_FILE} not found.")
        return

    # 1. PIVOT (Create Matrix)
    pivot_table = df.pivot_table(
        index="Opening_Name", 
        columns="Elo_Range", 
        values="Games_Count", 
        fill_value=0
    )
    # 2. SORT COLUMNS (Elo 0, 200, 400...)
    pivot_table = pivot_table.reindex(sorted(pivot_table.columns), axis=1)
    # 3. FILTER (Top 20 Most Popular)
    volume_series = pivot_table.sum(axis=1)
    top_openings = volume_series.sort_values(ascending=False).head(20).index
    pivot_table = pivot_table.loc[top_openings]
    # 4. CONVERT TO PERCENTAGE To normalize across Elo ratings
    pivot_table_pct = pivot_table.div(pivot_table.sum(axis=0), axis=1) * 100
    # 5. PLOTTING
    plt.figure(figsize=(16, 10))
    sns.set_context("notebook", font_scale=1.1)
    sns.heatmap(
        pivot_table_pct, 
        annot=True, 
        fmt=".1f",       # Shows 1 decimal place (e.g., 15.2%)
        cmap="magma_r",  # Hot color map
        linewidths=.5, 
        linecolor='black',
        vmin=0, vmax=30  # Cap colors at 30% to make smaller openings visible
    )
    # 6. LABELS
    plt.title("Chess Opening Meta by Elo (Percentage Share)", fontsize=18, weight='bold', pad=20)
    plt.xlabel("Elo Rating", fontsize=14, weight='bold')
    plt.ylabel("Opening Strategy", fontsize=14, weight='bold')
    plt.xticks(rotation=45)

    # 7. SAVE
    output_file = "Chess_Meta_Heatmap_PCT.png"
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Percentage Map generated: {output_file}")
    plt.show()

generate_percentage_heatmap()