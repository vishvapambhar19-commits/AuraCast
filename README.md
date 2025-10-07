<div align="center">
  <br />
  <h1>✨ AuraCast ✨</h1>
  <p>
    <b>A predictive air quality monitoring platform for North America, powered by NASA data.</b>
  </p>
  <br />

</div>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-black?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript&logoColor=white" alt="JavaScript">
  <img src="https://img.shields.io/badge/Deployment-Render-46E3B7?logo=render&logoColor=white" alt="Render">
</div>

## 🚀 Live Demo

> ## [**Click Here to Launch the Live AuraCast Application**](https://auracast.onrender.com)
>
> *(Note: The free backend may take 30-50 seconds to "wake up" on the first visit.)*

---

### The Problem

Outdoor air pollution is a major global health risk, yet real-time atmospheric data is often complex, fragmented, and difficult for the public to interpret. This creates a critical gap between available scientific data and the public's ability to make informed, daily decisions to protect their health.

### Our Solution: AuraCast

AuraCast is a full-stack web application that bridges this gap. It ingests, processes, and visualizes complex environmental data, transforming it into an intuitive and actionable tool. It provides both real-time monitoring and, crucially, a **predictive 24-hour forecast** to help users plan ahead.

### 🔑 Key Features

* 🛰️ **Multi-Source Data Integration:** Fuses satellite data from **NASA's TEMPO mission** with ground-based measurements from **AirNow** and weather data from **Open-Meteo**.
* 🔮 **Predictive 24-Hour Forecast:** Implements a weather-based heuristic model to predict how air quality will change over the next 24 hours based on wind, rain, and temperature forecasts.
* 🧠 **AI-Powered Health Insights:** Leverages the **Google Gemini API** to translate raw numbers into simple, conversational health advice and explanations about pollutants.
* 🗺️ **Dynamic & Interactive UI:** Features a live map (Leaflet.js), animated forecast charts (Chart.js), and a modern "glassmorphism" design for an engaging user experience.

### 💡 What Makes AuraCast Innovative?

1.  **Data Synthesis:** AuraCast doesn't just display data; it creates a more reliable picture by fusing high-altitude satellite data with on-the-ground measurements, providing a more complete and validated view of air quality.
2.  **Accessible Prediction:** Instead of relying on complex meteorological models, we developed a simple but effective rule-based prediction engine. This innovative approach makes forecasting accessible and demonstrates a practical method for turning weather data into public health insights.
3.  **Human-Centered AI:** We use Generative AI not as a gimmick, but as a "translator" to bridge the gap between scientific data and personal health, making the information meaningful and actionable for everyone.

### ⚙️ Technology & Data Flow

AuraCast uses a modern full-stack architecture. The data flows from official sources, through our Python backend for processing, to the user's browser for visualization.

**Frontend** `(HTML, CSS, JS)` ↔️ **Backend API** `(Python, Flask)` ↔️ **External APIs** `(NASA, AirNow, Google Gemini)`

### 🛠️ Local Setup

To run this project locally, clone the repository, create a Python virtual environment, and install the dependencies from `backend/requirements.txt`. Set up your API keys in a `.env` file within the `backend` folder and run the Flask server.
