# 🇮🇩 PUMA Dashboard - Setup Guide

## Panduan Lengkap Setup React + TypeScript Frontend dengan Tema Merah Putih Indonesia

---

## 📦 Prerequisites

Pastikan Anda sudah menginstall:
- **Node.js** (v18 atau lebih baru)
- **Python** (v3.8 atau lebih baru)
- **npm** atau **yarn**

---

## 🚀 Quick Start

### 1️⃣ Setup Backend (Python)

```bash
# Pastikan di root directory project
cd c:\Users\ASUS ZENBOOK\Desktop\UNESA\uav-mlops-dashboard

# Aktifkan virtual environment (jika ada)
.\venv\Scripts\activate

# Install dependencies (jika belum)
pip install -r requirements.txt

# Jalankan API server
python api_server.py
```

Backend akan running di: **http://localhost:5000**

### 2️⃣ Setup Frontend (React + TypeScript)

```bash
# Masuk ke folder frontend
cd frontend

# Install dependencies (sudah dilakukan)
npm install

# Jalankan development server
npm run dev
```

Frontend akan running di: **http://localhost:5173**

---

## 🎨 Fitur Dashboard

### ✨ Modern Features
- ✅ **React 18** + **TypeScript** untuk type safety
- ✅ **Vite** untuk development super cepat
- ✅ **Material-UI (MUI)** untuk UI components
- ✅ **Chart.js** untuk visualisasi real-time
- ✅ **Axios** untuk type-safe API calls
- ✅ **Auto-refresh** setiap 5 detik
- ✅ **Responsive Design** untuk semua device

### 🇮🇩 Indonesia Red & White Theme
- **Primary Color**: Merah Indonesia (#DC143C)
- **Secondary Color**: Putih (#FFFFFF)
- **Accent Color**: Emas (#FFD700)
- **Background**: Dark mode dengan gradient
- **Animations**: Pulse effect untuk anomaly detection

---

## 📁 Project Structure

```
uav-mlops-dashboard/
├── frontend/                    # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/         # React Components
│   │   │   ├── Header.tsx      # Header dengan gradient merah
│   │   │   ├── StatusCard.tsx  # Card untuk status UAV
│   │   │   ├── AnomalyChart.tsx # Chart anomaly score
│   │   │   ├── MetricsChart.tsx # Chart altitude & battery
│   │   │   └── TelemetryTable.tsx # Tabel data telemetry
│   │   ├── services/           # API Services
│   │   │   └── api.ts          # Type-safe API calls
│   │   ├── theme/              # MUI Theme
│   │   │   └── theme.ts        # Indonesia red-white theme
│   │   ├── types/              # TypeScript Types
│   │   │   └── uav.ts          # UAV data types
│   │   ├── App.tsx             # Main app component
│   │   ├── main.tsx            # Entry point
│   │   └── index.css           # Global styles
│   ├── index.html              # HTML template
│   ├── package.json            # Dependencies
│   ├── tsconfig.json           # TypeScript config
│   └── vite.config.ts          # Vite config
│
├── api_server.py               # Python Flask Backend
├── app.py                      # Main application
├── requirements.txt            # Python dependencies
├── data/                       # Database & data files
├── models/                     # ML models
└── src/                        # Python source code
```

---

## 🔌 API Endpoints

Backend menyediakan endpoints berikut:

### Main Endpoints (untuk React Frontend)
- `GET /telemetry/latest?history_limit=150` - Latest telemetry + history
- `GET /status` - Database connection status
- `GET /telemetry/anomalies` - Anomalies only

### Legacy Endpoints
- `GET /api/telemetry` - All telemetry data
- `GET /api/stats` - Dashboard statistics
- `GET /api/health` - Health check

---

## 🎯 Development Workflow

### Running Both Servers

**Terminal 1 - Backend:**
```bash
cd c:\Users\ASUS ZENBOOK\Desktop\UNESA\uav-mlops-dashboard
python api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd c:\Users\ASUS ZENBOOK\Desktop\UNESA\uav-mlops-dashboard\frontend
npm run dev
```

### Accessing the Dashboard

1. **Frontend (React)**: http://localhost:5173
2. **Backend API**: http://localhost:5000
3. **Old HTML Dashboard**: http://localhost:5000 (served by Flask)

---

## 🛠️ Customization

### Mengubah Warna Theme

Edit file `frontend/src/theme/theme.ts`:

```typescript
export const colors = {
  primary: {
    main: '#DC143C',      // Ubah warna merah
    light: '#FF4757',
    dark: '#B91C1C',
  },
  // ... dst
};
```

### Mengubah API URL

Edit file `frontend/src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:5000'; // Ubah sesuai backend
```

### Mengubah Auto-refresh Interval

Edit file `frontend/src/App.tsx`:

```typescript
// Auto-refresh every 5 seconds
useEffect(() => {
  const interval = setInterval(() => {
    fetchData();
  }, 5000); // Ubah nilai ini (dalam milliseconds)
  
  return () => clearInterval(interval);
}, [historyLimit]);
```

---

## 📊 Components Overview

### 1. Header Component
- Gradient merah Indonesia
- Database status indicator
- Model information
- Last update timestamp

### 2. Status Cards
- System status (Normal/Anomaly)
- Real-time timestamp
- Current altitude
- Battery level dengan color coding
- Flight mode

### 3. Anomaly Chart
- Line chart dengan gradient merah
- Highlighted anomaly points (gold color)
- Selectable history limit
- Smooth animations

### 4. Metrics Chart
- Dual Y-axis (Altitude & Battery)
- Color-coded lines
- Interactive tooltips

### 5. Telemetry Table
- Sticky header
- Anomaly highlighting
- Indonesian datetime format
- Scrollable dengan max 50 rows

---

## 🐛 Troubleshooting

### Frontend tidak bisa connect ke Backend

**Problem**: CORS error atau connection refused

**Solution**:
1. Pastikan backend running di port 5000
2. Check `api_server.py` sudah ada `CORS(app)`
3. Verify API_BASE_URL di `frontend/src/services/api.ts`

### TypeScript Errors

**Problem**: Type errors di IDE

**Solution**:
```bash
cd frontend
npm install
```

### Chart tidak muncul

**Problem**: Chart.js tidak ter-register

**Solution**: Sudah di-handle di `AnomalyChart.tsx` dan `MetricsChart.tsx` dengan `ChartJS.register()`

### Build Error

**Problem**: Build gagal

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 🚀 Production Build

### Build Frontend

```bash
cd frontend
npm run build
```

Output akan ada di folder `frontend/dist/`

### Serve Production Build

```bash
npm run preview
```

Atau integrate dengan Flask backend untuk serve static files.

---

## 📝 Notes

### Backend Tidak Diubah
- Backend Python (`api_server.py`) hanya ditambahkan 3 endpoints baru
- Semua fungsi existing tetap berjalan
- Database, models, dan logic tidak berubah

### Compatibility
- React 18
- TypeScript 5
- Vite 7
- Material-UI v6
- Chart.js v4

---

## 👨‍💻 Developer

**Surya Hanjaya**
- Modern React + TypeScript architecture
- Indonesia red-white theme design
- Type-safe API integration
- Real-time data visualization

---

## 📄 License

Developed for UAV MLOps Project - UNESA

---

**PUMA Dashboard v2.0** 🇮🇩
Powered by React + TypeScript + Vite 🚀
