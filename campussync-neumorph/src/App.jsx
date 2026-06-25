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
  Sliders,
  Power
} from 'lucide-react';

function App() {
  const [role, setRole] = useState('student');
  const [sosActive, setSosActive] = useState(false);
  const [sosCountdown, setSosCountdown] = useState(3);
  const [soundAlert, setSoundAlert] = useState(true);
  const [reports, setReports] = useState([
    { id: 1, category: 'Medical Rescue', location: 'Science Library - Floor 2', status: 'En Route', time: '5m ago' },
    { id: 2, category: 'Facilities Alert', location: 'Student Union Quad', status: 'Resolved', time: '2h ago' }
  ]);
  const [newReport, setNewReport] = useState({ category: 'Medical Rescue', location: '', details: '' });

  // Admin state
  const [activeSignals, setActiveSignals] = useState([
    { id: 'SIG-901', category: 'Security Beacon Alert', location: 'Engineering Hall East', time: '1m ago', status: 'Pending Dispatch' },
    { id: 'SIG-892', category: 'Medical Emergency Core', location: 'Gymnasia Complex', time: '4m ago', status: 'Responders En Route' }
  ]);

  const [responders, setResponders] = useState([
    { id: 'R-10', name: 'Officer John', unit: 'Safety squad 1', status: 'Active', location: 'Library' },
    { id: 'R-12', name: 'Officer Clara', unit: 'Safety squad 2', status: 'At Base', location: 'Union' }
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
        location: 'Main Gate Intersection',
        time: 'Just now',
        status: 'Pending Dispatch'
      };
      setActiveSignals(prev => [newSignal, ...prev]);
      setReports(prev => [{
        id: Date.now(),
        category: 'Quick Beacon SOS',
        location: 'Main Gate Intersection',
        status: 'Pending Dispatch',
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
      status: 'Awaiting Dispatch',
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
    <div className="min-h-screen bg-[#e0e0e0] text-slate-700 p-6 md:p-10 font-sans select-none flex flex-col gap-8">
      
      {/* Neumorphic Header Desk */}
      <header className="neumorph-card-out p-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#e0e0e0] flex items-center justify-center text-red-500 shadow-[inset_2px_2px_5px_#bebebe,inset_-2px_-2px_5px_#ffffff]">
            <Power className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight text-slate-800 font-display">CAMPUS_SYNC Console</h1>
            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Tactical Safety Hardware Desk</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button 
            onClick={() => setRole(role === 'student' ? 'admin' : 'student')}
            className={`neumorph-btn px-6 py-3 text-xs font-bold uppercase tracking-wider ${role === 'admin' ? 'neumorph-btn-active text-indigo-600' : ''}`}
          >
            SYS CONSOLE: {role === 'student' ? 'STUDENT DESK' : 'ADMIN DESK'}
          </button>
          
          <button 
            onClick={() => setSoundAlert(!soundAlert)}
            className={`w-12 h-12 flex items-center justify-center rounded-2xl neumorph-btn ${!soundAlert ? 'neumorph-btn-active' : ''}`}
          >
            {soundAlert ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>
        </div>
      </header>

      {role === 'student' ? (
        /* ================= STUDENT DESK ================= */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Physical Button Mold */}
          <div className="lg:col-span-5 flex flex-col gap-8">
            <div className="neumorph-card-out p-8 flex flex-col items-center text-center">
              <span className="text-[10px] text-slate-400 font-bold uppercase px-3 py-1 bg-[#e0e0e0] shadow-[inset_2px_2px_5px_#bebebe,inset_-2px_-2px_5px_#ffffff] rounded-full mb-6">
                SAFETY BROADCAST SYSTEM
              </span>
              
              <h2 className="text-lg font-bold text-slate-800 mb-2 font-display">HOLD TO ACTIVATE</h2>
              <p className="text-xs text-slate-500 mb-8 max-w-xs leading-relaxed">
                Firmly press the molded button below for 3 seconds. The physical spring activates telemetry rescue beacon.
              </p>

              {/* Inset physical button */}
              <div className="w-40 h-40 rounded-full bg-[#e0e0e0] shadow-[inset_8px_8px_16px_#bebebe,inset_-8px_-8px_16px_#ffffff] flex items-center justify-center">
                <button
                  onMouseDown={handleSosPress}
                  onMouseUp={handleSosRelease}
                  onMouseLeave={handleSosRelease}
                  onTouchStart={handleSosPress}
                  onTouchEnd={handleSosRelease}
                  className={`w-32 h-32 rounded-full flex flex-col items-center justify-center transition-all duration-150 ${
                    sosActive 
                      ? 'shadow-[inset_4px_4px_8px_#bebebe,inset_-4px_-4px_8px_#ffffff] scale-95 text-red-500' 
                      : 'shadow-[6px_6px_12px_#bebebe,-6px_-6px_12px_#ffffff] text-slate-500'
                  }`}
                  style={{ backgroundColor: '#e0e0e0' }}
                >
                  <Flame className="w-10 h-10 mb-2" />
                  <span className="font-extrabold text-[10px] uppercase tracking-widest font-display">
                    {sosActive ? `LOCK (${sosCountdown}s)` : 'PUSH SOS'}
                  </span>
                </button>
              </div>

              {sosActive && (
                <div className="mt-8 w-full neumorph-card-in h-4 overflow-hidden p-1">
                  <div 
                    className="bg-red-500 h-full rounded-full transition-all duration-1000"
                    style={{ width: `${((3 - sosCountdown) / 3) * 100}%` }}
                  />
                </div>
              )}
            </div>

            <div className="neumorph-card-out p-6 flex flex-col">
              <h3 className="font-bold text-xs uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2">
                <Radio className="w-4 h-4 text-indigo-600 animate-pulse" /> TELEMETRY RX
              </h3>
              <div className="text-xs text-slate-500 space-y-2">
                <p className="flex justify-between border-b border-slate-300/40 pb-2">
                  <span>GPS Core Status</span>
                  <span className="font-bold">ENGAGED</span>
                </p>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-7 flex flex-col gap-8">
            <div className="neumorph-card-out p-8">
              <h3 className="text-md font-bold text-slate-800 font-display mb-6">// DEBOSS EMERGENCY PARAMS</h3>
              
              <form onSubmit={handleCreateReport} className="space-y-6">
                <div>
                  <label className="block text-slate-500 font-bold mb-2 text-xs uppercase tracking-wider ml-1">INCIDENT GRADE</label>
                  <select 
                    value={newReport.category}
                    onChange={(e) => setNewReport({ ...newReport, category: e.target.value })}
                    className="w-full p-4 neumorph-input text-sm font-semibold focus:outline-none"
                  >
                    <option value="Medical Rescue">Medical Rescue Unit</option>
                    <option value="Threat Alert">Threat Protection Team</option>
                    <option value="Fire Hazard">Fire Dispatch Alert</option>
                    <option value="Facilities Alert">Facilities Outage</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-500 font-bold mb-2 text-xs uppercase tracking-wider ml-1">COORDINATE / CAMPUS AREA</label>
                  <input 
                    type="text" 
                    placeholder="Enter physical location details"
                    value={newReport.location}
                    onChange={(e) => setNewReport({ ...newReport, location: e.target.value })}
                    className="w-full p-4 neumorph-input text-sm placeholder-slate-400 focus:outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-slate-500 font-bold mb-2 text-xs uppercase tracking-wider ml-1">DETAILS SYNOPSIS</label>
                  <textarea 
                    placeholder="Describe scene parameters..."
                    value={newReport.details}
                    onChange={(e) => setNewReport({ ...newReport, details: e.target.value })}
                    className="w-full p-4 neumorph-input h-32 text-sm placeholder-slate-400 focus:outline-none"
                  />
                </div>

                <button 
                  type="submit" 
                  className="w-full neumorph-btn p-4 text-sm font-bold uppercase tracking-wider flex items-center justify-center gap-2"
                >
                  <Send className="w-4 h-4" /> TRANSMIT SIGNAL
                </button>
              </form>
            </div>

            {/* List */}
            <div className="neumorph-card-out p-6">
              <h3 className="font-bold text-xs uppercase tracking-widest text-slate-500 mb-4 ml-1">LOGGED TRANSMISSIONS</h3>
              <div className="space-y-4">
                {reports.map((rep) => (
                  <div key={rep.id} className="neumorph-card-in p-5 flex justify-between items-center gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-extrabold text-slate-800 text-sm">{rep.category}</span>
                        <span className="text-[10px] text-slate-400">{rep.time}</span>
                      </div>
                      <p className="text-slate-500 text-xs flex items-center gap-1 font-mono">
                        <MapPin className="w-3.5 h-3.5" /> GPS: {rep.location}
                      </p>
                    </div>
                    <span className="px-3.5 py-1.5 rounded-full font-bold text-xs bg-[#e0e0e0] shadow-[2px_2px_5px_#bebebe,-2px_-2px_5px_#ffffff] text-slate-600">
                      {rep.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      ) : (
        /* ================= ADMIN DESK ================= */
        <div className="flex flex-col gap-6">
          
          <div className="flex gap-4 p-2 bg-[#e0e0e0] shadow-[inset_2px_2px_5px_#bebebe,inset_-2px_-2px_5px_#ffffff] rounded-2xl self-start">
            <button 
              className="px-5 py-2 rounded-xl font-bold text-xs uppercase tracking-wider shadow-[2px_2px_5px_#bebebe,-2px_-2px_5px_#ffffff] text-slate-800"
            >
              ACTIVE ALARMS ({activeSignals.length})
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {activeSignals.map((sig) => (
              <div key={sig.id} className="neumorph-card-out p-6 flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-[10px] text-slate-400 font-mono">{sig.id}</span>
                    <span className="text-[10px] font-bold text-rose-600 shadow-[inset_2px_2px_4px_#bebebe,inset_-2px_-2px_4px_#ffffff] px-2.5 py-1 rounded-full bg-[#e0e0e0]">ACTIVE</span>
                  </div>

                  <h4 className="text-sm font-bold text-slate-800 mb-2 uppercase">{sig.category}</h4>
                  <p className="text-xs text-slate-500 flex items-center gap-1 mb-6">
                    <MapPin className="w-3.5 h-3.5 text-indigo-500" /> COORDINATES: {sig.location}
                  </p>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-slate-300/40">
                  <span className="text-xs font-semibold text-slate-500">{sig.status}</span>
                  <button 
                    onClick={() => setActiveSignals(prev => prev.filter(s => s.id !== sig.id))}
                    className="neumorph-btn px-4 py-2 text-xs font-bold uppercase tracking-wider"
                  >
                    RESOLVE BEACON
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
