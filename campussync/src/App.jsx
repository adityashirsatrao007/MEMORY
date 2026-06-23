import { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { 
  Shield, 
  MapPin, 
  Clock, 
  Radio, 
  Flame, 
  Send,
  Zap,
  ArrowDown,
  Layers,
  HeartPulse,
  Activity,
  UserCheck
} from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

function App() {
  const [role, setRole] = useState('student');
  const [sosActive, setSosActive] = useState(false);
  const [sosCountdown, setSosCountdown] = useState(3);
  const [reports, setReports] = useState([
    { id: 1, category: 'Medical Rescue', location: 'Science Library - Floor 2', status: 'En Route', time: '5m ago' },
    { id: 2, category: 'Facilities Alert', location: 'Student Union Quad', status: 'Resolved', time: '2h ago' }
  ]);
  const [newReport, setNewReport] = useState({ category: 'Medical Rescue', location: '', details: '' });

  // Pinned DOM & WebGL references
  const containerRef = useRef(null);
  const scrollyContainerRef = useRef(null);
  const slide1Ref = useRef(null);
  const slide2Ref = useRef(null);
  const slide3Ref = useRef(null);
  const slide4Ref = useRef(null);
  const slide5Ref = useRef(null);

  // Single unified useEffect for ThreeJS + GSAP ScrollTrigger
  useEffect(() => {
    if (!containerRef.current || !scrollyContainerRef.current) return;

    // --- 1. Three.js Scene Setup ---
    const scene = new THREE.Scene();

    // Use window sizes as fallback for robust initialization when container client bounds are 0
    const width = containerRef.current.clientWidth || window.innerWidth;
    const height = containerRef.current.clientHeight || window.innerHeight;

    const camera = new THREE.PerspectiveCamera(
      45,
      width / height,
      0.1,
      1000
    );
    camera.position.set(0, 5, 9);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    
    // Clear to avoid multiple canvas accumulation
    containerRef.current.innerHTML = '';
    containerRef.current.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.95);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f0ff, 2.5, 50);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    // Alert Light (activated on final slide)
    const redAlertLight = new THREE.PointLight(0xff0055, 0, 50);
    redAlertLight.position.set(0, 3, 3);
    scene.add(redAlertLight);

    // Dashboard texture
    const textureLoader = new THREE.TextureLoader();
    const dashboardTexture = textureLoader.load('/campus_dashboard.png');

    // 3D Plane Mesh
    const geometry = new THREE.PlaneGeometry(8, 8);
    const material = new THREE.MeshBasicMaterial({
      map: dashboardTexture,
      transparent: true,
      opacity: 0.95,
      side: THREE.DoubleSide
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.rotation.x = -Math.PI / 2;
    scene.add(mesh);

    // Holographic Grid Overlay (higher segments for morphing terrain)
    const gridGeometry = new THREE.PlaneGeometry(8.1, 8.1, 32, 32);
    const gridMaterial = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.18,
      side: THREE.DoubleSide
    });
    const gridMesh = new THREE.Mesh(gridGeometry, gridMaterial);
    gridMesh.rotation.x = -Math.PI / 2;
    gridMesh.position.y = 0.02; // Offset
    scene.add(gridMesh);

    // Extract original coordinates for terrain wave morphing
    const gridPosAttr = gridGeometry.attributes.position;
    const originalGridCoords = gridPosAttr.array.slice();

    // Node particles
    const particleGeo = new THREE.BufferGeometry();
    const particleCount = 200;
    const posArray = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i++) {
      posArray[i] = (Math.random() - 0.5) * 15;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const particleMat = new THREE.PointsMaterial({
      size: 0.04,
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.6
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // Interactive Floating 3D Nodes (Cubes & Octahedrons)
    const shapesGroup = new THREE.Group();
    scene.add(shapesGroup);
    const shapeGeometries = [
      new THREE.BoxGeometry(0.35, 0.35, 0.35),
      new THREE.OctahedronGeometry(0.25)
    ];
    const shapes = [];
    for (let i = 0; i < 20; i++) {
      const geo = shapeGeometries[Math.floor(Math.random() * shapeGeometries.length)];
      const mat = new THREE.MeshPhongMaterial({
        color: Math.random() > 0.5 ? 0x00f0ff : 0xa855f7,
        transparent: true,
        opacity: 0.55,
        wireframe: Math.random() > 0.6,
        shininess: 80,
        specular: 0xffffff
      });
      const meshShape = new THREE.Mesh(geo, mat);
      meshShape.position.set(
        (Math.random() - 0.5) * 14,
        (Math.random() - 0.5) * 9,
        (Math.random() - 0.5) * 12
      );
      meshShape.rotation.set(
        Math.random() * Math.PI,
        Math.random() * Math.PI,
        0
      );
      meshShape.userData = {
        rotX: (Math.random() - 0.5) * 0.015,
        rotY: (Math.random() - 0.5) * 0.015,
        floatSpeed: 0.001 + Math.random() * 0.002,
        floatDistance: 0.15 + Math.random() * 0.25,
        initialY: meshShape.position.y
      };
      shapesGroup.add(meshShape);
      shapes.push(meshShape);
    }

    // Dynamic Connections Linking the Nodes
    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.18
    });
    const lineGeometry = new THREE.BufferGeometry();
    const linePositions = new Float32Array(shapes.length * shapes.length * 6);
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    const connectionLines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(connectionLines);

    // SOS beacon marker
    const beaconGeo = new THREE.SphereGeometry(0.18, 16, 16);
    const beaconMat = new THREE.MeshBasicMaterial({ color: 0xff3b30 });
    const beacon = new THREE.Mesh(beaconGeo, beaconMat);
    beacon.position.set(0.5, 0.3, 0.5);
    scene.add(beacon);

    // --- 2. Cursor tracking for interactive parallax ---
    const mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };
    const handleMouseMove = (event) => {
      mouse.targetX = (event.clientX / window.innerWidth) - 0.5;
      mouse.targetY = (event.clientY / window.innerHeight) - 0.5;
    };
    window.addEventListener('mousemove', handleMouseMove);

    // --- 3. GSAP ScrollTrigger Setup ---
    // Timeline to animate camera & DOM text sections
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: scrollyContainerRef.current,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 2.0 // Slower, smoother transition
      }
    });

    // Initial state setup
    gsap.set(slide1Ref.current, { opacity: 1, y: 0, pointerEvents: 'auto' });
    gsap.set(slide2Ref.current, { opacity: 0, y: 30, pointerEvents: 'none' });
    gsap.set(slide3Ref.current, { opacity: 0, y: 30, pointerEvents: 'none' });
    gsap.set(slide4Ref.current, { opacity: 0, y: 30, pointerEvents: 'none' });
    gsap.set(slide5Ref.current, { opacity: 0, y: 30, pointerEvents: 'none' });

    // Timeline steps representing 5 scroll phases with holds/pauses
    tl.to({}, { duration: 1.8 }) // Initial hold on slide 1
      .to(slide1Ref.current, { opacity: 0, y: -30, duration: 1.0, pointerEvents: 'none' })
      .to(camera.position, { x: 3, y: 3.5, z: 6, duration: 1.8 }, '<')
      .to(slide2Ref.current, { opacity: 1, y: 0, duration: 1.0, pointerEvents: 'auto' })
      
      .to({}, { duration: 1.8 }) // Hold on slide 2
      .to(slide2Ref.current, { opacity: 0, y: -30, duration: 1.0, pointerEvents: 'none' })
      .to(camera.position, { x: -3, y: 2, z: 5.5, duration: 1.8 }, '<')
      .to(mesh.position, { y: -0.5, duration: 1.8 }, '<')
      .to(gridMesh.position, { y: -0.48, duration: 1.8 }, '<')
      .to(slide3Ref.current, { opacity: 1, y: 0, duration: 1.0, pointerEvents: 'auto' })
      
      .to({}, { duration: 1.8 }) // Hold on slide 3
      .to(slide3Ref.current, { opacity: 0, y: -30, duration: 1.0, pointerEvents: 'none' })
      .to(camera.position, { x: 0, y: 1.5, z: 4.5, duration: 1.8 }, '<')
      .to(mesh.rotation, { x: -Math.PI / 6, duration: 1.8 }, '<')
      .to(gridMesh.rotation, { x: -Math.PI / 6, duration: 1.8 }, '<')
      .to(slide4Ref.current, { opacity: 1, y: 0, duration: 1.0, pointerEvents: 'auto' })

      .to({}, { duration: 1.8 }) // Hold on slide 4
      .to(slide4Ref.current, { opacity: 0, y: -30, duration: 1.0, pointerEvents: 'none' })
      .to(camera.position, { x: 0, y: 5, z: 10, duration: 1.8 }, '<')
      .to(mesh.rotation, { x: -Math.PI / 3, duration: 1.8 }, '<')
      .to(gridMesh.rotation, { x: -Math.PI / 3, duration: 1.8 }, '<')
      .to(redAlertLight, { intensity: 6.0, duration: 1.8 }, '<')
      .to(pointLight, { intensity: 0.1, duration: 1.8 }, '<')
      .to(slide5Ref.current, { opacity: 1, y: 0, duration: 1.0, pointerEvents: 'auto' })
      
      .to({}, { duration: 1.8 }); // Final hold on slide 5

    // --- 4. Animation Loop ---
    let animationFrameId;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      // Smooth mouse interpolation (lerp)
      mouse.x += (mouse.targetX - mouse.x) * 0.05;
      mouse.y += (mouse.targetY - mouse.y) * 0.05;

      // Mouse tilts scene rotation
      scene.rotation.y = mouse.x * 0.25;
      scene.rotation.x = mouse.y * 0.15;

      // Camera Emergency Vibration Shake (if Alert light is active)
      if (redAlertLight.intensity > 1.0) {
        const shake = redAlertLight.intensity * 0.0035;
        camera.position.x += (Math.random() - 0.5) * shake;
        camera.position.y += (Math.random() - 0.5) * shake;
      }

      // Slow idle spin
      mesh.rotation.z = Math.sin(Date.now() * 0.0003) * 0.05;
      gridMesh.rotation.z = Math.sin(Date.now() * 0.0003) * 0.05;
      particles.rotation.y += 0.0002;

      // Floating shapes animation
      shapes.forEach(s => {
        s.rotation.x += s.userData.rotX;
        s.rotation.y += s.userData.rotY;
        s.position.y = s.userData.initialY + Math.sin(Date.now() * s.userData.floatSpeed) * s.userData.floatDistance;
      });

      // Update Node Laser Connections
      let lineIdx = 0;
      const linePositionsAttr = connectionLines.geometry.attributes.position;
      const linePosArray = linePositionsAttr.array;
      for (let i = 0; i < shapes.length; i++) {
        for (let j = i + 1; j < shapes.length; j++) {
          const dist = shapes[i].position.distanceTo(shapes[j].position);
          if (dist < 4.5) {
            linePosArray[lineIdx++] = shapes[i].position.x;
            linePosArray[lineIdx++] = shapes[i].position.y;
            linePosArray[lineIdx++] = shapes[i].position.z;
            linePosArray[lineIdx++] = shapes[j].position.x;
            linePosArray[lineIdx++] = shapes[j].position.y;
            linePosArray[lineIdx++] = shapes[j].position.z;
          }
        }
      }
      linePositionsAttr.needsUpdate = true;
      connectionLines.geometry.setDrawRange(0, lineIdx);

      // Digital Grid Mesh displacement/morph wave terrain
      const timeVal = Date.now() * 0.0012;
      const scrollRatio = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight || 1);
      const pos = gridGeometry.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        const x = originalGridCoords[i * 3];
        const y = originalGridCoords[i * 3 + 1];
        const wave = Math.sin(x * 0.6 + timeVal) * Math.cos(y * 0.6 + timeVal) * (0.12 + scrollRatio * 0.45);
        pos.setZ(i, wave);
      }
      pos.needsUpdate = true;

      // Pulse beacon sphere
      const pulse = 1 + Math.sin(Date.now() * 0.006) * 0.15;
      beacon.scale.set(pulse, pulse, pulse);

      // Keep camera looking at center
      camera.lookAt(0, 0, 0);

      renderer.render(scene, camera);
    };
    animate();

    // Resize handler
    const handleResize = () => {
      if (!containerRef.current || !renderer) return;
      const w = containerRef.current.clientWidth || window.innerWidth;
      const h = containerRef.current.clientHeight || window.innerHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      ScrollTrigger.getAll().forEach(st => st.kill());
      if (renderer && containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, []);

  // SOS button holding
  useEffect(() => {
    let interval;
    if (sosActive && sosCountdown > 0) {
      interval = setInterval(() => {
        setSosCountdown(prev => prev - 1);
      }, 1000);
    } else if (sosCountdown === 0 && sosActive) {
      const newSignal = {
        id: Date.now(),
        category: 'Quick Beacon SOS',
        location: 'Library Plaza Intersection',
        status: 'Awaiting Rescue',
        time: 'Just now'
      };
      setReports(prev => [newSignal, ...prev]);
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
    setNewReport({ category: 'Medical Rescue', location: '', details: '' });
  };

  return (
    <div className="min-h-screen bg-[#030008] text-slate-100 font-sans selection:bg-purple-500 selection:text-white">
      
      {/* HUD Header */}
      <header className="fixed top-0 left-0 right-0 z-50 p-6 flex justify-between items-center bg-[#030008]/40 backdrop-blur-xl border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-sky-500 to-purple-500 flex items-center justify-center shadow-[0_0_20px_rgba(56,189,248,0.3)]">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-display font-bold tracking-widest text-lg bg-gradient-to-r from-sky-400 to-purple-400 bg-clip-text text-transparent">CAMPUS_SYNC</span>
            <span className="text-[9px] block text-slate-500 tracking-wider">SECURE TELEMETRY ENGINE</span>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-8 text-xs uppercase font-bold tracking-widest text-slate-400">
          <a href="#try-it" className="hover:text-sky-400 transition-colors">Sandbox Desk</a>
        </nav>
      </header>

      {/* Main Scrollytelling Pinned Section */}
      <div ref={scrollyContainerRef} className="relative z-10 h-[800vh]">
        
        {/* Pinned WebGL viewport container */}
        <div className="webgl-bg-container fixed inset-0 w-screen h-screen pointer-events-none z-0">
          <div ref={containerRef} className="w-full h-full relative" />
        </div>

        {/* Pinned text slides overlay */}
        <div className="fixed inset-0 w-screen h-screen flex items-center px-6 md:px-20 pointer-events-none z-20">
          <div className="max-w-xl w-full pointer-events-auto flex flex-col gap-6 relative h-[350px]">
            
            {/* Slide 1: Hero */}
            <div ref={slide1Ref} className="absolute inset-0 flex flex-col items-start gap-6 select-none opacity-0 pointer-events-none">
              <span className="bg-sky-500/10 border border-sky-500/20 text-sky-400 text-xs font-bold tracking-widest uppercase px-4 py-1.5 rounded-full">
                Phase 01 // Secure Network Telemetry
              </span>
              <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight leading-none font-display text-white">
                Real-Time <br />
                <span className="text-gradient">Campus Response</span> <br />
                Synthesizer
              </h1>
              <p className="text-slate-400 text-sm md:text-base leading-relaxed font-semibold">
                Connecting students and security desks through an instant, localized 3D mesh network. Zero lag, high fidelity dispatch.
              </p>
              <div className="flex items-center gap-2 text-slate-500 text-xs font-bold uppercase mt-4">
                <ArrowDown className="w-4 h-4 animate-bounce" /> Scroll to explore network nodes
              </div>
            </div>

            {/* Slide 2: Nodes */}
            <div ref={slide2Ref} className="absolute inset-0 flex flex-col items-start gap-6 select-none opacity-0 pointer-events-none">
              <span className="bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold tracking-widest uppercase px-4 py-1.5 rounded-full">
                Phase 02 // Node Triangulation
              </span>
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-none font-display text-white">
                Localized Mesh Network
              </h1>
              <p className="text-slate-400 text-sm md:text-base leading-relaxed">
                Campus devices function as interactive wireless routers. As you move, the grid dynamically calculates peer-to-peer latency connections to form a robust safety shield.
              </p>
            </div>

            {/* Slide 3: Morphing Data Terrain */}
            <div ref={slide3Ref} className="absolute inset-0 flex flex-col items-start gap-6 select-none opacity-0 pointer-events-none">
              <span className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold tracking-widest uppercase px-4 py-1.5 rounded-full">
                Phase 03 // 3D Topography
              </span>
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-none font-display text-white">
                Dynamic Incident Mapping
              </h1>
              <p className="text-slate-400 text-sm md:text-base leading-relaxed">
                Watch the terrain grid morph in real-time. Alert densities distort the grid mesh, creating immediate visual elevation peaks at high-priority hotspots for dispatcher awareness.
              </p>
            </div>

            {/* Slide 4: Dispatcher Desk */}
            <div ref={slide4Ref} className="absolute inset-0 flex flex-col items-start gap-6 select-none opacity-0 pointer-events-none">
              <span className="bg-pink-500/10 border border-pink-500/20 text-pink-400 text-xs font-bold tracking-widest uppercase px-4 py-1.5 rounded-full">
                Phase 04 // Command Center
              </span>
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-none font-display text-white">
                Interactive Control Desks
              </h1>
              <p className="text-slate-400 text-sm md:text-base leading-relaxed">
                Emergency dispatchers oversee the campus in an interactive 3D space. Panning the camera focuses on specific incident beacons, linking dispatch paths to responders.
              </p>
            </div>

            {/* Slide 5: SOS Alert System */}
            <div ref={slide5Ref} className="absolute inset-0 flex flex-col items-start gap-6 select-none opacity-0 pointer-events-none">
              <span className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-bold tracking-widest uppercase px-4 py-1.5 rounded-full">
                Phase 05 // Active Emergency Beacon
              </span>
              <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-none font-display text-white">
                Fast SOS Integration
              </h1>
              <p className="text-slate-400 text-sm md:text-base leading-relaxed">
                Activating the SOS button emits high-frequency packets. Watch the 3D beacons pulse, shifting lights to active red warning alerts while routing immediate dispatch vectors.
              </p>
            </div>

          </div>
        </div>

      </div>

      {/* Section 4: Live Sandboxed Console Embed */}
      <section id="try-it" className="relative min-h-screen flex flex-col justify-center px-6 md:px-20 py-20 bg-slate-950/90 border-t border-white/5 z-30">
        <div className="max-w-5xl mx-auto w-full flex flex-col gap-10">
          
          <div className="text-center max-w-xl mx-auto flex flex-col items-center gap-3">
            <span className="bg-purple-500/10 border border-purple-500/20 text-purple-300 text-[10px] font-bold tracking-widest uppercase px-4 py-1 rounded-full">
              LIVE SANDBOX EXPERIMENT
            </span>
            <h2 className="text-3xl md:text-4xl font-bold font-display tracking-tight text-white">
              Interact with the System
            </h2>
            <p className="text-slate-400 text-xs md:text-sm">
              Toggle modes to test student report dispatch and real-time response beacons below.
            </p>
          </div>

          {/* Embedded Sandbox Panel */}
          <div className="w-full bg-[#05020c]/60 border border-white/10 rounded-2xl p-6 md:p-8 backdrop-blur-2xl shadow-[0_0_50px_rgba(168,85,247,0.1)] flex flex-col gap-6">
            
            <div className="flex flex-col md:flex-row justify-between items-center gap-4 pb-6 border-b border-white/5">
              <div className="flex items-center gap-3">
                <span className="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></span>
                <span className="text-xs font-bold tracking-wider text-emerald-400 font-mono">SANDBOX_LINK: RUNNING_LOCAL</span>
              </div>
              <div className="flex gap-3 bg-white/5 p-1 rounded-xl border border-white/5">
                <button 
                  onClick={() => setRole('student')}
                  className={`px-4 py-2 rounded-lg text-xs font-bold uppercase transition-all ${role === 'student' ? 'bg-gradient-to-r from-sky-500 to-purple-500 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
                >
                  Student Desk
                </button>
                <button 
                  onClick={() => setRole('admin')}
                  className={`px-4 py-2 rounded-lg text-xs font-bold uppercase transition-all ${role === 'admin' ? 'bg-gradient-to-r from-sky-500 to-purple-500 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
                >
                  Dispatcher Dashboard
                </button>
              </div>
            </div>

            {role === 'student' ? (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                
                {/* Emergency Trigger */}
                <div className="lg:col-span-5 flex flex-col gap-6">
                  <div className="p-6 rounded-xl bg-white/2.5 border border-white/5 flex flex-col items-center justify-center text-center">
                    <span className="text-[10px] text-pink-400 bg-pink-500/10 border border-pink-500/20 px-3 py-1 rounded-full mb-6 font-bold">
                      FAST INTERACTION BEACON
                    </span>
                    <h3 className="text-base font-bold text-slate-200 mb-2">Instant Beacon Link</h3>
                    <p className="text-xs text-slate-400 mb-6 leading-relaxed">
                      Hold down the trigger button below for 3 seconds to emit a simulation telemetry packet.
                    </p>

                    <button
                      onMouseDown={handleSosPress}
                      onMouseUp={handleSosRelease}
                      onMouseLeave={handleSosRelease}
                      onTouchStart={handleSosPress}
                      onTouchEnd={handleSosRelease}
                      className={`w-32 h-32 rounded-full border flex flex-col items-center justify-center transition-all duration-300 ${
                        sosActive 
                          ? 'bg-purple-600/30 border-purple-500 shadow-[0_0_30px_rgba(168,85,247,0.4)] scale-95' 
                          : 'bg-white/5 border-white/10 hover:bg-white/10'
                      }`}
                    >
                      <Flame className={`w-8 h-8 mb-1.5 ${sosActive ? 'text-purple-400 animate-ping' : 'text-slate-300'}`} />
                      <span className="font-bold text-[10px] tracking-widest uppercase">
                        {sosActive ? `TX-ING` : 'SOS LINK'}
                      </span>
                    </button>

                    {sosActive && (
                      <div className="mt-6 w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
                        <div 
                          className="bg-gradient-to-r from-sky-400 to-purple-500 h-full rounded-full transition-all duration-1000"
                          style={{ width: `${((3 - sosCountdown) / 3) * 100}%` }}
                        />
                      </div>
                    )}
                  </div>
                </div>

                {/* Report Submit form */}
                <div className="lg:col-span-7 flex flex-col gap-6">
                  <form onSubmit={handleCreateReport} className="space-y-4">
                    <div>
                      <label className="block text-slate-400 font-bold mb-2 text-[10px] uppercase tracking-wider">INCIDENT CLASS</label>
                      <select 
                        value={newReport.category}
                        onChange={(e) => setNewReport({ ...newReport, category: e.target.value })}
                        className="w-full p-3 rounded-lg bg-white/2.5 border border-white/10 text-sm focus:outline-none focus:border-purple-500 text-slate-200"
                      >
                        <option value="Medical Rescue">Medical Assistance Dispatch</option>
                        <option value="Security Protection">Danger Protection Patrol</option>
                        <option value="Fire Hazard">Fire Event Warning</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-slate-400 font-bold mb-2 text-[10px] uppercase tracking-wider">PHYSICAL LOCATION</label>
                      <input 
                        type="text" 
                        placeholder="e.g. Science Library Room 202"
                        value={newReport.location}
                        onChange={(e) => setNewReport({ ...newReport, location: e.target.value })}
                        className="w-full p-3 rounded-lg bg-white/2.5 border border-white/10 text-sm placeholder-slate-600 focus:outline-none focus:border-purple-500 text-slate-200"
                        required
                      />
                    </div>

                    <button 
                      type="submit" 
                      className="w-full p-3 bg-gradient-to-r from-sky-500 to-purple-500 rounded-lg text-xs font-bold uppercase tracking-wider text-white shadow-lg hover:brightness-110 active:scale-95 transition-all"
                    >
                      <Send className="w-4 h-4 inline mr-1" /> Dispatch Telemetry Report
                    </button>
                  </form>
                </div>

              </div>
            ) : (
              /* ================= DISPATCHER VIEW ================= */
              <div className="flex flex-col gap-4">
                <h3 className="text-sm font-bold uppercase tracking-widest text-slate-300">Active Campus Alarms</h3>
                <div className="space-y-3">
                  {reports.map((rep) => (
                    <div key={rep.id} className="p-4 rounded-xl bg-white/2.5 border border-white/5 flex justify-between items-center gap-4 hover:border-purple-500/30 transition-all">
                      <div className="flex gap-4 items-center">
                        <div className="w-1.5 h-8 rounded-full bg-gradient-to-b from-sky-400 to-purple-500"></div>
                        <div>
                          <div className="flex items-center gap-2 mb-0.5">
                            <span className="font-bold text-slate-200 text-xs">{rep.category}</span>
                            <span className="text-[9px] text-slate-500">{rep.time}</span>
                          </div>
                          <p className="text-slate-400 text-[10px] flex items-center gap-1">
                            <MapPin className="w-3 h-3 text-purple-400" /> {rep.location}
                          </p>
                        </div>
                      </div>
                      <span className="px-3 py-1 rounded-full font-bold text-[9px] bg-purple-500/10 text-purple-300 border border-purple-500/15">
                        {rep.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        </div>
      </section>

    </div>
  );
}

export default App;
