import {
  ActionIcon,
  Avatar,
  Button,
  Container,
  Group,
  LoadingOverlay,
  Paper,
  ScrollArea,
  Stack,
  Text,
  Textarea,
  Title,
  Tooltip,
} from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { ThreadsNav } from "../ThreadsNav/ThreadsNav";

import classes from "./Chat.module.css";
import { useCallback, useEffect, useRef, useState } from "react";
import { IconSend2, IconTrash } from "@tabler/icons-react";
import { getHotkeyHandler } from "@mantine/hooks";
import Markdown from "react-markdown";

import {
  useAssistant,
  useMessageList,
  useThreadList,
} from "django-ai-assistant-client";
import { Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";

// Define types locally since they're not exported from the client
interface Thread {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
}

interface ThreadMessage {
  id: string;
  type: 'human' | 'ai';
  content: string;
  created_at: string;
}

function ChatMessage({
  message,
  deleteMessage,
}: {
  message: ThreadMessage;
  deleteMessage: ({ messageId }: { messageId: string }) => Promise<void>;
}) {
  const isUserMessage = message.type === "human";

  const DeleteButton = () => (
    <Tooltip label="Delete message" withArrow position="bottom">
      <ActionIcon
        variant="light"
        color="red"
        size="sm"
        onClick={async () => {
          await deleteMessage({ messageId: message.id });
        }}
        aria-label="Delete message"
      >
        <IconTrash style={{ width: "70%", height: "70%" }} stroke={1.5} />
      </ActionIcon>
    </Tooltip>
  );

  return (
    <Group
      gap="lg"
      align="flex-end"
      justify={isUserMessage ? "flex-end" : "flex-start"}
    >
      {!isUserMessage ? (
        <Avatar color="green" radius="xl">
          AI
        </Avatar>
      ) : null}

      {isUserMessage ? <DeleteButton /> : null}

      <Paper
        flex={1}
        maw="75%"
        shadow="none"
        radius="lg"
        p="xs"
        px="md"
        bg="var(--mantine-color-gray-0)"
      >
        <Group gap="md" justify="space-between" align="top">
          <Markdown className={classes.mdMessage}>{message.content}</Markdown>
        </Group>
      </Paper>

      {!isUserMessage ? <DeleteButton /> : null}
    </Group>
  );
}

function ChatMessageList({
  messages,
  deleteMessage,
}: {
  messages: ThreadMessage[];
  deleteMessage: ({ messageId }: { messageId: string }) => Promise<void>;
}) {
  if (messages.length === 0) {
    return <Text c="dimmed">No messages.</Text>;
  }

  return (
    <Stack gap="xl">
      {messages.map((message, index) => (
        <ChatMessage
          key={index}
          message={message}
          deleteMessage={deleteMessage}
        />
      ))}
    </Stack>
  );
}

export function Chat({ assistantId }: { assistantId: string }) {
  const [activeThread, setActiveThread] = useState<Thread | null>(null);
  const [inputValue, setInputValue] = useState<string>("");
  const { accessToken, isAuthenticated } = useAuth();

  // Log the current configuration
  useEffect(() => {
    console.log('[Chat] Component mounted/updated:', {
      assistantId,
      isAuthenticated,
      hasAccessToken: !!accessToken,
      // Try to check if the client has the config
      djangoAIAssistantConfig: (window as any).__DJANGO_AI_ASSISTANT_CONFIG__
    });
  }, [assistantId, isAuthenticated, accessToken]);

  const { fetchThreads, threads, createThread, deleteThread } = useThreadList({
    assistantId,
  });
  const {
    fetchMessages,
    messages,
    loadingFetchMessages,
    createMessage,
    loadingCreateMessage,
    deleteMessage,
    loadingDeleteMessage,
  } = useMessageList({ threadId: activeThread?.id?.toString() ?? null });

  const { fetchAssistant, assistant } = useAssistant({ assistantId });

  const loadingMessages =
    loadingFetchMessages || loadingCreateMessage || loadingDeleteMessage;
  const isThreadSelected = Boolean(activeThread);
  const isChatActive = activeThread && !loadingMessages;

  const scrollViewport = useRef<HTMLDivElement>(null);
  const scrollToBottom = useCallback(
    () =>
      // setTimeout is used because scrollViewport.current?.scrollHeight update is not
      // being triggered in time for the scrollTo method to work properly.
      setTimeout(
        () =>
          scrollViewport.current?.scrollTo({
            top: scrollViewport.current!.scrollHeight,
            behavior: "smooth",
          }),
        500
      ),
    [scrollViewport]
  );

  // Load threads and assistant details when component mounts and user is authenticated:
  useEffect(() => {
    async function loadAssistantAndThreads() {
      console.log('[Chat] loadAssistantAndThreads called:', {
        isAuthenticated,
        hasAccessToken: !!accessToken,
        accessTokenPreview: accessToken ? `${accessToken.substring(0, 20)}...` : null,
        assistantId
      });
      
      if (!isAuthenticated || !accessToken) {
        console.log('[Chat] Not authenticated, skipping load');
        return; // Don't try to load if not authenticated
      }
      
      try {
        console.log('[Chat] Fetching assistant...');
        await fetchAssistant();
        console.log('[Chat] Assistant fetched successfully');
        
        console.log('[Chat] Fetching threads...');
        await fetchThreads();
        console.log('[Chat] Threads fetched successfully');
      } catch (error) {
        console.error('[Chat] Error loading assistant and threads:', error);
        if (error instanceof Error) {
          console.error('[Chat] Error details:', {
            message: error.message,
            stack: error.stack
          });
        }
      }
    }

    loadAssistantAndThreads();
  }, [fetchThreads, fetchAssistant, isAuthenticated, accessToken]);

  // Load messages when threadId changes:
  useEffect(() => {
    console.log('[Chat] Thread changed:', {
      assistantId,
      threadId: activeThread?.id,
      hasThread: !!activeThread
    });
    
    if (!assistantId) return;
    if (!activeThread) return;

    fetchMessages();
    scrollToBottom();
  }, [assistantId, activeThread?.id, fetchMessages]);

  async function handleCreateMessage() {
    console.log('[Chat] Creating message:', {
      hasThread: !!activeThread,
      messageLength: inputValue.length
    });
    
    if (!activeThread) return;

    await createMessage({
      assistantId,
      messageTextValue: inputValue,
    });

    setInputValue("");
    scrollToBottom();
  }

  return (
    <>
      <ThreadsNav
        threads={threads}
        selectedThreadId={activeThread?.id}
        selectThread={setActiveThread}
        createThread={createThread}
        deleteThread={deleteThread}
      />
      <main className={classes.main}>
        <Container className={classes.chatContainer}>
          <Stack className={classes.chat}>
            <Title mt="md" order={2}>
              Chat: {assistant?.name || "Loading…"}
            </Title>
            <ScrollArea
              pos="relative"
              type="auto"
              h="100%"
              px="xs"
              viewportRef={scrollViewport}
            >
              <LoadingOverlay
                visible={loadingMessages}
                zIndex={1000}
                overlayProps={{ blur: 2 }}
              />
              {isThreadSelected ? (
                <ChatMessageList
                  messages={messages || []}
                  deleteMessage={deleteMessage}
                />
              ) : (
                <Text c="dimmed">
                  Select or create a thread to start chatting.
                </Text>
              )}
            </ScrollArea>
            <Textarea
              mt="auto"
              mb="3rem"
              placeholder={
                isChatActive
                  ? "Enter user message… (Ctrl↵ to send)"
                  : "Please create or select a thread on the sidebar"
              }
              autosize
              minRows={2}
              disabled={!isChatActive}
              onChange={(e) => setInputValue(e.currentTarget.value)}
              value={inputValue}
              onKeyDown={getHotkeyHandler([["mod+Enter", handleCreateMessage]])}
              rightSection={
                <Button
                  variant="filled"
                  color="teal"
                  aria-label="Send message"
                  fz="xs"
                  rightSection={
                    <IconSend2
                      stroke={1.5}
                      style={{ width: "70%", height: "70%" }}
                    />
                  }
                  disabled={!isChatActive}
                  onClick={(e) => {
                    handleCreateMessage();
                    e.preventDefault();
                  }}
                >
                  Send
                </Button>
              }
              rightSectionWidth={120}
            />
          </Stack>
        </Container>
      </main>
    </>
  );
}
