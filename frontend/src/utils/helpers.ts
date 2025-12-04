// Quick fix for React re-render issue
// Add this to force component re-render when data changes

export const forceUpdate = () => {
    return Date.now();
};
