import { ReactNode } from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

type Props = {
	children: ReactNode;
};

const Providers = ({ children }: Props) => {
	return (
		<NextThemesProvider
			attribute="class"
			defaultTheme="light"
			enableSystem
			disableTransitionOnChange
		>
			{children}
		</NextThemesProvider>
	);
};

export default Providers;
