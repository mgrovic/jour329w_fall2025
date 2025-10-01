import React, { useState, useEffect } from "react";
import './index.css';

const TAGS_JSON_PATH = "/workspaces/jour329w_fall2025/data/tags.json";

function App() {
  const [tags, setTags] = useState([]);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("alpha");
  const [selectedTag, setSelectedTag] = useState(null);
  const [categoryFilter, setCategoryFilter] = useState("");

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

  // Get all unique categories for filter dropdown
  const categories = Array.from(new Set(tags.map(tag => tag.category).filter(Boolean)));

  // Filter and sort logic
  const filteredTags = tags
    .filter((tag) => {
      const matchesSearch = tag.name.toLowerCase().includes(search.toLowerCase());
      const matchesCategory = categoryFilter ? tag.category === categoryFilter : true;
      return matchesSearch && matchesCategory;
    })
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
      // If sorting by category, sort tags by category name
      if (categoryFilter) {
        return 0; // No sort, just filter
      }
      return 0;
    });

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <header className="sticky top-0 z-20 bg-white shadow-md border-b border-gray-200 py-4 mb-8">
        <div className="max-w-6xl mx-auto flex flex-col items-center">
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-1">CNS Tag Browser</h1>
          <span className="text-sm text-gray-600 font-medium">Capital News Service Data Viewer</span>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4">
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
            onChange={e => setSort(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="alpha">Alphabetical</option>
            <option value="count">By Frequency</option>
          </select>
          <select
            value={categoryFilter}
            onChange={e => setCategoryFilter(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredTags.map((tag) => {
            return (
              <div
                key={tag.id}
                className="border-2 border-yellow-400 bg-gradient-to-br from-blue-50 via-yellow-100 to-white rounded-xl shadow-lg p-5 flex flex-col gap-2 cursor-pointer hover:border-blue-500 hover:bg-yellow-50 transition-all duration-150"
                onClick={() => setSelectedTag(tag)}
              >
                <div className="font-bold text-lg text-blue-800 mb-1">{tag.name}</div>
                <div className="flex flex-col sm:flex-row gap-2 mb-2">
                  <span className="inline-block px-2 py-1 rounded bg-yellow-300 text-yellow-900 text-xs font-semibold">{tag.category || 'Unknown'}</span>
                  <span className="inline-block px-2 py-1 rounded bg-blue-200 text-blue-900 text-xs font-semibold">Posts: {tag.count}</span>
                </div>
                {Array.isArray(tag.links) && tag.links.length > 0 ? (
                  <div className="flex flex-col gap-1 mt-2">
                    {tag.links.map((link, i) => (
                      <a
                        key={i}
                        href={link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 underline text-xs hover:text-yellow-700"
                      >
                        View Tag {i + 1}
                      </a>
                    ))}
                  </div>
                ) : tag.link ? (
                  <a
                    href={tag.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline text-xs hover:text-yellow-700"
                  >
                    View Tag
                  </a>
                ) : null}
              </div>
            );
          })}
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
              {/* Description removed as requested */}
              <div className="mb-2">Posts: {selectedTag.count}</div>
              {Array.isArray(selectedTag.links) && selectedTag.links.length > 0 ? (
                <div className="flex flex-col gap-1 mt-2">
                  {selectedTag.links.map((link, i) => (
                    <a
                      key={i}
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 underline"
                    >
                      Go to Tag Page {i + 1}
                    </a>
                  ))}
                </div>
              ) : selectedTag.link ? (
                <a
                  href={selectedTag.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 underline"
                >
                  Go to Tag Page
                </a>
              ) : null}
            </div>
          </div>
        )}
        </main>
    </div>
  );
}

export default App;
