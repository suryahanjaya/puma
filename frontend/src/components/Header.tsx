import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { colors } from '../theme/theme';

interface HeaderProps {
    dbStatus: boolean;
    lastUpdate: string;
}

const Header: React.FC<HeaderProps> = ({ dbStatus, lastUpdate }) => {
    return (
        <Box
            sx={{
                background: colors.accent.redGradient,
                borderBottom: `4px solid ${colors.accent.gold}`,
                boxShadow: '0 4px 20px rgba(220, 20, 60, 0.25)',
                position: 'sticky',
                top: 0,
                zIndex: 1000,
            }}
        >
            <Box
                sx={{
                    maxWidth: '1400px',
                    margin: '0 auto',
                    padding: '1.25rem 2rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    gap: 2,
                }}
            >
                {/* Logo & Title */}
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2.5 }}>
                    {/* Logo PUMA */}
                    <Box
                        sx={{
                            width: 60,
                            height: 60,
                            borderRadius: '12px',
                            background: 'rgba(255, 255, 255, 0.95)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                            border: '2px solid rgba(255, 255, 255, 0.3)',
                            backdropFilter: 'blur(10px)',
                        }}
                    >
                        <svg width="40" height="40" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                            {/* Simple Drone Icon */}
                            <circle cx="50" cy="50" r="12" fill="#DC143C" />
                            {/* Propellers */}
                            <circle cx="25" cy="25" r="8" fill="#DC143C" opacity="0.7" />
                            <circle cx="75" cy="25" r="8" fill="#DC143C" opacity="0.7" />
                            <circle cx="25" cy="75" r="8" fill="#DC143C" opacity="0.7" />
                            <circle cx="75" cy="75" r="8" fill="#DC143C" opacity="0.7" />
                            {/* Arms */}
                            <line x1="50" y1="50" x2="25" y2="25" stroke="#DC143C" strokeWidth="3" />
                            <line x1="50" y1="50" x2="75" y2="25" stroke="#DC143C" strokeWidth="3" />
                            <line x1="50" y1="50" x2="25" y2="75" stroke="#DC143C" strokeWidth="3" />
                            <line x1="50" y1="50" x2="75" y2="75" stroke="#DC143C" strokeWidth="3" />
                        </svg>
                    </Box>

                    <Box>
                        <Typography
                            variant="h1"
                            sx={{
                                fontSize: '2.25rem',
                                fontWeight: 900,
                                color: colors.text.white,
                                letterSpacing: '0.1em',
                                textShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
                                mb: 0.5,
                            }}
                        >
                            PUMA
                        </Typography>
                        <Typography
                            variant="body2"
                            sx={{
                                color: 'rgba(255, 255, 255, 0.95)',
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                letterSpacing: '0.02em',
                            }}
                        >
                            Predictive UAV Monitoring & Anomaly Detection
                        </Typography>
                    </Box>
                </Box>

                {/* Status Info */}
                <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
                    {/* Database Status */}
                    <Chip
                        label={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <Box
                                    sx={{
                                        width: 8,
                                        height: 8,
                                        borderRadius: '50%',
                                        backgroundColor: dbStatus ? colors.status.normal : colors.status.anomaly,
                                        animation: dbStatus ? 'pulse 2s ease-in-out infinite' : 'none',
                                    }}
                                />
                                <Typography variant="body2" sx={{ fontWeight: 700 }}>
                                    Database {dbStatus ? 'Connected' : 'Disconnected'}
                                </Typography>
                            </Box>
                        }
                        sx={{
                            backgroundColor: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(10px)',
                            color: colors.text.primary,
                            fontWeight: 600,
                            padding: '0.5rem 1rem',
                            height: 'auto',
                            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                        }}
                    />

                    {/* Model Info */}
                    <Chip
                        label="LOF Novelty Model"
                        sx={{
                            backgroundColor: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(10px)',
                            color: colors.text.primary,
                            fontWeight: 700,
                            padding: '0.5rem 1rem',
                            height: 'auto',
                            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                        }}
                    />

                    {/* Last Update */}
                    <Chip
                        label={
                            <Box>
                                <Typography variant="caption" sx={{ fontSize: '0.7rem', opacity: 0.7 }}>
                                    Last Update
                                </Typography>
                                <Typography variant="body2" sx={{ fontWeight: 700 }}>
                                    {lastUpdate}
                                </Typography>
                            </Box>
                        }
                        sx={{
                            backgroundColor: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(10px)',
                            color: colors.text.primary,
                            padding: '0.5rem 1rem',
                            height: 'auto',
                            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                        }}
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default Header;
