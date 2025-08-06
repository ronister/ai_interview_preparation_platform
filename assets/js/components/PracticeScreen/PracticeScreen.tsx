import { useAuth } from '../../contexts/AuthContext';

export function PracticeScreen() {
  const { threads, selectedThreadId, selectThread, createThread, deleteThread } =
    useThreads({
      assistantId: "python_practice_assistant",
    });
  const { sendMessage, isQuerying } = useAssistant({
    assistantId: "python_practice_assistant",
    threadId: selectedThreadId || undefined,
  });
  const [displayHistory, setDisplayHistory] = useState<DisplayMessage[]>([]);
  const [viewMode, setViewMode] = useState<'split' | 'full'>('split');
  const { user } = useAuth();

  // Custom debounce function
  const debounceTimeoutRef = React.useRef<NodeJS.Timeout | null>(null);

  // Auto-save current progress to localStorage
  const saveProgress = React.useCallback(() => {
    // Clear any existing timeout
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }

    // Set new timeout
    debounceTimeoutRef.current = setTimeout(() => {
      if (selectedThreadId && displayHistory.length > 0) {
        const progressKey = `practice_progress_${user?.id}_${selectedThreadId}`;
        localStorage.setItem(progressKey, JSON.stringify({
          displayHistory,
          timestamp: Date.now(),
        }));
        console.log('[PracticeScreen] Progress auto-saved');
      }
    }, 2000); // Save after 2 seconds of no activity
  }, [selectedThreadId, displayHistory, user?.id]);

  // Save progress whenever display history changes
  useEffect(() => {
    saveProgress();
  }, [displayHistory, saveProgress]);

  // Restore progress on mount or thread change
  useEffect(() => {
    if (selectedThreadId && user?.id) {
      const progressKey = `practice_progress_${user?.id}_${selectedThreadId}`;
      const savedProgress = localStorage.getItem(progressKey);
      
      if (savedProgress) {
        try {
          const { displayHistory: savedHistory } = JSON.parse(savedProgress);
          setDisplayHistory(savedHistory);
          console.log('[PracticeScreen] Progress restored from localStorage');
        } catch (error) {
          console.error('[PracticeScreen] Error restoring progress:', error);
        }
      }
    }
  }, [selectedThreadId, user?.id]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (debounceTimeoutRef.current) {
        clearTimeout(debounceTimeoutRef.current);
      }
    };
  }, []);

  // ... existing code ...
} 