import React from 'react';
import { Box, Typography, FormControl, Select, MenuItem, Card, CardContent } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { colors } from '../theme/theme';
import type { UAVTelemetry } from '../types/uav';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

interface AnomalyChartProps {
    data: UAVTelemetry[];
    historyLimit: number;
    onHistoryLimitChange: (limit: number) => void;
}

const AnomalyChart: React.FC<AnomalyChartProps> = ({
    data,
    historyLimit,
    onHistoryLimitChange
}) => {
    // Prepare chart data
    const chartData = {
        labels: data.map(d => d.dt ? new Date(d.dt).toLocaleTimeString('id-ID') : new Date(d.timestamp * 1000).toLocaleTimeString('id-ID')),
        datasets: [
            {
                label: 'Anomaly Score',
                data: data.map(d => d.anomaly_score),
                borderColor: colors.primary.main,
                backgroundColor: (context: any) => {
                    const ctx = context.chart.ctx;
                    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
                    gradient.addColorStop(0, `${colors.primary.main}40`);
                    gradient.addColorStop(1, `${colors.primary.main}00`);
                    return gradient;
                },
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: (context: any) => {
                    return data[context.dataIndex]?.is_anomaly ? 6 : 2;
                },
                pointBackgroundColor: (context: any) => {
                    return data[context.dataIndex]?.is_anomaly
                        ? colors.accent.gold
                        : colors.primary.main;
                },
                pointBorderColor: colors.secondary.main,
                pointBorderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                backgroundColor: colors.background.paper,
                titleColor: colors.text.primary,
                bodyColor: colors.text.secondary,
                borderColor: colors.primary.main,
                borderWidth: 1,
                padding: 12,
                displayColors: false,
                callbacks: {
                    label: (context: any) => {
                        const isAnomaly = data[context.dataIndex]?.is_anomaly;
                        return [
                            `Score: ${context.parsed.y.toFixed(4)}`,
                            isAnomaly ? '⚠️ ANOMALY DETECTED' : '✓ Normal',
                        ];
                    },
                },
            },
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(220, 20, 60, 0.1)',
                },
                ticks: {
                    color: colors.text.secondary,
                    maxRotation: 45,
                    minRotation: 45,
                },
            },
            y: {
                grid: {
                    color: 'rgba(220, 20, 60, 0.1)',
                },
                ticks: {
                    color: colors.text.secondary,
                },
            },
        },
    };

    return (
        <Card>
            <CardContent>
                {/* Chart Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="h5" sx={{ fontWeight: 600, color: colors.text.primary }}>
                            📊 Anomaly Score Timeline
                        </Typography>
                    </Box>

                    <FormControl size="small">
                        <Select
                            value={historyLimit}
                            onChange={(e) => onHistoryLimitChange(Number(e.target.value))}
                            sx={{
                                color: colors.text.primary,
                                '.MuiOutlinedInput-notchedOutline': {
                                    borderColor: colors.primary.main,
                                },
                                '&:hover .MuiOutlinedInput-notchedOutline': {
                                    borderColor: colors.primary.light,
                                },
                            }}
                        >
                            <MenuItem value={50}>Last 50 points</MenuItem>
                            <MenuItem value={100}>Last 100 points</MenuItem>
                            <MenuItem value={150}>Last 150 points</MenuItem>
                            <MenuItem value={300}>Last 300 points</MenuItem>
                        </Select>
                    </FormControl>
                </Box>

                {/* Chart */}
                <Box sx={{ height: 350 }}>
                    <Line data={chartData} options={options} />
                </Box>
            </CardContent>
        </Card>
    );
};

export default AnomalyChart;
