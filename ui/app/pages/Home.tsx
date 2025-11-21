import { useState } from "react";

export default function Home() {
  const [apiResponse, setApiResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchFromApi = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000");
      const data = await response.json();
      setApiResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      setApiResponse(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-center p-4">
      <h1 className="text-2xl">Case Management</h1>

      <div className="mt-6">
        <button
          onClick={fetchFromApi}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? "Loading..." : "Fetch from API"}
        </button>

        {apiResponse && (
          <pre className="mt-4 p-4 bg-gray-100 rounded text-left inline-block">
            {apiResponse}
          </pre>
        )}
      </div>
    </div>
  );
}
