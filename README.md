# 🗺️ Waste Management Optimizer

Waste Management Optimizer is a web application designed to plan and visualize optimized waste collection routes. It uses geospatial tools, real-time height data, and a sleek UI to support environmentally conscious waste disposal.

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
pip install  .
```

```env
ORS_API_KEY=your_openrouteservice_api_key
```

## Setting Up Detectro with Flask

This project integrates the Detectron2 object detection framework into a Flask web application for detecting dumpsites. If you're cloning this repository for the first time, follow the steps below to set up your environment.

### 4. Set up Detectron2

Detectron2 must be installed from source:

```bash
pip install git+https://github.com/facebookresearch/detectron2.git
```

Ensure your system meets the requirements for PyTorch and OpenCV.

### 5. Dataset and model setup

**Important Notes:**

- The trained model weights (`model_final.pth`) have been removed from the repository because they exceed GitHub’s 100MB file size limit.
- You will need to retrain the model or obtain the `output/model_final.pth` file separately.
- The dataset used for training has **not been uploaded** to this repository. Place your dataset in the appropriate directory (e.g., `./dataset/train/`) following COCO-style annotations or your custom format.

To train from the dataset you will need to run the train.py. This will create output/ folder in detectron and you will move it to the uppeer layer of the folder so that flask can easily access it

```bash
python train.py
```

Make sure all the images have the same widht and height

```bash
python resize.py

```

Edit the pathway inside resize if your data is somewhere else

### 6. Running the app

Ensure your `.env` file is configured correctly with your OpenRouteService API key.

Then, run the Flask application:

```bash
flask --app flaskr run --debug
```

---

(You can get a free ORS API key from [heigit.org](https://heigit.org))

### 5. Run the app

```bash
flask --app app run
```

Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 🔗 Useful Links

- [Leaflet.js Documentation](https://leafletjs.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
