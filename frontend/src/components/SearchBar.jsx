import { useState } from 'react';

export default function SearchBar({ onSearch }) {
  const [keyword, setKeyword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(keyword);
  };

  const handleClear = () => {
    setKeyword('');
    onSearch('');
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="키워드로 검색"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
      />
      <button type="submit">검색</button>
      {keyword && (
        <button type="button" className="btn-secondary" onClick={handleClear}>
          전체보기
        </button>
      )}
    </form>
  );
}
