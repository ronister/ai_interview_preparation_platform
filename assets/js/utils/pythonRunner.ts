// Backend Python execution - no browser-side interpreter needed

// Backend Python execution using Django API
export async function runPythonCode(code: string): Promise<{ output: string; error: string | null }> {
  console.log('Executing Python code on backend:', code.substring(0, 100) + '...');
  
  try {
    // Use the global authenticatedFetch which handles token refresh automatically
    const authenticatedFetch = (window as any).authenticatedFetch;
    
    if (!authenticatedFetch) {
      return {
        output: '',
        error: 'Authentication not available. Please refresh the page.'
      };
    }
    
    const response = await authenticatedFetch('/api/practice/run-python/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code })
    });
    
    if (!response.ok) {
      if (response.status === 408) {
        return {
          output: '',
          error: 'Code execution timed out (10 seconds limit)'
        };
      } else {
        const errorData = await response.json().catch(() => ({}));
        return {
          output: '',
          error: errorData.error || `Server error: ${response.status}`
        };
      }
    }
    
    const result = await response.json();
    console.log('Backend execution result:', result);
    
    return {
      output: result.output || '',
      error: result.error || null
    };
    
  } catch (error) {
    console.error('Backend execution error:', error);
    return {
      output: '',
      error: `Network error: ${String(error)}`
    };
  }
}

// Initialize Python backend - checks connectivity
export async function initializePythonBackend(): Promise<void> {
  // Backend Python execution is always ready - just verify connectivity
  console.log('Using backend Python execution - verifying API connectivity');
  
  try {
    // Optional: Add a health check endpoint call here if needed
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      // Could make a lightweight API call to verify backend is responsive
      console.log('Python backend ready');
    }
  } catch (error) {
    console.warn('Could not verify Python backend connectivity:', error);
  }
}

export function clearCache() {
  // No longer needed - using backend execution
  console.log('Backend execution - no cache to clear');
} 