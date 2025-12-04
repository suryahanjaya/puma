import React from 'react';
import {
    Box,
    Typography,
    Card,
    CardContent,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip,
} from '@mui/material';
import { colors } from '../theme/theme';
import type { UAVTelemetry } from '../types/uav';

interface TelemetryTableProps {
    data: UAVTelemetry[];
    anomalyCount: number;
    totalRecords: number;
}

const TelemetryTable: React.FC<TelemetryTableProps> = ({
    data,
    anomalyCount,
    totalRecords
}) => {
    const getStatusColor = (isAnomaly: boolean) => {
        return isAnomaly ? colors.status.anomaly : colors.status.normal;
    };

    const getStatusLabel = (isAnomaly: boolean) => {
        return isAnomaly ? 'ANOMALY' : 'NORMAL';
    };

    const formatTimestamp = (data: UAVTelemetry) => {
        // Gunakan field 'dt' jika tersedia, atau konversi timestamp Unix
        if (data.dt) {
            return new Date(data.dt).toLocaleString('id-ID', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
            });
        }
        return new Date(data.timestamp * 1000).toLocaleString('id-ID', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
        });
    };

    return (
        <Card>
            <CardContent>
                {/* Table Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h5" sx={{ fontWeight: 600, color: colors.text.primary }}>
                        Recent Telemetry Data
                    </Typography>

                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Chip
                            label={`Anomalies: ${anomalyCount}`}
                            sx={{
                                backgroundColor: `${colors.primary.main}30`,
                                color: colors.primary.light,
                                fontWeight: 600,
                                borderLeft: `3px solid ${colors.primary.main}`,
                            }}
                        />
                        <Chip
                            label={`Total: ${totalRecords} records`}
                            sx={{
                                backgroundColor: `${colors.status.info}30`,
                                color: colors.status.info,
                                fontWeight: 600,
                                borderLeft: `3px solid ${colors.status.info}`,
                            }}
                        />
                    </Box>
                </Box>

                {/* Table */}
                <TableContainer sx={{ maxHeight: 500 }}>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    Timestamp
                                </TableCell>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    Status
                                </TableCell>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    Anomaly Score
                                </TableCell>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    Altitude (m)
                                </TableCell>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    Battery (%)
                                </TableCell>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    Mode
                                </TableCell>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    System Status
                                </TableCell>
                                <TableCell sx={{
                                    backgroundColor: colors.background.paper,
                                    color: colors.text.primary,
                                    fontWeight: 700,
                                    borderBottom: `2px solid ${colors.primary.main}`,
                                }}>
                                    Event
                                </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.slice(0, 50).map((row, index) => (
                                <TableRow
                                    key={index}
                                    sx={{
                                        backgroundColor: row.is_anomaly
                                            ? `${colors.primary.main}10`
                                            : 'transparent',
                                        '&:hover': {
                                            backgroundColor: row.is_anomaly
                                                ? `${colors.primary.main}20`
                                                : 'rgba(255, 255, 255, 0.05)',
                                        },
                                        borderLeft: row.is_anomaly
                                            ? `3px solid ${colors.primary.main}`
                                            : '3px solid transparent',
                                    }}
                                >
                                    <TableCell sx={{ color: colors.text.secondary, fontSize: '0.875rem' }}>
                                        {formatTimestamp(row)}
                                    </TableCell>
                                    <TableCell>
                                        <Chip
                                            label={getStatusLabel(row.is_anomaly)}
                                            size="small"
                                            sx={{
                                                backgroundColor: `${getStatusColor(row.is_anomaly)}30`,
                                                color: getStatusColor(row.is_anomaly),
                                                fontWeight: 700,
                                                fontSize: '0.75rem',
                                            }}
                                        />
                                    </TableCell>
                                    <TableCell sx={{
                                        color: row.is_anomaly ? colors.primary.light : colors.text.secondary,
                                        fontWeight: row.is_anomaly ? 700 : 400,
                                    }}>
                                        {row.anomaly_score.toFixed(4)}
                                    </TableCell>
                                    <TableCell sx={{ color: colors.text.secondary }}>
                                        {row.altitude.toFixed(2)}
                                    </TableCell>
                                    <TableCell sx={{ color: colors.text.secondary }}>
                                        {row.battery_level.toFixed(1)}
                                    </TableCell>
                                    <TableCell sx={{ color: colors.text.secondary }}>
                                        {row.flight_mode}
                                    </TableCell>
                                    <TableCell sx={{ color: colors.text.secondary }}>
                                        {row.system_status}
                                    </TableCell>
                                    <TableCell sx={{ color: colors.text.secondary }}>
                                        {row.event}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </CardContent>
        </Card>
    );
};

export default TelemetryTable;
