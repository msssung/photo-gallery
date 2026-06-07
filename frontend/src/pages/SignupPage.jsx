import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import './SignupPage.css';

export default function SignupPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/api/auth/signup', { username, password });
      navigate('/login');
    } catch (err) {
      if (err.response?.status === 400) {
        setError('이미 사용 중인 아이디입니다.');
      } else {
        setError(`오류: ${err.response?.data?.detail || err.message}`);
      }
    }
  };

  return (
    <div className="signup-bg">
      <div className="signup-card">
        {/* Logo */}
        <div className="signup-logo">
          <div className="signup-logo-icon">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#1E1410" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
          </div>
          <span className="signup-logo-text">Photo Gallery</span>
        </div>

        <p className="signup-eyebrow">Create account</p>
        <h2 className="signup-title">회원가입</h2>

        <form onSubmit={handleSubmit}>
          <div className="signup-field">
            <label>아이디</label>
            <input
              type="text"
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="signup-field">
            <label>비밀번호</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit">회원가입</button>
        </form>

        <div className="signup-divider"><span>또는</span></div>
        <button type="button" className="signup-login-btn" onClick={() => navigate('/login')}>
          로그인
        </button>
        <p className="signup-footer">
          이미 계정이 있으신가요? <Link to="/login">로그인</Link>
        </p>
      </div>
    </div>
  );
}
