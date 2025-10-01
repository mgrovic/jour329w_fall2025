import React, { useState, useEffect } from "react";
import './index.css';

const TAGS_JSON_PATH = "/workspaces/jour329w_fall2025/data/tags.json";

function App() {
  const [tags, setTags] = useState([]);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("alpha");
  const [selectedTag, setSelectedTag] = useState(null);

  useEffect(() => {
    // Try to fetch tags.json from public directory
    fetch("/tags.json")
      .then((res) => {
        if (!res.ok) throw new Error("tags.json not found");
        return res.json();
      })
      .then((data) => setTags(data))
      .catch(() => {
        // If not found, try absolute path (for dev only)
        fetch("/workspaces/jour329w_fall2025/data/tags.json")
          .then((res) => {
            if (!res.ok) throw new Error("tags.json not found");
            return res.json();
          })
          .then((data) => setTags(data))
          .catch(() => setTags([]));
      });
  }, []);

  // Filter and sort logic
  const filteredTags = tags
    .filter((tag) =>
      tag.name.toLowerCase().includes(search.toLowerCase())
    )
    .sort((a, b) => {
      if (sort === "alpha") {
        // Move tags starting with non-letters to the bottom
        const getSortKey = (name) => {
          const firstChar = name.trim()[0]?.toLowerCase() || '';
          return /^[a-z]/.test(firstChar) ? firstChar : 'zzzz' + firstChar;
        };
        const keyA = getSortKey(a.name);
        const keyB = getSortKey(b.name);
        if (keyA === keyB) {
          return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
        }
        return keyA.localeCompare(keyB);
      } else if (sort === "count") {
        return b.count - a.count;
      }
      return 0;
    });

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-4 text-center">CNS Tag Browser</h1>
        <div className="flex flex-col md:flex-row gap-2 mb-4">
          <input
            type="text"
            placeholder="Search tags..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border rounded px-3 py-2 flex-1"
          />
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="alpha">Alphabetical</option>
            <option value="count">By Frequency</option>
          </select>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredTags.map((tag) => (
            <div
              key={tag.id}
              className="bg-white rounded shadow p-4 cursor-pointer hover:bg-blue-50"
              onClick={() => setSelectedTag(tag)}
            >
              <div className="font-semibold text-lg">{tag.name}</div>
              <div className="text-sm text-gray-600">{tag.description || "No description"}</div>
              <div className="text-xs text-gray-400">Posts: {tag.count}</div>
              <a
                href={tag.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline text-xs"
              >
                View Tag
              </a>
            </div>
          ))}
        </div>
        {selectedTag && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
            <div className="bg-white rounded shadow-lg p-6 max-w-md w-full relative">
              <button
                className="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
                onClick={() => setSelectedTag(null)}
              >
                &times;
              </button>
              <h2 className="text-xl font-bold mb-2">{selectedTag.name}</h2>
              <p className="mb-2">{selectedTag.description || "No description available."}</p>
              <div className="mb-2">Posts: {selectedTag.count}</div>
              <a
                href={selectedTag.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline"
              >
                Go to Tag Page
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
