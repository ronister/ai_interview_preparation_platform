// Network request logger to help debug authentication issues

export function setupNetworkLogging() {
  const originalFetch = window.fetch;
  
  window.fetch = async function(...args) {
    const [url, options = {}] = args;
    
    console.log('[NetworkLogger] Fetch request:', {
      url,
      method: options.method || 'GET',
      headers: options.headers,
      hasAuthHeader: !!(options.headers as any)?.['Authorization'],
      authHeaderPreview: (options.headers as any)?.['Authorization'] 
        ? `${(options.headers as any)['Authorization'].substring(0, 30)}...` 
        : null
    });
    
    try {
      const response = await originalFetch.apply(this, args);
      
      console.log('[NetworkLogger] Response:', {
        url,
        status: response.status,
        statusText: response.statusText,
        headers: {
          contentType: response.headers.get('content-type'),
          wwwAuthenticate: response.headers.get('www-authenticate')
        }
      });
      
      // Clone response to read error details for 401s
      if (response.status === 401) {
        const clonedResponse = response.clone();
        try {
          const errorData = await clonedResponse.json();
          console.log('[NetworkLogger] 401 Error details:', errorData);
        } catch (e) {
          console.log('[NetworkLogger] Could not parse 401 error response as JSON');
        }
      }
      
      return response;
    } catch (error) {
      console.error('[NetworkLogger] Fetch error:', {
        url,
        error: error instanceof Error ? error.message : error
      });
      throw error;
    }
  };
  
  console.log('[NetworkLogger] Network logging enabled');
} 