# ♟️ Chess Meta Analyst (Nov 2025)

## Overview
A data engineering project that scrapes, processes, and visualizes chess opening trends across different Elo ratings on Chess.com. The goal is to identify the "Meta" strategies used at different skill levels, from Beginner (400 Elo) to Master (2000+ Elo).

## 📊 Results
![Heatmap](assets/example_heatmap.png)
*Figure 1: Percentage share of opening moves normalized by Elo range.*

## 🛠️ Architecture
The pipeline consists of three sequential modules:
1.  **The Collector (`chess.com_users_collector.py`):** Crawls matches to harvest active usernames (Graph Traversal).
2.  **The Scanner (`Oppenings_statistics_scanner.py`):** Fetches matches for harvest users, parses PGNs, and aggregates opening stats.
3.  **The Visualizer (`Oppenings_statistics_visualizer.py`):** Transforms raw CSV data into a normalized Seaborn Heatmap.

## 🚀 How to Run
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Harvest Users:**
    Run `src/chess.com_users_collector.py`. It will populate `data/players_lists_nov.txt`.
3.  **Fetch Stats:**
    Run `src/Oppenings_statistics_scanner.py`. It reads the list and generates `data/Oppenings_stats.csv`.
4.  **Generate Intelligence:**
    Run `src/Oppenings_statistics_visualizer.py`. It outputs the final Heatmap.

## 📈 Key Insights
* **The "Italian Game" Dominance:** Heavily favored by beginners (800-1200 Elo) but usage declines at master levels.
* **The "Sicilian" Curve:** Usage correlates positively with Elo, becoming the dominant response to e4 above 2000 Elo.

