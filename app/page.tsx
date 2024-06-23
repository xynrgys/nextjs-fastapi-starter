import Image from "next/image";
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-3xl text-white font-semibold mb-6">Welcome to SerpentAPI</h1>
        <p className="text-lg text-gray-600 mb-6">Explore and enjoy the features of our comprehensive API services.</p>
        <div className="space-x-4">
          <Link href="/signin">
            <a className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition duration-200">Sign In</a>
          </Link>
          <Link href="/signup">
            <a className="inline-block px-6 py-3 bg-green-600 text-white rounded-lg text-sm font-semibold hover:bg-green-700 transition duration-200">Sign Up</a>
          </Link>
        </div>
      </div>
    </div>
  );
}