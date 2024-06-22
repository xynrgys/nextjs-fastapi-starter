import { GetServerSideProps } from 'next';
import Cookies from 'js-cookie';
import jwt from 'jsonwebtoken';

export const getServerSideProps: GetServerSideProps = async (context) => {
  const token = Cookies.get('token', { req: context.req });

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

    return {
      props: {
        user,
      },
    };
  } catch (error) {
    return {
      redirect: {
        destination: '/signin',
        permanent: false,
      },
    };
  }
};

export default function DashboardPage({ user }) {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user.email}!</p>
      {/* Render private content */}
    </div>
  );
}