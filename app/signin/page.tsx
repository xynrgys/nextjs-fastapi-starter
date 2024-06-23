'use client';

import { useState } from 'react';
import { createClient } from '@supabase/supabase-js'
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const supabaseClient = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_KEY!
    );

    const { error } = await supabaseClient.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      console.error('Sign-in failed:', error.message);
    } else {
      const { data: { session } } = await supabaseClient.auth.getSession();
      if (session) {
        Cookies.set('access_token', session.access_token);
        router.push('/dashboard');
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md p-8 bg-white rounded shadow-md">
        <h2 className="mb-6 text-2xl text-black font-semibold text-center">Sign In</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-600">
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 text-sm text-black border rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-600"
              placeholder="Enter your email"
              required
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-600">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 text-sm text-black border rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-600"
              placeholder="Enter your password"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}
