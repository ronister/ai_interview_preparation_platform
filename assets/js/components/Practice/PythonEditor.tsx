import React, { useRef, useEffect, useState } from 'react';
import AceEditor from 'react-ace';
import { Button, Group, Paper } from '@mantine/core';
import { IconPlayerPlay, IconSend } from '@tabler/icons-react';

import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/ext-language_tools';

interface PythonEditorProps {
  code: string;
  onChange: (code: string) => void;
  onRun: () => void;
  onSubmit: () => void;
  onAbandon?: () => void;
  isRunning: boolean;
  isSubmitting: boolean;
  isAbandoning?: boolean;
  isSubmitDisabled?: boolean;
  showNextButton?: boolean;
  onNextProblem?: () => void;
}

export function PythonEditor({ 
  code, 
  onChange, 
  onRun, 
  onSubmit, 
  onAbandon,
  isRunning, 
  isSubmitting,
  isAbandoning = false,
  isSubmitDisabled = false,
  showNextButton = false,
  onNextProblem
}: PythonEditorProps) {
  const editorRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [editorHeight, setEditorHeight] = useState('400px');

  useEffect(() => {
    // Calculate available height
    const updateHeight = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const buttonHeight = 60; // Approximate height of buttons + margins
        const availableHeight = rect.height - buttonHeight;
        setEditorHeight(`${Math.max(300, availableHeight)}px`);
      }
    };

    updateHeight();
    window.addEventListener('resize', updateHeight);
    
    // Force update after a short delay to ensure layout is complete
    setTimeout(updateHeight, 100);
    
    // Force editor refresh to show scrollbars
    setTimeout(() => {
      if (editorRef.current && editorRef.current.editor) {
        editorRef.current.editor.resize();
        editorRef.current.editor.renderer.updateFull();
      }
    }, 200);

    return () => {
      window.removeEventListener('resize', updateHeight);
    };
  }, []);

  // Add CSS for visible scrollbars
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      /* Make scrollbar track visible */
      .ace_scrollbar {
        opacity: 1 !important;
        background-color: rgba(0, 0, 0, 0.3) !important;
      }
      
      /* Vertical scrollbar */
      .ace_scrollbar-v {
        width: 14px !important;
        right: 0 !important;
        cursor: pointer !important;
      }
      
      /* Horizontal scrollbar */
      .ace_scrollbar-h {
        height: 14px !important;
        bottom: 0 !important;
        cursor: pointer !important;
      }
      
      /* Scrollbar thumb (the draggable part) */
      .ace_scrollbar-inner {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 7px !important;
        border: 2px solid transparent !important;
        background-clip: padding-box !important;
      }
      
      /* Scrollbar thumb on hover */
      .ace_scrollbar-inner:hover {
        background-color: rgba(255, 255, 255, 0.6) !important;
      }
      
      /* Scrollbar thumb when active/dragging */
      .ace_scrollbar-inner:active {
        background-color: rgba(255, 255, 255, 0.8) !important;
      }
      
      /* Ensure the corner between scrollbars is visible */
      .ace_scroller {
        margin-right: 0 !important;
      }
      
      /* Fallback: Native scrollbar styling for webkit browsers */
      .ace_content::-webkit-scrollbar,
      .ace_scroller::-webkit-scrollbar {
        width: 14px !important;
        height: 14px !important;
      }
      
      .ace_content::-webkit-scrollbar-track,
      .ace_scroller::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3) !important;
      }
      
      .ace_content::-webkit-scrollbar-thumb,
      .ace_scroller::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.4) !important;
        border-radius: 7px !important;
      }
      
      .ace_content::-webkit-scrollbar-thumb:hover,
      .ace_scroller::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.6) !important;
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <Paper 
      ref={containerRef}
      shadow="sm" 
      radius="md" 
      p="sm" 
      style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%' }}
    >
      <Group justify="flex-start" gap="sm" mb="sm">
        <Button
          leftSection={<IconPlayerPlay size={16} />}
          variant="light"
          onClick={onRun}
          loading={isRunning}
          disabled={isSubmitting}
        >
          Run
        </Button>
        <Button
          leftSection={<IconSend size={16} />}
          onClick={onSubmit}
          loading={isSubmitting}
          disabled={isRunning || isSubmitDisabled}
        >
          Submit
        </Button>
        {onAbandon && (
          <Button
            variant="light"
            color="orange"
            onClick={onAbandon}
            loading={isAbandoning}
            disabled={isRunning || isSubmitting || showNextButton}
          >
            Skip Question
          </Button>
        )}
        {showNextButton && onNextProblem && (
          <Button
            variant="filled"
            color="blue"
            onClick={onNextProblem}
            disabled={isRunning || isSubmitting}
          >
            Next Problem
          </Button>
        )}
      </Group>
      
      <div style={{ flex: 1, border: '1px solid var(--mantine-color-gray-3)', borderRadius: '4px', overflow: 'visible', position: 'relative' }}>
        <AceEditor
          ref={editorRef}
          mode="python"
          theme="monokai"
          onChange={onChange}
          value={code}
          name="python-editor"
          wrapEnabled={false}
          editorProps={{ $blockScrolling: true }}
          onLoad={(editor) => {
            // Force scrollbar visibility
            editor.setShowInvisibles(false);
            editor.renderer.setScrollMargin(0, 0, 0, 0);
            editor.renderer.setPadding(10);
            
            // Update scrollbar settings
            editor.setOptions({
              animatedScroll: false
            });
            
            // Force a resize to show scrollbars
            setTimeout(() => {
              editor.resize();
              editor.renderer.updateFull();
            }, 100);
          }}
          setOptions={{
            enableBasicAutocompletion: false,
            enableLiveAutocompletion: false,
            enableSnippets: true,
            showLineNumbers: true,
            tabSize: 4,
            useWorker: false,
            showInvisibles: false,
            displayIndentGuides: true,
            scrollPastEnd: true,
            animatedScroll: false
          }}
          fontSize={14}
          width="100%"
          height={editorHeight}
          style={{
            lineHeight: '1.5'
          }}
        />
      </div>
    </Paper>
  );
} 