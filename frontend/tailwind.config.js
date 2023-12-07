/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		fontFamily: {
			header: ['"Hammersmith One"', 'sans-serif']
		},
		colors: {
			primary: {
				DEFAULT: '#6a1b9a',
				dark: '#b18bd3',
				mid: '#d2bae9',
				light: '#f7f1fb',
				ligther: '#f9f7fb'
			},
			background: '#ffffff',
			error: '#cc1b1b',
			yellowish: {
				DEFAULT: 'rgb(245 245 245)',
				light: '#fbfbfa'
			},
			secondary: {
				DEFAULT: '#61988e',
				light: '#d0ebe6'
			},
			grey: {
				DEFAULT: '#333333',
				dark: '#73726f',
				darker: '#989895',
				light: '#d3d3d3',
				lighter: '#e0e0e0'
			},
			black: {
				DEFAULT: '#000000',
				transparent: '#0000000A'
			},
			white: {
				DEFAULT: '#ffffff'
			},
			project: {
				DEFAULT: '#5549DD',
				dark: '#3723ff',
				mid: '#8aa2ff',
				light: '#b4c3ff',
				lighter: '#E4EAFF'
			},
			report: {
				DEFAULT: '#ffa800',
				dark: '#ff8e05',
				mid: '#ffc146',
				light: '#ffe6b5',
				lighter: '#fff4f4'
			}
		},
		extend: {
			gridTemplateColumns: {
				home: 'repeat(auto-fill, minmax(275px, 1fr))'
			}
		}
	},
	plugins: [require('@tailwindcss/typography')]
};
