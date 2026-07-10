import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import axios from 'axios';
import { updateField, fillFromAI, resetForm } from './store';

const API = 'http://localhost:8000';

function App() {
  const form = useSelector((state) => state.interaction);
  const dispatch = useDispatch();

  const [chatInput, setChatInput] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFieldChange = (field, value) => {
    dispatch(updateField({ field, value }));
  };

  const handleChatSend = async () => {
    if (!chatInput.trim()) return;
    setLoading(true);
    setChatLog((prev) => [...prev, { role: 'user', text: chatInput }]);

    try {
      const res = await axios.post(`${API}/chat`, { message: chatInput });
      setChatLog((prev) => [...prev, { role: 'ai', text: res.data.reply }]);

      // Also fetch latest saved interaction to auto-fill form
      const listRes = await axios.get(`${API}/interactions`);
      if (listRes.data.length > 0) {
        const latest = listRes.data[listRes.data.length - 1];
        dispatch(fillFromAI({
          hcp_name: latest.hcp_name || '',
          interaction_type: latest.interaction_type || 'Meeting',
          topics_discussed: latest.topics_discussed || '',
          sentiment: latest.sentiment || 'Neutral',
          outcomes: latest.outcomes || '',
          follow_up_actions: latest.follow_up_actions || '',
        }));
      }
    } catch (err) {
      setChatLog((prev) => [...prev, { role: 'ai', text: 'Error: ' + err.message }]);
    }
    setChatInput('');
    setLoading(false);
  };

  const handleManualSave = async () => {
    try {
      await axios.post(`${API}/interactions/manual`, form);
      alert('Saved manually!');
      dispatch(resetForm());
    } catch (err) {
      alert('Error saving: ' + err.message);
    }
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', display: 'flex', gap: 30, maxWidth: 1100, margin: '30px auto', padding: 20 }}>
      {/* LEFT: FORM */}
      <div style={{ flex: 1.3 }}>
        <h2>Log HCP Interaction</h2>

        <label style={label}>HCP Name</label>
        <input style={input} value={form.hcp_name} onChange={(e) => handleFieldChange('hcp_name', e.target.value)} placeholder="Search or select HCP..." />

        <label style={label}>Interaction Type</label>
        <select style={input} value={form.interaction_type} onChange={(e) => handleFieldChange('interaction_type', e.target.value)}>
          <option>Meeting</option>
          <option>Call</option>
          <option>Email</option>
        </select>

        <label style={label}>Attendees</label>
        <input style={input} value={form.attendees} onChange={(e) => handleFieldChange('attendees', e.target.value)} placeholder="Enter names..." />

        <label style={label}>Topics Discussed</label>
        <textarea style={{ ...input, height: 70 }} value={form.topics_discussed} onChange={(e) => handleFieldChange('topics_discussed', e.target.value)} />

        <label style={label}>Sentiment</label>
        <div style={{ display: 'flex', gap: 15, marginBottom: 15 }}>
          {['Positive', 'Neutral', 'Negative'].map((s) => (
            <label key={s} style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <input type="radio" checked={form.sentiment === s} onChange={() => handleFieldChange('sentiment', s)} />
              {s}
            </label>
          ))}
        </div>

        <label style={label}>Outcomes</label>
        <textarea style={{ ...input, height: 60 }} value={form.outcomes} onChange={(e) => handleFieldChange('outcomes', e.target.value)} />

        <label style={label}>Follow-up Actions</label>
        <textarea style={{ ...input, height: 60 }} value={form.follow_up_actions} onChange={(e) => handleFieldChange('follow_up_actions', e.target.value)} />

        <button onClick={handleManualSave} style={saveBtn}>Save Interaction</button>
      </div>

      {/* RIGHT: AI CHAT */}
      <div style={{ flex: 1, border: '1px solid #ddd', borderRadius: 10, padding: 15, height: 'fit-content' }}>
        <h3 style={{ marginTop: 0 }}>🤖 AI Assistant</h3>
        <p style={{ fontSize: 13, color: '#666' }}>Log interaction via chat, e.g. "Met Dr. Smith, discussed Product X, positive sentiment"</p>

        <div style={{ maxHeight: 300, overflowY: 'auto', marginBottom: 10 }}>
          {chatLog.map((msg, i) => (
            <div key={i} style={{
              background: msg.role === 'user' ? '#e8f0fe' : '#f0f0f0',
              padding: 8, borderRadius: 6, marginBottom: 6, fontSize: 14
            }}>
              <strong>{msg.role === 'user' ? 'You: ' : 'AI: '}</strong>{msg.text}
            </div>
          ))}
        </div>

        <textarea
          style={{ ...input, height: 60 }}
          placeholder="Describe interaction..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
        />
        <button onClick={handleChatSend} disabled={loading} style={saveBtn}>
          {loading ? 'Processing...' : 'Log via AI'}
        </button>
      </div>
    </div>
  );
}

const label = { display: 'block', fontSize: 13, fontWeight: 600, marginBottom: 4, marginTop: 12 };
const input = { width: '100%', padding: 8, border: '1px solid #ccc', borderRadius: 6, fontFamily: 'Inter, sans-serif', boxSizing: 'border-box' };
const saveBtn = { marginTop: 15, padding: '8px 18px', background: '#4f46e5', color: 'white', border: 'none', borderRadius: 6, cursor: 'pointer' };

export default App;