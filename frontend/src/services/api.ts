import axios from 'axios';
import type {
    UAVTelemetry,
    TelemetryResponse,
    LatestTelemetry,
    DatabaseStatus
} from '../types/uav';

// API Base URL - sesuaikan dengan backend Python Anda
const API_BASE_URL = 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// API Service Functions
export const uavApi = {
    // Get all telemetry data
    getAllTelemetry: async (limit?: number): Promise<TelemetryResponse> => {
        const params = limit ? { limit } : {};
        const response = await api.get<TelemetryResponse>('/telemetry', { params });
        return response.data;
    },

    // Get latest telemetry
    getLatestTelemetry: async (historyLimit: number = 150): Promise<LatestTelemetry> => {
        const response = await api.get<LatestTelemetry>('/telemetry/latest', {
            params: { history_limit: historyLimit }
        });
        return response.data;
    },

    // Get database status
    getDatabaseStatus: async (): Promise<DatabaseStatus> => {
        const response = await api.get<DatabaseStatus>('/status');
        return response.data;
    },

    // Get anomalies only
    getAnomalies: async (): Promise<UAVTelemetry[]> => {
        const response = await api.get<UAVTelemetry[]>('/telemetry/anomalies');
        return response.data;
    },
};

export default api;
