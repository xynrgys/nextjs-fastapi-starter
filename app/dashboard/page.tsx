import Cookies from 'js-cookie';

export default async function DashboardPage() {
  const accessToken = Cookies.get('access_token');

  if (!accessToken) {
    return {
      redirect: {
        destination: '/signin',
        permanent: false,
      },
    };
  }

  try {
    const response = await fetch('/api/protected', {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (response.ok) {
      const data = await response.json();
      return (
        <div>
          <h1>Dashboard</h1>
          <p>{data.message}</p>
          {/* Render private content */}
        </div>
      );
    } else {
      // Handle unauthorized access
      return {
        redirect: {
          destination: '/signin',
          permanent: false,
        },
      };
    }
  } catch (error) {
    console.error('Failed to fetch protected data:', error);
    return {
      redirect: {
        destination: '/signin',
        permanent: false,
      },
    };
  }
}
