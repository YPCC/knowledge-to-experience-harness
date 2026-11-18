import { useState, useMemo, useEffect } from 'react';
import { Search, Play, MessageCircle, Tag, Clock, ChevronRight, Video, Filter } from 'lucide-react';
import './App.css';

interface VideoMeta {
  id: string;
  title: string;
  description: string;
  type: string;
  duration: string;
  tags: string[];
  source: string;
  thumbnail?: string;
  videoUrl?: string;
  transcript?: { time: string; text: string }[];
  related?: string[];
}

function App() {
  const [videos, setVideos] = useState<VideoMeta[]>([]);
  const [search, setSearch] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<VideoMeta | null>(null);
  const [chatOpen, setChatOpen] = useState(true);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<{ role: 'user' | 'assistant'; text: string }[]>([
    { role: 'assistant', text: 'Ask me anything about the selected video. Answers are grounded in the transcript (or clearly marked as external exploration).' },
  ]);

  useEffect(() => {
    // Prefer generated/ via backend if available, fall back to static videos.json
    const load = async () => {
      try {
        const r = await fetch('http://localhost:8765/api/videos');
        if (r.ok) {
          const data = await r.json();
          if (data.videos && data.videos.length) {
            setVideos(data.videos);
            return;
          }
        }
      } catch (e) { /* backend not running */ }
      fetch('/videos.json')
        .then(r => r.json())
        .then(setVideos)
        .catch(() => setVideos([]));
    };
    load();
  }, []);

  const allTags = useMemo(() => {
    const tags = new Set<string>();
    videos.forEach(v => v.tags.forEach(t => tags.add(t)));
    return Array.from(tags).sort();
  }, [videos]);

  const filtered = useMemo(() => {
    return videos.filter(v => {
      const matchesSearch = !search ||
        v.title.toLowerCase().includes(search.toLowerCase()) ||
        v.description.toLowerCase().includes(search.toLowerCase()) ||
        v.tags.some(t => t.toLowerCase().includes(search.toLowerCase()));
      const matchesTags = selectedTags.length === 0 || selectedTags.every(t => v.tags.includes(t));
      return matchesSearch && matchesTags;
    });
  }, [videos, search, selectedTags]);

  const relatedVideos = useMemo(() => {
    if (!selectedVideo) return [];
    const byId = new Map(videos.map(v => [v.id, v]));
    const explicit = (selectedVideo.related || []).map(id => byId.get(id)).filter(Boolean) as VideoMeta[];
    const tagOverlap = videos
      .filter(v => v.id !== selectedVideo.id)
      .map(v => ({
        video: v,
        score: v.tags.filter(t => selectedVideo.tags.includes(t)).length
      }))
      .filter(x => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 4)
      .map(x => x.video);
    const combined = [...explicit];
    tagOverlap.forEach(v => {
      if (!combined.find(c => c.id === v.id)) combined.push(v);
    });
    return combined.slice(0, 5);
  }, [selectedVideo, videos]);

  const handleChat = () => {
    if (!chatInput.trim() || !selectedVideo) return;
    const userMsg = chatInput.trim();
    setChatMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatInput('');

    const query = userMsg.toLowerCase();
    const matches = (selectedVideo.transcript || []).filter(line =>
      line.text.toLowerCase().includes(query) ||
      query.split(' ').some(word => word.length > 3 && line.text.toLowerCase().includes(word))
    );

    let response = '';
    if (matches.length > 0) {
      const cites = matches.slice(0, 3).map(m => `[${m.time}] ${m.text}`).join('\n');
      response = `**Grounded in this video** (transcript search):\n${cites}\n\nSource: ${selectedVideo.source}`;
    } else {
      response = `**No exact match in this video's transcript.**\n\nThis is **external exploration** (not grounded in the video): Related concepts from the source include neuro-symbolic design, Context Graph, Decision Traces, and grounding to official coding systems.\n\nSource: ${selectedVideo.source}`;
    }

    setTimeout(() => {
      setChatMessages(prev => [...prev, { role: 'assistant', text: response }]);
    }, 400);
  };

  if (selectedVideo) {
    return (
      <div className="player-view">
        <header className="player-header">
          <button className="back-btn" onClick={() => setSelectedVideo(null)}>
            <ChevronRight size={18} style={{ transform: 'rotate(180deg)' }} /> Back to library
          </button>
          <h1>{selectedVideo.title}</h1>
          <div className="meta-row">
            <span className="badge">{selectedVideo.type}</span>
            <span><Clock size={14} /> {selectedVideo.duration}</span>
            <span>Source: {selectedVideo.source}</span>
          </div>
        </header>
        <div className="player-layout">
          <div className="video-column">
            {selectedVideo.videoUrl ? (
              <video controls className="video-player" src={selectedVideo.videoUrl} />
            ) : (
              <div className="video-placeholder">
                <Video size={48} />
                <p>Video coming soon — generated from source material</p>
              </div>
            )}
            <div className="transcript">
              <h3>Transcript</h3>
              {selectedVideo.transcript?.map((line, i) => (
                <div key={i} className="transcript-line">
                  <span className="time">{line.time}</span>
                  <span>{line.text}</span>
                </div>
              )) || <p>Transcript will appear here after generation.</p>}
            </div>
            {relatedVideos.length > 0 && (
              <div className="related-section">
                <h3>Relevant Content</h3>
                <p className="related-hint">Based on tags and learning paths — continue exploring:</p>
                <div className="related-grid">
                  {relatedVideos.map(rv => (
                    <article key={rv.id} className="related-card" onClick={() => setSelectedVideo(rv)}>
                      <div className="related-thumb"><Play size={20} /></div>
                      <div>
                        <h4>{rv.title}</h4>
                        <span className="badge">{rv.type}</span>
                        <span className="duration">{rv.duration}</span>
                      </div>
                    </article>
                  ))}
                </div>
              </div>
            )}
          </div>
          <aside className={`chat-sidebar ${chatOpen ? 'open' : ''}`}>
            <div className="chat-header">
              <MessageCircle size={18} /> Grounded Chat
              <button onClick={() => setChatOpen(!chatOpen)}>{chatOpen ? 'Hide' : 'Show'}</button>
            </div>
            {chatOpen && (
              <>
                <div className="chat-messages">
                  {chatMessages.map((m, i) => (
                    <div key={i} className={`message ${m.role}`}>{m.text}</div>
                  ))}
                </div>
                <div className="chat-input">
                  <input
                    value={chatInput}
                    onChange={e => setChatInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleChat()}
                    placeholder="Ask about this video..."
                  />
                  <button onClick={handleChat}>Send</button>
                </div>
              </>
            )}
          </aside>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <Video size={28} />
          <div>
            <h1>Knowledge-to-Experience</h1>
            <p>Trusted learning experiences from any source</p>
          </div>
        </div>
        <div className="search-bar">
          <Search size={18} />
          <input
            placeholder="Search videos, tags, concepts..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
      </header>

      <div className="filters">
        <Filter size={16} />
        <span>Tags:</span>
        {allTags.map(tag => (
          <button
            key={tag}
            className={`tag ${selectedTags.includes(tag) ? 'active' : ''}`}
            onClick={() => toggleTag(tag)}
          >
            <Tag size={12} /> {tag}
          </button>
        ))}
        {selectedTags.length > 0 && (
          <button className="clear" onClick={() => setSelectedTags([])}>Clear</button>
        )}
      </div>

      <main className="video-grid">
        {filtered.length === 0 && <p className="empty">No videos match your filters. (Loaded from /videos.json)</p>}
        {filtered.map(video => (
          <article key={video.id} className="video-card" onClick={() => setSelectedVideo(video)}>
            <div className="thumbnail">
              <Play size={32} />
              <span className="duration">{video.duration}</span>
            </div>
            <div className="card-body">
              <h3>{video.title}</h3>
              <p>{video.description}</p>
              <div className="card-meta">
                <span className="badge">{video.type}</span>
                <span className="tags">{video.tags.slice(0, 3).join(' · ')}</span>
              </div>
            </div>
          </article>
        ))}
      </main>

      <footer className="footer">
        Knowledge in. Trusted experiences out. · Modular harness · Generic sources (GitHub, PowerPoint, papers, docs)
      </footer>
    </div>
  );
}

export default App;
