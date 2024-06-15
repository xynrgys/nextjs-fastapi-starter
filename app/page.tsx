import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded shadow-md">
        <h2 className="mb-6 text-2xl font-semibold text-center">Welcome to Our Site</h2>
        <p className="mb-4 text-center">To get started, please sign up.</p>
        <div className="flex justify-center">
          <Link href="/signup">
            <a className="px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
              Sign Up
            </a>
          </Link>
        </div>
      </div>
    </div>
  );
}
