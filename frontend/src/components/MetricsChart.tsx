import React from 'react';
import { Box, Typography, Card, CardContent, Chip } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { colors } from '../theme/theme';
import type { UAVTelemetry } from '../types/uav';

interface MetricsChartProps {
    data: UAVTelemetry[];
}

const MetricsChart: React.FC<MetricsChartProps> = ({ data }) => {
    // Prepare chart data
    const chartData = {
        labels: data.map(d => d.dt ? new Date(d.dt).toLocaleTimeString('id-ID') : new Date(d.timestamp * 1000).toLocaleTimeString('id-ID')),
        datasets: [
            {
                label: 'Altitude (m)',
                data: data.map(d => d.altitude),
                borderColor: colors.status.info,
                backgroundColor: `${colors.status.info}20`,
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                fill: true,
                tension: 0.4,
                yAxisID: 'y',
            },
            {
                label: 'Battery (%)',
                data: data.map(d => d.battery_level),
                borderColor: colors.status.normal,
                backgroundColor: `${colors.status.normal}20`,
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                fill: true,
                tension: 0.4,
                yAxisID: 'y1',
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index' as const,
            intersect: false,
        },
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
                type: 'linear' as const,
                display: true,
                position: 'left' as const,
                min: 0, // Start from 0
                grid: {
                    color: 'rgba(59, 130, 246, 0.1)',
                },
                ticks: {
                    color: colors.status.info,
                },
                title: {
                    display: true,
                    text: 'Altitude (m)',
                    color: colors.status.info,
                },
            },
            y1: {
                type: 'linear' as const,
                display: true,
                position: 'right' as const,
                min: 0,
                max: 100,
                grid: {
                    drawOnChartArea: false,
                },
                ticks: {
                    color: colors.status.normal,
                },
                title: {
                    display: true,
                    text: 'Battery (%)',
                    color: colors.status.normal,
                },
            },
        },
    };

    return (
        <Card>
            <CardContent>
                {/* Chart Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h5" sx={{ fontWeight: 600, color: colors.text.primary }}>
                        Flight Metrics
                    </Typography>

                    {/* Legend */}
                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Chip
                            label="Altitude"
                            size="small"
                            sx={{
                                backgroundColor: `${colors.status.info}30`,
                                color: colors.status.info,
                                borderLeft: `3px solid ${colors.status.info}`,
                                fontWeight: 600,
                            }}
                        />
                        <Chip
                            label="Battery"
                            size="small"
                            sx={{
                                backgroundColor: `${colors.status.normal}30`,
                                color: colors.status.normal,
                                borderLeft: `3px solid ${colors.status.normal}`,
                                fontWeight: 600,
                            }}
                        />
                    </Box>
                </Box>

                {/* Chart */}
                <Box sx={{ height: 350 }}>
                    <Line data={chartData} options={options} />
                </Box>
            </CardContent>
        </Card>
    );
};

export default MetricsChart;
