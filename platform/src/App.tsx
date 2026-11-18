import React, { useEffect, useState, useMemo } from 'react';
import './App.css';

interface TranscriptLine {
  time: string;
  text: string;
}

interface Video {
  id: string;
  title: string;
  description: string;
  type: string;
  duration: string;
  tags: string[];
  source: string;
  videoUrl: string;
  transcript: TranscriptLine[];
}

const App: React.FC = () => {
  const [videos, setVideos] = useState<Video[]>([]);
  const [search, setSearch] = useState('');
  const [selectedTag, setSelectedTag] = useState<string | null>(null);
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<{ role: 'user' | 'bot'; text: string }[]>([]);

  useEffect(() => {
    fetch('/videos.json')
      .then(r => r.json())
      .then(setVideos)
      .catch(err => console.error('Failed to load videos.json', err));
  }, []);

  const allTags = useMemo(() => {
    const s = new Set<string>();
    videos.forEach(v => v.tags.forEach(t => s.add(t)));
    return Array.from(s).sort();
  }, [videos]);

  const filtered = useMemo(() => {
    return videos.filter(v => {
      const matchSearch = !search || 
        v.title.toLowerCase().includes(search.toLowerCase()) ||
        v.description.toLowerCase().includes(search.toLowerCase()) ||
        v.tags.some(t => t.toLowerCase().includes(search.toLowerCase()));
      const matchTag = !selectedTag || v.tags.includes(selectedTag);
      return matchSearch && matchTag;
    });
  }, [videos, search, selectedTag]);

  const handleChat = () => {
    if (!chatInput.trim() || !selectedVideo) return;
    const query = chatInput.trim();
    setChatMessages(prev => [...prev, { role: 'user', text: query }]);
    setChatInput('');

    // Simple grounded search in transcript
    const lower = query.toLowerCase();
    const hits = selectedVideo.transcript.filter(line => 
      line.text.toLowerCase().includes(lower) || lower.split(' ').some(w => line.text.toLowerCase().includes(w) && w.length > 3)
    );

    let reply: string;
    if (hits.length > 0) {
      reply = `**Grounded in this video:**\n` + hits.map(h => `• [${h.time}] ${h.text}`).join('\n');
    } else {
      reply = `No direct match in this video's transcript. This would be **external exploration** mode (web search or broader knowledge).`;
    }
    setChatMessages(prev => [...prev, { role: 'bot', text: reply }]);
  };

  if (selectedVideo) {
    return (
      <div className="app dark">
        <header>
          <button onClick={() => setSelectedVideo(null)}>← Back</button>
          <h1>{selectedVideo.title}</h1>
        </header>
        <div className="player-layout">
          <div className="player">
            <video src={selectedVideo.videoUrl} controls width="100%" />
            <p className="meta">{selectedVideo.type} · {selectedVideo.duration} · {selectedVideo.source}</p>
            <p>{selectedVideo.description}</p>
          </div>
          <div className="side">
            <div className="transcript">
              <h3>Transcript</h3>
              {selectedVideo.transcript.map((line, i) => (
                <div key={i} className="line">
                  <span className="time">{line.time}</span> {line.text}
                </div>
              ))}
            </div>
            <div className="chat">
              <h3>Grounded Chat</h3>
              <div className="messages">
                {chatMessages.map((m, i) => (
                  <div key={i} className={`msg ${m.role}`}>{m.text}</div>
                ))}
              </div>
              <div className="input-row">
                <input
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleChat()}
                  placeholder="Ask about this video..."
                />
                <button onClick={handleChat}>Send</button>
              </div>
              <small>Answers cite the transcript when possible. External exploration is labeled.</small>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app dark">
      <header>
        <h1>Knowledge-to-Experience Platform</h1>
        <input
          className="search"
          placeholder="Search videos, tags, descriptions..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </header>
      <div className="tags">
        <button className={!selectedTag ? 'active' : ''} onClick={() => setSelectedTag(null)}>All</button>
        {allTags.map(t => (
          <button key={t} className={selectedTag === t ? 'active' : ''} onClick={() => setSelectedTag(t === selectedTag ? null : t)}>
            {t}
          </button>
        ))}
      </div>
      <div className="grid">
        {filtered.map(v => (
          <div key={v.id} className="card" onClick={() => setSelectedVideo(v)}>
            <div className="thumb">▶ {v.duration}</div>
            <h3>{v.title}</h3>
            <p>{v.description}</p>
            <div className="badges">
              <span className="type">{v.type}</span>
              {v.tags.slice(0, 3).map(t => <span key={t} className="tag">{t}</span>)}
            </div>
          </div>
        ))}
      </div>
      {filtered.length === 0 && <p className="empty">No videos match your search.</p>}
    </div>
  );
};

export default App;
