import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import './App.css'
import { AppProvider } from './context/AppContext'
import ContextTester from './components/demo/ContextTester'
import ApiTester from './components/ApiTester'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes by default
      retry: 1, // Only retry failed requests once
      refetchOnWindowFocus: true, // Refetch when window regains focus
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppProvider>
        <Router>
          <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8">Executive Orders Archive</h1>
            
            {/* Context Tester Component */}
            <ContextTester />
            
            {/* API Tester Component */}
            <ApiTester />
          </div>
        </Router>
      </AppProvider>
      
      {/* Add Query DevTools in development mode only */}
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  )
}

export default App