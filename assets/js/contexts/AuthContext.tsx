import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { notifications } from '@mantine/notifications';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface RegisterData {
  username: string;
  password: string;
  password2: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize authentication state on mount
  useEffect(() => {
    console.log('[AuthContext] Initializing authentication state');
    
    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    
    if (storedAccessToken && storedRefreshToken) {
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
      fetchUserProfile(storedAccessToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  // Create authenticated fetch wrapper with automatic token refresh
  const authenticatedFetch = async (url: string, options: RequestInit = {}) => {
    const token = localStorage.getItem('accessToken');
    
    const headers = {
      ...options.headers,
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    };
    
    let response = await fetch(url, { ...options, headers });
    
    // If we get a 401, try to refresh the token
    if (response.status === 401 && localStorage.getItem('refreshToken')) {
      console.log('[AuthContext] Token expired, refreshing...');
      const newToken = await refreshAccessToken();
      
      if (newToken) {
        // Retry the request with the new token
        headers['Authorization'] = `Bearer ${newToken}`;
        response = await fetch(url, { ...options, headers });
      }
    }
    
    return response;
  };

  // Make authenticatedFetch available globally
  useEffect(() => {
    (window as any).authenticatedFetch = authenticatedFetch;
  }, []);

  const fetchUserProfile = async (token: string) => {
    try {
      const response = await fetch('/api/auth/profile/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const userData = await response.json();
        console.log('[AuthContext] User profile loaded:', userData.username);
          setUser(userData);
      } else if (response.status === 401) {
        // Token is invalid, try to refresh
        await refreshAccessToken();
      }
    } catch (error) {
      console.error('[AuthContext] Error fetching user profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const refreshAccessToken = async () => {
    const storedRefreshToken = localStorage.getItem('refreshToken');
    if (!storedRefreshToken) {
      console.log('[AuthContext] No refresh token, logging out');
      await logout();
      return null;
    }

    try {
      const response = await fetch('/api/auth/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: storedRefreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('[AuthContext] Token refreshed successfully');
        
        // Update tokens in state and localStorage
        setAccessToken(data.access);
        localStorage.setItem('accessToken', data.access);
        
        if (data.refresh) {
          setRefreshToken(data.refresh);
          localStorage.setItem('refreshToken', data.refresh);
        }
        
        return data.access;
      } else {
        console.log('[AuthContext] Token refresh failed, logging out');
        await logout();
      }
    } catch (error) {
      console.error('[AuthContext] Error refreshing token:', error);
      await logout();
    }
    
    return null;
  };

  const login = async (username: string, password: string) => {
    console.log('[AuthContext] Logging in user:', username);
    
    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('[AuthContext] Login successful');
        
        // Set state
        setUser(data.user);
        setAccessToken(data.access);
        setRefreshToken(data.refresh);
        
        // Save to localStorage
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
        
        notifications.show({
          title: 'Login Successful',
          message: `Welcome back, ${data.user.username}!`,
          color: 'green',
        });
      } else {
        throw new Error(data.error || 'Login failed');
      }
    } catch (error: any) {
      console.error('[AuthContext] Login failed:', error);
      notifications.show({
        title: 'Login Failed',
        message: error.message || 'Invalid credentials',
        color: 'red',
      });
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      const response = await fetch('/api/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        notifications.show({
          title: 'Registration Successful',
          message: 'Please log in with your credentials',
          color: 'green',
        });
        // Auto-login after registration
        await login(userData.username, userData.password);
      } else {
        throw new Error(Object.values(data).flat().join(', '));
      }
    } catch (error: any) {
      notifications.show({
        title: 'Registration Failed',
        message: error.message,
        color: 'red',
      });
      throw error;
    }
  };

  const logout = async () => {
    console.log('[AuthContext] Logging out user');
    
    try {
      if (refreshToken && accessToken) {
        await fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            refresh_token: refreshToken,
          }),
        });
      }
    } catch (error) {
      console.error('[AuthContext] Error during logout:', error);
    } finally {
      // Clear state and localStorage
      setUser(null);
      setAccessToken(null);
      setRefreshToken(null);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      
      console.log('[AuthContext] Logout completed');
    }
  };

  const value = {
    user,
    accessToken,
    refreshToken,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 