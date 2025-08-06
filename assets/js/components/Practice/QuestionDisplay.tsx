import React from 'react';
import { Paper, Text, Stack, Badge, Group, Avatar, Card, List, ThemeIcon } from '@mantine/core';
import { IconRobot, IconUser, IconCheck, IconX } from '@tabler/icons-react';
import Markdown from 'react-markdown';

interface Message {
  id: string;
  type: 'system' | 'question' | 'feedback';
  content: string;
  grade?: number;
  timestamp: Date;
}

interface QuestionDisplayProps {
  messages: Message[];
  onFeedbackMount?: (element: HTMLDivElement) => void;
}

export function QuestionDisplay({ messages, onFeedbackMount }: QuestionDisplayProps) {
  return (
    <Stack 
      gap="md" 
      style={{ 
        padding: '16px',
        paddingBottom: '16px',
        minHeight: 'fit-content',
        width: '100%',
        boxSizing: 'border-box'
      }}
    >
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
    </Stack>
  );
}

function MessageItem({ message }: { message: Message }) {
  const feedbackRef = React.useRef<HTMLDivElement>(null);
  
  React.useEffect(() => {
    if (message.type === 'feedback' && feedbackRef.current) {
      const { onFeedbackMount } = (window as any).__feedbackCallback || {};
      if (onFeedbackMount) {
        onFeedbackMount(feedbackRef.current);
      }
    }
  }, [message.type]);

  if (message.type === 'system') {
    return (
      <Group gap="sm" align="flex-start">
        <Avatar color="blue" radius="xl" size="sm">
          <IconRobot size={20} />
        </Avatar>
        <Paper 
          shadow="xs" 
          p="md" 
          radius="md" 
          style={{ 
            flex: 1,
            backgroundColor: 'var(--mantine-color-blue-0)'
          }}
        >
          <Text size="sm">{message.content}</Text>
        </Paper>
      </Group>
    );
  }

  if (message.type === 'question') {
    return (
      <Group gap="sm" align="flex-start">
        <Avatar color="teal" radius="xl" size="sm">
          <IconRobot size={20} />
        </Avatar>
        <Card shadow="sm" padding="lg" radius="md" withBorder style={{ flex: 1 }}>
          <Stack gap="sm">
            <Group justify="space-between">
              <Text fw={600}>New Question</Text>
              <Badge variant="light" color="teal">
                Practice Problem
              </Badge>
            </Group>
            <Markdown>{message.content}</Markdown>
          </Stack>
        </Card>
      </Group>
    );
  }

  if (message.type === 'feedback') {
    const gradeColor = getGradeColor(message.grade || 0);
    
    return (
      <Group gap="sm" align="flex-start" ref={feedbackRef}>
        <Avatar color="grape" radius="xl" size="sm">
          <IconRobot size={20} />
        </Avatar>
        <Card shadow="sm" padding="lg" radius="md" withBorder style={{ flex: 1 }}>
          <Stack gap="md">
            <Group justify="space-between">
              <Text fw={600}>Feedback</Text>
              {message.grade !== undefined && (
                <Badge 
                  size="lg" 
                  color={gradeColor}
                  variant="filled"
                >
                  Grade: {message.grade}/10
                </Badge>
              )}
            </Group>
            
            <FeedbackContent content={message.content} />
          </Stack>
        </Card>
      </Group>
    );
  }

  return null;
}

