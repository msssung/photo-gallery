import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

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
    <div className="auth-container">
      <h2>로그인</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="아이디"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">로그인</button>
      </form>
      <p style={{ marginTop: '1rem', textAlign: 'center' }}>
        계정이 없으신가요? <Link to="/signup">회원가입</Link>
      </p>
    </div>
  );
}
