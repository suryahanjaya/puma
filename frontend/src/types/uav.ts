// UAV Telemetry Data Types
export interface UAVTelemetry {
    timestamp: number;      // Unix timestamp (seconds)
    dt: string;            // Datetime string format: "YYYY/MM/DD HH:MM:SS"
    date: string;          // Date string format: "YYYY/MM/DD"
    altitude: number;
    battery_level: number;
    flight_mode: string;
    system_status: string;
    event: string;
    anomaly_score: number;
    is_anomaly: boolean;
}

// API Response Types
export interface TelemetryResponse {
    data: UAVTelemetry[];
    total: number;
    anomaly_count: number;
}

export interface LatestTelemetry {
    latest: UAVTelemetry;
    history: UAVTelemetry[];
}

export interface DatabaseStatus {
    status: string;
    connected: boolean;
    message?: string;
}

// Chart Data Types
export interface ChartDataPoint {
    timestamp: string;
    value: number;
}

export interface MetricsChartData {
    altitude: ChartDataPoint[];
    battery: ChartDataPoint[];
}
