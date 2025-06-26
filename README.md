# 🗺️ Waste Management Optimizer

Waste Management Optimizer is a web application designed to plan and visualize optimized waste collection routes. It uses geospatial tools, real-time height data, and a sleek UI to support environmentally conscious waste disposal.

[Mobile-app Guide](./EcoFriendlyApp/README.md)

## 🚀 Features

- Optimized multi-point routing using OpenRouteService
- Interactive maps powered by Leaflet.js
- Elevation-aware route planning using Height API
- Distance and time estimation
- Simple authentication (login/register)
- Clean TailwindCSS-based UI

## 🛠️ Technologies Used

| Layer      | Technology                                        |
| ---------- | ------------------------------------------------- |
| Frontend   | HTML, TailwindCSS, Leaflet.js                     |
| Backend    | Flask (Python)                                    |
| APIs       | OpenRouteService API, Open-Elevation / Height API |
| Mapping    | OpenStreetMap (via Leaflet tiles)                 |
| Templating | Jinja2                                            |
| Auth       | Flask Sessions, simple username-based login       |

## 🧰 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/mtendekuyokwa19/gaiathon.git
cd waste-optimizer
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure `requirements.txt` includes packages like:

```text
flask
requests
jinja2
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
ORS_API_KEY=your_openrouteservice_api_key
```

(You can get a free ORS API key from [heigit.org](https://heigit.org))

### 5. Run the app

```bash
flask --app app run
```

Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 🔗 Useful Links

- [Leaflet.js Documentation](https://leafletjs.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
