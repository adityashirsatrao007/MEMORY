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
  Cpu,
  Terminal,
  Grid
} from 'lucide-react';

function App() {
  const [role, setRole] = useState('student');
  const [sosActive, setSosActive] = useState(false);
  const [sosCountdown, setSosCountdown] = useState(3);
  const [soundAlert, setSoundAlert] = useState(true);
  const [reports, setReports] = useState([
    { id: 1, category: 'MEDICAL CORE', location: 'SECTOR-C / LIBRARY L2', status: 'UNITS DISPATCHED', time: '05:00 ago' },
    { id: 2, category: 'SYSTEM INCIDENT', location: 'SECTOR-A / STUDENT CTR', status: 'RESOLVED', time: '02:00:00 ago' }
  ]);
  const [newReport, setNewReport] = useState({ category: 'MEDICAL CORE', location: '', details: '' });

  // Admin state
  const [adminTab, setAdminTab] = useState('signals');
  const [activeSignals, setActiveSignals] = useState([
    { id: 'SIG-901', category: 'THREAT ALERT INTRUSION', location: 'SECTOR-E / ENG HALL', time: '01:00 ago', status: 'AWAITING RESPONSE' },
    { id: 'SIG-892', category: 'MEDICAL ALERT SYSTEM', location: 'SECTOR-F / RECREATION', time: '04:00 ago', status: 'UNITS EN ROUTE' }
  ]);

  const [responders, setResponders] = useState([
    { id: 'R-10', name: 'UNIT MILLER', unit: 'TACTICAL M-1', status: 'DISPATCHED', location: 'SECTOR-C' },
    { id: 'R-12', name: 'UNIT CHEN', unit: 'ALPHA FOOT-P', status: 'STANDBY', location: 'SECTOR-A' }
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
        category: 'BEACON ACTIVATED',
        location: 'GPS GRID // PLAZA MAIN',
        time: '00:00 ago',
        status: 'AWAITING RESPONSE'
      };
      setActiveSignals(prev => [newSignal, ...prev]);
      setReports(prev => [{
        id: Date.now(),
        category: 'BEACON ACTIVATED',
        location: 'PLAZA MAIN',
        status: 'AWAITING RESPONSE',
        time: '00:00 ago'
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
      category: newReport.category.toUpperCase(),
      location: newReport.location.toUpperCase(),
      status: 'AWAITING DISPATCH',
      time: '00:00 ago'
    };
    setReports(prev => [reportData, ...prev]);
    setActiveSignals(prev => [{
      id: `SIG-${Math.floor(100 + Math.random() * 900)}`,
      category: reportData.category,
      location: reportData.location,
      time: reportData.time,
      status: reportData.status
    }, ...prev]);
    setNewReport({ category: 'MEDICAL CORE', location: '', details: '' });
  };

  return (
    <div className="min-h-screen bg-[#050209] text-[#00f0ff] p-6 md:p-8 font-mono select-none relative overflow-hidden">
      {/* Sci-Fi Grid lines */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(0,240,255,0.015)_1px,transparent_1px),linear-gradient(to_bottom,rgba(0,240,255,0.015)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none"></div>

      {/* Holographic background glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[140px] pointer-events-none"></div>
      <div className="absolute bottom-[20%] right-[-10%] w-[600px] h-[600px] bg-purple-600/5 rounded-full blur-[160px] pointer-events-none"></div>

      {/* Header HUD */}
      <header className="glass-panel p-5 rounded-xl flex flex-col md:flex-row justify-between items-center gap-4 mb-8 border border-cyan-500/20">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
            <Cpu className="w-6 h-6 text-cyan-400 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-widest text-cyan-300">CAMPUS_SYNC_SYS // HUD</h1>
            <p className="text-xs text-cyan-500/70 font-mono">TELEMETRY LINK STATUS: STEADY</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button 
            onClick={() => setRole(role === 'student' ? 'admin' : 'student')}
            className="glass-btn px-5 py-2 rounded-lg text-xs font-bold uppercase tracking-wider text-cyan-400 border border-cyan-500/30"
          >
            SYSMODE: {role === 'student' ? 'NODE_PORTAL' : 'SYS_ADMIN'}
          </button>
          
          <button 
            onClick={() => setSoundAlert(!soundAlert)}
            className="w-10 h-10 flex items-center justify-center rounded-lg bg-cyan-950/20 border border-cyan-500/20 text-cyan-400 transition-all hover:bg-cyan-500/10"
          >
            {soundAlert ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>
        </div>
      </header>

      {role === 'student' ? (
        /* ================= STUDENT PORTAL ================= */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
          
          {/* Beacon Console HUD */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            <div className="glass-panel p-6 rounded-xl border border-cyan-500/20 flex flex-col items-center justify-center text-center">
              <span className="text-xs text-purple-400 border border-purple-500/30 bg-purple-500/5 px-3 py-1 rounded mb-6 tracking-widest">
                CYBERNETIC SATELLITE BEACON
              </span>
              
              <h2 className="text-lg font-bold text-cyan-200 mb-2 tracking-widest">SOS PROTOCOL 77</h2>
              <p className="text-xs text-cyan-500/60 mb-8 max-w-xs leading-relaxed">
                INITIATE DUPLEX GSM BEACON LOCATOR. KEEP PRESSED TO TRANSMIT CURRENT CELL COORDINATES.
              </p>

              {/* Glowing circular trigger */}
              <button
                onMouseDown={handleSosPress}
                onMouseUp={handleSosRelease}
                onMouseLeave={handleSosRelease}
                onTouchStart={handleSosPress}
                onTouchEnd={handleSosRelease}
                className={`w-40 h-40 rounded-full border-2 transition-all flex flex-col items-center justify-center relative ${
                  sosActive 
                    ? 'border-red-500 bg-red-950/20 shadow-[0_0_30px_rgba(239,68,68,0.4)]' 
                    : 'border-cyan-500 bg-cyan-950/10 shadow-[0_0_20px_rgba(6,182,212,0.15)]'
                }`}
              >
                {/* Radar animation sweep */}
                <div className="absolute inset-2 rounded-full border border-dashed border-cyan-500/20 animate-spin"></div>
                <Flame className={`w-10 h-10 mb-2 ${sosActive ? 'text-red-500 animate-ping' : 'text-cyan-400'}`} />
                <span className="text-xs font-bold tracking-widest uppercase">
                  {sosActive ? `TXING (${sosCountdown}s)` : 'ENGAGE SOS'}
                </span>
              </button>

              {sosActive && (
                <div className="mt-8 w-full bg-cyan-950/30 border border-cyan-500/30 rounded-sm h-3 overflow-hidden p-0.5">
                  <div 
                    className="bg-red-500 h-full transition-all duration-1000"
                    style={{ width: `${((3 - sosCountdown) / 3) * 100}%` }}
                  />
                </div>
              )}
            </div>

            <div className="glass-panel p-5 rounded-xl border border-cyan-500/20 flex flex-col">
              <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                <Terminal className="w-4 h-4" /> FEED LOGS
              </h3>
              <div className="text-xs text-cyan-500/70 space-y-2 font-mono">
                <p>&gt; SECURE PROTOCOL SYNCED...</p>
                <p>&gt; READY FOR GPS BEACON DISPATCH...</p>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-7 flex flex-col gap-6">
            <div className="glass-panel p-6 rounded-xl border border-cyan-500/20">
              <h3 className="text-md font-bold text-cyan-300 uppercase tracking-widest mb-6 pb-2 border-b border-cyan-500/20">
                // TRANSMIT INCIDENT DATAFRAME
              </h3>
              
              <form onSubmit={handleCreateReport} className="space-y-6">
                <div>
                  <label className="block text-xs font-bold text-cyan-500 uppercase tracking-widest mb-2">ALERT VECTOR CLASS</label>
                  <select 
                    value={newReport.category}
                    onChange={(e) => setNewReport({ ...newReport, category: e.target.value })}
                    className="w-full p-3 glass-input rounded text-sm focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
                  >
                    <option value="MEDICAL CORE">MEDICAL ASSISTANCE INTERFACE</option>
                    <option value="INTRUDER THREAT">INTRUDER HAZARD THREAT</option>
                    <option value="HAZARDOUS DETONATION">HAZARDOUS DISCHARGE DETECT</option>
                    <option value="SYSTEM INCIDENT">INFRASTRUCTURE CORE MALFUNCTION</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-cyan-500 uppercase tracking-widest mb-2">TELEMETRY GRID LOCATOR</label>
                  <input 
                    type="text" 
                    placeholder="ENTER LOCATOR ADDRESS OR SECTOR ID"
                    value={newReport.location}
                    onChange={(e) => setNewReport({ ...newReport, location: e.target.value })}
                    className="w-full p-3 glass-input rounded text-sm placeholder-cyan-900 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-cyan-500 uppercase tracking-widest mb-2">TELEMETRY PAYLOAD DETAILS</label>
                  <textarea 
                    placeholder="ENTER SPECIFIC DESCRIPTIVE EVENT PARAMETERS..."
                    value={newReport.details}
                    onChange={(e) => setNewReport({ ...newReport, details: e.target.value })}
                    className="w-full p-3 glass-input rounded text-sm h-28 placeholder-cyan-900 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
                  />
                </div>

                <button 
                  type="submit" 
                  className="w-full glass-btn p-3 rounded font-bold uppercase tracking-widest text-sm text-cyan-400 border border-cyan-500/30 flex items-center justify-center gap-2"
                >
                  <Send className="w-4 h-4" /> BROADCAST INCIDENT DATAFRAME
                </button>
              </form>
            </div>

            {/* List */}
            <div className="glass-panel p-5 rounded-xl border border-cyan-500/20">
              <h3 className="text-xs font-bold uppercase tracking-widest text-cyan-300 mb-4">// HISTORICAL DATASTREAM</h3>
              <div className="space-y-4">
                {reports.map((rep) => (
                  <div key={rep.id} className="glass-panel p-4 rounded border border-cyan-500/10 flex justify-between items-center gap-4 transition-all hover:bg-cyan-500/5">
                    <div>
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-xs text-purple-400 font-bold tracking-wider">{rep.category}</span>
                        <span className="text-[10px] text-cyan-600">{rep.time}</span>
                      </div>
                      <p className="text-xs text-cyan-200 flex items-center gap-1 font-mono">
                        <MapPin className="w-3.5 h-3.5 text-cyan-500" /> GPS LOC: {rep.location}
                      </p>
                    </div>
                    <span className="text-[10px] font-bold text-cyan-400 bg-cyan-950/30 border border-cyan-500/20 px-3 py-1 rounded">
                      {rep.status || 'TRANSMITTING'}
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      ) : (
        /* ================= ADMIN CONSOLE ================= */
        <div className="flex flex-col gap-6 relative z-10">
          
          <div className="flex gap-4 border-b border-cyan-500/20 pb-4">
            <button 
              onClick={() => setAdminTab('signals')}
              className={`px-5 py-2 text-xs font-bold uppercase tracking-widest rounded border ${adminTab === 'signals' ? 'border-cyan-400 text-cyan-300 bg-cyan-950/20' : 'border-transparent text-cyan-500'}`}
            >
              ACTIVE SIGNALS ({activeSignals.length})
            </button>
            <button 
              onClick={() => setAdminTab('responders')}
              className={`px-5 py-2 text-xs font-bold uppercase tracking-widest rounded border ${adminTab === 'responders' ? 'border-cyan-400 text-cyan-300 bg-cyan-950/20' : 'border-transparent text-cyan-500'}`}
            >
              ACTIVE OFFICERS ({responders.length})
            </button>
          </div>

          {adminTab === 'signals' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {activeSignals.map((sig) => (
                <div key={sig.id} className="glass-panel p-5 rounded-xl border border-cyan-500/20 flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-[10px] text-cyan-500 bg-cyan-950/40 border border-cyan-500/20 px-2 py-0.5 rounded font-mono">{sig.id}</span>
                      <span className="text-[10px] text-red-400 border border-red-500/20 bg-red-950/20 px-2.5 py-0.5 rounded">CRITICAL</span>
                    </div>

                    <h4 className="text-sm font-bold tracking-widest text-cyan-200 mb-2 uppercase">{sig.category}</h4>
                    <p className="text-xs text-cyan-500/70 flex items-center gap-1 mb-6">
                      <MapPin className="w-3.5 h-3.5 text-cyan-400" /> LOCATOR: {sig.location}
                    </p>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-cyan-500/10">
                    <span className="text-[10px] text-yellow-400 font-bold tracking-wider">{sig.status}</span>
                    <button 
                      onClick={() => setActiveSignals(prev => prev.filter(s => s.id !== sig.id))}
                      className="glass-btn px-3 py-1.5 rounded text-[10px] font-bold uppercase tracking-wider text-cyan-400 border border-cyan-500/30"
                    >
                      DISMISS BEACON
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {adminTab === 'responders' && (
            <div className="glass-panel p-6 rounded-xl border border-cyan-500/20">
              <h3 className="text-sm font-bold uppercase tracking-widest text-cyan-300 mb-6">POLICE TELEMETRY GRID</h3>
              <div className="space-y-4">
                {responders.map(resp => (
                  <div key={resp.id} className="p-4 bg-cyan-950/10 border border-cyan-500/10 rounded flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div className="flex gap-4 items-center">
                      <div className="w-10 h-10 rounded border border-cyan-500/30 bg-cyan-950/30 flex items-center justify-center font-bold text-xs text-cyan-400">
                        {resp.id}
                      </div>
                      <div>
                        <h4 className="text-xs font-bold uppercase tracking-widest text-cyan-200">{resp.name}</h4>
                        <span className="text-[9px] font-bold text-cyan-500 bg-cyan-950/40 border border-cyan-500/10 px-2 py-0.5 rounded uppercase tracking-wider">{resp.unit}</span>
                      </div>
                    </div>
                    <div className="text-xs text-cyan-500/70 flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5 text-cyan-400" /> SECTOR ASSIGNMENT: {resp.location}
                    </div>
                    <span className="text-[10px] text-cyan-400 border border-cyan-500/20 bg-cyan-950/20 px-3 py-1 rounded font-bold uppercase">
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
