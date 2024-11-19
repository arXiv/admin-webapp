import { createTheme } from '@mui/material/styles';
import { defaultTheme, defaultDarkTheme } from 'react-admin';

const lightTheme = createTheme({
    ...defaultTheme,
    palette: {
        ...defaultTheme.palette,
        primary: {
            main: '#1010A0',
        },
    },
    components: {
        MuiAppBar: {
            styleOverrides: {
                root: {
                    backgroundColor: '#990000', // Background color for AppBar in light theme
                },
            },
        },
    },
});

const darkTheme = createTheme({
    ...defaultDarkTheme,
    palette: {
        ...defaultDarkTheme.palette,
        mode: 'dark',
        primary: {
            main: '#B0B0FF',
        },
    },
    components: {
        MuiAppBar: {
            styleOverrides: {
                root: {
                    backgroundColor: '#990000', // Background color for AppBar in dark theme
                },
            },
        },
    },
});

export { lightTheme, darkTheme };
