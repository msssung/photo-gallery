import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import MessageItem from '../components/MessageItem';
import './MessagesPage.css';

export default function MessagesPage() {
  const [messages, setMessages] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const res = await api.get('/api/messages');
      setMessages(res.data);
    } catch {
      setMessages([]);
    }
  };

  const handleReply = async (messageId, content) => {
    try {
      await api.post(`/api/messages/${messageId}/reply`, { content });
      alert('답장을 보냈습니다.');
    } catch {
      alert('답장 전송에 실패했습니다.');
    }
  };

  const handleDelete = async (messageId) => {
    try {
      await api.delete(`/api/messages/${messageId}`);
      setMessages((prev) => prev.filter((m) => m.id !== messageId));
    } catch {
      alert('삭제에 실패했습니다.');
    }
  };

  return (
    <div className="messages-page-wrap">
      <header className="navbar">
        <h1>메시지함</h1>
        <button onClick={() => navigate('/main')}>← 갤러리로</button>
      </header>

      <div className="messages-page">
        <div className="messages-page-header">
          <h2>메시지함</h2>
          <p>수신된 메시지 {messages.length}개</p>
        </div>

        {messages.length === 0 ? (
          <div className="dm-empty">
            <div className="dm-empty-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3D2B20" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
              </svg>
            </div>
            <p>받은 메시지가 없습니다.</p>
          </div>
        ) : (
          messages.map((msg) => (
            <MessageItem
              key={msg.id}
              message={msg}
              onReply={handleReply}
              onDelete={handleDelete}
            />
          ))
        )}
      </div>
    </div>
  );
}
