from pathlib import Path
import re
import numpy as np
import pandas as pd

# ==========================================
# 1. CONFIGURATION & FILE PATHS
# ==========================================
DATA_DIR = Path(r"DIR")
INPUT_FILE = DATA_DIR / "vgchartz-2024.csv"
OUTPUT_FILE = DATA_DIR / "games_final.csv"

# ==========================================
# 2. PLATFORM METADATA REFERENCE
# ==========================================
PLATFORM_METADATA = {
    # Platform: (Full Name, Manufacturer, Form Factor, Is_Handheld)
    "2600": ("Atari 2600", "Atari", "Home Console", False),
    "5200": ("Atari 5200", "Atari", "Home Console", False),
    "7800": ("Atari 7800", "Atari", "Home Console", False),
    "3DO": ("3DO Interactive Multiplayer", "3DO Company", "Home Console", False),
    "3DS": ("Nintendo 3DS", "Nintendo", "Handheld", True),
    "Aco": ("Acorn Archimedes / Electron", "Acorn", "Computer / PC", False),
    "ACPC": ("Amstrad CPC", "Amstrad", "Computer / PC", False),
    "AJ": ("Atari Jaguar", "Atari", "Home Console", False),
    "All": ("All Platforms", "Aggregate", "Aggregate", False),
    "Amig": ("Commodore Amiga", "Commodore", "Computer / PC", False),
    "And": ("Android", "Google", "Mobile / Smart Device", True),
    "ApII": ("Apple II", "Apple", "Computer / PC", False),
    "Arc": ("Arcade Cabinet", "Arcade", "Arcade Machine", False),
    "AST": ("Atari ST", "Atari", "Computer / PC", False),
    "BBCM": ("BBC Micro", "Acorn / BBC", "Computer / PC", False),
    "BRW": ("Browser Game", "Web", "Computer / PC", False),
    "C128": ("Commodore 128", "Commodore", "Computer / PC", False),
    "C64": ("Commodore 64", "Commodore", "Computer / PC", False),
    "CD32": ("Amiga CD32", "Commodore", "Home Console", False),
    "CDi": ("Philips CD-i", "Philips", "Home Console", False),
    "CV": ("ColecoVision", "Coleco", "Home Console", False),
    "DC": ("Sega Dreamcast", "Sega", "Home Console", False),
    "DS": ("Nintendo DS", "Nintendo", "Handheld", True),
    "DSi": ("Nintendo DSi", "Nintendo", "Handheld", True),
    "DSiW": ("Nintendo DSiWare", "Nintendo", "Handheld", True),
    "FDS": ("Famicom Disk System", "Nintendo", "Home Console", False),
    "FMT": ("FM Towns / Marty", "Fujitsu", "Computer / PC", False),
    "GB": ("Game Boy", "Nintendo", "Handheld", True),
    "GBA": ("Game Boy Advance", "Nintendo", "Handheld", True),
    "GBC": ("Game Boy Color", "Nintendo", "Handheld", True),
    "GC": ("Nintendo GameCube", "Nintendo", "Home Console", False),
    "GEN": ("Sega Genesis / Mega Drive", "Sega", "Home Console", False),
    "GG": ("Sega Game Gear", "Sega", "Handheld", True),
    "GIZ": ("Gizmondo", "Tiger Telematics", "Handheld", True),
    "Int": ("Intellivision", "Mattel", "Home Console", False),
    "iOS": ("Apple iOS", "Apple", "Mobile / Smart Device", True),
    "iQue": ("iQue Player", "Nintendo", "Home Console", False),
    "Linux": ("Linux", "Open Source", "Computer / PC", False),
    "Lynx": ("Atari Lynx", "Atari", "Handheld", True),
    "Mob": ("Mobile (Generic/J2ME)", "Generic Mobile", "Mobile / Smart Device", True),
    "MS": ("Sega Master System", "Sega", "Home Console", False),
    "MSD": ("MS-DOS", "Microsoft", "Computer / PC", False),
    "MSX": ("MSX", "MSX Group", "Computer / PC", False),
    "N64": ("Nintendo 64", "Nintendo", "Home Console", False),
    "NES": ("Nintendo Entertainment System", "Nintendo", "Home Console", False),
    "NG": ("Neo Geo (AES / MVS)", "SNK", "Home Console", False),
    "NGage": ("Nokia N-Gage", "Nokia", "Handheld", True),
    "NS": ("Nintendo Switch", "Nintendo", "Hybrid", True),
    "OR": ("Oculus Rift / VR", "Oculus / Meta", "VR Headset", False),
    "OSX": ("macOS", "Apple", "Computer / PC", False),
    "Ouya": ("Ouya", "Ouya Inc.", "Home Console", False),
    "PC": ("Personal Computer (Windows)", "PC / Windows", "Computer / PC", False),
    "PCE": ("PC Engine / TurboGrafx-16", "NEC / Hudson", "Home Console", False),
    "PCFX": ("PC-FX", "NEC", "Home Console", False),
    "PS": ("PlayStation (PS1)", "Sony", "Home Console", False),
    "PS2": ("PlayStation 2", "Sony", "Home Console", False),
    "PS3": ("PlayStation 3", "Sony", "Home Console", False),
    "PS4": ("PlayStation 4", "Sony", "Home Console", False),
    "PS5": ("PlayStation 5", "Sony", "Home Console", False),
    "PSN": ("PlayStation Network", "Sony", "Home Console", False),
    "PSP": ("PlayStation Portable", "Sony", "Handheld", True),
    "PSV": ("PlayStation Vita", "Sony", "Handheld", True),
    "S32X": ("Sega 32X", "Sega", "Home Console", False),
    "SAT": ("Sega Saturn", "Sega", "Home Console", False),
    "SCD": ("Sega CD", "Sega", "Home Console", False),
    "Series": ("Xbox Series X/S", "Microsoft", "Home Console", False),
    "SNES": ("Super Nintendo Entertainment System", "Nintendo", "Home Console", False),
    "TG16": ("TurboGrafx-16", "NEC / Hudson", "Home Console", False),
    "VB": ("Virtual Boy", "Nintendo", "Handheld", True),
    "VC": ("Virtual Console", "Nintendo", "Home Console", False),
    "Wii": ("Nintendo Wii", "Nintendo", "Home Console", False),
    "WiiU": ("Nintendo Wii U", "Nintendo", "Home Console", False),
    "WinP": ("Windows Phone", "Microsoft", "Mobile / Smart Device", True),
    "WS": ("WonderSwan", "Bandai", "Handheld", True),
    "WW": ("WiiWare", "Nintendo", "Home Console", False),
    "X360": ("Xbox 360", "Microsoft", "Home Console", False),
    "XB": ("Xbox", "Microsoft", "Home Console", False),
    "XBL": ("Xbox Live Arcade", "Microsoft", "Home Console", False),
    "XOne": ("Xbox One", "Microsoft", "Home Console", False),
    "XS": ("Xbox Series X/S", "Microsoft", "Home Console", False),
    "ZXS": ("ZX Spectrum", "Sinclair", "Computer / PC", False),
}

