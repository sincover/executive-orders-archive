/**
 * UI related types for the Executive Orders Archive
 */

// Common props for components
export interface BaseProps {
  className?: string;
  id?: string;
}

// Common props with children
export interface PropsWithChildren extends BaseProps {
  children: React.ReactNode;
}

// Theme options
export type Theme = 'light' | 'dark' | 'system';

// Component sizes
export type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

// Variant options for UI components
export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'destructive';

// Common UI state
export interface UIState {
  theme: Theme;
  sidebarOpen: boolean;
  mobileSidebarOpen: boolean;
}
