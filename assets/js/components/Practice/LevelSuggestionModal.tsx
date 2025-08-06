import React from 'react';
import { Modal, Text, Group, Button, Stack, Alert } from '@mantine/core';
import { IconTrendingUp, IconTrendingDown, IconInfoCircle } from '@tabler/icons-react';

interface LevelSuggestion {
  type: 'level_up' | 'level_down';
  current_level: number;
  suggested_level: number;
  reason: string;
}

interface LevelSuggestionModalProps {
  isOpen: boolean;
  suggestion: LevelSuggestion | null;
  onAccept: () => void;
  onDecline: () => void;
  onClose: () => void;
}

export function LevelSuggestionModal({ 
  isOpen, 
  suggestion, 
  onAccept, 
  onDecline, 
  onClose 
}: LevelSuggestionModalProps) {
  if (!suggestion) return null;

  const isLevelUp = suggestion.type === 'level_up';
  const icon = isLevelUp ? <IconTrendingUp size={24} /> : <IconTrendingDown size={24} />;
  const color = isLevelUp ? 'green' : 'orange';
  const title = isLevelUp ? 'Level Up Suggestion' : 'Level Down Suggestion';

  return (
    <Modal
      opened={isOpen}
      onClose={onClose}
      title={title}
      size="sm"
      centered
      withCloseButton={false}
      closeOnClickOutside={false}
      closeOnEscape={false}
    >
      <Stack gap="md">
        <Alert
          icon={icon}
          color={color}
          variant="light"
        >
          <Text size="sm">
            {suggestion.reason}
          </Text>
        </Alert>

        <Stack gap="xs">
          <Text size="sm" fw={500}>
            Would you like to change your difficulty level?
          </Text>
          <Group gap="xs">
            <Text size="sm" c="dimmed">
              Current Level: {suggestion.current_level}
            </Text>
            <Text size="sm" c="dimmed">
              →
            </Text>
            <Text size="sm" c="dimmed">
              Suggested Level: {suggestion.suggested_level}
            </Text>
          </Group>
        </Stack>

        <Group justify="flex-end" gap="sm">
          <Button
            variant="light"
            color="gray"
            onClick={onDecline}
            size="sm"
          >
            Keep Current Level
          </Button>
          <Button
            color={color}
            onClick={onAccept}
            size="sm"
          >
            {isLevelUp ? 'Level Up' : 'Level Down'}
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
} 