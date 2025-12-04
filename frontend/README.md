# 🇮🇩 PUMA Dashboard - React + TypeScript Frontend

Modern UAV MLOps Dashboard dengan tema **Merah Putih Indonesia** 🚁

## 🎨 Features

- ✅ **React 18** + **TypeScript** untuk type safety
- ✅ **Vite** untuk development yang super cepat
- ✅ **Material-UI (MUI)** untuk UI components
- ✅ **Chart.js** untuk visualisasi data real-time
- ✅ **Axios** untuk API calls yang type-safe
- ✅ **Indonesia Red & White Theme** 🇮🇩
- ✅ **Auto-refresh** setiap 5 detik
- ✅ **Responsive Design** untuk semua device
- ✅ **Dark Mode** dengan aksen merah Indonesia

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Development Server
```bash
npm run dev
```

Dashboard akan berjalan di: **http://localhost:5173**

### 3. Build untuk Production
```bash
npm run build
```

## 🔧 Configuration

### API Backend URL
Edit file `src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:5000'; // Sesuaikan dengan backend Anda
```

### Theme Colors
Edit file `src/theme/theme.ts` untuk customize warna:
- Primary: Merah Indonesia (#DC143C)
- Secondary: Putih (#FFFFFF)
- Accent: Emas (#FFD700)

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Header.tsx       # Header dengan gradient merah
│   │   ├── StatusCard.tsx   # Card untuk status UAV
│   │   ├── AnomalyChart.tsx # Chart anomaly score
│   │   ├── MetricsChart.tsx # Chart altitude & battery
│   │   └── TelemetryTable.tsx # Tabel data telemetry
│   ├── services/            # API services
│   │   └── api.ts           # Axios API calls (type-safe)
│   ├── theme/               # MUI theme
│   │   └── theme.ts         # Indonesia red-white theme
│   ├── types/               # TypeScript types
│   │   └── uav.ts           # UAV data types
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── index.html               # HTML template
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript config
└── vite.config.ts           # Vite config
```

## 🎨 Design System

### Colors
- **Primary Red**: #DC143C (Merah Indonesia)
- **Light Red**: #FF4757
- **Dark Red**: #B91C1C
- **White**: #FFFFFF
- **Gold Accent**: #FFD700
- **Background**: #0F172A (Dark blue)
- **Paper**: #1E293B (Lighter dark)

### Typography
- Font Family: **Inter** (Google Fonts)
- Weights: 300, 400, 500, 600, 700, 800, 900

## 🔌 API Endpoints

Dashboard menggunakan endpoints berikut dari Python backend:

- `GET /telemetry/latest?history_limit=150` - Latest telemetry + history
- `GET /telemetry` - All telemetry data
- `GET /status` - Database status
- `GET /telemetry/anomalies` - Anomalies only

## 🛠️ Tech Stack

- **React 18** - UI Framework
- **TypeScript** - Type Safety
- **Vite** - Build Tool
- **Material-UI (MUI)** - UI Components
- **Chart.js** + **react-chartjs-2** - Data Visualization
- **Axios** - HTTP Client
- **Emotion** - CSS-in-JS (untuk MUI)

## 📊 Features Detail

### 1. Real-time Monitoring
- Auto-refresh setiap 5 detik
- Live update untuk semua metrics
- Timestamp real-time

### 2. Anomaly Detection Visualization
- Chart dengan gradient merah
- Highlight anomaly points dengan warna emas
- Tooltip dengan detail informasi

### 3. Flight Metrics
- Dual Y-axis chart (Altitude & Battery)
- Color-coded untuk mudah dibaca
- Smooth animations

### 4. Telemetry Table
- Sticky header
- Highlight anomaly rows dengan background merah
- Formatted Indonesian datetime
- Scrollable dengan max 50 rows visible

### 5. Status Cards
- Animated pulse untuk anomaly
- Color-coded status
- Icon-based untuk visual clarity

## 🎯 Development

### Run Development Server
```bash
npm run dev
```

### Type Checking
```bash
npm run type-check
```

### Lint Code
```bash
npm run lint
```

### Build Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 👨‍💻 Developer

**Surya Hanjaya**
- Dashboard dengan tema Indonesia 🇮🇩
- Modern React + TypeScript architecture
- Type-safe API integration

## 📝 License

Developed for UAV MLOps Project - UNESA

---

**PUMA Dashboard v2.0** - Powered by React + TypeScript + Vite 🚀
