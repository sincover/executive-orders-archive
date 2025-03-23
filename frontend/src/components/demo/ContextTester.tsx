import React from 'react';
import { useOrderSelection, useFilters, useTimelineRange, useDarkMode, useViewMode } from '../../context/AppContext';

const ContextTester: React.FC = () => {
  // Use all custom hooks
  const { selectedOrderId, selectOrder } = useOrderSelection();
  const { filters, setFilters, resetFilters } = useFilters();
  const { timelineRange, setTimelineRange } = useTimelineRange();
  const { isDarkMode, toggleDarkMode } = useDarkMode();
  const { view, setView } = useViewMode();

  // Example filters to set
  const sampleFilters = {
    president: 'Joe Biden',
    status: 'Active'
  };

  // Example timeline range to set
  const lastSixMonths = () => {
    const endDate = new Date().toISOString();
    const startDate = new Date();
    startDate.setMonth(startDate.getMonth() - 6);
    return { startDate: startDate.toISOString(), endDate };
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric', 
      month: 'short', 
      day: 'numeric'
    });
  };

  return (
    <div className="glass-card p-6 mb-8">
      <h2 className="text-xl font-bold mb-4">Context State Demonstration</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Selected Order Section */}
        <div className="border p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Selected Order</h3>
          <div className="mb-2">Current: {selectedOrderId || 'None'}</div>
          <div className="flex space-x-2">
            <button 
              onClick={() => selectOrder('EO-12345')} 
              className="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            >
              Select Sample Order
            </button>
            <button 
              onClick={() => selectOrder(null)} 
              className="px-3 py-1 bg-gray-300 rounded-md hover:bg-gray-400"
            >
              Clear Selection
            </button>
          </div>
        </div>
        
        {/* Filters Section */}
        <div className="border p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Filters</h3>
          <div className="mb-2">
            <span className="font-medium">Current Filters:</span>
            <pre className="text-xs bg-gray-100 p-2 rounded mt-1 max-h-20 overflow-auto">
              {JSON.stringify(filters, null, 2) || 'None'}
            </pre>
          </div>
          <div className="flex space-x-2">
            <button 
              onClick={() => setFilters(sampleFilters)} 
              className="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            >
              Set Sample Filters
            </button>
            <button 
              onClick={resetFilters} 
              className="px-3 py-1 bg-gray-300 rounded-md hover:bg-gray-400"
            >
              Reset Filters
            </button>
          </div>
        </div>
        
        {/* Timeline Range Section */}
        <div className="border p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Timeline Range</h3>
          <div className="mb-2">
            <div>
              <span className="font-medium">Start:</span> {formatDate(timelineRange.startDate)}
            </div>
            <div>
              <span className="font-medium">End:</span> {formatDate(timelineRange.endDate)}
            </div>
          </div>
          <div className="flex space-x-2">
            <button 
              onClick={() => {
                const { startDate, endDate } = lastSixMonths();
                setTimelineRange(startDate, endDate);
              }} 
              className="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            >
              Set to Last 6 Months
            </button>
          </div>
        </div>
        
        {/* Dark Mode Section */}
        <div className="border p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Dark Mode</h3>
          <div className="mb-2">Current: {isDarkMode ? 'Enabled' : 'Disabled'}</div>
          <button 
            onClick={toggleDarkMode} 
            className="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Toggle Dark Mode
          </button>
        </div>
        
        {/* View Mode Section */}
        <div className="border p-4 rounded-lg">
          <h3 className="font-semibold mb-2">View Mode</h3>
          <div className="mb-2">Current: {view}</div>
          <div className="flex space-x-2">
            <button 
              onClick={() => setView('timeline')} 
              className={`px-3 py-1 rounded-md ${view === 'timeline' ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              Timeline
            </button>
            <button 
              onClick={() => setView('list')} 
              className={`px-3 py-1 rounded-md ${view === 'list' ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              List
            </button>
            <button 
              onClick={() => setView('grid')} 
              className={`px-3 py-1 rounded-md ${view === 'grid' ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              Grid
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContextTester;