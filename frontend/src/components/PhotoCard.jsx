import { useState, useEffect } from 'react';

export default function PhotoCard({ photo, isOwner, onDm, onUpdate }) {
  const [editing, setEditing] = useState(false);
  const [description, setDescription] = useState(photo.description || '');
  const [keywords, setKeywords] = useState(photo.keywords || '');

  useEffect(() => {
    setDescription(photo.description || '');
    setKeywords(photo.keywords || '');
  }, [photo.description, photo.keywords]);

  const handleSave = () => {
    onUpdate(photo.id, description, keywords);
    setEditing(false);
  };

  return (
    <div className="photo-card">
      <img
        src={`http://localhost:8000${photo.image_url}`}
        alt={photo.description || '사진'}
      />
      <div className="photo-info">
        <span className="photo-user">@{photo.username}</span>
        {editing ? (
          <>
            <input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="설명"
            />
            <input
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="키워드 (쉼표로 구분)"
            />
            <div className="card-actions">
              <button onClick={handleSave}>저장</button>
              <button className="btn-secondary" onClick={() => setEditing(false)}>취소</button>
            </div>
          </>
        ) : (
          <>
            {photo.description && <p>{photo.description}</p>}
            {photo.keywords && <p className="keywords">#{photo.keywords}</p>}
            <div className="card-actions">
              {isOwner ? (
                <button className="btn-secondary" onClick={() => setEditing(true)}>수정</button>
              ) : (
                <button onClick={onDm}>DM</button>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
