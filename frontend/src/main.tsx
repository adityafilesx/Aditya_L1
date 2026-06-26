import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { AppProviders } from '@app/providers';
import { AppRouter } from '@app/routes';
import '@styles/theme/variables.css';
import '@styles/theme/motion.css';
import '@styles/theme/typography.css';
import '@styles/theme/responsive.css';
import '@styles/theme/accessibility.css';
import '@styles/index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppProviders>
      <AppRouter />
    </AppProviders>
  </StrictMode>,
);
