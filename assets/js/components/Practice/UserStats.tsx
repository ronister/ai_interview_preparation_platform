import React from 'react';
import { Paper, Group, Text, Stack, Badge, Slider, Box } from '@mantine/core';
import { IconUser, IconTrophy, IconTarget, IconChartBar, IconCheck, IconStar, IconAdjustments } from '@tabler/icons-react';

interface UserStatsProps {
  username: string;
  currentLevel: number;
  manualLevel: number;
  totalQuestions: number;
  correctAnswers: number;
  successRate: number;
  averageGrade: number;
  onLevelChange: (level: number) => void;
  disabled?: boolean;
}

export function UserStats({ 
  username, 
  currentLevel, 
  manualLevel, 
  totalQuestions, 
  correctAnswers, 
  successRate, 
  averageGrade, 
  onLevelChange,
  disabled = false
}: UserStatsProps) {
  return (
    <Paper 
      shadow="sm" 
      radius="md" 
      p="md" 
      withBorder
      style={{ backgroundColor: 'var(--mantine-color-gray-0)', minWidth: '380px' }}
    >
      <Stack gap="md">
        <Group justify="space-between" wrap="nowrap">
          <Group gap="xs">
            <IconUser size={20} style={{ color: 'var(--mantine-color-blue-6)' }} />
            <Text fw={600} size="sm">{username}</Text>
          </Group>
          <Box style={{ minWidth: 160 }}>
            <Group gap="xs" justify="flex-end">
              <IconAdjustments size={16} style={{ color: disabled ? 'var(--mantine-color-gray-4)' : 'var(--mantine-color-gray-6)' }} />
              <Text size="xs" c={disabled ? 'dimmed' : 'dimmed'}>Difficulty Level</Text>
            </Group>
            <Slider
              value={manualLevel}
              onChange={disabled ? () => {} : onLevelChange}
              min={1}
              max={5}
              step={1}
              size="sm"
              color={disabled ? 'gray' : getLevelColor(manualLevel)}
              marks={[
                { value: 1, label: '1' },
                { value: 2, label: '2' },
                { value: 3, label: '3' },
                { value: 4, label: '4' },
                { value: 5, label: '5' },
              ]}
              styles={{
                mark: { fontSize: '15px' },
                markLabel: { fontSize: '15px' },
                thumb: {
                  backgroundColor: disabled ? 'white' : undefined,
                  borderColor: disabled ? 'var(--mantine-color-gray-4)' : undefined,
                  cursor: disabled ? 'not-allowed' : 'pointer',
                  width: '14px',
                  height: '14px',
                  border: disabled ? '2px solid var(--mantine-color-gray-4)' : undefined
                },
                track: disabled ? {
                  backgroundColor: 'var(--mantine-color-gray-3)',
                  cursor: 'not-allowed'
                } : undefined,
                bar: disabled ? {
                  backgroundColor: 'var(--mantine-color-gray-4)',
                } : undefined,
                root: disabled ? {
                  cursor: 'not-allowed'
                } : undefined
              }}
            />
          </Box>
        </Group>
        
        <Stack gap="sm" style={{ paddingTop: '18px', paddingBottom: '4px' }}>
          <Group gap="lg" justify="space-between">
            <Group gap="xs">
              <IconTarget size={18} style={{ color: 'var(--mantine-color-gray-6)' }} />
              <Text size="sm" c="dimmed">Questions: {totalQuestions}</Text>
            </Group>
            <Group gap="xs">
              <IconCheck size={18} style={{ color: 'var(--mantine-color-green-6)' }} />
              <Text size="sm" c="dimmed">Correct: {correctAnswers}</Text>
            </Group>
          </Group>
          <Group gap="lg" justify="space-between">
            <Group gap="xs">
              <IconChartBar size={18} style={{ color: 'var(--mantine-color-gray-6)' }} />
              <Text size="sm" c="dimmed">Success: {successRate}%</Text>
            </Group>
            <Group gap="xs">
              <IconStar size={18} style={{ color: 'var(--mantine-color-yellow-6)' }} />
              <Text size="sm" c="dimmed">Average Grade: {averageGrade.toFixed(1)}/10</Text>
            </Group>
          </Group>
        </Stack>
      </Stack>
    </Paper>
  );
}

function getLevelColor(level: number): string {
  switch (level) {
    case 1:
      return 'green';
    case 2:
      return 'lime';
    case 3:
      return 'yellow';
    case 4:
      return 'orange';
    case 5:
      return 'red';
    default:
      return 'gray';
  }
} 