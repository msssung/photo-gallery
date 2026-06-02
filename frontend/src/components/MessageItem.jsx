import { useState } from 'react';

export default function MessageItem({ message, onReply, onDelete }) {
  const [replying, setReplying] = useState(false);
  const [replyContent, setReplyContent] = useState('');

  const handleReply = () => {
    if (!replyContent.trim()) return;
    onReply(message.id, replyContent);
    setReplyContent('');
    setReplying(false);
  };

  return (
    <div className={`message-item ${!message.is_read ? 'unread' : ''}`}>
      <div className="message-header">
        <span className="sender">@{message.sender_username}</span>
        <span className="date">
          {new Date(message.created_at).toLocaleString('ko-KR')}
        </span>
        {message.parent_id && <span className="reply-badge">답장</span>}
      </div>
      <p className="message-content">{message.content}</p>
      <div className="message-actions">
        <button onClick={() => setReplying(!replying)}>Reply</button>
        <button className="delete-btn" onClick={() => onDelete(message.id)}>Delete</button>
      </div>
      {replying && (
        <div className="reply-form">
          <textarea
            value={replyContent}
            onChange={(e) => setReplyContent(e.target.value)}
            placeholder="답장 내용을 입력하세요"
            rows={3}
          />
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button onClick={handleReply}>전송</button>
            <button className="btn-secondary" onClick={() => setReplying(false)}>취소</button>
          </div>
        </div>
      )}
    </div>
  );
}
