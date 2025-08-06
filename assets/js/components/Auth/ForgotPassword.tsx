import React from 'react';
import {
  Container,
  Paper,
  Title,
  Text,
  Button,
  Center,
  Box,
  ThemeIcon,
  Stack,
  Anchor,
} from '@mantine/core';
import { IconMail, IconArrowLeft } from '@tabler/icons-react';
import { Link } from 'react-router-dom';

export function ForgotPassword() {
  // For now, we'll use hardcoded email. This would be fetched from the backend
  const adminEmail = 'roni.shternberg@gmail.com';

  return (
    <Container size={420} my={40}>
      <Button
        component={Link}
        to="/login"
        variant="subtle"
        leftSection={<IconArrowLeft size={16} />}
        mb="xl"
      >
        Back to login
      </Button>

      <Paper withBorder shadow="lg" p={40} radius="md">
        <Center mb="xl">
          <ThemeIcon
            size={64}
            radius="xl"
            variant="light"
            color="blue"
          >
            <IconMail size={32} />
          </ThemeIcon>
        </Center>

        <Title
          order={2}
          ta="center"
          style={{
            fontFamily: `Greycliff CF, sans-serif`,
            fontWeight: 700,
          }}
          mb="md"
        >
          Password Reset
        </Title>

        <Stack spacing="md">
          <Text ta="center" c="dimmed" size="lg">
            Forgot password is not implemented yet.
          </Text>
          
          <Text ta="center" size="md">
            Please contact the site admin at{' '}
            <Anchor href={`mailto:${adminEmail}`} fw={500}>
              {adminEmail}
            </Anchor>
          </Text>
        </Stack>

        <Box mt="xl">
          <Text ta="center" size="sm" c="dimmed">
            We apologize for the inconvenience.
          </Text>
        </Box>
      </Paper>
    </Container>
  );
} 