function FeedbackContent({ content }: { content: string }) {
  try {
    const data = JSON.parse(content);
    
    // Handle skipped questions (expectedOutput but no feedback)
    if (data.expectedOutput && data.feedback === null) {
      return (
        <Stack gap="sm">
          <div>
            <Text size="sm" fw={500} mb={4} c="blue">Solution:</Text>
            <Paper 
              p="xs" 
              radius="sm" 
              style={{ 
                backgroundColor: 'var(--mantine-color-blue-0)',
                overflowX: 'auto',
                maxWidth: '100%'
              }}
            >
              <Text 
                size="sm" 
                style={{ 
                  fontFamily: 'monospace', 
                  whiteSpace: 'pre',
                  display: 'block'
                }}
              >
                {data.expectedOutput}
              </Text>
            </Paper>
          </div>
        </Stack>
      );
    }
    
    // Handle new format with expectedOutput and feedback
    if (data.expectedOutput && data.feedback) {
      const feedback = data.feedback;
      return (
        <Stack gap="sm">
          {/* Show Expected Output first */}
          <div>
            <Text size="sm" fw={500} mb={4} c="blue">Solution:</Text>
            <Paper 
              p="xs" 
              radius="sm" 
              style={{ 
                backgroundColor: 'var(--mantine-color-blue-0)',
                overflowX: 'auto',
                maxWidth: '100%'
              }}
            >
              <Text 
                size="sm" 
                style={{ 
                  fontFamily: 'monospace', 
                  whiteSpace: 'pre',
                  display: 'block'
                }}
              >
                {data.expectedOutput}
              </Text>
            </Paper>
          </div>
          
          {/* Then show feedback */}
          <Text size="sm" fw={600}>{feedback.overall}</Text>
          
          <List size="sm" spacing="xs" mt={8}>
            {feedback.correctness && feedback.correctness.message && feedback.correctness.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Correctness (40%):</Text> {feedback.correctness.score !== undefined ? `${(feedback.correctness.score * 10).toFixed(1)} - ` : ''}{feedback.correctness.message}
                  </Text>
                  {(feedback.correctness.issues?.length > 0 || feedback.correctness.strengths?.length > 0) && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.correctness.issues?.map((issue: string, idx: number) => (
                        <List.Item key={`issue-${idx}`} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{issue}</Text>
                        </List.Item>
                      ))}
                      {feedback.correctness.strengths?.map((strength: string, idx: number) => (
                        <List.Item key={`strength-${idx}`} icon={
                          <ThemeIcon color="blue" size={16} radius="xl">
                            <IconCheck size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{strength}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
            
            {feedback.code_quality && feedback.code_quality.message && feedback.code_quality.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Code Quality (30%):</Text> {feedback.code_quality.score !== undefined ? `${(feedback.code_quality.score * 10).toFixed(1)} - ` : ''}{feedback.code_quality.message}
                  </Text>
                  {feedback.code_quality.issues?.length > 0 && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.code_quality.issues.map((issue: string, idx: number) => (
                        <List.Item key={idx} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{issue}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
            
            {feedback.efficiency && feedback.efficiency.message && feedback.efficiency.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Efficiency (20%):</Text> {feedback.efficiency.score !== undefined ? `${(feedback.efficiency.score * 10).toFixed(1)} - ` : ''}{feedback.efficiency.message}
                  </Text>
                  {(feedback.efficiency.inefficiencies?.length > 0 || feedback.efficiency.suggestions?.length > 0) && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.efficiency.inefficiencies?.map((issue: string, idx: number) => (
                        <List.Item key={`ineff-${idx}`} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{issue}</Text>
                        </List.Item>
                      ))}
                      {feedback.efficiency.suggestions?.map((suggestion: string, idx: number) => (
                        <List.Item key={`sugg-${idx}`} icon={
                          <ThemeIcon color="blue" size={16} radius="xl">
                            <IconCheck size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{suggestion}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
            
            {feedback.sophistication && feedback.sophistication.message && feedback.sophistication.message !== 'No code to evaluate.' && (
              <List.Item>
                <Stack gap={4}>
                  <Text size="sm">
                    <Text component="span" fw={500}>Sophistication (10%):</Text> {feedback.sophistication.score !== undefined ? `${(feedback.sophistication.score * 10).toFixed(1)} - ` : ''}{feedback.sophistication.message}
                  </Text>
                  {(feedback.sophistication.advanced_techniques?.length > 0 || feedback.sophistication.areas_for_improvement?.length > 0) && (
                    <List size="sm" spacing={2} ml="md">
                      {feedback.sophistication.advanced_techniques?.map((technique: string, idx: number) => (
                        <List.Item key={`tech-${idx}`} icon={
                          <ThemeIcon color="blue" size={16} radius="xl">
                            <IconCheck size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{technique}</Text>
                        </List.Item>
                      ))}
                      {feedback.sophistication.areas_for_improvement?.map((area: string, idx: number) => (
                        <List.Item key={`area-${idx}`} icon={
                          <ThemeIcon color="orange" size={16} radius="xl">
                            <IconX size={10} />
                          </ThemeIcon>
                        }>
                          <Text size="sm">{area}</Text>
                        </List.Item>
                      ))}
                    </List>
                  )}
                </Stack>
              </List.Item>
            )}
          </List>
        </Stack>
      );
    }
    
    // Handle old format (just feedback)
    const feedback = data.overall ? data : data.feedback || data;
    
    return (
      <Stack gap="sm">
        <Text size="sm" fw={600}>{feedback.overall}</Text>
        
        <List size="sm" spacing="xs" mt={8}>
          {feedback.correctness && feedback.correctness.message && feedback.correctness.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Correctness (40%):</Text> {feedback.correctness.score !== undefined ? `${(feedback.correctness.score * 10).toFixed(1)} - ` : ''}{feedback.correctness.message}
                </Text>
                {(feedback.correctness.issues?.length > 0 || feedback.correctness.strengths?.length > 0) && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.correctness.issues?.map((issue: string, idx: number) => (
                      <List.Item key={`issue-${idx}`} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{issue}</Text>
                      </List.Item>
                    ))}
                    {feedback.correctness.strengths?.map((strength: string, idx: number) => (
                      <List.Item key={`strength-${idx}`} icon={
                        <ThemeIcon color="blue" size={16} radius="xl">
                          <IconCheck size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{strength}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
          
          {feedback.code_quality && feedback.code_quality.message && feedback.code_quality.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Code Quality (30%):</Text> {feedback.code_quality.score !== undefined ? `${(feedback.code_quality.score * 10).toFixed(1)} - ` : ''}{feedback.code_quality.message}
                </Text>
                {feedback.code_quality.issues?.length > 0 && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.code_quality.issues.map((issue: string, idx: number) => (
                      <List.Item key={idx} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{issue}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
          
          {feedback.efficiency && feedback.efficiency.message && feedback.efficiency.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Efficiency (20%):</Text> {feedback.efficiency.score !== undefined ? `${(feedback.efficiency.score * 10).toFixed(1)} - ` : ''}{feedback.efficiency.message}
                </Text>
                {(feedback.efficiency.inefficiencies?.length > 0 || feedback.efficiency.suggestions?.length > 0) && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.efficiency.inefficiencies?.map((issue: string, idx: number) => (
                      <List.Item key={`ineff-${idx}`} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{issue}</Text>
                      </List.Item>
                    ))}
                    {feedback.efficiency.suggestions?.map((suggestion: string, idx: number) => (
                      <List.Item key={`sugg-${idx}`} icon={
                        <ThemeIcon color="blue" size={16} radius="xl">
                          <IconCheck size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{suggestion}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
          
          {feedback.sophistication && feedback.sophistication.message && feedback.sophistication.message !== 'No code to evaluate.' && (
            <List.Item>
              <Stack gap={4}>
                <Text size="sm">
                  <Text component="span" fw={500}>Sophistication (10%):</Text> {feedback.sophistication.score !== undefined ? `${(feedback.sophistication.score * 10).toFixed(1)} - ` : ''}{feedback.sophistication.message}
                </Text>
                {(feedback.sophistication.advanced_techniques?.length > 0 || feedback.sophistication.areas_for_improvement?.length > 0) && (
                  <List size="sm" spacing={2} ml="md">
                    {feedback.sophistication.advanced_techniques?.map((technique: string, idx: number) => (
                      <List.Item key={`tech-${idx}`} icon={
                        <ThemeIcon color="blue" size={16} radius="xl">
                          <IconCheck size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{technique}</Text>
                      </List.Item>
                    ))}
                    {feedback.sophistication.areas_for_improvement?.map((area: string, idx: number) => (
                      <List.Item key={`area-${idx}`} icon={
                        <ThemeIcon color="orange" size={16} radius="xl">
                          <IconX size={10} />
                        </ThemeIcon>
                      }>
                        <Text size="sm">{area}</Text>
                      </List.Item>
                    ))}
                  </List>
                )}
              </Stack>
            </List.Item>
          )}
        </List>
      </Stack>
    );
  } catch {
    return <Text size="sm">{content}</Text>;
  }
}

function getGradeColor(grade: number): string {
  if (grade >= 9) return 'green';
  if (grade >= 7) return 'lime';
  if (grade >= 5) return 'yellow';
  if (grade >= 3) return 'orange';
  return 'red';
} 