# ==========================================
# 3. TRANSFORMATION FUNCTIONS
# ==========================================
def load_and_filter_sales(filepath: Path) -> pd.DataFrame:
    """Loads CSV and removes records without total_sales."""
    df = pd.read_csv(filepath)
    return df.dropna(subset=["total_sales"]).copy()


def calculate_decades(df: pd.DataFrame) -> pd.DataFrame:
    """Parses timestamps with fallback and computes 2-digit decade strings."""
    release_dt = pd.to_datetime(df["release_date"], errors="coerce")
    update_dt = pd.to_datetime(df["last_update"], errors="coerce")
    target_dt = release_dt.fillna(update_dt)

    years = target_dt.dt.year
    # Compute decades (e.g., 1984 -> 80s, 2005 -> 00s)
    decades = ((years % 100) // 10 * 10).astype("Int64").astype(str).str.zfill(2) + "s"

    df["decade"] = decades
    return df[df["decade"] != "<NA>s"].copy()


def normalize_titles(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts franchise base title by stripping subtitles and sequel digits."""
    df["base_title"] = (
        df["title"]
        .astype(str)
        .str.split(r"[:\-\–]")
        .str[0]
        .str.replace(r"\s+[0-9IVXLCDM]+$", "", regex=True)
        .str.strip()
    )
    return df


def enrich_metadata(df: pd.DataFrame, platform_col: str = "console") -> pd.DataFrame:
    """Merges console dimension metadata into the games dataset."""
    ref_df = (
        pd.DataFrame.from_dict(
            PLATFORM_METADATA,
            orient="index",
            columns=["Platform_Full_Name", "Manufacturer", "Form_Factor", "Is_Handheld"],
        )
        .reset_index()
        .rename(columns={"index": platform_col})
    )
    return df.merge(ref_df, on=platform_col, how="left")


def print_decade_benchmarks(df: pd.DataFrame) -> None:
    """Prints diagnostic top records per decade for critic score and sales."""
    print("\n" + "=" * 40)
    print("RECORD COUNT BY DECADE:")
    print("=" * 40)
    print(df["decade"].value_counts().sort_index())

    with pd.option_context("display.max_columns", None, "display.width", 1000):
        # Top Critic Score
        valid_critic = df.dropna(subset=["decade", "critic_score"])
        if not valid_critic.empty:
            idx_critic = valid_critic.groupby("decade")["critic_score"].idxmax()
            print("\n=== HIGHEST CRITIC SCORE PER DECADE ===")
            print(valid_critic.loc[idx_critic, ["decade", "title", "console", "critic_score", "total_sales"]])

        # Top Sales
        valid_sales = df.dropna(subset=["decade", "total_sales"])
        if not valid_sales.empty:
            idx_sales = valid_sales.groupby("decade")["total_sales"].idxmax()
            print("\n=== HIGHEST TOTAL SALES PER DECADE ===")
            print(valid_sales.loc[idx_sales, ["decade", "title", "console", "total_sales", "critic_score"]])
    print("=" * 40 + "\n")


# ==========================================
# 4. MAIN EXECUTION ROUTINE
# ==========================================
def main():
    print(f"Loading data from: {INPUT_FILE}")
    df = load_and_filter_sales(INPUT_FILE)
    df = calculate_decades(df)
    df = normalize_titles(df)
    df_final = enrich_metadata(df, platform_col="console")

    print_decade_benchmarks(df_final)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"Successfully processed {len(df_final):,} rows.")
    print(f"Exported to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()