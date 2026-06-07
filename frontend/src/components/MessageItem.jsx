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
    <div className="dm-item">
      <div className="dm-header">
        <div className="dm-sender-info">
          <div className="dm-avatar">
            <i className="ti ti-user" style={{ fontSize: '14px', color: '#C17F5A' }}></i>
          </div>
          <span className="dm-sender-name">{message.sender_username}</span>
          {message.parent_id && <span className="dm-reply-badge">답장</span>}
        </div>
        <span className="dm-date">
          {new Date(message.created_at).toLocaleString('ko-KR')}
        </span>
      </div>

      <p className="dm-content">{message.content}</p>

      <div className="dm-actions">
        <button className="dm-reply-btn" onClick={() => setReplying(!replying)}>Reply</button>
        <button className="dm-delete-btn" onClick={() => onDelete(message.id)}>Delete</button>
      </div>

      {replying && (
        <div className="dm-reply-form">
          <p className="dm-reply-label">답장 대상: {message.sender_username}</p>
          <textarea
            value={replyContent}
            onChange={(e) => setReplyContent(e.target.value)}
            placeholder="답장 내용을 입력하세요"
          />
          <div className="dm-reply-btns">
            <button className="dm-cancel-btn" onClick={() => setReplying(false)}>취소</button>
            <button className="dm-send-btn" onClick={handleReply}>전송</button>
          </div>
        </div>
      )}
    </div>
  );
}
