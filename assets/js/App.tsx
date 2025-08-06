import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";

import React, { useEffect, useState } from "react";
import {
  Container,
  createTheme,
  List,
  MantineProvider,
  rem,
  ThemeIcon,
  Title,
  Button,
  Group,
} from "@mantine/core";
import { Notifications, notifications } from "@mantine/notifications";
import {
  IconChecklist,
  IconBrandDjango,
  IconXboxX,
  IconBubble,
  IconLogout,
  IconUser,
} from "@tabler/icons-react";
import { Chat, PracticeScreen } from "@/components";
import { createBrowserRouter, Link, RouterProvider, useNavigate } from "react-router-dom";
import {
  configAIAssistant,
  useAssistantList,
} from "django-ai-assistant-client";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { Login } from "./components/Auth/Login";
import { Register } from "./components/Auth/Register";
import { ForgotPassword } from "./components/Auth/ForgotPassword";
import { PrivateRoute } from "./components/Auth/PrivateRoute";
import { setupNetworkLogging } from "./utils/networkLogger";
import { setupDjangoAIAssistantAuth } from "./utils/djangoAIAssistantAuth";

// Setup auth override immediately before any components load
// This ensures we catch the django-ai-assistant-client's fetch before it's used
setupDjangoAIAssistantAuth(null); // Initial setup without token
setupNetworkLogging();

const theme = createTheme({});

// Configure AI Assistant with authentication - Must run inside AuthProvider
const ConfigureAIAssistant = () => {
  const { accessToken } = useAuth();
  const lastConfiguredTokenRef = React.useRef<string | null>(null);

  useEffect(() => {
    // Skip if we've already configured with this token
    if (accessToken === lastConfiguredTokenRef.current) {
      return;
    }

    console.log('[ConfigureAIAssistant] Updating with token:', {
      hasToken: !!accessToken,
      tokenPreview: accessToken ? `${accessToken.substring(0, 20)}...` : null
    });
    
    // Update the auth override with the actual token
    setupDjangoAIAssistantAuth(accessToken);
    
    // Also configure via the official API (in case it works)
    const config = { 
      BASE: "ai-assistant",
      HEADERS: accessToken ? {
        'Authorization': `Bearer ${accessToken}`
      } : {}
    };
    
    console.log('[ConfigureAIAssistant] Configuration:', {
      BASE: config.BASE,
      hasAuthHeader: !!config.HEADERS?.Authorization
    });
    
    configAIAssistant(config);
    
    // Remember the last configured token
    lastConfiguredTokenRef.current = accessToken;
  }, [accessToken]);

  return null;
};

const PageWrapper = ({ children }: { children: React.ReactNode }) => {
  // This component allows to use react-router-dom's Link component
  // in the children components.
  return (
    <>
      <Notifications position="top-right" />
      {children}
    </>
  );
};

