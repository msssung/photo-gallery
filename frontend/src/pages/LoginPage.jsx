import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import './LoginPage.css';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/api/users').then((res) => setUsers(res.data)).catch(() => {});
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/api/auth/login', { username, password });
      const token = res.data.access_token;
      const payload = JSON.parse(atob(token.split('.')[1]));
      localStorage.setItem('access_token', token);
      localStorage.setItem('username', username);
      localStorage.setItem('user_id', payload.sub);
      navigate('/main');
    } catch {
      setError('아이디 또는 비밀번호가 틀렸습니다.');
    }
  };

  return (
    <div className="dark-login">
      {/* ── Left Panel ── */}
      <div className="dll-left">
        {/* Background typography */}
        <div className="dll-bg-text">PHOTO<br />GALLERY</div>

        {/* Decorative circles */}
        <div className="dll-circle dll-circle-1" />
        <div className="dll-circle dll-circle-2" />
        <div className="dll-circle dll-circle-3" />

        {/* Logo */}
        <div className="dll-logo">
          <div className="dll-logo-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1E1410" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
          </div>
          <span className="dll-logo-text">Photo Gallery</span>
        </div>

        {/* Main content */}
        <div className="dll-content">
          <h1>나의 사진을<br />세상과 나누세요</h1>
          <p>소중한 순간을 업로드하고,<br />다른 사람들의 이야기를 함께 감상하세요.</p>

          <div className="dll-features">
            <div className="dll-feature">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C17F5A" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z" />
                <circle cx="12" cy="13" r="4" />
              </svg>
              <span className="dll-feature-label">사진 업로드</span>
            </div>
            <div className="dll-feature">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C17F5A" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <span className="dll-feature-label">키워드 검색</span>
            </div>
            <div className="dll-feature">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C17F5A" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
              </svg>
              <span className="dll-feature-label">다이렉트 메시지</span>
            </div>
          </div>

          {users.length > 0 && (
            <div className="dll-user-section">
              <div className="dll-user-divider" />
              <p className="dll-user-title">사용자 목록</p>
              <div className="dll-user-list">
                {users.map((u) => (
                  <div key={u.id} className="dll-user-item">
                    <div className="dll-user-avatar">
                      <i className="ti ti-user" style={{ fontSize: '12px', color: '#C17F5A' }} />
                    </div>
                    <span className="dll-user-name">{u.username}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Bottom divider */}
        <div className="dll-bottom-divider">
          <div className="dll-divider-line" />
          <span>SINCE 2026</span>
          <div className="dll-divider-line" />
        </div>
      </div>

      {/* ── Right Panel ── */}
      <div className="dll-right">
        <p className="dll-eyebrow">Welcome</p>
        <h2>로그인</h2>
        <p className="dll-subtitle">계정에 로그인하여 갤러리를 시작하세요</p>

        <form onSubmit={handleSubmit}>
          <div className="dll-field">
            <label>아이디</label>
            <input
              type="text"
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="dll-field">
            <label>비밀번호</label>
            <input
              type="password"
              placeholder="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit" className="dll-submit">로그인</button>
        </form>

        <div className="dll-divider"><span>또는</span></div>
        <button type="button" className="dll-signup" onClick={() => navigate('/signup')}>
          회원가입
        </button>
        <p className="dll-footer">
          처음 방문하시나요? <Link to="/signup">계정 만들기</Link>
        </p>
      </div>
    </div>
  );
}
