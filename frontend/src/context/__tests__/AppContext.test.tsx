import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { AppProvider, useAppContext, useOrderSelection, useFilters, useTimelineRange, useDarkMode, useViewMode } from '../AppContext';

// Mock component to test hooks
const TestComponent = () => {
  const { state, dispatch } = useAppContext();
  const { selectedOrderId, selectOrder } = useOrderSelection();
  const { filters, setFilters, resetFilters } = useFilters();
  const { timelineRange, setTimelineRange } = useTimelineRange();
  const { isDarkMode, toggleDarkMode } = useDarkMode();
  const { view, setView } = useViewMode();

  return (
    <div>
      <div data-testid="state">{JSON.stringify(state)}</div>
      <button 
        data-testid="select-order-btn" 
        onClick={() => selectOrder('123')}
      >
        Select Order
      </button>
      <button 
        data-testid="clear-order-btn" 
        onClick={() => selectOrder(null)}
      >
        Clear Order
      </button>
      <button 
        data-testid="set-filters-btn" 
        onClick={() => setFilters({ president: 'Test President' })}
      >
        Set Filters
      </button>
      <button 
        data-testid="reset-filters-btn" 
        onClick={() => resetFilters()}
      >
        Reset Filters
      </button>
      <button 
        data-testid="set-timeline-range-btn" 
        onClick={() => setTimelineRange('2020-01-01T00:00:00Z', '2020-12-31T23:59:59Z')}
      >
        Set Timeline Range
      </button>
      <button 
        data-testid="toggle-dark-mode-btn" 
        onClick={() => toggleDarkMode()}
      >
        Toggle Dark Mode
      </button>
      <button 
        data-testid="set-view-btn" 
        onClick={() => setView('list')}
      >
        Set View
      </button>
    </div>
  );
};

describe('AppContext', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    
    // Reset any DOM modifications
    document.documentElement.classList.remove('dark');
  });

  it('should initialize with default state', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );
    
    const stateElement = screen.getByTestId('state');
    const state = JSON.parse(stateElement.textContent || '{}');
    
    expect(state.selectedOrderId).toBeNull();
    expect(state.filters).toEqual({});
    expect(state.view).toBe('timeline');
    expect(state.isDarkMode).toBe(false);
    expect(state.timelineRange).toBeDefined();
    expect(new Date(state.timelineRange.startDate).getFullYear()).toBe(new Date().getFullYear() - 1);
  });

  it('should select and clear an order', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );
    
    fireEvent.click(screen.getByTestId('select-order-btn'));
    
    const stateElement = screen.getByTestId('state');
    let state = JSON.parse(stateElement.textContent || '{}');
    expect(state.selectedOrderId).toBe('123');
    
    fireEvent.click(screen.getByTestId('clear-order-btn'));
    state = JSON.parse(screen.getByTestId('state').textContent || '{}');
    expect(state.selectedOrderId).toBeNull();
  });

  it('should set and reset filters', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );
    
    fireEvent.click(screen.getByTestId('set-filters-btn'));
    
    const stateElement = screen.getByTestId('state');
    let state = JSON.parse(stateElement.textContent || '{}');
    expect(state.filters.president).toBe('Test President');
    
    fireEvent.click(screen.getByTestId('reset-filters-btn'));
    state = JSON.parse(screen.getByTestId('state').textContent || '{}');
    expect(state.filters).toEqual({});
  });

  it('should set timeline range', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );
    
    fireEvent.click(screen.getByTestId('set-timeline-range-btn'));
    
    const stateElement = screen.getByTestId('state');
    const state = JSON.parse(stateElement.textContent || '{}');
    expect(state.timelineRange.startDate).toBe('2020-01-01T00:00:00Z');
    expect(state.timelineRange.endDate).toBe('2020-12-31T23:59:59Z');
  });

  it('should toggle dark mode and update DOM', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );
    
    expect(document.documentElement.classList.contains('dark')).toBe(false);
    
    fireEvent.click(screen.getByTestId('toggle-dark-mode-btn'));
    
    const stateElement = screen.getByTestId('state');
    const state = JSON.parse(stateElement.textContent || '{}');
    expect(state.isDarkMode).toBe(true);
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    expect(localStorage.getItem('eo-dark-mode')).toBe('true');
  });

  it('should set view mode', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );
    
    fireEvent.click(screen.getByTestId('set-view-btn'));
    
    const stateElement = screen.getByTestId('state');
    const state = JSON.parse(stateElement.textContent || '{}');
    expect(state.view).toBe('list');
  });

  it('should load dark mode preference from localStorage', () => {
    // Set dark mode preference in localStorage
    localStorage.setItem('eo-dark-mode', 'true');
    
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );
    
    const stateElement = screen.getByTestId('state');
    const state = JSON.parse(stateElement.textContent || '{}');
    expect(state.isDarkMode).toBe(true);
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('should throw error when useAppContext is used outside of provider', () => {
    // Suppress error logs in test
    const originalConsoleError = console.error;
    console.error = jest.fn();
    
    // Expect an error when rendering TestComponent without AppProvider
    expect(() => {
      render(<TestComponent />);
    }).toThrow('useAppContext must be used within an AppProvider');
    
    // Restore console.error
    console.error = originalConsoleError;
  });
});