const ExampleIndex = () => {
  const { user, logout, isAuthenticated, accessToken } = useAuth();
  const navigate = useNavigate();

  // Ensure we have the latest auth state when component mounts
  useEffect(() => {
    console.log('[ExampleIndex] Component mounted, current auth state:', {
      isAuthenticated,
      username: user?.username,
      hasAccessToken: !!accessToken,
      timestamp: new Date().toISOString()
    });
    
    // Check what's in localStorage vs what's in state
    const storedToken = localStorage.getItem('accessToken');
    console.log('[ExampleIndex] Mount - State vs Storage comparison:', {
      stateUsername: user?.username,
      stateToken: accessToken ? `${accessToken.substring(0, 20)}...` : null,
      storageToken: storedToken ? `${storedToken.substring(0, 20)}...` : null,
      tokensMatch: accessToken === storedToken
    });
  }, []); // Only run once on mount

  const handleHTMXClick = async (e: React.MouseEvent) => {
    e.preventDefault();
    
    console.log('[ExampleIndex] HTMX link clicked', {
      currentUser: user?.username,
      isAuthenticated,
      hasAccessToken: !!accessToken,
      timestamp: new Date().toISOString()
    });
    
    if (!isAuthenticated) {
      // If not authenticated, redirect to login
      console.log('[ExampleIndex] Not authenticated, redirecting to login');
      navigate('/login?next=/htmx/');
      return;
    }
    
    try {
      console.log('[ExampleIndex] Creating session for HTMX demo');
      
      // Create a session from JWT token
      const response = await fetch('/create-session/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies to set session
      });
      
      const result = await response.json();
      
      if (result.success) {
        console.log('[ExampleIndex] Session created successfully, navigating to HTMX demo');
        // Navigate to HTMX demo page
        window.location.href = '/htmx/';
      } else {
        console.error('[ExampleIndex] Failed to create session:', result.message);
        navigate('/login?next=/htmx/');
      }
    } catch (error) {
      console.error('[ExampleIndex] Error creating session:', error);
      navigate('/login?next=/htmx/');
    }
  };

  const handleClearProgress = () => {
    const confirmed = window.confirm(`Are you sure you want to clear all progress of ${user?.username}?`);
    
    if (confirmed) {
      clearUserProgress();
    }
  };

  const clearUserProgress = async () => {
    try {
              console.log('[ExampleIndex] Clearing progress for user:', user?.username);
        const response = await (window as any).authenticatedFetch('/api/practice/clear-progress/', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        });
      
      if (response.ok) {
        console.log('[ExampleIndex] Progress cleared successfully');
        notifications.show({
          title: 'Success',
          message: 'Clear Progress completed',
          color: 'green',
        });
      } else {
        console.error('[ExampleIndex] Failed to clear progress, response:', response.status);
        const errorData = await response.json().catch(() => ({}));
        notifications.show({
          title: 'Error',
          message: errorData.message || 'Failed to clear progress. Please try again.',
          color: 'red',
        });
      }
    } catch (error) {
      console.error('[ExampleIndex] Error clearing progress:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to clear progress. Please try again.',
        color: 'red',
      });
    }
  };

  return (
    <Container>
      <Group justify="apart" mb="xl">
        <Title order={2} my="md">
          Adaptive Python Interview Preparation Platform Using AI Agents
        </Title>
        {isAuthenticated && (
          <Group>
            <Button
              variant="subtle"
              leftSection={<IconUser size={16} />}
              // onClick={() => navigate('/profile')}
            >
              {user?.username}
            </Button>
            <Button
              variant="light"
              color="orange"
              onClick={handleClearProgress}
            >
              Clear User Progress
            </Button>
            <Button
              variant="light"
              color="red"
              leftSection={<IconLogout size={16} />}
              style={{
                border: 'none',
                '&:hover': {
                  backgroundColor: 'var(--mantine-color-red-7)',
                }
              }}
              onClick={logout}
            >
              Logout
            </Button>
          </Group>
        )}
      </Group>

      <List spacing="sm" size="md" center>
        <List.Item
          icon={
            <ThemeIcon color="teal" size={28} radius="xl">
              <IconChecklist style={{ width: rem(18), height: rem(18) }} />
            </ThemeIcon>
          }
        >
          <Link to="/practice">Python Coding Practice</Link>
        </List.Item>
        <List.Item
          icon={
            <ThemeIcon color="blue" size={28} radius="xl">
              <IconBrandDjango style={{ width: rem(18), height: rem(18) }} />
            </ThemeIcon>
          }
          style={{ display: 'none' }}
        >
          <Link to="/rag-chat">Django Docs RAG Chat</Link>
        </List.Item>
        <List.Item
          icon={
            <ThemeIcon color="blue" size={28} radius="xl">
              <IconBubble style={{ width: rem(18), height: rem(18) }} />
            </ThemeIcon>
          }
        >
          <a href="/htmx/" onClick={handleHTMXClick}>Chat Threads</a>
        </List.Item>
      </List>
    </Container>
  );
};

const Redirect = ({ to }: { to: string }) => {
  window.location.href = to;
  return null;
};

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <PageWrapper>
        <PrivateRoute>
          <ExampleIndex />
        </PrivateRoute>
      </PageWrapper>
    ),
  },
  {
    path: "/login",
    element: (
      <PageWrapper>
        <Login />
      </PageWrapper>
    ),
  },
  {
    path: "/register",
    element: (
      <PageWrapper>
        <Register />
      </PageWrapper>
    ),
  },
  {
    path: "/forgot-password",
    element: (
      <PageWrapper>
        <ForgotPassword />
      </PageWrapper>
    ),
  },
  {
    path: "/practice",
    element: (
      <PageWrapper>
        <PrivateRoute>
          <PracticeScreen />
        </PrivateRoute>
      </PageWrapper>
    ),
  },
  {
    path: "/rag-chat",
    element: (
      <PageWrapper>
        <PrivateRoute>
          <Chat assistantId="django_docs_assistant" />
        </PrivateRoute>
      </PageWrapper>
    ),
  },
  {
    path: "/admin",
    element: (
      <PageWrapper>
        <Redirect to="/admin/" />
      </PageWrapper>
    ),
  },
]);

const App = () => {
  return (
    <MantineProvider theme={theme}>
      <AuthProvider>
        <ConfigureAIAssistant />
        <RouterProvider router={router} />
      </AuthProvider>
    </MantineProvider>
  );
};

export default App;
