'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  signUp: async () => {},
  signIn: async () => {},
  signOut: () => {},
});

/**
 * ❗ IMPORTANT
 * FastAPI backend port (NOT Next.js)
 */
const API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');

    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  /**
   * 🔐 SIGNUP
   */
  const signUp = async (name: string, email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    });

    const contentType = response.headers.get('content-type');

    if (!contentType?.includes('application/json')) {
      const text = await response.text();
      console.error('Non-JSON response:', text);
      throw new Error('Backend JSON response nahi de raha');
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Signup failed');
    }

    const userData: User = {
      id: data.user_id,
      email: data.email,
      name: data.name,
    };

    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', data.access_token);
    setUser(userData);
  };

  /**
   * 🔐 LOGIN
   */
  const signIn = async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const contentType = response.headers.get('content-type');

    if (!contentType?.includes('application/json')) {
      const text = await response.text();
      console.error('Non-JSON response:', text);
      throw new Error('Backend JSON response nahi de raha');
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Login failed');
    }

    const userData: User = {
      id: data.user_id,
      email: data.email,
      name: data.name,
    };

    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', data.access_token);
    setUser(userData);
  };

  const signOut = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, signUp, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
