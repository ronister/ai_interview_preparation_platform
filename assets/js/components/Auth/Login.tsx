import React, { useState } from 'react';
import {
  TextInput,
  PasswordInput,
  Button,
  Paper,
  Title,
  Text,
  Container,
  Group,
  Anchor,
  Center,
  Box,
  LoadingOverlay,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconUser, IconLock } from '@tabler/icons-react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link, useLocation } from 'react-router-dom';

export function Login() {
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const form = useForm({
    initialValues: {
      username: '',
      password: '',
    },
    validate: {
      username: (value: string) => (!value ? 'Username is required' : null),
      password: (value: string) => (!value ? 'Password is required' : null),
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    setIsLoading(true);
    try {
      await login(values.username, values.password);
      // Always navigate to home page after login
      navigate('/', { replace: true });
    } catch (error) {
      // Error is handled in AuthContext
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container size={420} my={40}>
      <Title
        ta="center"
        style={{
          fontFamily: `Greycliff CF, sans-serif`,
          fontWeight: 900,
        }}
      >
        Welcome back!
      </Title>
      <Text c="dimmed" size="sm" ta="center" mt={5}>
        Do not have an account yet?{' '}
        <Anchor component={Link} to="/register" size="sm">
          Create account
        </Anchor>
      </Text>

      <Paper withBorder shadow="md" p={30} mt={30} radius="md" pos="relative">
        <LoadingOverlay visible={isLoading} />
        
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <TextInput
            label="Username"
            placeholder="Your username"
            leftSection={<IconUser size={16} />}
            required
            {...form.getInputProps('username')}
          />
          
          <PasswordInput
            label="Password"
            placeholder="Your password"
            leftSection={<IconLock size={16} />}
            required
            mt="md"
            {...form.getInputProps('password')}
          />
          
          <Group justify="apart" mt="lg">
            <Anchor component={Link} to="/forgot-password" size="sm">
              Forgot password?
            </Anchor>
          </Group>
          
          <Button fullWidth mt="xl" type="submit" disabled={isLoading}>
            Sign in
          </Button>
        </form>
      </Paper>
    </Container>
  );
} 