import React, { useState, useEffect } from "react";
import './index.css';
import './custom-modern.css';

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
          return /^[a-z]/.test(firstChar) ? name.toLowerCase() : 'zzzz' + name.toLowerCase();
        };
        return getSortKey(a.name).localeCompare(getSortKey(b.name));
      } else if (sort === "count") {
        return b.count - a.count;
      }
      return 0;
    });

  return (
    <div>
      <header>
        <span className="text-sm text-yellow-700 font-medium">Capital News Service Data Viewer</span>
      </header>
      <main className="main-content">
        <div className="flex flex-col md:flex-row gap-2 mb-4" style={{ position: 'relative' }}>
          <button
            className="sort-dropdown"
            style={{ background: '#6366f1', color: '#fff', fontWeight: 700, borderRadius: '0.5rem', padding: '0.5rem 1rem', border: 'none', fontSize: '1rem', cursor: 'pointer', boxShadow: '0 2px 8px rgba(99,102,241,0.12)' }}
            onClick={() => {
              let sourceTags = filteredTags.length > 0 ? filteredTags : tags;
              if (sourceTags.length > 0) {
                const randomIdx = Math.floor(Math.random() * sourceTags.length);
                const tag = sourceTags[randomIdx];
                setSelectedTag(tag);
              } else {
                alert('No tags available to select.');
              }
            }}
          >
            🎲 Random Tag
          </button>
          <input
            type="text"
            placeholder="Search tags..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="search-bar"
          />
          <select
            value={sort}
            onChange={e => setSort(e.target.value)}
            className="sort-dropdown"
          >
            <option value="alpha">Alphabetical</option>
            <option value="count">By Frequency</option>
          </select>
          <select
            value={categoryFilter}
            onChange={e => setCategoryFilter(e.target.value)}
            className="sort-dropdown"
          >
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          {selectedTag && (
            <div style={{ position: 'absolute', top: '110%', left: 0, zIndex: 20 }}>
              <div className="bg-white rounded shadow-lg p-6 max-w-md w-80 relative border border-gray-200" style={{ minWidth: '320px' }}>
                <button
                  className="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
                  onClick={() => setSelectedTag(null)}
                  style={{ fontSize: '1.5rem', fontWeight: 'bold', background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  &times;
                </button>
                <h2 className="text-xl font-bold mb-2">{selectedTag.name}</h2>
                <div className="mb-2">Posts: {selectedTag.count}</div>
                <div className="mb-2">Category: {selectedTag.category || 'Unknown'}</div>
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
                ) : null}
              </div>
            </div>
          )}
        </div>
        <div>
          {filteredTags.map((tag) => (
            <div
              key={tag.id}
              className="tag-card cursor-pointer"
              onClick={() => setSelectedTag(tag)}
            >
              <div className="tag-title">{tag.name}</div>
              <div className="tag-meta">
                <span className="tag-category">{tag.category || 'Unknown'}</span>
                <span className="tag-count">Posts: {tag.count}</span>
              </div>
              <div className="tag-links">
                {Array.isArray(tag.links) && tag.links.length > 0 ? (
                  tag.links.map((link, i) => (
                    <a
                      key={i}
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View Tag {i + 1}
                    </a>
                  ))
                ) : tag.link ? (
                  <a
                    href={tag.link}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View Tag
                  </a>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      </main>

    </div>
  );
}

export default App;
