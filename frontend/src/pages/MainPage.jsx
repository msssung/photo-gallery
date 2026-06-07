import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import PhotoCard from '../components/PhotoCard';
import SearchBar from '../components/SearchBar';
import './MainPage.css';

export default function MainPage() {
  const [photos, setPhotos] = useState([]);
  const [users, setUsers] = useState([]);
  const [dmTarget, setDmTarget] = useState(null);
  const [dmContent, setDmContent] = useState('');
  const navigate = useNavigate();

  const isLoggedIn = !!localStorage.getItem('access_token');
  const currentUserId = parseInt(localStorage.getItem('user_id'));
  const currentUsername = localStorage.getItem('username');

  useEffect(() => {
    fetchPhotos();
    fetchUsers();
  }, []);

  const fetchPhotos = async () => {
    try {
      const res = await api.get('/api/photos');
      setPhotos(res.data);
    } catch {
      setPhotos([]);
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await api.get('/api/users');
      setUsers(res.data);
    } catch {
      setUsers([]);
    }
  };

  const handleSearch = async (keyword) => {
    if (!keyword.trim()) {
      fetchPhotos();
      return;
    }
    try {
      const res = await api.get(`/api/photos/search?keyword=${encodeURIComponent(keyword)}`);
      setPhotos(res.data);
    } catch {
      setPhotos([]);
    }
  };

  const handleLogout = async () => {
    try { await api.post('/api/auth/logout'); } catch {}
    localStorage.clear();
    navigate('/login');
  };

  const handleDmOpen = (userId, username) => {
    setDmTarget({ user_id: userId, username });
    setDmContent('');
  };

  const handleDmSend = async () => {
    if (!dmContent.trim()) return;
    try {
      await api.post('/api/messages', {
        receiver_id: dmTarget.user_id,
        content: dmContent,
      });
      setDmTarget(null);
      alert('메시지가 전송됐습니다.');
    } catch {
      alert('전송 실패');
    }
  };

  const handlePhotoUpdate = async (photoId, description, keywords) => {
    try {
      await api.put(`/api/photos/${photoId}`, { description, keywords });
      fetchPhotos();
    } catch {
      alert('수정 실패');
    }
  };

  return (
    <div className="main-container">
      <header className="navbar">
        <h1>Photo Gallery</h1>
        <div className="navbar-actions">
          <span>{currentUsername}</span>
          <button onClick={() => navigate('/upload')}>사진 업로드</button>
          <button onClick={() => navigate('/messages')}>메시지함</button>
          <button onClick={handleLogout}>로그아웃</button>
        </div>
      </header>

      <div className="content">
        <aside className="sidebar">
          <h3>사용자 목록</h3>
          <ul>
            {users.map((u) => (
              <li key={u.id}>{u.username}</li>
            ))}
          </ul>
        </aside>

        <main className="photo-area">
          {isLoggedIn ? (
            <>
              <SearchBar onSearch={handleSearch} />
              <p className="section-title">My Gallery</p>
              {photos.filter((p) => p.username === currentUsername).length === 0 ? (
                <p className="section-empty">아직 업로드한 사진이 없습니다.</p>
              ) : (
                <div className="photo-grid">
                  {photos.filter((p) => p.username === currentUsername).map((photo) => (
                    <PhotoCard
                      key={photo.id}
                      photo={photo}
                      isOwner={true}
                      onDm={() => handleDmOpen(photo.user_id, photo.username)}
                      onUpdate={handlePhotoUpdate}
                    />
                  ))}
                </div>
              )}
              <p className="section-title section-title--others">Others' Gallery</p>
              {photos.filter((p) => p.username !== currentUsername).length === 0 ? (
                <p className="empty">사진이 없습니다.</p>
              ) : (
                <div className="photo-grid">
                  {photos.filter((p) => p.username !== currentUsername).map((photo) => (
                    <PhotoCard
                      key={photo.id}
                      photo={photo}
                      isOwner={false}
                      onDm={() => handleDmOpen(photo.user_id, photo.username)}
                      onUpdate={handlePhotoUpdate}
                    />
                  ))}
                </div>
              )}
            </>
          ) : (
            <>
              {photos.length === 0 ? (
                <p className="empty">사진이 없습니다.</p>
              ) : (
                <div className="photo-grid">
                  {photos.map((photo) => (
                    <PhotoCard
                      key={photo.id}
                      photo={photo}
                      isOwner={photo.user_id === currentUserId}
                      onDm={() => handleDmOpen(photo.user_id, photo.username)}
                      onUpdate={handlePhotoUpdate}
                    />
                  ))}
                </div>
              )}
            </>
          )}
        </main>
      </div>

      {dmTarget && (
        <div className="modal-overlay" onClick={() => setDmTarget(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>{dmTarget.username}에게 메시지 보내기</h3>
            <textarea
              value={dmContent}
              onChange={(e) => setDmContent(e.target.value)}
              placeholder="메시지 내용을 입력하세요"
              rows={4}
            />
            <div className="modal-actions">
              <button onClick={handleDmSend}>전송</button>
              <button className="btn-secondary" onClick={() => setDmTarget(null)}>취소</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
