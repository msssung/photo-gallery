import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import './UploadPage.css';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState('');
  const [keywords, setKeywords] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('파일을 선택해주세요.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('description', description);
    formData.append('keywords', keywords);

    try {
      await api.post('/api/photos', formData);
      navigate('/main');
    } catch {
      setError('업로드에 실패했습니다.');
    }
  };

  return (
    <div className="upload-page-bg">
      <div className="auth-container upload-page">
        <h2>사진 업로드</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <input
            type="text"
            placeholder="설명"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <input
            type="text"
            placeholder="키워드 (쉼표로 구분, 예: 여행,풍경,바다)"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
          />
          {error && <p className="error">{error}</p>}
          <button type="submit">업로드</button>
          <button type="button" className="btn-secondary" onClick={() => navigate('/main')}>
            취소
          </button>
        </form>
      </div>
    </div>
  );
}
