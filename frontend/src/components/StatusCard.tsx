import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { colors } from '../theme/theme';

interface StatusCardProps {
    title: string;
    value: string | number;
    label: string;
    color?: string;
    isAnomaly?: boolean;
    isSystemStatus?: boolean;
}

const StatusCard: React.FC<StatusCardProps> = ({
    title,
    value,
    label,
    color,
    isAnomaly = false,
    isSystemStatus = false
}) => {
    // Determine styles based on isSystemStatus
    const getBackground = () => {
        if (isSystemStatus) {
            // Glassy Green or Red
            return isAnomaly
                ? 'rgba(220, 20, 60, 0.85)' // Anomaly (Red)
                : 'rgba(16, 185, 129, 0.85)'; // Normal (Green)
        }
        // Glassy White for other cards
        return 'rgba(255, 255, 255, 0.6)';
    };

    const getTextColor = (defaultColor: string) => {
        if (isSystemStatus) return colors.text.white;
        return defaultColor;
    };

    const getBorder = () => {
        if (isSystemStatus) return '1px solid rgba(255, 255, 255, 0.3)';
        return isAnomaly
            ? `2px solid ${colors.primary.main}`
            : '1px solid rgba(255, 255, 255, 0.6)';
    };

    return (
        <Card
            sx={{
                height: '100%',
                background: getBackground(),
                backdropFilter: 'blur(12px)',
                WebkitBackdropFilter: 'blur(12px)', // Safari support
                border: getBorder(),
                boxShadow: isSystemStatus
                    ? '0 8px 32px 0 rgba(31, 38, 135, 0.15)'
                    : '0 8px 32px 0 rgba(31, 38, 135, 0.07)',
                position: 'relative',
                overflow: 'hidden',
                color: isSystemStatus ? colors.text.white : 'inherit',
                transition: 'transform 0.3s ease, box-shadow 0.3s ease',
                '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: '0 12px 40px 0 rgba(31, 38, 135, 0.15)',
                },
                '&::before': (isAnomaly && !isSystemStatus) ? {
                    content: '""',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    height: '5px',
                    background: colors.accent.redGradient,
                    animation: 'pulse 2s ease-in-out infinite',
                } : {},
            }}
        >
            <CardContent sx={{ padding: '1.5rem !important' }}>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    {/* Content */}
                    <Box sx={{ flex: 1 }}>
                        <Typography
                            variant="h6"
                            sx={{
                                color: getTextColor(colors.text.secondary),
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                mb: 0.5,
                                textTransform: 'uppercase',
                                letterSpacing: '0.05em',
                                opacity: isSystemStatus ? 0.9 : 1
                            }}
                        >
                            {title}
                        </Typography>

                        <Typography
                            variant="h4"
                            sx={{
                                color: getTextColor(color || colors.text.primary),
                                fontWeight: 800,
                                mb: 0.5,
                                fontSize: '1.75rem',
                            }}
                        >
                            {value}
                        </Typography>

                        <Typography
                            variant="body2"
                            sx={{
                                color: getTextColor(colors.text.secondary),
                                fontSize: '0.75rem',
                                fontWeight: 500,
                                opacity: isSystemStatus ? 0.9 : 1
                            }}
                        >
                            {label}
                        </Typography>
                    </Box>
                </Box>

                {/* Animated pulse for anomaly */}
                {isAnomaly && (
                    <Box
                        sx={{
                            position: 'absolute',
                            top: 16,
                            right: 16,
                            width: 14,
                            height: 14,
                            borderRadius: '50%',
                            backgroundColor: isSystemStatus ? colors.text.white : colors.primary.main,
                            animation: 'pulse 2s ease-in-out infinite',
                            boxShadow: isSystemStatus ? '0 0 10px rgba(255, 255, 255, 0.6)' : '0 0 10px rgba(220, 20, 60, 0.6)',
                        }}
                    />
                )}
            </CardContent>
        </Card>
    );
};

export default StatusCard;
