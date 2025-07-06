# 🧠 LocalGPT-Delhi Assistant

A locally running intelligent assistant designed specifically for Delhi — providing contextual answers related to metro routes, food recommendations, and city navigation without relying on external APIs.

![Delhi Metro](https://img.shields.io/badge/Metro-Route%20Intelligence-blue) ![LocalGPT](https://img.shields.io/badge/Offline-GPT%20Powered-red) ![Made in India](https://img.shields.io/badge/Made%20in-India-orange)

---

## 🚀 Features

- 🗺️ **Offline Metro Route Intelligence**  
  Ask: “How to go from Dwarka to Kashmere Gate?”  
  → Returns optimal path, interchanges, line names using GTFS data parsing.

- 🍽️ **Delhi Food Suggestions**  
  Ask: “Best food in Karol Bagh?” or “Where to get momos near Hauz Khas?”  
  → Curated local food responses from scraped dataset.

- 🔌 **Runs Fully Locally**  
  No APIs, no internet — runs via Local LLM (LLaMA/Gemma) and ChromaDB.

- 🔄 **GTFS Integration**  
  Parsed official Delhi Metro transit data for real station-to-station routing.

---

## 🧰 Tech Stack

| Layer        | Tech Used              |
|--------------|------------------------|
| 💬 LLM       | Local LLaMA / Gemma (gguf) |
| 🧠 Embeddings | `InstructorXL` + `ChromaDB` |
| 🔍 Search     | Local vector search    |
| 📂 Data       | GTFS `stops.txt`, `routes.txt`, custom food.txt |
| 🖥️ Frontend  | Terminal CLI           |
| ⚙️ Backend   | Python (LangChain-style workflow) |

---

## 🛠️ Setup

1. **Clone repo**

``bash
git clone https://github.com/yuriverma/localgpt-delhi-assistant.git
cd localgpt-delhi-assistant

2. **Install dependencies**
   pip install -r requirements.txt
3. **Activate virtual environment (if not already)**
   source venv/bin/activate
4. **Startup pipeline**
   python3 startup.py
5. **Run Assistant**
   python3 app.py

## 📁 Directory Structure
localgpt-delhi-assistant/
│
├── app.py
├── startup.py
├── embedder.py
├── updater/
│   ├── generate_metro_routes.py
│   └── food_scraper.py (optional)
│
├── data/
│   ├── metro_gtfs/
│   │   ├── stops.txt
│   │   ├── routes.txt
│   │   ├── stop_times.txt
│   │   └── ...
│   ├── food.txt
│   ├── metro.txt (auto-generated)
│   └── metro_routes.txt (auto-generated)


## 🔮 Future Scope
# 📱 Voice Assistant Integration
Convert CLI into Jarvis-style voice bot with TTS/STT modules.

# 📍 Location-aware Routing
GPS integration to auto-detect source station.

# 🕐 Real-Time ETA
Use offline schedule from GTFS stop_times.txt to calculate next train times.

# 📊 Footfall-Based Recommendations
Suggest less-crowded routes or stations at a given time.

# 🧠 Continual Learning
Feedback loop to improve embeddings based on user corrections.

# 🌐 Web Interface
Add a Streamlit or React dashboard with map-based metro routing.

## 🤝 Contribution
Pull requests are welcome! If you'd like to add more cities or new modules (auto-rickshaw, DTC bus planner, etc.), feel free to fork and submit a PR.

## ⚠️ Disclaimer
This tool is made for educational and offline experimentation purposes. All GTFS data belongs to respective authorities (like DMRC), and no API is used in real-time.

## 🧔 Built by Yuri Verma





