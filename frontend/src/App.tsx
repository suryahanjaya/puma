import { useState, useEffect } from 'react';
import { ThemeProvider, CssBaseline, Box, Container, CircularProgress, Typography } from '@mui/material';

import { theme, colors } from './theme/theme';
import Header from './components/Header';
import StatusCard from './components/StatusCard';
import AnomalyChart from './components/AnomalyChart';
import MetricsChart from './components/MetricsChart';
import TelemetryTable from './components/TelemetryTable';
import { uavApi } from './services/api';
import type { UAVTelemetry } from './types/uav';

function App() {
  const [telemetryData, setTelemetryData] = useState<UAVTelemetry[]>([]);
  const [latestData, setLatestData] = useState<UAVTelemetry | null>(null);
  const [dbStatus, setDbStatus] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [historyLimit, setHistoryLimit] = useState<number>(150);
  const [lastUpdate, setLastUpdate] = useState<string>('--:--:--');

  // Fetch data from API
  const fetchData = async () => {
    try {
      console.log('🔄 Fetching data from API...');

      // Get latest telemetry with history
      const response = await uavApi.getLatestTelemetry(historyLimit);
      console.log('✅ Data received:', response);
      console.log('📊 History length:', response.history?.length);
      console.log('📍 Latest data:', response.latest);

      setTelemetryData(response.history || []);
      setLatestData(response.latest);

      // Update last update time
      const now = new Date();
      setLastUpdate(now.toLocaleTimeString('id-ID'));

      // Check database status
      try {
        const status = await uavApi.getDatabaseStatus();
        console.log('💾 Database status:', status);
        setDbStatus(status.connected);
      } catch (error) {
        console.error('❌ Database status error:', error);
        setDbStatus(false);
      }

      setLoading(false);
    } catch (error) {
      console.error('❌ Error fetching data:', error);
      setLoading(false);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [historyLimit]);

  // Auto-refresh every 1 second for real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, 1000); // Update setiap 1 detik (real-time)

    return () => clearInterval(interval);
  }, [historyLimit]);

  // Calculate statistics
  const anomalyCount = telemetryData.filter(d => d.is_anomaly).length;
  const totalRecords = telemetryData.length;

  // Get battery status label
  const getBatteryLabel = (battery: number) => {
    if (battery >= 80) return 'Fully Charged';
    if (battery >= 50) return 'Good';
    if (battery >= 20) return 'Low';
    return 'Critical';
  };

  // Get battery color
  const getBatteryColor = (battery: number) => {
    if (battery >= 50) return colors.status.normal;
    if (battery >= 20) return colors.status.warning;
    return colors.status.anomaly;
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh',
            background: '#FFFFFF',
          }}
        >
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress size={60} sx={{ color: colors.primary.main }} />
            <Typography variant="h6" sx={{ color: colors.text.secondary }}>
              Loading PUMA Dashboard...
            </Typography>
          </Box>
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(180deg, #FFF0F0 0%, #FFFFFF 100%)',
        }}
      >
        {/* Header */}
        <Header dbStatus={dbStatus} lastUpdate={lastUpdate} />

        {/* Main Content */}
        <Container maxWidth="xl" sx={{ py: 4 }}>
          {/* Status Cards */}
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
            <Box sx={{ flex: '1 1 calc(20% - 24px)', minWidth: '200px' }}>
              <StatusCard
                title="System Status"
                value={latestData?.is_anomaly ? 'ANOMALY' : 'NORMAL'}
                label="ML Detection"
                color={latestData?.is_anomaly ? colors.primary.main : colors.status.normal}
                isAnomaly={Boolean(latestData?.is_anomaly)}
                isSystemStatus={true}
              />
            </Box>
            <Box sx={{ flex: '1 1 calc(20% - 24px)', minWidth: '200px' }}>
              <StatusCard
                title="Timestamp"
                value={latestData ? (latestData.dt ? new Date(latestData.dt).toLocaleTimeString('id-ID') : new Date(latestData.timestamp * 1000).toLocaleTimeString('id-ID')) : '--:--:--'}
                label="Real-time"
              />
            </Box>
            <Box sx={{ flex: '1 1 calc(20% - 24px)', minWidth: '200px' }}>
              <StatusCard
                title="Altitude"
                value={`${latestData?.altitude.toFixed(1) || '0.0'} m`}
                label="Current Height"
              />
            </Box>
            <Box sx={{ flex: '1 1 calc(20% - 24px)', minWidth: '200px' }}>
              <StatusCard
                title="Battery Level"
                value={`${latestData?.battery_level.toFixed(1) || '100.0'} %`}
                label={getBatteryLabel(latestData?.battery_level || 100)}
                color={getBatteryColor(latestData?.battery_level || 100)}
              />
            </Box>
            <Box sx={{ flex: '1 1 calc(20% - 24px)', minWidth: '200px' }}>
              <StatusCard
                title="Flight Mode"
                value={latestData?.flight_mode || 'Auto'}
                label="Current Mode"
              />
            </Box>
          </Box>

          {/* Charts */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, mb: 4 }}>
            {telemetryData.length > 0 ? (
              <>
                <AnomalyChart
                  data={telemetryData}
                  historyLimit={historyLimit}
                  onHistoryLimitChange={setHistoryLimit}
                />
                <MetricsChart
                  data={telemetryData}
                />
              </>
            ) : (
              <Box sx={{
                textAlign: 'center',
                py: 8,
                backgroundColor: colors.background.light,
                borderRadius: 2,
                border: `2px solid ${colors.border.light}`
              }}>
                <Typography variant="h6" sx={{ color: colors.text.secondary }}>
                  Loading chart data...
                </Typography>
                <Typography variant="body2" sx={{ color: colors.text.secondary, mt: 1 }}>
                  Waiting for telemetry data from backend
                </Typography>
              </Box>
            )}
          </Box>

          {/* Telemetry Table */}
          {telemetryData.length > 0 ? (
            <TelemetryTable
              data={telemetryData}
              anomalyCount={anomalyCount}
              totalRecords={totalRecords}
            />
          ) : (
            <Box sx={{
              textAlign: 'center',
              py: 8,
              backgroundColor: colors.background.light,
              borderRadius: 2,
              border: `2px solid ${colors.border.light}`
            }}>
              <Typography variant="h6" sx={{ color: colors.text.secondary }}>
                No telemetry data available
              </Typography>
              <Typography variant="body2" sx={{ color: colors.text.secondary, mt: 1 }}>
                Make sure uav_producer.py and api_server.py are running
              </Typography>
            </Box>
          )}
        </Container>

        {/* Footer */}
        <Box
          sx={{
            borderTop: `4px solid ${colors.accent.gold}`,
            background: colors.accent.redGradient,
            py: 3,
            mt: 6,
            boxShadow: '0 -4px 20px rgba(220, 20, 60, 0.15)',
          }}
        >
          <Container maxWidth="xl">
            <Typography
              variant="body2"
              align="center"
              sx={{ color: colors.text.white, fontWeight: 600 }}
            >
              PUMA Dashboard v2.0 | Developed by <strong style={{ color: colors.accent.gold }}>Surya Hanjaya</strong> |
              Real-time UAV Anomaly Detection System 🇮🇩
            </Typography>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
