import { useState, useEffect } from 'react';
import { 
  Shield, 
  AlertTriangle, 
  MapPin, 
  Volume2, 
  VolumeX, 
  Clock, 
  Users, 
  Activity, 
  Flame, 
  Send,
  Zap,
  TrendingUp,
  UserPlus
} from 'lucide-react';

function App() {
  const [role, setRole] = useState('student');
  const [sosActive, setSosActive] = useState(false);
  const [sosCountdown, setSosCountdown] = useState(3);
  const [soundAlert, setSoundAlert] = useState(true);
  const [reports, setReports] = useState([
    { id: 1, category: 'MEDICAL EMERGENCY', location: 'Science Library - Floor 2', status: 'DISPATCHED', time: '5m ago', priority: 'HIGH' },
    { id: 2, category: 'FACILITIES FAILURE', location: 'Student Union Quad', status: 'RESOLVED', time: '2h ago', priority: 'LOW' }
  ]);
  const [newReport, setNewReport] = useState({ category: 'MEDICAL', location: '', details: '' });

  // Admin states
  const [adminTab, setAdminTab] = useState('signals');
  const [activeSignals, setActiveSignals] = useState([
    { id: 'SIG-901', category: 'ACTIVE THREAT ALERT', location: 'Engineering Hall - West wing', time: '1m ago', status: 'AWAITING DISPATCH', priority: 'CRITICAL' },
    { id: 'SIG-892', category: 'MEDICAL EMERGENCY', location: 'Recreation Center Gym', time: '4m ago', status: 'EN ROUTE', priority: 'HIGH' },
    { id: 'SIG-884', category: 'FIRE ALARM DUST', location: 'Chemistry Lab 102', time: '12m ago', status: 'RESOLVED', priority: 'MEDIUM' }
  ]);

  const [responders, setResponders] = useState([
    { id: 'R-10', name: 'Officer Miller', unit: 'Tactical Mobile 1', status: 'Active Dispatch', location: 'Science Library' },
    { id: 'R-12', name: 'Officer Chen', unit: 'Foot Patrol Alpha', status: 'Stationed', location: 'Student Union' }
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
        category: 'PANIC SOS BEACON',
        location: 'GPS: LIBRARY PLAZA ENTRANCE',
        time: 'JUST NOW',
        status: 'AWAITING DISPATCH',
        priority: 'CRITICAL'
      };
      setActiveSignals(prev => [newSignal, ...prev]);
      setReports(prev => [{
        id: Date.now(),
        category: 'PANIC SOS BEACON',
        location: 'LIBRARY PLAZA ENTRANCE',
        status: 'AWAITING DISPATCH',
        time: 'JUST NOW',
        priority: 'CRITICAL'
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
      category: newReport.category.toUpperCase() + ' INCIDENT',
      location: newReport.location.toUpperCase(),
      status: 'AWAITING DISPATCH',
      time: 'JUST NOW',
      priority: newReport.category === 'ACTIVE THREAT' || newReport.category === 'MEDICAL' ? 'HIGH' : 'MEDIUM'
    };
    setReports(prev => [reportData, ...prev]);
    setActiveSignals(prev => [{
      id: `SIG-${Math.floor(100 + Math.random() * 900)}`,
      category: reportData.category,
      location: reportData.location,
      time: reportData.time,
      status: reportData.status,
      priority: reportData.priority
    }, ...prev]);
    setNewReport({ category: 'MEDICAL', location: '', details: '' });
  };

  const handleDispatch = (sigId) => {
    setActiveSignals(prev => prev.map(sig => sig.id === sigId ? { ...sig, status: 'DISPATCHED' } : sig));
  };

  return (
    <div className="min-h-screen bg-[#FFFBEB] text-black font-sans select-none border-[12px] border-black p-4 md:p-8 flex flex-col gap-8">
      
      {/* Brutalist Warning Ribbon Header */}
      <div className="bg-red-500 text-white border-4 border-black p-4 brutalist-card flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-4">
          <div className="bg-yellow-400 text-black border-4 border-black p-2 font-black text-3xl rotate-[-2deg]">
            CAMPUS_SYNC.v1
          </div>
          <span className="font-mono text-xs tracking-wider uppercase bg-black text-yellow-300 px-2 py-1">
            STATUS: ACTIVE RADAR BROADCASTING
          </span>
        </div>
        
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setRole(role === 'student' ? 'admin' : 'student')}
            className="brutalist-btn px-6 py-2 bg-yellow-300 text-black font-black hover:bg-black hover:text-white"
          >
            SWITCH TO: {role === 'student' ? 'ADMIN_CONSOLE' : 'STUDENT_PORTAL'}
          </button>
          
          <button 
            onClick={() => setSoundAlert(!soundAlert)}
            className="border-4 border-black p-2 bg-white brutalist-card hover:bg-red-200"
          >
            {soundAlert ? <Volume2 className="w-6 h-6" /> : <VolumeX className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {role === 'student' ? (
        /* ================= STUDENT PORTAL ================= */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Col 1: Panic Button Box */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            <div className="brutalist-card bg-red-400 p-8 flex flex-col items-center justify-center text-center border-4 border-black relative overflow-hidden">
              <div className="absolute top-0 left-0 bg-yellow-400 text-black px-4 py-1 border-r-4 border-b-4 border-black font-black uppercase text-xs tracking-widest font-mono">
                SECURE EMERGENCY LINK
              </div>
              <Flame className="w-16 h-16 mb-4 animate-bounce text-black" />
              
              <h2 className="text-4xl font-black uppercase mb-2 tracking-tight leading-none">
                PANIC ALARM
              </h2>
              <p className="font-mono text-sm font-bold text-black mb-6 bg-yellow-200/60 p-2 border-2 border-black border-dashed">
                PRESS AND HOLD TO ACTIVATE BROADCAST. BEACON WILL TRANSMIT INSTANTLY.
              </p>

              <button
                onMouseDown={handleSosPress}
                onMouseUp={handleSosRelease}
                onMouseLeave={handleSosRelease}
                onTouchStart={handleSosPress}
                onTouchEnd={handleSosRelease}
                className={`w-48 h-48 rounded-full border-8 border-black text-2xl font-black transition-all uppercase flex items-center justify-center select-none ${
                  sosActive 
                    ? 'bg-black text-red-500 scale-95 shadow-none' 
                    : 'bg-red-600 text-white shadow-[8px_8px_0px_0px_#000]'
                }`}
              >
                {sosActive ? `SOS ( ${sosCountdown}s )` : 'HOLD TO SOS'}
              </button>

              {sosActive && (
                <div className="mt-6 w-full bg-white border-4 border-black h-8 overflow-hidden relative">
                  <div 
                    className="bg-yellow-400 h-full transition-all duration-1000 border-r-4 border-black"
                    style={{ width: `${((3 - sosCountdown) / 3) * 100}%` }}
                  />
                  <div className="absolute inset-0 flex items-center justify-center font-mono font-black text-xs">
                    EMITTING BROADCAST OVER GSM
                  </div>
                </div>
              )}
            </div>

            {/* Quick Status Bar */}
            <div className="brutalist-card bg-yellow-300 p-6 border-4 border-black">
              <h3 className="font-black text-xl mb-2 uppercase flex items-center gap-2">
                <Zap className="w-5 h-5" /> RECENTLY DETECTED BEACONS
              </h3>
              <div className="font-mono text-sm space-y-2">
                <div className="flex justify-between border-b-2 border-black/30 pb-1">
                  <span>MED BEACON #40</span>
                  <span className="font-bold text-red-600">PENDING DISPATCH</span>
                </div>
                <div className="flex justify-between border-b-2 border-black/30 pb-1">
                  <span>FIRE BEACON #12</span>
                  <span className="font-bold text-green-700">RESOLVED</span>
                </div>
              </div>
            </div>
          </div>

          {/* Col 2: Situation Report Form */}
          <div className="lg:col-span-7 flex flex-col gap-6">
            <div className="brutalist-card bg-white p-8 border-4 border-black">
              <h3 className="text-3xl font-black uppercase mb-6 border-b-4 border-black pb-2">
                SUBMIT INCIDENT DESK
              </h3>
              
              <form onSubmit={handleCreateReport} className="space-y-6">
                <div>
                  <label className="block uppercase font-black mb-2 text-sm">SELECT EMERGENCY GRADE</label>
                  <select 
                    value={newReport.category}
                    onChange={(e) => setNewReport({ ...newReport, category: e.target.value })}
                    className="w-full p-4 brutalist-input text-lg font-black focus:outline-none focus:bg-yellow-50"
                  >
                    <option value="MEDICAL">MEDICAL ASSISTANCE REQUIRED</option>
                    <option value="ACTIVE THREAT">ACTIVE SECURITY THREAT</option>
                    <option value="FIRE OUTBREAK">FIRE OR EXPLOSIVE HAZARD</option>
                    <option value="FACILITY HAZARD">INFRASTRUCTURE EMERGENCY</option>
                  </select>
                </div>

                <div>
                  <label className="block uppercase font-black mb-2 text-sm">EXACT CAMPUS LOCATION</label>
                  <input 
                    type="text" 
                    placeholder="e.g. DORM BUILDING B, ROOM 302"
                    value={newReport.location}
                    onChange={(e) => setNewReport({ ...newReport, location: e.target.value })}
                    className="w-full p-4 brutalist-input text-lg font-bold placeholder-black/40 focus:outline-none focus:bg-yellow-50"
                    required
                  />
                </div>

                <div>
                  <label className="block uppercase font-black mb-2 text-sm">INCIDENT LOGS / DESCRIPTION</label>
                  <textarea 
                    placeholder="Type details of the situation here (optional)"
                    value={newReport.details}
                    onChange={(e) => setNewReport({ ...newReport, details: e.target.value })}
                    className="w-full p-4 brutalist-input h-32 text-md font-medium focus:outline-none focus:bg-yellow-50"
                  />
                </div>

                <button 
                  type="submit" 
                  className="w-full brutalist-btn p-4 bg-yellow-400 hover:bg-black hover:text-yellow-400 text-xl font-black uppercase flex items-center justify-center gap-2"
                >
                  <Send className="w-6 h-6" /> TRANSMIT SITUATION REPORT
                </button>
              </form>
            </div>

            {/* List of active student reports */}
            <div className="brutalist-card bg-orange-200 p-6 border-4 border-black">
              <h3 className="font-black text-xl mb-4 uppercase">YOUR REPORT FILED LOGS</h3>
              <div className="space-y-4">
                {reports.map((rep) => (
                  <div key={rep.id} className="bg-white border-4 border-black p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-2 shadow-[4px_4px_0px_0px_#000]">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="bg-black text-white px-2 py-0.5 text-xs font-mono font-bold uppercase">{rep.category}</span>
                        <span className="font-mono text-xs text-black/60">{rep.time}</span>
                      </div>
                      <p className="font-black flex items-center gap-1"><MapPin className="w-4 h-4" /> {rep.location}</p>
                    </div>
                    <span className="bg-yellow-400 text-black border-2 border-black font-black px-3 py-1 text-xs">
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
        <div className="flex flex-col gap-6">
          
          {/* Tab Selection buttons */}
          <div className="flex gap-4 border-b-4 border-black pb-4">
            <button 
              onClick={() => setAdminTab('signals')}
              className={`brutalist-btn px-6 py-3 font-black uppercase ${adminTab === 'signals' ? 'bg-yellow-400' : 'bg-white'}`}
            >
              BROADCAST SIGNALS ({activeSignals.length})
            </button>
            <button 
              onClick={() => setAdminTab('responders')}
              className={`brutalist-btn px-6 py-3 font-black uppercase ${adminTab === 'responders' ? 'bg-yellow-400' : 'bg-white'}`}
            >
              RESPONDERS AT POSTS ({responders.length})
            </button>
            <button 
              onClick={() => setAdminTab('stats')}
              className={`brutalist-btn px-6 py-3 font-black uppercase ${adminTab === 'stats' ? 'bg-yellow-400' : 'bg-white'}`}
            >
              ANALYTICS GRIDS
            </button>
          </div>

          {adminTab === 'signals' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {activeSignals.map((sig) => (
                <div key={sig.id} className="brutalist-card bg-white p-6 border-4 border-black flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-center mb-4">
                      <span className="font-mono font-black text-sm bg-black text-white px-2 py-0.5">{sig.id}</span>
                      <span className={`border-2 border-black px-2 py-0.5 text-xs font-black uppercase ${
                        sig.priority === 'CRITICAL' ? 'bg-red-500 text-white' : 'bg-yellow-400 text-black'
                      }`}>{sig.priority}</span>
                    </div>

                    <h4 className="text-2xl font-black uppercase mb-2 flex items-center gap-2">
                      <AlertTriangle className="w-6 h-6 text-red-600" /> {sig.category}
                    </h4>
                    <p className="font-mono text-sm mb-4 font-bold flex items-center gap-1 text-black/80">
                      <MapPin className="w-4 h-4 text-black" /> {sig.location}
                    </p>
                    <p className="font-mono text-xs text-black/60 mb-6">SIGNAL RECEIVED: {sig.time}</p>
                  </div>

                  <div className="flex items-center justify-between border-t-4 border-black pt-4">
                    <span className="font-mono text-xs font-black uppercase text-orange-600 bg-orange-100 border-2 border-orange-600 px-2 py-0.5">{sig.status}</span>
                    {sig.status === 'AWAITING DISPATCH' && (
                      <button 
                        onClick={() => handleDispatch(sig.id)}
                        className="brutalist-btn px-4 py-2 bg-yellow-300 text-xs text-black"
                      >
                        DISPATCH DISASTER RESPONDERS
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {adminTab === 'responders' && (
            <div className="brutalist-card bg-white p-8 border-4 border-black">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-3xl font-black uppercase">RESPONDERS ON CALL</h3>
                <button className="brutalist-btn px-4 py-2 bg-yellow-300 flex items-center gap-2">
                  <UserPlus className="w-5 h-5" /> RECRUIT OFFICER
                </button>
              </div>
              <div className="space-y-4">
                {responders.map(resp => (
                  <div key={resp.id} className="border-4 border-black p-4 bg-yellow-50 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div className="flex gap-4 items-center">
                      <div className="w-12 h-12 bg-black border-4 border-black text-yellow-300 font-black flex items-center justify-center text-lg">
                        {resp.id}
                      </div>
                      <div>
                        <h4 className="text-lg font-black uppercase">{resp.name}</h4>
                        <span className="font-mono text-xs bg-black text-white px-2 py-0.5">{resp.unit}</span>
                      </div>
                    </div>
                    <div className="font-mono text-sm font-bold flex items-center gap-1">
                      <MapPin className="w-4 h-4" /> CURRENT ZONE: {resp.location}
                    </div>
                    <span className="bg-green-300 border-2 border-black px-3 py-1 font-black text-xs uppercase">
                      {resp.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {adminTab === 'stats' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="brutalist-card bg-blue-300 p-6 border-4 border-black">
                <h4 className="font-black text-lg uppercase mb-4">INCIDENT HISTORIAN</h4>
                <div className="text-6xl font-black mb-4">42</div>
                <p className="font-mono text-xs uppercase font-bold text-black/70">Total events recorded on server in past 24 hours.</p>
              </div>
              
              <div className="brutalist-card bg-green-300 p-6 border-4 border-black">
                <h4 className="font-black text-lg uppercase mb-4">RESPONSE VELOCITY</h4>
                <div className="text-6xl font-black mb-4">1.8m</div>
                <p className="font-mono text-xs uppercase font-bold text-black/70">Average duration to dispatch responder units to location.</p>
              </div>

              <div className="brutalist-card bg-orange-300 p-6 border-4 border-black">
                <h4 className="font-black text-lg uppercase mb-4">OPERATIONAL EFFICIENCY</h4>
                <div className="text-6xl font-black mb-4">98%</div>
                <p className="font-mono text-xs uppercase font-bold text-black/70">Events resolved successfully by emergency control desk.</p>
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}

export default App;
