"use client";

import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input
        type="text"
        placeholder="Axtar..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-2 rounded mr-2"
      />
      <button type="submit" className="bg-blue-600 text-white p-2 rounded">
        Axtar
      </button>
    </form>
  );
}
