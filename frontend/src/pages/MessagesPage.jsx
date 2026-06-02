import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import MessageItem from '../components/MessageItem';

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
    <div className="main-container">
      <header className="navbar">
        <h1>메시지함</h1>
        <button onClick={() => navigate('/main')}>← 갤러리로</button>
      </header>
      <div className="messages-list">
        {messages.length === 0 ? (
          <p className="empty">받은 메시지가 없습니다.</p>
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
