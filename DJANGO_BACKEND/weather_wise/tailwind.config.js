// tailwind.config.js
module.exports = {
    darkMode: 'class', // Enables dark mode support
    theme: {
        extend: {
            colors: {
                primary: {
                    light: '#10b981', // Tailwind's green-500 for light mode
                    dark: '#4ade80', // Tailwind's green-400 for dark mode
                },
                secondary: {
                    light: '#f43f5e', // Tailwind's red-500 for light mode
                    dark: '#fb7185', // Tailwind's red-400 for dark mode
                },
                background: {
                    light: '#f9fafb', // Light background
                    dark: '#1e293b', // Dark background
                },
                text: {
                    light: '#111827', // Light text
                    dark: '#f9fafb', // Dark text
                },
            },
            fontFamily: {
                roboto: ['Roboto', 'sans-serif'],
                quicksand: ['"Quicksand"', 'sans-serif'],
            },
        },
    },
    plugins: [],
    content: ['./templates/**/*.html'], // Ensure this points to your Django templates
};
