import { createTheme } from '@mui/material/styles';

// Indonesia Red & White Theme Colors - LIGHT MODE (Putih dominan!)
export const colors = {
    // Primary - Merah Indonesia
    primary: {
        main: '#DC143C',      // Merah Indonesia (Crimson Red)
        light: '#FF4757',     // Merah Terang
        dark: '#B91C1C',      // Merah Gelap
        contrastText: '#FFFFFF',
    },

    // Secondary - Putih Indonesia
    secondary: {
        main: '#FFFFFF',      // Putih
        light: '#F9FAFB',     // Off-white
        dark: '#E5E7EB',      // Abu-abu terang
        contrastText: '#DC143C',
    },

    // Accent Colors
    accent: {
        gold: '#FFD700',      // Emas (untuk highlights)
        darkRed: '#8B0000',   // Merah Tua
        lightRed: '#FFE5E5',  // Merah Muda Terang
        redGradient: 'linear-gradient(135deg, #DC143C 0%, #B91C1C 100%)',
    },

    // Status Colors
    status: {
        normal: '#10B981',    // Hijau (Normal)
        warning: '#F59E0B',   // Kuning (Warning)
        anomaly: '#DC143C',   // Merah Indonesia (Anomaly)
        info: '#3B82F6',      // Biru (Info)
    },

    // Background - PUTIH!
    background: {
        default: '#FFFFFF',   // Putih murni
        paper: '#FFFFFF',     // Putih murni
        light: '#F9FAFB',     // Off-white untuk cards
        gradient: 'linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%)',
        redStripe: 'linear-gradient(180deg, #DC143C 0%, #DC143C 50%, #FFFFFF 50%, #FFFFFF 100%)', // Bendera Indonesia
    },

    // Text - GELAP untuk kontras di background putih
    text: {
        primary: '#1F2937',   // Hitam/abu gelap
        secondary: '#6B7280', // Abu-abu
        disabled: '#9CA3AF',  // Abu-abu terang
        white: '#FFFFFF',     // Putih untuk text di background merah
    },

    // Borders
    border: {
        light: '#E5E7EB',
        main: '#D1D5DB',
        red: '#DC143C',
    },
};

// Create MUI Theme with Indonesia Colors - LIGHT MODE
export const theme = createTheme({
    palette: {
        mode: 'light',  // LIGHT MODE!
        primary: {
            main: colors.primary.main,
            light: colors.primary.light,
            dark: colors.primary.dark,
            contrastText: colors.primary.contrastText,
        },
        secondary: {
            main: colors.secondary.main,
            light: colors.secondary.light,
            dark: colors.secondary.dark,
            contrastText: colors.secondary.contrastText,
        },
        background: {
            default: colors.background.default,
            paper: colors.background.paper,
        },
        text: {
            primary: colors.text.primary,
            secondary: colors.text.secondary,
            disabled: colors.text.disabled,
        },
        success: {
            main: colors.status.normal,
        },
        warning: {
            main: colors.status.warning,
        },
        error: {
            main: colors.status.anomaly,
        },
        info: {
            main: colors.status.info,
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontSize: '2.5rem',
            fontWeight: 800,
            letterSpacing: '-0.02em',
            color: colors.primary.main,
        },
        h2: {
            fontSize: '2rem',
            fontWeight: 700,
            letterSpacing: '-0.01em',
        },
        h3: {
            fontSize: '1.5rem',
            fontWeight: 600,
        },
        h4: {
            fontSize: '1.25rem',
            fontWeight: 600,
        },
        h5: {
            fontSize: '1.125rem',
            fontWeight: 600,
        },
        h6: {
            fontSize: '1rem',
            fontWeight: 500,
        },
    },
    shape: {
        borderRadius: 12,
    },
    components: {
        MuiCard: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                    backgroundColor: colors.background.light,
                    border: `2px solid ${colors.border.light}`,
                    boxShadow: '0 2px 8px rgba(220, 20, 60, 0.08)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                        borderColor: colors.primary.main,
                        transform: 'translateY(-4px)',
                        boxShadow: '0 12px 24px rgba(220, 20, 60, 0.15)',
                    },
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: 'none',
                    fontWeight: 600,
                    borderRadius: 8,
                },
                contained: {
                    boxShadow: '0 4px 12px rgba(220, 20, 60, 0.25)',
                    '&:hover': {
                        boxShadow: '0 6px 20px rgba(220, 20, 60, 0.35)',
                    },
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                },
            },
        },
    },
});

export default theme;
