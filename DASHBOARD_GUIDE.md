# 🚀 PUMA Dashboard - Quick Start Guide

## Modern HTML Dashboard (Recommended)

### Step 1: Start the Data Producer
```bash
python src/uav_producer.py
```

### Step 2: Start the API Server
Open a **new terminal** and run:
```bash
python api_server.py
```

### Step 3: Open the Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

---

## Alternative: Streamlit Dashboard (Legacy)

### Start Streamlit
```bash
streamlit run app.py
```

Then open: `http://localhost:8501`

---

## 📊 Dashboard Features

### Modern HTML Dashboard
- ✨ **Beautiful Dark Theme** with glassmorphism effects
- 📈 **Real-time Charts** using Chart.js
- 🎯 **Live Status Cards** with animations
- 📋 **Interactive Data Table**
- 🔄 **Auto-refresh** every 1.5 seconds
- 📱 **Fully Responsive** design

### API Endpoints
- `GET /api/telemetry?limit=150` - Get latest telemetry with anomaly predictions
- `GET /api/stats` - Get dashboard statistics
- `GET /api/health` - Health check

---

## 🎨 Customization

### Change Refresh Rate
Edit `static/js/dashboard.js`:
```javascript
const CONFIG = {
    REFRESH_INTERVAL: 1500, // Change to your preferred interval (ms)
    ...
};
```

### Change History Limit
Use the dropdown in the dashboard or edit:
```javascript
DEFAULT_HISTORY_LIMIT: 150, // Change default value
```

---

## 🛠️ Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `api_server.py`:
```python
app.run(debug=True, port=5001, host='0.0.0.0')  # Change port
```

### Database Not Found
Make sure `uav_producer.py` is running first to create the database.

### Charts Not Loading
Check browser console (F12) for errors. Ensure Chart.js CDN is accessible.

---

## 📁 Project Structure

```
uav-mlops-dashboard/
├── dashboard.html          # Modern HTML dashboard
├── api_server.py          # Flask API backend
├── app.py                 # Streamlit dashboard (legacy)
├── static/
│   ├── css/
│   │   └── dashboard.css  # Styling
│   └── js/
│       └── dashboard.js   # Dashboard logic
├── src/
│   └── uav_producer.py    # Data generator
├── models/                # ML models
└── data/                  # Database & datasets
```

---

**Developed by Surya Hanjaya** 🚁
