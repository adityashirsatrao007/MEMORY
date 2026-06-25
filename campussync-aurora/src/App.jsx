import { useState, useEffect } from 'react';
import { 
  Shield, 
  MapPin, 
  Volume2, 
  VolumeX, 
  Clock, 
  Radio, 
  Users, 
  Activity, 
  Flame, 
  Send,
  Eye,
  HeartHandshake,
  Compass
} from 'lucide-react';

function App() {
  const [role, setRole] = useState('student');
  const [sosActive, setSosActive] = useState(false);
  const [sosCountdown, setSosCountdown] = useState(3);
  const [soundAlert, setSoundAlert] = useState(true);
  const [reports, setReports] = useState([
    { id: 1, category: 'Medical Rescue', location: 'Science Library - Floor 2', status: 'Units Dispatched', time: '5 mins ago' },
    { id: 2, category: 'Maintenance Needed', location: 'Student Union Quad', status: 'Resolved', time: '2 hours ago' }
  ]);
  const [newReport, setNewReport] = useState({ category: 'Medical Rescue', location: '', details: '' });

  // Admin state
  const [activeSignals, setActiveSignals] = useState([
    { id: 'SIG-901', category: 'Active Danger Warning', location: 'Engineering Hall B', time: '1 min ago', status: 'Pending Rescue' },
    { id: 'SIG-892', category: 'Medical Emergency Alert', location: 'Campus Gymnasium', time: '4 mins ago', status: 'En Route' }
  ]);

  const [responders, setResponders] = useState([
    { id: 'R-10', name: 'Officer Leo', unit: 'First Support 1', status: 'Dispatched', location: 'Sector 3 (Library)' },
    { id: 'R-12', name: 'Officer Aria', unit: 'First Support 2', status: 'Stationed', location: 'Sector 1 (Union)' }
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
        category: 'Quick Beacon SOS',
        location: 'Main Quad Plaza Entrance',
        time: 'Just now',
        status: 'Awaiting Rescue'
      };
      setActiveSignals(prev => [newSignal, ...prev]);
      setReports(prev => [{
        id: Date.now(),
        category: 'Quick Beacon SOS',
        location: 'Main Quad Plaza Entrance',
        status: 'Awaiting Rescue',
        time: 'Just now'
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
    const reportData = {
      id: Date.now(),
      category: newReport.category,
      location: newReport.location,
      status: 'Awaiting Help',
      time: 'Just now'
    };
    setReports(prev => [reportData, ...prev]);
    setActiveSignals(prev => [{
      id: `SIG-${Math.floor(100 + Math.random() * 900)}`,
      category: reportData.category,
      location: reportData.location,
      time: reportData.time,
      status: reportData.status
    }, ...prev]);
    setNewReport({ category: 'Medical Rescue', location: '', details: '' });
  };

  return (
    <div className="min-h-screen bg-[#06030c] text-slate-100 p-6 md:p-12 font-sans relative overflow-hidden">
      
      {/* Mesh gradients for background */}
      <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-purple-700/10 rounded-full blur-[150px] orb-1 pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[700px] h-[700px] bg-indigo-600/10 rounded-full blur-[180px] orb-2 pointer-events-none"></div>
      <div className="absolute top-[30%] left-[40%] w-[400px] h-[400px] bg-pink-500/5 rounded-full blur-[130px] pointer-events-none"></div>

      {/* Aurora Header */}
      <header className="aurora-card p-6 mb-12 flex flex-col md:flex-row justify-between items-center gap-6 relative z-10">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 flex items-center justify-center text-white shadow-lg">
            <Compass className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent font-display">
              CAMPUS_SYNC
            </h1>
            <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Aesthetic Guardian Network</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button 
            onClick={() => setRole(role === 'student' ? 'admin' : 'student')}
            className="aurora-btn px-6 py-2.5 text-xs font-bold uppercase tracking-wider"
          >
            Mode: {role === 'student' ? 'Student Link' : 'Admin Hub'}
          </button>
          
          <button 
            onClick={() => setSoundAlert(!soundAlert)}
            className="w-10 h-10 flex items-center justify-center rounded-xl bg-white/5 border border-white/10 text-slate-300 hover:bg-white/10 transition-all active:scale-95"
          >
            {soundAlert ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>
        </div>
      </header>

      {role === 'student' ? (
        /* ================= STUDENT PORTAL ================= */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
          
          {/* Beacon Console */}
          <div className="lg:col-span-5 flex flex-col gap-8">
            <div className="aurora-card p-8 flex flex-col items-center text-center">
              <span className="bg-purple-500/10 text-purple-300 border border-purple-500/20 font-bold text-xs uppercase px-4 py-1.5 rounded-full mb-6 tracking-wide">
                HOLOGRAPHIC DURESS BUTTON
              </span>
              
              <h2 className="text-xl font-bold mb-2 font-display">Press to Broadcast</h2>
              <p className="text-xs text-slate-400 mb-8 max-w-xs leading-relaxed">
                Hold button below. This broadcasts an SOS telemetry packet using the local campus mesh network.
              </p>

              {/* Glowing interactive button */}
              <button
                onMouseDown={handleSosPress}
                onMouseUp={handleSosRelease}
                onMouseLeave={handleSosRelease}
                onTouchStart={handleSosPress}
                onTouchEnd={handleSosRelease}
                className={`w-40 h-40 rounded-full flex flex-col items-center justify-center transition-all duration-300 border ${
                  sosActive 
                    ? 'bg-purple-600/30 border-purple-500 shadow-[0_0_40px_rgba(168,85,247,0.5)]' 
                    : 'bg-white/5 border-white/10 shadow-[0_0_20px_rgba(255,255,255,0.05)]'
                }`}
              >
                <Flame className={`w-10 h-10 mb-2 ${sosActive ? 'text-purple-400 animate-ping' : 'text-slate-300'}`} />
                <span className="font-extrabold text-xs uppercase tracking-widest font-display">
                  {sosActive ? `TRANSMITTING` : 'SOS LINK'}
                </span>
              </button>

              {sosActive && (
                <div className="mt-8 w-full bg-white/5 rounded-full h-2 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-purple-500 to-indigo-500 h-full rounded-full transition-all duration-1000"
                    style={{ width: `${((3 - sosCountdown) / 3) * 100}%` }}
                  />
                </div>
              )}
            </div>

            <div className="aurora-card p-6 flex flex-col">
              <h3 className="font-bold text-sm uppercase tracking-widest text-slate-300 mb-4 flex items-center gap-2">
                <Radio className="w-4 h-4 animate-pulse text-purple-400" /> Mesh Sync Node
              </h3>
              <div className="space-y-3 text-xs text-slate-400">
                <p className="flex justify-between border-b border-white/5 pb-2">
                  <span>GPS Tracking</span>
                  <span className="text-purple-400">Locking Coordinates...</span>
                </p>
                <p className="flex justify-between">
                  <span>Transmitter</span>
                  <span className="text-indigo-400">Standard Active</span>
                </p>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-7 flex flex-col gap-8">
            <div className="aurora-card p-8">
              <h3 className="text-lg font-bold font-display text-slate-200 mb-6 flex items-center gap-2">
                <HeartHandshake className="w-5 h-5 text-purple-400" /> Log Emergency Telemetry
              </h3>
              
              <form onSubmit={handleCreateReport} className="space-y-6">
                <div>
                  <label className="block text-slate-400 font-bold mb-2 text-xs uppercase tracking-wider ml-1">INCIDENT GRADE</label>
                  <select 
                    value={newReport.category}
                    onChange={(e) => setNewReport({ ...newReport, category: e.target.value })}
                    className="w-full p-4 aurora-input text-sm font-semibold focus:outline-none"
                  >
                    <option value="Medical Rescue">Medical Rescue Assistance</option>
                    <option value="Threat Protection">Danger Defense Alert</option>
                    <option value="Fire Response">Fire Hazard Incident</option>
                    <option value="Maintenance Needed">Facilities Issue Report</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-400 font-bold mb-2 text-xs uppercase tracking-wider ml-1">PHYSICAL SECTOR / LOCATION</label>
                  <input 
                    type="text" 
                    placeholder="Enter specific campus coordinates or room number"
                    value={newReport.location}
                    onChange={(e) => setNewReport({ ...newReport, location: e.target.value })}
                    className="w-full p-4 aurora-input text-sm placeholder-slate-600 focus:outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-400 font-bold mb-2 text-xs uppercase tracking-wider ml-1">INCIDENT SYNOPSIS</label>
                  <textarea 
                    placeholder="Provide details about the emergency scene..."
                    value={newReport.details}
                    onChange={(e) => setNewReport({ ...newReport, details: e.target.value })}
                    className="w-full p-4 aurora-input h-32 text-sm placeholder-slate-600 focus:outline-none"
                  />
                </div>

                <button 
                  type="submit" 
                  className="w-full aurora-btn p-4 text-sm font-bold uppercase tracking-wider flex items-center justify-center gap-2"
                >
                  <Send className="w-4 h-4" /> Transmit Signal
                </button>
              </form>
            </div>

            {/* List */}
            <div className="aurora-card p-6">
              <h3 className="font-bold text-sm uppercase tracking-widest text-slate-300 mb-4 ml-1">Live Safety Feeds</h3>
              <div className="space-y-4">
                {reports.map((rep) => (
                  <div key={rep.id} className="aurora-card p-5 flex justify-between items-center gap-4 transition-all duration-300 hover:border-purple-500/30">
                    <div className="flex gap-4 items-center">
                      <div className="w-1.5 h-10 rounded-full bg-gradient-to-b from-purple-500 to-indigo-500"></div>
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-bold text-slate-200">{rep.category}</span>
                          <span className="text-[10px] text-slate-500">{rep.time}</span>
                        </div>
                        <p className="text-slate-400 text-xs flex items-center gap-1">
                          <MapPin className="w-3.5 h-3.5 text-purple-400" /> {rep.location}
                        </p>
                      </div>
                    </div>
                    <span className="px-3 py-1 rounded-lg font-bold text-[10px] bg-white/5 text-purple-300 border border-purple-500/10">
                      {rep.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      ) : (
        /* ================= ADMIN HUB ================= */
        <div className="flex flex-col gap-8 relative z-10">
          
          <div className="flex gap-4 p-1 bg-white/5 rounded-2xl border border-white/10 self-start">
            <button 
              onClick={() => setRole('admin')}
              className="px-5 py-2 rounded-xl font-bold text-xs uppercase tracking-wider bg-purple-500/15 text-purple-300 border border-purple-500/20"
            >
              Active Alarms ({activeSignals.length})
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {activeSignals.map((sig) => (
              <div key={sig.id} className="aurora-card p-6 flex flex-col justify-between border-l-2 border-l-purple-500">
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-[10px] text-slate-500 font-mono">{sig.id}</span>
                    <span className="text-[10px] font-bold text-purple-300 bg-purple-500/10 px-2.5 py-0.5 rounded-full">Active</span>
                  </div>

                  <h4 className="text-lg font-bold text-slate-200 mb-2 font-display">{sig.category}</h4>
                  <p className="text-xs text-slate-400 flex items-center gap-1 mb-6">
                    <MapPin className="w-3.5 h-3.5 text-purple-400" /> Assigned: {sig.location}
                  </p>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-white/5">
                  <span className="text-xs font-semibold text-slate-400">{sig.status}</span>
                  <button 
                    onClick={() => setActiveSignals(prev => prev.filter(s => s.id !== sig.id))}
                    className="aurora-btn px-4 py-2 text-xs font-bold uppercase tracking-wider"
                  >
                    Clear Alarm
                  </button>
                </div>
              </div>
            ))}
          </div>

        </div>
      )}
    </div>
  );
}

export default App;
