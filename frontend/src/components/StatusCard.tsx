import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { colors } from '../theme/theme';

interface StatusCardProps {
    icon: string;
    title: string;
    value: string | number;
    label: string;
    color?: string;
    isAnomaly?: boolean;
}

const StatusCard: React.FC<StatusCardProps> = ({
    icon,
    title,
    value,
    label,
    color,
    isAnomaly = false
}) => {
    return (
        <Card
            sx={{
                height: '100%',
                background: isAnomaly
                    ? `linear-gradient(135deg, ${colors.accent.lightRed} 0%, ${colors.background.light} 100%)`
                    : colors.background.light,
                border: isAnomaly
                    ? `3px solid ${colors.primary.main}`
                    : `2px solid ${colors.border.light}`,
                position: 'relative',
                overflow: 'hidden',
                '&::before': isAnomaly ? {
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
                    {/* Icon */}
                    <Box
                        sx={{
                            fontSize: '2.5rem',
                            lineHeight: 1,
                            filter: isAnomaly ? 'drop-shadow(0 0 8px rgba(220, 20, 60, 0.5))' : 'none',
                            animation: isAnomaly ? 'pulse 2s ease-in-out infinite' : 'none',
                        }}
                    >
                        {icon}
                    </Box>

                    {/* Content */}
                    <Box sx={{ flex: 1 }}>
                        <Typography
                            variant="h6"
                            sx={{
                                color: colors.text.secondary,
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                mb: 0.5,
                                textTransform: 'uppercase',
                                letterSpacing: '0.05em',
                            }}
                        >
                            {title}
                        </Typography>

                        <Typography
                            variant="h4"
                            sx={{
                                color: color || colors.text.primary,
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
                                color: colors.text.secondary,
                                fontSize: '0.75rem',
                                fontWeight: 500,
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
                            backgroundColor: colors.primary.main,
                            animation: 'pulse 2s ease-in-out infinite',
                            boxShadow: '0 0 10px rgba(220, 20, 60, 0.6)',
                        }}
                    />
                )}
            </CardContent>
        </Card>
    );
};

export default StatusCard;
