import React, { useState, useEffect, useRef } from 'react';
import { ScrollArea, Stack, Group, Button, Box } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { IconLogout } from '@tabler/icons-react';
import { useAuth } from '../../contexts/AuthContext';
import { UserStats } from './UserStats';
import { LevelSuggestionModal } from './LevelSuggestionModal';
import { QuestionDisplay } from './QuestionDisplay';
import { PythonEditor } from './PythonEditor';
import { OutputPanel } from './OutputPanel';
import { initializePythonBackend, runPythonCode } from '../../utils/pythonRunner';

interface UserStatsData {
  username: string;
  current_level: number;
  manual_level: number;
  total_questions_attempted: number;
  correct_answers_count: number;
  success_rate: number;
  average_grade: number;
}

interface Question {
  id: number;
  instruction: string;
  input: string;
  output: string;
  difficulty_level: number;
}

interface Message {
  id: string;
  type: 'system' | 'question' | 'feedback';
  content: string;
  grade?: number;
  timestamp: Date;
}

interface LevelSuggestion {
  type: 'level_up' | 'level_down';
  current_level: number;
  suggested_level: number;
  reason: string;
}

export function PracticeScreen() {
  // Ensure no body margin/padding
  React.useEffect(() => {
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.height = '100vh';
    document.body.style.overflow = 'hidden';
  }, []);

  const { user, accessToken, logout } = useAuth();
  const [userStats, setUserStats] = useState<UserStatsData>({
    username: '',
    current_level: 3,
    manual_level: 3,
    total_questions_attempted: 0,
    correct_answers_count: 0,
    success_rate: 0,
    average_grade: 0.0
  });
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isAbandoning, setIsAbandoning] = useState(false);
  const [showNextButton, setShowNextButton] = useState(false);
  const [isSubmitDisabled, setIsSubmitDisabled] = useState(false);
  const [levelSuggestion, setLevelSuggestion] = useState<LevelSuggestion | null>(null);
  const [showLevelModal, setShowLevelModal] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const levelChangeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Store user ID in a ref to avoid re-creating saveProgress
  const userIdRef = useRef<number | undefined>(user?.id);
  useEffect(() => {
    userIdRef.current = user?.id;
  }, [user?.id]);

  // Auto-save code to localStorage
  const saveProgress = React.useCallback(() => {
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }

    saveTimeoutRef.current = setTimeout(() => {
      if (currentQuestion && code) {
        const progressKey = `practice_code_${userIdRef.current}_${currentQuestion.id}`;
        localStorage.setItem(progressKey, JSON.stringify({
          code,
          questionId: currentQuestion.id,
          timestamp: Date.now()
        }));
        console.log('[PracticeScreen] Code auto-saved');
      }
    }, 1000); // Save after 1 second of no changes
  }, [code, currentQuestion]);

  // Save code whenever it changes
  useEffect(() => {
    saveProgress();
  }, [code, saveProgress]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
      if (levelChangeTimeoutRef.current) {
        clearTimeout(levelChangeTimeoutRef.current);
      }
    };
  }, []);

  // Load Python backend and fetch initial data on mount
  const isInitializedRef = useRef(false);
  
  useEffect(() => {
    if (!accessToken || isInitializedRef.current) return;

    // Mark as initialized to prevent re-running
    isInitializedRef.current = true;

    // Initialize Python backend
    initializePythonBackend().then(() => {
      console.log('Python backend initialized for practice screen');
    }).catch((error) => {
      console.error('Failed to initialize Python backend:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to initialize Python runtime',
        color: 'red'
      });
    });

    // Add welcome message
    const displayName = user?.first_name || user?.username || 'there';
    setMessages([{
      id: '1',
      type: 'system',
      content: `Welcome ${displayName}! Let's start practicing Python coding problems.`,
      timestamp: new Date()
    }]);

    fetchUserStats();
    fetchNextQuestion();
  }, [!!accessToken]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollAreaRef.current) {
      // Check if the last message is a feedback message
      const lastMessage = messages[messages.length - 1];
      if (lastMessage && lastMessage.type === 'feedback') {
        // Set up callback for when feedback element is mounted
        (window as any).__feedbackCallback = {
          onFeedbackMount: (element: HTMLDivElement) => {
            // Small delay to ensure element is fully rendered
            setTimeout(() => {
              element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest' 
              });
            }, 100);
          }
        };
      } else {
        // For other messages, scroll to bottom
        scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
      }
    }
  }, [messages]);

  const fetchUserStats = async () => {
    try {
      const response = await (window as any).authenticatedFetch('/api/practice/user-stats/');

      if (response.ok) {
        const data = await response.json();
        setUserStats(data);
      }
    } catch (error) {
      console.error('Error fetching user stats:', error);
    }
  };

  const setManualLevel = async (level: number) => {
    // Clear any existing timeout
    if (levelChangeTimeoutRef.current) {
      clearTimeout(levelChangeTimeoutRef.current);
    }

    // Update the level in the UI immediately for responsiveness
    setUserStats(prev => ({ ...prev, manual_level: level }));

         // Debounce the API call
     levelChangeTimeoutRef.current = setTimeout(async () => {
       try {
         const response = await (window as any).authenticatedFetch('/api/practice/set-manual-level/', {
           method: 'POST',
           headers: {
             'Content-Type': 'application/json'
           },
           body: JSON.stringify({ level })
         });

        if (response.ok) {
          const data = await response.json();
          setUserStats(data.user_stats);
          notifications.show({
            title: 'Level Updated',
            message: `Difficulty level set to ${level}`,
            color: 'blue'
          });
        }
      } catch (error) {
        console.error('Error setting manual level:', error);
        notifications.show({
          title: 'Error',
          message: 'Failed to update difficulty level',
          color: 'red'
        });
        // Revert the UI change if API call failed
        await fetchUserStats();
      }
    }, 1000); // Wait 1 second after user stops changing level
  };

  const fetchNextQuestion = async () => {
    try {
      const response = await (window as any).authenticatedFetch('/api/practice/next-question/');

      if (response.ok) {
        const data = await response.json();
        setCurrentQuestion(data.question);
        setUserStats(data.user_stats);
        
        // Add the current question to messages
        const questionMessage: Message = {
          id: Date.now().toString(),
          type: 'question',
          content: formatQuestionContent(data.question),
          timestamp: new Date()
        };
        
        // Clear any previous questions/feedback and keep only welcome message + current question
        setMessages(prev => {
          const welcomeMessage = prev.find(msg => msg.type === 'system');
          return welcomeMessage ? [welcomeMessage, questionMessage] : [questionMessage];
        });
        
        // Check for saved code for this question
        const progressKey = `practice_code_${userIdRef.current}_${data.question.id}`;
        const savedProgress = localStorage.getItem(progressKey);
        
        if (savedProgress) {
          try {
            const { code: savedCode } = JSON.parse(savedProgress);
            setCode(savedCode);
            console.log('[PracticeScreen] Restored saved code for question');
          } catch (error) {
            console.error('[PracticeScreen] Error restoring saved code:', error);
            setCode('');
          }
        } else {
          setCode('');
        }

        setOutput('');
        setError(null);
        setShowNextButton(false); // Hide next button for new question
        setIsSubmitDisabled(false); // Re-enable submit button for new question
      }
    } catch (error) {
      console.error('Error fetching next question:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to fetch next question',
        color: 'red'
      });
    }
  };

  const formatQuestionContent = (question: Question): string => {
    let content = `**Problem:**\n${question.instruction}\n\n`;
    if (question.input) {
      content += `**Input:**\n${question.input}`;
    }
    return content;
  };

  const runCode = async () => {
    setIsRunning(true);
    setError(null);
    setOutput('');

    try {
      console.log('Running code:', code.substring(0, 50) + '...');
      console.log('Auth token available:', !!accessToken);
      const result = await runPythonCode(code);
      console.log('Code execution result:', result);
      
      if (result.error) {
        console.error('Python execution error:', result.error);
        setError(result.error);
      } else if (result.output) {
        setOutput(result.output);
      } else {
        setOutput('(No output)');
      }
    } catch (error) {
      console.error('Error running Python code:', error);
      setError(`JavaScript Error: ${String(error)}`);
    } finally {
      setIsRunning(false);
    }
  };

  const submitCode = async () => {
    if (!currentQuestion) return;

    setIsSubmitting(true);
    
    // First, clear output and error states (like runCode does)
    setError(null);
    setOutput('');
    
    try {
      // First run the code to get output
      console.log('Submitting code:', code.substring(0, 50) + '...');
      console.log('Auth token available:', !!accessToken);
      
      let result;
      try {
        result = await runPythonCode(code);
        console.log('Code execution result:', result);
      } catch (error) {
        console.error('Error running Python code:', error);
        setError(`JavaScript Error: ${String(error)}`);
        setIsSubmitting(false);
        return;
      }
      
      // Display the output in the output panel (like runCode does)
      if (result.error) {
        console.error('Python execution error:', result.error);
        setError(result.error);
      } else if (result.output) {
        setOutput(result.output);
      } else {
        setOutput('(No output)');
      }
      
      // Store the output for backend submission
      const codeOutput = result.output || '';
      const codeError = result.error || null;
      
      // Submit to backend
      const response = await (window as any).authenticatedFetch('/api/practice/submit-solution/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question_id: currentQuestion.id,
          code: code
        })
      });

      if (response.ok) {
        const result = await response.json();
        
        // Add feedback message with expected output
        const feedbackContent = {
          expectedOutput: currentQuestion.output,
          feedback: result.feedback,
          grade: result.grade
        };
        
        const feedbackMessage: Message = {
          id: Date.now().toString(),
          type: 'feedback',
          content: JSON.stringify(feedbackContent),
          grade: result.grade,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, feedbackMessage]);

        // Update user stats
        await fetchUserStats();

        // Handle level suggestion
        if (result.level_suggestion) {
          setLevelSuggestion(result.level_suggestion);
          setShowLevelModal(true);
        }

        // Show next button and disable submit button
        setShowNextButton(true);
        setIsSubmitDisabled(true);
        
        // Clear saved progress for this question since it's been submitted
        const progressKey = `practice_code_${userIdRef.current}_${currentQuestion.id}`;
        localStorage.removeItem(progressKey);
        console.log('[PracticeScreen] Cleared saved code after successful submission');
      }
    } catch (error) {
      console.error('Error submitting code:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to submit solution',
        color: 'red'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLevelSuggestionAccept = async () => {
    if (!levelSuggestion) return;
    
    await setManualLevel(levelSuggestion.suggested_level);
    
    // Show level change notification after user accepts
    notifications.show({
      title: 'Level Changed!',
      message: `You are now at Level ${levelSuggestion.suggested_level}`,
      color: 'blue'
    });
    
    setShowLevelModal(false);
    setLevelSuggestion(null);
  };

  const handleLevelSuggestionDecline = () => {
    setShowLevelModal(false);
    setLevelSuggestion(null);
  };

  const handleLogout = async () => {
    try {
      await logout();
      notifications.show({
        title: 'Logged Out',
        message: 'You have been successfully logged out',
        color: 'green'
      });
    } catch (error) {
      console.error('Logout error:', error);
      notifications.show({
        title: 'Logout Error',
        message: 'There was an issue logging out',
        color: 'red'
      });
    }
  };

  const handleNextProblem = async () => {
    setShowNextButton(false);
    await fetchNextQuestion();
  };

  const abandonQuestion = async () => {
    if (!currentQuestion) return;

    setIsAbandoning(true);
    
         try {
       const response = await (window as any).authenticatedFetch('/api/practice/abandon-question/', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json'
         }
       });

      if (response.ok) {
        const result = await response.json();
        
        // Show the expected output as solution (without grade or feedback)
        const solutionContent = {
          expectedOutput: currentQuestion.output,
          feedback: null,
          grade: null,
          isSkipped: true
        };
        
        const solutionMessage: Message = {
          id: Date.now().toString(),
          type: 'feedback',
          content: JSON.stringify(solutionContent),
          timestamp: new Date()
        };
        setMessages(prev => [...prev, solutionMessage]);
        
        // Update user stats
        await fetchUserStats();

        // Handle level suggestion
        if (result.level_suggestion) {
          setLevelSuggestion(result.level_suggestion);
          setShowLevelModal(true);
        }

        // Show abandonment notification
        notifications.show({
          title: 'Question Skipped',
          message: 'The question has been skipped, recorded as a failed attempt and graded as 0',
          color: 'orange'
        });

        // Clear saved progress for this question
        const progressKey = `practice_code_${userIdRef.current}_${currentQuestion.id}`;
        localStorage.removeItem(progressKey);
        
        // Show next button and disable submit button
        setShowNextButton(true);
        setIsSubmitDisabled(true);
      }
    } catch (error) {
      console.error('Error abandoning question:', error);
      notifications.show({
        title: 'Error',
        message: 'Failed to abandon question',
        color: 'red'
      });
    } finally {
      setIsAbandoning(false);
    }
  };

  return (
    <div style={{ 
      height: '100vh', 
      width: '100vw', 
      overflow: 'hidden', 
      display: 'flex', 
      padding: '16px', 
      gap: '16px',
      boxSizing: 'border-box'
    }}>
      {/* Left side - Chat UI */}
      <div style={{ 
        flex: '0 0 40%', 
        height: '100%', 
        overflow: 'hidden', 
        display: 'flex', 
        flexDirection: 'column' 
      }}>
        <Stack gap="md" style={{ height: '100%', flex: 1 }}>
            <Group justify="space-between" align="flex-start">
              <UserStats 
                username={userStats.username}
                currentLevel={userStats.current_level}
                manualLevel={userStats.manual_level}
                totalQuestions={userStats.total_questions_attempted}
                correctAnswers={userStats.correct_answers_count}
                successRate={userStats.success_rate}
                averageGrade={userStats.average_grade}
                onLevelChange={setManualLevel}
                disabled={!showNextButton}
              />
              <Button 
                variant="light" 
                color="red" 
                leftSection={<IconLogout size={16} />}
                style={{
                  marginTop: 12,
                  border: 'none',
                  '&:hover': {
                    backgroundColor: 'var(--mantine-color-red-7)',
                  }
                }}
                onClick={handleLogout}
              >
                Logout
              </Button>
            </Group>
            
            <Box style={{ 
              flex: 1, 
              position: 'relative', 
              minHeight: 0,
              maxHeight: '100%',
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <ScrollArea 
                style={{ 
                  height: '80vh',
                  width: '100%',
                  minHeight: 0
                }} 
                viewportRef={scrollAreaRef}
                type="auto"
                scrollbarSize={12}
                scrollbars="y"
                styles={(theme) => ({
                  viewport: {
                    paddingBottom: '16px',
                  },
                  scrollbar: {
                    width: 14,
                    paddingLeft: 2,
                    paddingRight: 2,
                    zIndex: 10,
                  },
                  thumb: {
                    backgroundColor: theme.colors.gray[5],
                  },
                  root: {
                    height: '100%'
                  },
                })}
              >
                <QuestionDisplay messages={messages} />
              </ScrollArea>
            </Box>
        </Stack>
      </div>

      {/* Right side - Code Editor and Output */}
      <div style={{ flex: '1', height: '100%', overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        <div style={{ flex: '1.5', minHeight: 0, display: 'flex', overflow: 'hidden' }}>
          <PythonEditor
            code={code}
            onChange={setCode}
            onRun={runCode}
            onSubmit={submitCode}
            onAbandon={abandonQuestion}
            isRunning={isRunning}
            isSubmitting={isSubmitting}
            isAbandoning={isAbandoning}
            isSubmitDisabled={isSubmitDisabled}
            showNextButton={showNextButton}
            onNextProblem={handleNextProblem}
          />
        </div>
        
        <div style={{ flex: '1', minHeight: 0, display: 'flex', overflow: 'hidden' }}>
          <OutputPanel
            output={output}
            error={error}
            isLoading={isRunning}
          />
        </div>
      </div>

      {/* Level Suggestion Modal */}
      <LevelSuggestionModal
        isOpen={showLevelModal}
        suggestion={levelSuggestion}
        onAccept={handleLevelSuggestionAccept}
        onDecline={handleLevelSuggestionDecline}
        onClose={handleLevelSuggestionDecline}
      />
    </div>
  );
} 