import Cookies from 'js-cookie';
import jwt from 'jsonwebtoken';

export default async function DashboardPage() {
  const token = Cookies.get('token');

  if (!token) {
    return {
      redirect: {
        destination: '/signin',
        permanent: false,
      },
    };
  }

  try {
    const decoded = jwt.verify(token, 'your_secret_key');
    const user = decoded.user; // Assuming the JWT payload contains user information

    return (
      <div>
        <h1>Dashboard</h1>
        <p>Welcome, {user.email}!</p>
        {/* Render private content */}
      </div>
    );
  } catch (error) {
    return {
      redirect: {
        destination: '/signin',
        permanent: false,
      },
    };
  }
}
