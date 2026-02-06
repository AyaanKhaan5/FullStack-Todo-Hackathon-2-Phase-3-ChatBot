'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Mail, Lock, User, ArrowRight } from 'lucide-react';

import { useAuth } from '@/contexts/AuthContext';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Card, {
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/Card';
import { fadeVariants, slideUpVariants } from '@/lib/animations';

export default function SignupPage() {
  const router = useRouter();
  const { user, signUp } = useAuth();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      router.replace('/tasks');
    }
  }, [user, router]);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await signUp(name, email, password);
      router.push('/tasks');
    } catch (err: any) {
      setError(err.message || 'Failed to sign up');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-background-primary px-4">
      <motion.div
        className="w-full max-w-md"
        variants={fadeVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={slideUpVariants} className="text-center mb-8">
          <h1 className="text-3xl font-bold gradient-text">Todo App</h1>
          <p className="text-text-secondary mt-1">
            Create your account
          </p>
        </motion.div>

        <motion.div variants={slideUpVariants}>
          <Card variant="elevated" className="p-8">
            <CardHeader className="px-0 pt-0">
              <CardTitle>Create Account</CardTitle>
              <CardDescription>
                Sign up to start managing tasks
              </CardDescription>
            </CardHeader>

            <CardContent className="px-0 pb-0">
              {error && (
                <div className="mb-4 p-3 rounded-md bg-red-500/10 border border-red-500/20">
                  <p className="text-sm text-red-500">{error}</p>
                </div>
              )}

              <form onSubmit={handleSignup} className="space-y-5">
                <Input
                  label="Name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  leftIcon={<User size={18} />}
                  required
                />

                <Input
                  label="Email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  leftIcon={<Mail size={18} />}
                  required
                />

                <Input
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  leftIcon={<Lock size={18} />}
                  helperText="Minimum 8 characters"
                  minLength={8}
                  required
                />

                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  isLoading={loading}
                  rightIcon={!loading ? <ArrowRight size={18} /> : undefined}
                  className="w-full"
                >
                  Create Account
                </Button>
              </form>

              <div className="text-center mt-6 text-sm text-text-muted">
                Already have an account?{' '}
                <Link href="/auth/login" className="text-primary">
                  Sign in
                </Link>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>
    </main>
  );
}
