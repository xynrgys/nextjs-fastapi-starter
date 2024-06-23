'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js'
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const accessToken = Cookies.get('access_token');

    if (!accessToken) {
      router.push('/signin');
      return;
    }

    const supabaseClient = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_KEY!
    );

    const fetchUserData = async () => {
      const { data: { user } } = await supabaseClient.auth.getUser(accessToken);
      setUser(user);
    };

    fetchUserData();
  }, [router]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user.email}!</p>
      {/* Render private content */}
    </div>
  );
}
