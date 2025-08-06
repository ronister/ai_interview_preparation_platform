// Override django-ai-assistant-client's fetch and XMLHttpRequest to include authentication
export function setupDjangoAIAssistantAuth(accessToken: string | null) {
  console.log('[DjangoAIAssistantAuth] Setting up with token:', {
    hasToken: !!accessToken,
    tokenPreview: accessToken ? `${accessToken.substring(0, 20)}...` : null
  });

  // Store the original implementations
  const originalFetch = window.fetch;
  const OriginalXHR = window.XMLHttpRequest;

  // Override fetch
  window.fetch = async function(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
    const url = typeof input === 'string' ? input : input instanceof Request ? input.url : input.toString();
    
    // Check if this is an AI assistant endpoint
    if (url.includes('/ai-assistant/')) {
      // Use authenticatedFetch if available (from AuthContext)
      if ((window as any).authenticatedFetch) {
        console.log('[DjangoAIAssistantAuth] Using authenticatedFetch for AI assistant request');
        return (window as any).authenticatedFetch(url, init);
      }
      
      console.log('[DjangoAIAssistantAuth] Intercepting AI assistant fetch request:', {
        url,
        method: init?.method || 'GET',
        hasToken: !!accessToken,
        originalHeaders: init?.headers
      });
      
      // Ensure credentials are included for session auth
      init = init || {};
      init.credentials = 'include'; // This ensures cookies are sent
      
      // Get the latest token from localStorage
      const currentToken = localStorage.getItem('accessToken') || accessToken;
      
      // Add auth header if we have a token
      if (currentToken) {
        init.headers = {
          ...init.headers,
          'Authorization': `Bearer ${currentToken}`,
          'Content-Type': 'application/json',
        };
        
        console.log('[DjangoAIAssistantAuth] Added auth header to fetch request');
      }
      
      console.log('[DjangoAIAssistantAuth] Final fetch request init:', {
        credentials: init.credentials,
        hasAuthHeader: !!(init.headers as any)?.['Authorization']
      });
    }
    
    const response = await originalFetch(input, init);
    
    if (url.includes('/ai-assistant/')) {
      console.log('[DjangoAIAssistantAuth] Fetch response:', {
        url,
        status: response.status,
        statusText: response.statusText
      });
      
      if (response.status === 401) {
        console.error('[DjangoAIAssistantAuth] 401 Unauthorized - Token may be invalid or missing');
        // Log response headers for debugging
        console.log('[DjangoAIAssistantAuth] Response headers:', {
          'www-authenticate': response.headers.get('www-authenticate'),
          'content-type': response.headers.get('content-type')
        });
      }
    }
    
    return response;
  };

  // Override XMLHttpRequest
  window.XMLHttpRequest = class extends OriginalXHR {
    private _url?: string;
    private _method?: string;

    open(method: string, url: string | URL, async?: boolean, username?: string | null, password?: string | null): void {
      this._method = method;
      this._url = url.toString();
      
      if (this._url.includes('/ai-assistant/')) {
        console.log('[DjangoAIAssistantAuth] Intercepting AI assistant XHR request:', {
          url: this._url,
          method: this._method,
          hasToken: !!accessToken
        });
      }
      
      super.open(method, url, async !== false, username, password);
    }

    setRequestHeader(name: string, value: string): void {
      // Let the original header be set first
      super.setRequestHeader(name, value);
      
      // Get the latest token from localStorage
      const currentToken = localStorage.getItem('accessToken') || accessToken;
      
      // If this is an AI assistant request and we haven't set auth yet
      if (this._url?.includes('/ai-assistant/') && currentToken && name.toLowerCase() !== 'authorization') {
        console.log('[DjangoAIAssistantAuth] Setting auth header on XHR');
        super.setRequestHeader('Authorization', `Bearer ${currentToken}`);
      }
    }

    send(body?: Document | XMLHttpRequestBodyInit | null): void {
      if (this._url?.includes('/ai-assistant/')) {
        // Ensure credentials are included
        this.withCredentials = true;
        
        // Get the latest token from localStorage
        const currentToken = localStorage.getItem('accessToken') || accessToken;
        
        // Add auth header if not already set
        if (currentToken) {
          try {
            super.setRequestHeader('Authorization', `Bearer ${currentToken}`);
            console.log('[DjangoAIAssistantAuth] Added auth header to XHR request');
          } catch (e) {
            // Header may have already been set
          }
        }
        
        // Add response listener
        this.addEventListener('load', () => {
          console.log('[DjangoAIAssistantAuth] XHR response:', {
            url: this._url,
            status: this.status,
            statusText: this.statusText
          });
          
          if (this.status === 401) {
            console.error('[DjangoAIAssistantAuth] XHR 401 Unauthorized');
          }
        });
      }
      
      super.send(body);
    }
  } as any;
  
  console.log('[DjangoAIAssistantAuth] Fetch and XHR overrides installed');
} 