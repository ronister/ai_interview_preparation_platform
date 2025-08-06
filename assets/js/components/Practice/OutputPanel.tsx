import React, { useEffect } from 'react';
import { Paper, ScrollArea, Text, Code, Stack, Loader, Center } from '@mantine/core';

interface OutputPanelProps {
  output: string;
  error: string | null;
  isLoading: boolean;
}

export function OutputPanel({ output, error, isLoading }: OutputPanelProps) {
  // Add CSS to force scrollbar visibility
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      /* Force Mantine ScrollArea scrollbar to be visible */
      .mantine-ScrollArea-scrollbar {
        opacity: 1 !important;
        background-color: rgba(0, 0, 0, 0.3) !important;
      }
      
      .mantine-ScrollArea-scrollbar[data-orientation="vertical"] {
        width: 14px !important;
        right: 2px !important;
        top: 2px !important;
        bottom: 2px !important;
      }
      
      .mantine-ScrollArea-scrollbar[data-orientation="horizontal"] {
        height: 14px !important;
        left: 2px !important;
        right: 2px !important;
        bottom: 2px !important;
      }
      
      .mantine-ScrollArea-thumb {
        opacity: 1 !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 7px !important;
        cursor: pointer !important;
        transition: background-color 0.2s !important;
      }
      
      .mantine-ScrollArea-thumb:hover {
        background-color: rgba(255, 255, 255, 0.6) !important;
      }
      
      .mantine-ScrollArea-thumb:active {
        background-color: rgba(255, 255, 255, 0.8) !important;
      }
      
      /* Ensure viewport doesn't hide content */
      .mantine-ScrollArea-viewport {
        padding-right: 16px !important;
        padding-bottom: 16px !important;
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);
  return (
    <Paper 
      shadow="sm" 
      radius="md" 
      p="sm" 
      style={{ 
        display: 'flex', 
        flexDirection: 'column',
        backgroundColor: 'var(--mantine-color-gray-0)',
        height: '100%',
        width: '100%',
        overflow: 'hidden'
      }}
    >
      <Text size="sm" fw={600} mb="xs" style={{ flexShrink: 0 }}>Output</Text>
      
      <div style={{ 
        flex: 1, 
        backgroundColor: '#1e1e1e',
        borderRadius: '4px',
        display: 'flex',
        flexDirection: 'column',
        minHeight: 0,
        position: 'relative'
      }}>
        <ScrollArea 
          type="always"
          scrollbarSize={14}
          scrollbars="xy"
          style={{ 
            flex: 1,
            padding: '12px'
          }}
        >
        <div style={{ minHeight: '100%', minWidth: 'max-content' }}>
          {isLoading ? (
            <Center h="100%">
              <Loader size="sm" />
            </Center>
          ) : (
            <Stack gap="xs">
              {error ? (
                <Code 
                  block 
                  color="red" 
                  style={{ 
                    backgroundColor: 'transparent', 
                    color: '#ff6b6b',
                    whiteSpace: 'pre',
                    display: 'block',
                    overflowX: 'visible'
                  }}
                >
                  {error}
                </Code>
              ) : output ? (
                <Code 
                  block 
                  style={{ 
                    backgroundColor: 'transparent', 
                    color: '#4caf50',
                    whiteSpace: 'pre',
                    display: 'block',
                    overflowX: 'visible'
                  }}
                >
                  {output}
                </Code>
              ) : (
                <Text size="sm" c="dimmed" style={{ fontFamily: 'monospace' }}>
                  {'> Output will appear here...'}
                </Text>
              )}
            </Stack>
          )}
        </div>
        </ScrollArea>
      </div>
    </Paper>
  );
} 