import { useState, useEffect } from 'react';
import { 
  Shield, 
  MapPin, 
  Volume2, 
  VolumeX, 
  Plus, 
  Clock, 
  Radio, 
  Users, 
  Activity, 
  Flame, 
  Send,
  LifeBuoy,
  Tv,
  HelpCircle
} from 'lucide-react';

function App() {
  const [role, setRole] = useState('student');
  const [sosActive, setSosActive] = useState(false);
  const [sosCountdown, setSosCountdown] = useState(3);
  const [soundAlert, setSoundAlert] = useState(true);
  const [reports, setReports] = useState([
    { id: 1, category: 'Medical Help', location: 'Science Library - Floor 2', status: 'En Route', time: '5m ago', color: '#ffb3ba' },
    { id: 2, category: 'Leaky Pipe', location: 'Student Union Quad', status: 'Resolved', time: '2h ago', color: '#baffc9' }
  ]);
  const [newReport, setNewReport] = useState({ category: 'Medical Help', location: '', details: '' });

  // Admin state
  const [adminTab, setAdminTab] = useState('signals');
  const [activeSignals, setActiveSignals] = useState([
    { id: 'SIG-901', category: 'Security Alert', location: 'Engineering Hall', time: '1m ago', status: 'Awaiting Help', color: '#ffdfba' },
    { id: 'SIG-892', category: 'Medical Alert', location: 'Gymnasium', time: '4m ago', status: 'En Route', color: '#ffb3ba' }
  ]);

  const [responders, setResponders] = useState([
    { id: 'R-10', name: 'Officer Leo', unit: 'Safety Team 1', status: 'Active', location: 'Library' },
    { id: 'R-12', name: 'Officer Mia', unit: 'Safety Team 2', status: 'Waiting', location: 'Union' }
  ]);

  useEffect(() => {
    let interval;
    if (sosActive && sosCountdown > 0) {
      interval = setInterval(() => {
        setSosCountdown(prev => prev - 1);
      }, 1000);
    } else if (sosCountdown === 0 && sosActive) {
      const newSignal = {
        id: `SIG-${Math.floor(100 + Math.random() * 900)}`,
        category: 'Quick Panic Beacon',
        location: 'GPS: Main Plaza Entrance',
        time: 'Just now',
        status: 'Awaiting Help',
        color: '#ffb3ba'
      };
      setActiveSignals(prev => [newSignal, ...prev]);
      setReports(prev => [{
        id: Date.now(),
        category: 'Quick Panic Beacon',
        location: 'Main Plaza Entrance',
        status: 'Awaiting Help',
        time: 'Just now',
        color: '#ffb3ba'
      }, ...prev]);
      setSosCountdown(0);
    }
    return () => clearInterval(interval);
  }, [sosActive, sosCountdown]);

  const handleSosPress = () => {
    setSosActive(true);
    setSosCountdown(3);
  };

  const handleSosRelease = () => {
    setSosActive(false);
  };

  const handleCreateReport = (e) => {
    e.preventDefault();
    if (!newReport.location) return;
    
    let color = '#bae1ff';
    if (newReport.category === 'Medical Help') color = '#ffb3ba';
    else if (newReport.category === 'Security Alert') color = '#ffdfba';
    else if (newReport.category === 'Fire Alarm') color = '#ffb3ba';

    const reportData = {
      id: Date.now(),
      category: newReport.category,
      location: newReport.location,
      status: 'Awaiting Help',
      time: 'Just now',
      color: color
    };
    setReports(prev => [reportData, ...prev]);
    setActiveSignals(prev => [{
      id: `SIG-${Math.floor(100 + Math.random() * 900)}`,
      category: reportData.category,
      location: reportData.location,
      time: reportData.time,
      status: reportData.status,
      color: reportData.color
    }, ...prev]);
    setNewReport({ category: 'Medical Help', location: '', details: '' });
  };

  const handleResolve = (sigId) => {
    setActiveSignals(prev => prev.filter(sig => sig.id !== sigId));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f0f4f8] to-[#e0eafc] text-[#334155] p-6 md:p-10 font-sans">
      
      {/* Volumetric Header Panel */}
      <header className="clay-card p-6 mb-8 flex flex-col md:flex-row justify-between items-center gap-6 bg-white/80">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-indigo-500 flex items-center justify-center text-white" style={{
            boxShadow: '0 8px 16px rgba(99, 102, 241, 0.3), inset 0 -4px 8px rgba(0,0,0,0.2), inset 0 4px 8px rgba(255,255,255,0.4)'
          }}>
            <LifeBuoy className="w-8 h-8 animate-spin" />
          </div>
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-600 to-pink-500 bg-clip-text text-transparent">
              CampusSync Bubbly
            </h1>
            <p className="text-sm font-semibold text-slate-500">Soft Safety Interface</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button 
            onClick={() => setRole(role === 'student' ? 'admin' : 'student')}
            className="clay-btn px-6 py-3 font-bold text-sm bg-gradient-to-r from-indigo-500 to-indigo-600 text-white"
          >
            Portal: {role === 'student' ? 'Student Desk' : 'Emergency Desk'}
          </button>
          
          <button 
            onClick={() => setSoundAlert(!soundAlert)}
            className="w-12 h-12 flex items-center justify-center rounded-full bg-slate-100 text-slate-600 transition-all hover:bg-slate-200 active:scale-90"
            style={{
              boxShadow: 'inset 0 -2px 4px rgba(0,0,0,0.1), inset 0 2px 4px rgba(255,255,255,0.8)'
            }}
          >
            {soundAlert ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {role === 'student' ? (
        /* ================= STUDENT PORTAL ================= */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Beacon Control */}
          <div className="lg:col-span-5 flex flex-col gap-8">
            <div className="clay-card bg-[#fff0f3] p-8 flex flex-col items-center text-center">
              <span className="bg-[#ffe3e8] text-[#ff4d6d] font-bold text-xs uppercase px-4 py-1.5 rounded-full mb-6">
                Instant Rescue Button
              </span>
              
              <h2 className="text-2xl font-bold mb-3 text-[#ff4d6d]">Hold to Alert</h2>
              <p className="text-sm font-semibold text-slate-500 mb-8 max-w-xs">
                Press and squeeze the jelly button for 3 seconds to emit a local beacon to safety team.
              </p>

              {/* Bouncy Jelly SOS Button */}
              <button
                onMouseDown={handleSosPress}
                onMouseUp={handleSosRelease}
                onMouseLeave={handleSosRelease}
                onTouchStart={handleSosPress}
                onTouchEnd={handleSosRelease}
                className={`w-44 h-44 rounded-full flex flex-col items-center justify-center transition-all duration-300 ${
                  sosActive 
                    ? 'bg-[#ff4d6d] text-white scale-90' 
                    : 'bg-[#ff85a1] text-white'
                }`}
                style={{
                  boxShadow: sosActive 
                    ? '0 5px 10px rgba(255, 77, 109, 0.4), inset 0 -6px 12px rgba(0,0,0,0.15), inset 0 6px 12px rgba(255,255,255,0.3)'
                    : '0 15px 30px rgba(255, 133, 161, 0.4), inset 0 -8px 16px rgba(0,0,0,0.25), inset 0 8px 16px rgba(255,255,255,0.4)'
                }}
              >
                <Flame className="w-12 h-12 mb-2 animate-bounce" />
                <span className="font-extrabold text-lg uppercase tracking-wide">
                  {sosActive ? `ALERTING (${sosCountdown}s)` : 'PRESS ME'}
                </span>
              </button>

              {sosActive && (
                <div className="mt-8 w-full bg-slate-100 rounded-full h-4 overflow-hidden relative p-0.5">
                  <div 
                    className="bg-[#ff4d6d] h-full rounded-full transition-all duration-1000"
                    style={{ width: `${((3 - sosCountdown) / 3) * 100}%` }}
                  />
                </div>
              )}
            </div>

            <div className="clay-card bg-[#eefaf6] p-6 flex flex-col">
              <h3 className="font-bold text-lg text-emerald-700 mb-4 flex items-center gap-2">
                <Radio className="w-5 h-5 animate-pulse" /> Active Broadcasts
              </h3>
              <div className="space-y-3 font-semibold text-sm">
                <div className="flex justify-between bg-white/60 p-3 rounded-xl">
                  <span>Rescue beacon active</span>
                  <span className="text-pink-500">Scanning GPS...</span>
                </div>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-7 flex flex-col gap-8">
            <div className="clay-card bg-white p-8">
              <h3 className="text-2xl font-bold text-slate-800 mb-6">Create Soft Alert</h3>
              
              <form onSubmit={handleCreateReport} className="space-y-6">
                <div>
                  <label className="block text-slate-500 font-bold mb-2 text-sm ml-2">ALERT CATEGORY</label>
                  <select 
                    value={newReport.category}
                    onChange={(e) => setNewReport({ ...newReport, category: e.target.value })}
                    className="w-full p-4 clay-input text-base font-bold focus:outline-none focus:ring-2 focus:ring-indigo-300"
                  >
                    <option value="Medical Help">Medical Help Required</option>
                    <option value="Security Alert">Security Assistance</option>
                    <option value="Fire Alarm">Fire Hazard spotted</option>
                    <option value="Leaky Pipe">Infrastructure Issue</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-500 font-bold mb-2 text-sm ml-2">WHERE IS IT?</label>
                  <input 
                    type="text" 
                    placeholder="e.g. Science Library Room 402"
                    value={newReport.location}
                    onChange={(e) => setNewReport({ ...newReport, location: e.target.value })}
                    className="w-full p-4 clay-input text-base font-bold placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-500 font-bold mb-2 text-sm ml-2">LOG DETAILS</label>
                  <textarea 
                    placeholder="Add details so safety officers can assist..."
                    value={newReport.details}
                    onChange={(e) => setNewReport({ ...newReport, details: e.target.value })}
                    className="w-full p-4 clay-input h-32 text-base font-semibold placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                  />
                </div>

                <button 
                  type="submit" 
                  className="w-full clay-btn p-4 bg-gradient-to-r from-indigo-500 to-indigo-600 text-white text-lg font-bold flex items-center justify-center gap-2"
                >
                  <Send className="w-5 h-5" /> Send Safety Alert
                </button>
              </form>
            </div>

            {/* List */}
            <div className="clay-card bg-[#f0f4ff] p-6">
              <h3 className="font-bold text-lg mb-4 ml-2">Recent Campus Alerts</h3>
              <div className="space-y-4">
                {reports.map((rep) => (
                  <div key={rep.id} className="clay-card p-5 bg-white flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition-all duration-300 hover:translate-y-[-2px]">
                    <div className="flex gap-4 items-center">
                      <div className="w-3 h-12 rounded-full" style={{ backgroundColor: rep.color }}></div>
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-extrabold text-[#334155]">{rep.category}</span>
                          <span className="text-xs text-slate-400">{rep.time}</span>
                        </div>
                        <p className="text-slate-500 font-semibold text-sm flex items-center gap-1">
                          <MapPin className="w-4 h-4" /> {rep.location}
                        </p>
                      </div>
                    </div>
                    <span className="px-4 py-1.5 rounded-full font-bold text-xs bg-slate-100 text-slate-600" style={{
                      boxShadow: 'inset 0 -2px 4px rgba(0,0,0,0.05), inset 0 2px 4px rgba(255,255,255,0.8)'
                    }}>
                      {rep.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      ) : (
        /* ================= ADMIN CONSOLE ================= */
        <div className="flex flex-col gap-8">
          
          <div className="flex gap-4 p-2 bg-slate-100 rounded-3xl self-start" style={{
            boxShadow: 'inset 0 3px 6px rgba(0,0,0,0.05)'
          }}>
            <button 
              onClick={() => setAdminTab('signals')}
              className={`px-6 py-2.5 rounded-2xl font-bold text-sm transition-all ${adminTab === 'signals' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500'}`}
            >
              Active Alarms ({activeSignals.length})
            </button>
            <button 
              onClick={() => setAdminTab('responders')}
              className={`px-6 py-2.5 rounded-2xl font-bold text-sm transition-all ${adminTab === 'responders' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500'}`}
            >
              Officers ({responders.length})
            </button>
          </div>

          {adminTab === 'signals' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {activeSignals.map((sig) => (
                <div key={sig.id} className="clay-card p-6 bg-white flex flex-col justify-between" style={{
                  borderLeft: `8px solid ${sig.color}`
                }}>
                  <div>
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-xs font-bold text-slate-400 font-mono">{sig.id}</span>
                      <span className="text-xs font-extrabold text-rose-500 bg-rose-50 px-3 py-1 rounded-full">High Alert</span>
                    </div>

                    <h4 className="text-xl font-bold text-slate-800 mb-2">{sig.category}</h4>
                    <p className="text-sm font-semibold text-slate-500 flex items-center gap-1 mb-6">
                      <MapPin className="w-4 h-4" /> {sig.location}
                    </p>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                    <span className="text-xs font-bold text-[#6366f1] bg-[#e0eafc] px-3 py-1 rounded-full">{sig.status}</span>
                    <button 
                      onClick={() => handleResolve(sig.id)}
                      className="clay-btn px-4 py-2 text-xs bg-gradient-to-r from-indigo-500 to-indigo-600 text-white font-bold"
                    >
                      Resolve Incident
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {adminTab === 'responders' && (
            <div className="clay-card bg-white p-8">
              <h3 className="text-xl font-bold text-slate-800 mb-6">Safety Responders</h3>
              <div className="space-y-4">
                {responders.map(resp => (
                  <div key={resp.id} className="p-4 bg-slate-50 rounded-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition-all hover:bg-slate-100">
                    <div className="flex gap-4 items-center">
                      <div className="w-12 h-12 rounded-xl bg-pink-200 text-pink-700 font-extrabold flex items-center justify-center text-base" style={{
                        boxShadow: 'inset 0 -2px 4px rgba(0,0,0,0.1), inset 0 2px 4px rgba(255,255,255,0.6)'
                      }}>
                        {resp.id}
                      </div>
                      <div>
                        <h4 className="text-base font-bold text-slate-800">{resp.name}</h4>
                        <span className="text-xs font-semibold text-slate-400 bg-white px-2 py-0.5 rounded-full shadow-sm">{resp.unit}</span>
                      </div>
                    </div>
                    <div className="text-sm font-semibold text-slate-500 flex items-center gap-1">
                      <MapPin className="w-4 h-4" /> Assigned: {resp.location}
                    </div>
                    <span className="px-3.5 py-1 rounded-full font-bold text-xs bg-emerald-100 text-emerald-600">
                      {resp.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}

export default App;
