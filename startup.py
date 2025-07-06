# startup.py

#from updater.metro_scraper import convert_dmrc_gtfs_to_metro_txt
from embedder import embed_food_data, embed_metro_data

def run_startup_pipeline():
    print("🚀 Running startup pipeline")

    # Step 1: Prepare metro.txt from GTFS files
   # convert_dmrc_gtfs_to_metro_txt()
    print("✅ Metro GTFS data converted.")

    # Step 2: Embed food.txt
    embed_food_data()
    print("✅ Food data embedded.")

    # Step 3: Embed metro.txt
    embed_metro_data()
    print("✅ Metro data embedded.")

    print("🎯 All steps completed successfully!")

if __name__ == "__main__":
    run_startup_pipeline()

