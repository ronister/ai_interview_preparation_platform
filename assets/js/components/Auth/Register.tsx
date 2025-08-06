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
  LoadingOverlay,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconUser, IconLock, IconMail } from '@tabler/icons-react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export function Register() {
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const form = useForm({
    initialValues: {
      username: '',
      email: '',
      password: '',
      password2: '',
      first_name: '',
      last_name: '',
    },
    validate: {
      username: (value: string) => {
        if (!value) return 'Username is required';
        if (value.length < 3) return 'Username must be at least 3 characters';
        return null;
      },
      email: (value: string) => {
        if (!value) return 'Email is required';
        if (!/^\S+@\S+$/.test(value)) return 'Invalid email';
        return null;
      },
      password: (value: string) => {
        if (!value) return 'Password is required';
        if (value.length < 8) return 'Password must be at least 8 characters';
        return null;
      },
      password2: (value: string, values: any) => {
        if (!value) return 'Please confirm your password';
        if (value !== values.password) return 'Passwords do not match';
        return null;
      },
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    setIsLoading(true);
    try {
      await register(values);
      navigate('/');
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
        Create an account
      </Title>
      <Text c="dimmed" size="sm" ta="center" mt={5}>
        Already have an account?{' '}
        <Anchor component={Link} to="/login" size="sm">
          Sign in
        </Anchor>
      </Text>

      <Paper withBorder shadow="md" p={30} mt={30} radius="md" pos="relative">
        <LoadingOverlay visible={isLoading} />
        
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Group grow>
            <TextInput
              label="First name"
              placeholder="Your first name"
              {...form.getInputProps('first_name')}
            />
            
            <TextInput
              label="Last name"
              placeholder="Your last name"
              {...form.getInputProps('last_name')}
            />
          </Group>

          <TextInput
            label="Username"
            placeholder="Choose a username"
            leftSection={<IconUser size={16} />}
            required
            mt="md"
            {...form.getInputProps('username')}
          />
          
          <TextInput
            label="Email"
            placeholder="your@email.com"
            leftSection={<IconMail size={16} />}
            required
            mt="md"
            {...form.getInputProps('email')}
          />
          
          <PasswordInput
            label="Password"
            placeholder="Create a password"
            leftSection={<IconLock size={16} />}
            required
            mt="md"
            {...form.getInputProps('password')}
          />
          
          <PasswordInput
            label="Confirm password"
            placeholder="Confirm your password"
            leftSection={<IconLock size={16} />}
            required
            mt="md"
            {...form.getInputProps('password2')}
          />
          
          <Button fullWidth mt="xl" type="submit" disabled={isLoading}>
            Create account
          </Button>
        </form>
      </Paper>
    </Container>
  );
} 