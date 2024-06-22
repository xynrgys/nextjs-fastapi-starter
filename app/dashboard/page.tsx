'use client'

import Cookies from 'js-cookie';
import { useEffect, useState } from 'react';

interface User {
  email: string;
  // Add any other properties you expect in the user data
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const accessToken = Cookies.get('access_token');

    if (!accessToken) {
      window.location.href = '/signin';
      return;
    }

    const fetchUserData = async () => {
      try {
        const isProduction = process.env.NODE_ENV === 'production';
        const baseUrl = isProduction ? '' : 'http://127.0.0.1:8000';
        const protectedUrl = `${baseUrl}/api/protected`;

        const response = await fetch(protectedUrl, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data.user);
        } else {
          // Handle unauthorized access
          window.location.href = '/signin';
        }
      } catch (error) {
        console.error('Failed to fetch user data:', error);
        window.location.href = '/signin';
      }
    };

    fetchUserData();
  }, []);

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
