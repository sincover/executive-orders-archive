import React, { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { FilterState } from '../types';

// Define context state type
interface AppState {
  selectedOrderId: string | null;
  filters: FilterState;
  timelineRange: {
    startDate: string;
    endDate: string;
  };
  isDarkMode: boolean;
  view: 'timeline' | 'list' | 'grid';
}

// Define possible actions
type AppAction = 
  | { type: 'SELECT_ORDER'; payload: string | null }
  | { type: 'SET_FILTERS'; payload: FilterState }
  | { type: 'RESET_FILTERS' }
  | { type: 'SET_TIMELINE_RANGE'; payload: { startDate: string; endDate: string } }
  | { type: 'TOGGLE_DARK_MODE' }
  | { type: 'SET_VIEW'; payload: 'timeline' | 'list' | 'grid' };

// Initial state
const initialState: AppState = {
  selectedOrderId: null,
  filters: {},
  timelineRange: {
    // Default to showing the last year
    startDate: new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString(),
    endDate: new Date().toISOString(),
  },
  isDarkMode: localStorage.getItem('eo-dark-mode') === 'true',
  view: 'timeline',
};

// Create the context
const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | undefined>(undefined);

// Reducer function
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SELECT_ORDER':
      return { ...state, selectedOrderId: action.payload };
    case 'SET_FILTERS':
      return { ...state, filters: { ...state.filters, ...action.payload } };
    case 'RESET_FILTERS':
      return { ...state, filters: {} };
    case 'SET_TIMELINE_RANGE':
      return { ...state, timelineRange: action.payload };
    case 'TOGGLE_DARK_MODE':
      // Persist dark mode preference to localStorage
      localStorage.setItem('eo-dark-mode', (!state.isDarkMode).toString());
      return { ...state, isDarkMode: !state.isDarkMode };
    case 'SET_VIEW':
      return { ...state, view: action.payload };
    default:
      return state;
  }
}

// Provider component
export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  
  // Apply dark mode class to body
  useEffect(() => {
    if (state.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [state.isDarkMode]);
  
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

// Custom hooks for using the context
export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}

// Specialized hooks for specific context actions
export function useOrderSelection() {
  const { state, dispatch } = useAppContext();
  
  const selectOrder = (orderId: string | null) => {
    dispatch({ type: 'SELECT_ORDER', payload: orderId });
  };
  
  return {
    selectedOrderId: state.selectedOrderId,
    selectOrder,
  };
}

export function useFilters() {
  const { state, dispatch } = useAppContext();
  
  const setFilters = (filters: FilterState) => {
    dispatch({ type: 'SET_FILTERS', payload: filters });
  };
  
  const resetFilters = () => {
    dispatch({ type: 'RESET_FILTERS' });
  };
  
  return {
    filters: state.filters,
    setFilters,
    resetFilters,
  };
}

export function useTimelineRange() {
  const { state, dispatch } = useAppContext();
  
  const setTimelineRange = (startDate: string, endDate: string) => {
    dispatch({ 
      type: 'SET_TIMELINE_RANGE', 
      payload: { startDate, endDate } 
    });
  };
  
  return {
    timelineRange: state.timelineRange,
    setTimelineRange,
  };
}

export function useDarkMode() {
  const { state, dispatch } = useAppContext();
  
  const toggleDarkMode = () => {
    dispatch({ type: 'TOGGLE_DARK_MODE' });
  };
  
  return {
    isDarkMode: state.isDarkMode,
    toggleDarkMode,
  };
}

export function useViewMode() {
  const { state, dispatch } = useAppContext();
  
  const setView = (view: 'timeline' | 'list' | 'grid') => {
    dispatch({ type: 'SET_VIEW', payload: view });
  };
  
  return {
    view: state.view,
    setView,
  };
}