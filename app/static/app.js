/**
 * HeatLens AI — 3D Urban Microclimate Intelligence Platform
 * CSE (AIML) Environmental Studies Decision Support System
 * 
 * Features:
 * - Real Three.js WebGL Interactive Planetary Globe (Hero Card)
 * - Cinematic 3D Urban Environment Scene Engine (Scroll-Driven Choreography)
 * - Ambient Parallax Particle Atmosphere
 * - Audited Intervention Arithmetic (Net Risk Reduction vs Increase)
 * - Defensible Illustrative Tree-Dispersion Uncertainty Quantification
 * - Multi-Layer Leaflet Spatial GIS with Resilient Fallbacks
 * - Explainable AI (Permutation MDA vs Gini MDI)
 */

// Application State
const state = {
  map: null,
  mapLayers: {},
  markers: [],
  selectedLocation: null,
  selectedPlaceMarker: null,
  activeFilterScope: 'core',
  predictionHistory: [],
  importanceData: [],
  activeImportanceMetric: 'perm', // 'perm' or 'gini'
  currentBaselineInputs: {
    ndvi: 0.25,
    impervious_pct: 70.0,
    tree_canopy_pct: 15.0,
    albedo: 0.18,
    air_temp_c: 34.0,
    relative_humidity_pct: 65.0
  },
  currentSimulationDeltas: {
    delta_tree_canopy_pct: 15.0,
    delta_impervious_pct: -10.0,
    delta_albedo: 0.08,
    preset_name: "Comprehensive Greening"
  },
  cinema3D: {
    scene: null,
    camera: null,
    renderer: null,
    planetGroup: null,
    cityGroup: null,
    satelliteGroup: null,
    scrollProgress: 0,
    targetProgress: 0,
    isReducedMotion: false
  }
};
window.state = state;

const $ = (id) => document.getElementById(id);

// Archetype Presets for Rapid Demonstration
const ARCHETYPES = {
  commercial: {
    name: "Dense Commercial (BKC)",
    ndvi: 0.14, impervious_pct: 86.0, tree_canopy_pct: 7.0,
    albedo: 0.16, air_temp_c: 35.5, relative_humidity_pct: 62.0
  },
  forest: {
    name: "Forest Edge (Sanjay Gandhi NP)",
    ndvi: 0.72, impervious_pct: 18.0, tree_canopy_pct: 68.0,
    albedo: 0.24, air_temp_c: 31.8, relative_humidity_pct: 74.0
  },
  industrial: {
    name: "Industrial Settlement (Dharavi)",
    ndvi: 0.08, impervious_pct: 92.0, tree_canopy_pct: 4.0,
    albedo: 0.13, air_temp_c: 36.2, relative_humidity_pct: 59.0
  },
  waterfront: {
    name: "Waterfront Park (Powai Lake)",
    ndvi: 0.54, impervious_pct: 38.0, tree_canopy_pct: 44.0,
    albedo: 0.22, air_temp_c: 32.5, relative_humidity_pct: 68.0
  },
  residential: {
    name: "Urban Residential (Shivaji Park)",
    ndvi: 0.36, impervious_pct: 58.0, tree_canopy_pct: 28.0,
    albedo: 0.20, air_temp_c: 33.6, relative_humidity_pct: 66.0
  }
};

// -----------------------------------------------------------------------------
// Toast Notifications
// -----------------------------------------------------------------------------
function showToast(message, duration = 3500) {
  const container = $('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>🌿</span> <div>${message}</div>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// -----------------------------------------------------------------------------
// Animated Number Counters
// -----------------------------------------------------------------------------
function animateCounters() {
  const counters = document.querySelectorAll('.counter');
  counters.forEach(counter => {
    const target = parseFloat(counter.getAttribute('data-target'));
    const duration = 1200; // ms
    const startTime = performance.now();

    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1.0);
      // Ease out cubic
      const ease = 1 - Math.pow(1 - progress, 3);
      const currentVal = Math.floor(ease * target);
      counter.textContent = currentVal.toLocaleString();

      if (progress < 1.0) {
        requestAnimationFrame(updateCounter);
      } else {
        counter.textContent = target.toLocaleString();
      }
    }
    requestAnimationFrame(updateCounter);
  });
}

// -----------------------------------------------------------------------------
// Theme Management
// -----------------------------------------------------------------------------
function initTheme() {
  const themeToggle = $('theme-toggle');
  const themeIcon = $('theme-icon');
  if (!themeToggle) return;

  const savedTheme = localStorage.getItem('heatlens-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

  themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('heatlens-theme', newTheme);
    themeIcon.textContent = newTheme === 'dark' ? '☀️' : '🌙';
  });
}

// -----------------------------------------------------------------------------
// Ambient Parallax Particle Atmosphere
// -----------------------------------------------------------------------------
function initAmbientCanvas() {
  const canvas = $('ambient-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  let width, height;
  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  const particles = [];
  const particleCount = 45;

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 1.8 + 0.6,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35 - 0.1,
      alpha: Math.random() * 0.45 + 0.1,
      color: Math.random() > 0.4 ? 'rgba(16, 185, 129, ' : 'rgba(6, 182, 212, '
    });
  }

  function renderParticles() {
    ctx.clearRect(0, 0, width, height);

    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color + p.alpha + ')';
      ctx.fill();
    });

    requestAnimationFrame(renderParticles);
  }
  renderParticles();
}

// -----------------------------------------------------------------------------
// UNIFIED MASTER THREE.JS CINEMATIC 3D ENGINE (Scroll Choreography & Interactivity)
// Coordinates all 6 environmental scenes dynamically on scroll:
// Scene 1: The Living Planet (Interactive 3D Earth, Mumbai Focus, Celestial Belt)
// Scene 2: The Urban Landscape (Morphology, River Corridor, Skyline Parallax)
// Scene 3: The Urban Heat Problem (Pulsing Amber Thermal Plumes, Convective Entrapment)
// Scene 4: AI Exploration (Scientific Analytical Lighting, ML Sensor Matrix)
// Scene 5: Cooling the City (Dynamic Greening Transformation, Tree Expansion, Cool Roofs)
// Scene 6: Satellite Orbit & Audit (Landsat & Sentinel Orbiters, Telemetry Radar Cones)
// -----------------------------------------------------------------------------
function initMasterCinematic3D() {
  const canvas = $('cinema-canvas');
  if (!canvas || !window.THREE) return;

  let width = window.innerWidth;
  let height = window.innerHeight;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x020806, 0.045);

  const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 150);
  camera.position.set(0, 0.2, 5.8);
  camera.lookAt(0.4, 0, 0);

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  } catch (err) {
    console.warn("Cinematic WebGL not supported, falling back gracefully.", err);
    if ($('cinema-3d-stage')) $('cinema-3d-stage').style.display = 'none';
    return;
  }

  // Atmospheric Lighting
  const ambLight = new THREE.AmbientLight(0x07281f, 1.4);
  scene.add(ambLight);

  const dirLight = new THREE.DirectionalLight(0x10b981, 2.0);
  dirLight.position.set(6, 14, 10);
  scene.add(dirLight);

  const cyanLight = new THREE.PointLight(0x06b6d4, 1.8, 25);
  cyanLight.position.set(-5, 4, 3);
  scene.add(cyanLight);

  const heatLight = new THREE.PointLight(0xef4444, 0.0, 20);
  heatLight.position.set(0, 3, 0);
  scene.add(heatLight);

  // =========================================================================
  // GROUP 1: THE LIVING PLANET (Scene 1 Focal Subject)
  // =========================================================================
  const planetGroup = new THREE.Group();
  scene.add(planetGroup);
  planetGroup.position.set(2.0, 0.1, 0);

  // 1. Core Sphere
  const coreGeo = new THREE.SphereGeometry(2.32, 48, 48);
  const coreMat = new THREE.MeshBasicMaterial({
    color: 0x031710,
    transparent: true,
    opacity: 0.96
  });
  const coreMesh = new THREE.Mesh(coreGeo, coreMat);
  planetGroup.add(coreMesh);

  // 2. Geodesic Cyan-Green Wireframe Grid
  const wireGeo = new THREE.IcosahedronGeometry(2.36, 4);
  const wireMat = new THREE.MeshBasicMaterial({
    color: 0x10b981,
    wireframe: true,
    transparent: true,
    opacity: 0.35
  });
  const wireMesh = new THREE.Mesh(wireGeo, wireMat);
  planetGroup.add(wireMesh);

  // 3. Glowing Atmospheric Halo (Outer Fresnel Rim)
  const haloGeo = new THREE.SphereGeometry(2.62, 36, 36);
  const haloMat = new THREE.MeshBasicMaterial({
    color: 0x06b6d4,
    transparent: true,
    opacity: 0.16,
    side: THREE.BackSide
  });
  const haloMesh = new THREE.Mesh(haloGeo, haloMat);
  planetGroup.add(haloMesh);

  // 4. Orbiting Microclimate Celestial Particle Swarm
  const pCount = 420;
  const pGeo = new THREE.BufferGeometry();
  const pPos = new Float32Array(pCount * 3);
  const pCol = new Float32Array(pCount * 3);
  const colEmerald = new THREE.Color(0x10b981);
  const colCyan = new THREE.Color(0x06b6d4);
  const colAmber = new THREE.Color(0xf59e0b);

  for (let i = 0; i < pCount; i++) {
    const phi = Math.acos(-1 + (2 * i) / pCount);
    const theta = Math.sqrt(pCount * Math.PI) * phi;
    const r = 2.48 + Math.random() * 0.55;

    pPos[i * 3] = r * Math.cos(theta) * Math.sin(phi);
    pPos[i * 3 + 1] = r * Math.sin(theta) * Math.sin(phi);
    pPos[i * 3 + 2] = r * Math.cos(phi);

    const randVal = Math.random();
    const c = randVal > 0.65 ? colAmber : randVal > 0.3 ? colEmerald : colCyan;
    pCol[i * 3] = c.r;
    pCol[i * 3 + 1] = c.g;
    pCol[i * 3 + 2] = c.b;
  }
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  pGeo.setAttribute('color', new THREE.BufferAttribute(pCol, 3));

  const pMat = new THREE.PointsMaterial({
    size: 0.05,
    vertexColors: true,
    transparent: true,
    opacity: 0.88
  });
  const pPoints = new THREE.Points(pGeo, pMat);
  planetGroup.add(pPoints);

  // 5. Global Hotspot Pins
  function latLonToVec3(lat, lon, radius) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    return new THREE.Vector3(
      -(radius * Math.sin(phi) * Math.cos(theta)),
      radius * Math.cos(phi),
      radius * Math.sin(phi) * Math.sin(theta)
    );
  }

  const hotspots = [
    { name: "Mumbai Study Extent", lat: 19.076, lon: 72.877, color: 0xef4444, scale: 0.09 },
    { name: "Tokyo Urban Core", lat: 35.676, lon: 139.650, color: 0xf59e0b, scale: 0.06 },
    { name: "Cairo Heat Sink", lat: 30.044, lon: 31.235, color: 0xf59e0b, scale: 0.06 },
    { name: "London Island", lat: 51.507, lon: -0.127, color: 0x10b981, scale: 0.05 },
    { name: "New York Canyon", lat: 40.712, lon: -74.006, color: 0xf59e0b, scale: 0.06 }
  ];

  const radarRings = [];
  hotspots.forEach(h => {
    const pos = latLonToVec3(h.lat, h.lon, 2.38);
    const pinGeo = new THREE.SphereGeometry(h.scale, 16, 16);
    const pinMat = new THREE.MeshBasicMaterial({ color: h.color });
    const pinMesh = new THREE.Mesh(pinGeo, pinMat);
    pinMesh.position.copy(pos);
    planetGroup.add(pinMesh);

    if (h.name.includes("Mumbai")) {
      // Double animated radar pulse rings
      for (let r = 0; r < 2; r++) {
        const ringGeo = new THREE.RingGeometry(0.12 + r * 0.06, 0.16 + r * 0.06, 24);
        const ringMat = new THREE.MeshBasicMaterial({
          color: 0xef4444,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.85
        });
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.position.copy(pos);
        ringMesh.lookAt(planetGroup.position);
        planetGroup.add(ringMesh);
        radarRings.push({ mesh: ringMesh, offset: r * 0.5 });
      }
    }
  });

  // Tilt to orient Mumbai facing camera in Scene 1
  planetGroup.rotation.x = 0.32;
  planetGroup.rotation.y = -1.05;

  // =========================================================================
  // GROUP 2: THE URBAN LANDSCAPE (Scenes 2, 3, 4, 5)
  // =========================================================================
  const cityGroup = new THREE.Group();
  scene.add(cityGroup);
  cityGroup.position.set(0, -32, 0); // Hidden initially in Scene 1
  cityGroup.visible = false;

  // 1. Terrain Ground
  const groundGeo = new THREE.PlaneGeometry(22, 22, 24, 24);
  const groundMat = new THREE.MeshLambertMaterial({ color: 0x02120b });
  const groundMesh = new THREE.Mesh(groundGeo, groundMat);
  groundMesh.rotation.x = -Math.PI / 2;
  groundMesh.position.y = -0.05;
  cityGroup.add(groundMesh);

  // River Channel
  const riverGeo = new THREE.PlaneGeometry(3.2, 22);
  const riverMat = new THREE.MeshBasicMaterial({
    color: 0x085240,
    transparent: true,
    opacity: 0.8
  });
  const riverMesh = new THREE.Mesh(riverGeo, riverMat);
  riverMesh.rotation.x = -Math.PI / 2;
  riverMesh.rotation.z = 0.32;
  riverMesh.position.set(1.8, -0.04, 0);
  cityGroup.add(riverMesh);

  // 2. Procedural Buildings (36 blocks)
  const buildingMeshes = [];
  const thermalPlumes = [];
  const coolRoofMaterials = [];
  const treeMeshes = [];

  const buildingMat = new THREE.MeshLambertMaterial({ color: 0x051d16 });
  const highRiseMat = new THREE.MeshLambertMaterial({ color: 0x062b21 });
  const wireEdgeMat = new THREE.LineBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.3 });

  for (let ix = -3; ix <= 3; ix++) {
    for (let iz = -3; iz <= 3; iz++) {
      if (Math.abs(ix - (iz * 0.32) - 1.5) < 1.1) continue; // river gap

      const isHighRise = (ix === -1 || ix === 0) && (iz === -1 || iz === 0);
      const isCommercial = Math.abs(ix) <= 1 && Math.abs(iz) <= 1;
      const bWidth = 0.6 + Math.random() * 0.35;
      const bDepth = 0.6 + Math.random() * 0.35;
      const bHeight = isHighRise ? (2.2 + Math.random() * 1.6) : (0.45 + Math.random() * 1.1);

      const bGeo = new THREE.BoxGeometry(bWidth, bHeight, bDepth);
      const bMesh = new THREE.Mesh(bGeo, isHighRise ? highRiseMat : buildingMat);
      const posX = ix * 1.2 + (Math.random() - 0.5) * 0.15;
      const posZ = iz * 1.2 + (Math.random() - 0.5) * 0.15;
      bMesh.position.set(posX, bHeight / 2, posZ);
      cityGroup.add(bMesh);
      buildingMeshes.push(bMesh);

      // Edges
      const edges = new THREE.EdgesGeometry(bGeo);
      const line = new THREE.LineSegments(edges, wireEdgeMat);
      bMesh.add(line);

      // Cool Roof Surface Cap
      if (isCommercial) {
        const roofGeo = new THREE.PlaneGeometry(bWidth * 0.94, bDepth * 0.94);
        const roofMat = new THREE.MeshBasicMaterial({
          color: 0x06b6d4,
          transparent: true,
          opacity: 0.15
        });
        const roofMesh = new THREE.Mesh(roofGeo, roofMat);
        roofMesh.rotation.x = -Math.PI / 2;
        roofMesh.position.set(0, (bHeight / 2) + 0.015, 0);
        bMesh.add(roofMesh);
        coolRoofMaterials.push(roofMat);
      }

      // Thermal Heat Plumes
      if (isHighRise || (Math.random() > 0.65 && isCommercial)) {
        const plumeGeo = new THREE.CylinderGeometry(0.25, 0.45, 1.8, 16, 1, true);
        const plumeMat = new THREE.MeshBasicMaterial({
          color: 0xf59e0b,
          transparent: true,
          opacity: 0.05,
          side: THREE.DoubleSide
        });
        const plumeMesh = new THREE.Mesh(plumeGeo, plumeMat);
        plumeMesh.position.set(posX, bHeight + 0.9, posZ);
        cityGroup.add(plumeMesh);
        thermalPlumes.push({ mesh: plumeMesh, mat: plumeMat, baseHeight: bHeight + 0.9 });
      }
    }
  }

  // 3. Procedural Low-Poly Trees (55 trees)
  const trunkMat = new THREE.MeshLambertMaterial({ color: 0x1f2923 });
  const foliageMat = new THREE.MeshLambertMaterial({ color: 0x10b981 });

  for (let t = 0; t < 55; t++) {
    const angle = Math.random() * Math.PI * 2;
    const dist = 1.3 + Math.random() * 5.2;
    const tx = Math.cos(angle) * dist;
    const tz = Math.sin(angle) * dist;

    const trunkGeo = new THREE.CylinderGeometry(0.035, 0.045, 0.28, 6);
    const trunk = new THREE.Mesh(trunkGeo, trunkMat);
    trunk.position.set(tx, 0.14, tz);

    const foliageGeo = new THREE.IcosahedronGeometry(0.20 + Math.random() * 0.12, 1);
    const foliage = new THREE.Mesh(foliageGeo, foliageMat);
    foliage.position.y = 0.26;
    trunk.add(foliage);

    cityGroup.add(trunk);
    treeMeshes.push(trunk);
  }

  // Atmospheric City Dust Particles
  const cityParticleCount = 140;
  const cpGeo = new THREE.BufferGeometry();
  const cpPos = new Float32Array(cityParticleCount * 3);
  for (let i = 0; i < cityParticleCount; i++) {
    cpPos[i * 3] = (Math.random() - 0.5) * 16;
    cpPos[i * 3 + 1] = Math.random() * 5.0;
    cpPos[i * 3 + 2] = (Math.random() - 0.5) * 16;
  }
  cpGeo.setAttribute('position', new THREE.BufferAttribute(cpPos, 3));
  const cpMat = new THREE.PointsMaterial({
    color: 0x34d399,
    size: 0.05,
    transparent: true,
    opacity: 0.6
  });
  const cityParticles = new THREE.Points(cpGeo, cpMat);
  cityGroup.add(cityParticles);

  // =========================================================================
  // GROUP 3: SATELLITE ORBITS & AUDIT (Scene 6 Focal Subject)
  // =========================================================================
  const satelliteGroup = new THREE.Group();
  scene.add(satelliteGroup);
  satelliteGroup.position.set(0, 36, 0); // Hidden initially
  satelliteGroup.visible = false;

  // 1. Curved Earth Horizon Arc
  const horizonGeo = new THREE.SphereGeometry(18, 48, 48);
  const horizonMat = new THREE.MeshLambertMaterial({
    color: 0x031812,
    transparent: true,
    opacity: 0.95
  });
  const horizonMesh = new THREE.Mesh(horizonGeo, horizonMat);
  horizonMesh.position.set(0, -19.5, 0);
  satelliteGroup.add(horizonMesh);

  // Atmospheric Horizon Glow
  const horizAtmGeo = new THREE.RingGeometry(17.8, 18.6, 64);
  const horizAtmMat = new THREE.MeshBasicMaterial({
    color: 0x06b6d4,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.35
  });
  const horizAtmMesh = new THREE.Mesh(horizAtmGeo, horizAtmMat);
  horizAtmMesh.rotation.x = -Math.PI / 2;
  horizAtmMesh.position.set(0, -1.5, 0);
  satelliteGroup.add(horizAtmMesh);

  // 2. 3 Satellite Orbital Trajectories
  const satellites = [];
  const orbitConfigs = [
    { name: "Landsat-9", radius: 5.6, inclination: 0.65, speed: 0.012, color: 0x06b6d4 },
    { name: "Sentinel-2", radius: 6.4, inclination: -0.45, speed: 0.016, color: 0x10b981 },
    { name: "ECOSTRESS", radius: 4.8, inclination: 0.25, speed: 0.020, color: 0xf59e0b }
  ];

  orbitConfigs.forEach(cfg => {
    // Orbital Track Ring
    const trackGeo = new THREE.RingGeometry(cfg.radius - 0.02, cfg.radius + 0.02, 64);
    const trackMat = new THREE.MeshBasicMaterial({
      color: cfg.color,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.22
    });
    const trackMesh = new THREE.Mesh(trackGeo, trackMat);
    trackMesh.rotation.x = Math.PI / 2 + cfg.inclination;
    satelliteGroup.add(trackMesh);

    // Satellite Model
    const satModel = new THREE.Group();
    // Central chassis
    const bodyGeo = new THREE.BoxGeometry(0.24, 0.24, 0.36);
    const bodyMat = new THREE.MeshLambertMaterial({ color: 0xd1d5db });
    const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
    satModel.add(bodyMesh);

    // Solar Wings
    const wingGeo = new THREE.BoxGeometry(0.85, 0.02, 0.22);
    const wingMat = new THREE.MeshBasicMaterial({ color: 0x1e40af });
    const wingMesh = new THREE.Mesh(wingGeo, wingMat);
    satModel.add(wingMesh);

    // Downward Scanning Radar/Telemetry Cone
    const coneGeo = new THREE.ConeGeometry(0.8, 2.4, 16, 1, true);
    const coneMat = new THREE.MeshBasicMaterial({
      color: cfg.color,
      transparent: true,
      opacity: 0.18,
      side: THREE.DoubleSide
    });
    const coneMesh = new THREE.Mesh(coneGeo, coneMat);
    coneMesh.position.y = -1.2;
    coneMesh.rotation.x = Math.PI;
    satModel.add(coneMesh);

    satelliteGroup.add(satModel);
    satellites.push({
      group: satModel,
      radius: cfg.radius,
      inclination: cfg.inclination,
      speed: cfg.speed,
      angle: Math.random() * Math.PI * 2,
      coneMat
    });
  });

  // =========================================================================
  // MOUSE / TOUCH DRAG ON HERO GLOBE (Scene 1 Interactivity)
  // =========================================================================
  let isDragging = false;
  let prevPos = { x: 0, y: 0 };
  const dragTarget = $('hero-globe-container') || $('hero');

  if (dragTarget) {
    dragTarget.addEventListener('mousedown', (e) => {
      isDragging = true;
      prevPos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', () => { isDragging = false; });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevPos.x;
      const deltaY = e.clientY - prevPos.y;
      planetGroup.rotation.y += deltaX * 0.006;
      planetGroup.rotation.x += deltaY * 0.006;
      prevPos = { x: e.clientX, y: e.clientY };
    });

    dragTarget.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        isDragging = true;
        prevPos = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      }
    }, { passive: true });

    window.addEventListener('touchend', () => { isDragging = false; });

    window.addEventListener('touchmove', (e) => {
      if (!isDragging || e.touches.length !== 1) return;
      const deltaX = e.touches[0].clientX - prevPos.x;
      const deltaY = e.touches[0].clientY - prevPos.y;
      planetGroup.rotation.y += deltaX * 0.006;
      planetGroup.rotation.x += deltaY * 0.006;
      prevPos = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }, { passive: true });
  }

  // =========================================================================
  // CONTINUOUS SCROLL-PROGRESS ENGINE (0.0 to 5.0 Continuous Lerp)
  // =========================================================================
  const sceneElements = [
    $('hero'),
    $('scene-landscape'),
    $('map-section'),
    $('inference-section'),
    $('simulator-section'),
    $('satellite-section')
  ];

  let targetProgress = 0.0;
  let currentProgress = 0.0;

  function calculateScrollProgress() {
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // Check positions of all 6 scenes
    const sceneOffsets = sceneElements.map(el => {
      if (!el) return 0;
      const rect = el.getBoundingClientRect();
      return rect.top + scrollY;
    });

    // Find which pair of scenes we are between
    let prog = 0.0;
    if (scrollY <= sceneOffsets[0]) {
      prog = 0.0;
    } else if (scrollY >= sceneOffsets[sceneOffsets.length - 1]) {
      prog = 5.0;
    } else {
      for (let i = 0; i < sceneOffsets.length - 1; i++) {
        const topCurrent = sceneOffsets[i];
        const topNext = sceneOffsets[i + 1];
        if (scrollY >= topCurrent && scrollY < topNext) {
          const span = Math.max(1, topNext - topCurrent);
          const frac = (scrollY - topCurrent) / span;
          prog = i + frac;
          break;
        }
      }
    }
    targetProgress = Math.min(5.0, Math.max(0.0, prog));
  }

  window.addEventListener('scroll', calculateScrollProgress, { passive: true });
  calculateScrollProgress();

  // Export control handle for intervention simulator real-time feedback
  window.update3DInterventionVisuals = function(deltaTree, deltaAlbedo) {
    const treeScaleFactor = 1.0 + (deltaTree / 40.0);
    treeMeshes.forEach(t => t.scale.set(treeScaleFactor, treeScaleFactor, treeScaleFactor));

    const roofBrightness = Math.min(1.0, 0.2 + (deltaAlbedo * 3.5));
    coolRoofMaterials.forEach(rm => {
      rm.opacity = roofBrightness;
      rm.color.setHex(deltaAlbedo > 0.05 ? 0xe0f2fe : 0x06b6d4);
    });
  };

  state.cinema3D = {
    scene,
    camera,
    renderer,
    planetGroup,
    cityGroup,
    satelliteGroup,
    scrollProgress: 0,
    targetProgress: 0,
    isReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches
  };
  window.masterCinematic3D = state.cinema3D;
  window.heatlensGlobe = planetGroup;

  // =========================================================================
  // ANIMATION LOOP
  // =========================================================================
  let time = 0;
  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function renderFrame() {
    requestAnimationFrame(renderFrame);
    time += 0.02;

    // Smooth lerp for continuous bidirectional scroll
    currentProgress += (targetProgress - currentProgress) * 0.085;
    const p = currentProgress;
    state.cinema3D.scrollProgress = p;
    state.cinema3D.targetProgress = targetProgress;

    // Pulse radar rings on Earth
    radarRings.forEach(r => {
      const ringScale = 1.0 + 0.25 * Math.sin(time * 3.0 + r.offset);
      r.mesh.scale.set(ringScale, ringScale, 1.0);
    });

    // Rotate Earth when not dragging
    if (!isDragging) {
      planetGroup.rotation.y += 0.0018;
    }
    pPoints.rotation.y -= 0.0006;

    // Orbit Satellites in Scene 6
    satellites.forEach(sat => {
      sat.angle += sat.speed;
      const x = Math.cos(sat.angle) * sat.radius;
      const z = Math.sin(sat.angle) * sat.radius;
      sat.group.position.set(x, Math.sin(sat.angle) * sat.inclination * 2.0, z);
      sat.group.lookAt(0, -19.5, 0);

      // Pulse radar telemetry cone
      const conePulse = 0.15 + 0.1 * Math.sin(time * 4.0);
      sat.coneMat.opacity = conePulse;
    });

    // -----------------------------------------------------------------------
    // SCENE-SPECIFIC 3D CHOREOGRAPHY
    // -----------------------------------------------------------------------
    if (!isReducedMotion) {
      if (p <= 1.0) {
        // SCENE 1 -> 2: Earth -> Urban Landscape
        const u = p;
        planetGroup.visible = (u < 0.92);
        cityGroup.visible = (u > 0.08);
        satelliteGroup.visible = false;

        // Earth transitions
        planetGroup.position.set(
          THREE.MathUtils.lerp(2.0, 0.0, u),
          THREE.MathUtils.lerp(0.1, 4.8, u),
          THREE.MathUtils.lerp(0.0, 2.0, u)
        );
        planetGroup.scale.setScalar(THREE.MathUtils.lerp(1.0, 1.7, u));

        // City rises from the mist
        cityGroup.position.y = THREE.MathUtils.lerp(-32, 0.0, Math.min(1.0, u * 1.3));
        cityGroup.rotation.y = 0.35 + u * 0.15;

        // Camera smoothly descends
        camera.position.set(
          THREE.MathUtils.lerp(0.0, 2.4, u),
          THREE.MathUtils.lerp(0.2, 2.6, u),
          THREE.MathUtils.lerp(5.8, 5.2, u)
        );
        camera.lookAt(
          THREE.MathUtils.lerp(0.4, 0.0, u),
          THREE.MathUtils.lerp(0.0, 0.3, u),
          0
        );

        // Lighting
        ambLight.color.setHex(0x07281f);
        dirLight.color.setHex(0x10b981);
        heatLight.intensity = 0.0;
        thermalPlumes.forEach(pl => { pl.mat.opacity = 0.05; });
      }
      else if (p <= 2.0) {
        // SCENE 2 -> 3: Urban Landscape -> Urban Heat Problem
        const u = p - 1.0;
        planetGroup.visible = false;
        cityGroup.visible = true;
        cityGroup.position.y = 0.0;
        satelliteGroup.visible = false;

        camera.position.set(
          THREE.MathUtils.lerp(2.4, 3.2, u),
          THREE.MathUtils.lerp(2.6, 3.8, u),
          THREE.MathUtils.lerp(5.2, 4.4, u)
        );
        camera.lookAt(0, THREE.MathUtils.lerp(0.3, 0.5, u), 0);
        cityGroup.rotation.y = THREE.MathUtils.lerp(0.5, 0.85, u);

        // Transition lighting to warm amber
        const ambR = THREE.MathUtils.lerp(0.04, 0.22, u);
        const ambG = THREE.MathUtils.lerp(0.18, 0.10, u);
        ambLight.color.setRGB(ambR, ambG, 0.04);
        dirLight.color.setHex(u > 0.4 ? 0xf59e0b : 0x10b981);

        // Ignites red heat glow
        heatLight.intensity = u * 2.4;

        // Plumes pulse with heat
        const plumePulse = Math.sin(time * 3.5) * 0.2 + 0.45;
        thermalPlumes.forEach(pl => {
          pl.mat.opacity = THREE.MathUtils.lerp(0.08, plumePulse, u);
          pl.mat.color.setHex(0xf59e0b);
          pl.mesh.scale.set(
            1.0 + plumePulse * 0.3 * u,
            1.0 + plumePulse * 0.6 * u,
            1.0 + plumePulse * 0.3 * u
          );
        });
      }
      else if (p <= 3.0) {
        // SCENE 3 -> 4: Urban Heat Problem -> AI Exploration
        const u = p - 2.0;
        planetGroup.visible = false;
        cityGroup.visible = true;
        cityGroup.position.y = 0.0;
        satelliteGroup.visible = false;

        camera.position.set(
          THREE.MathUtils.lerp(3.2, 1.4, u),
          THREE.MathUtils.lerp(3.8, 4.2, u),
          THREE.MathUtils.lerp(4.4, 4.6, u)
        );
        camera.lookAt(0, THREE.MathUtils.lerp(0.5, 0.4, u), 0);
        cityGroup.rotation.y = THREE.MathUtils.lerp(0.85, 1.25, u);

        // Scientific high-contrast laboratory matrix lighting
        ambLight.color.setHex(0x05201b);
        dirLight.color.setHex(0x06b6d4);
        heatLight.intensity = (1.0 - u) * 2.4;

        // Plumes diminish
        thermalPlumes.forEach(pl => {
          pl.mat.opacity = THREE.MathUtils.lerp(0.45, 0.12, u);
        });
      }
      else if (p <= 4.0) {
        // SCENE 4 -> 5: AI Exploration -> Cooling the City
        const u = p - 3.0;
        planetGroup.visible = false;
        cityGroup.visible = true;
        cityGroup.position.y = 0.0;
        satelliteGroup.visible = false;

        camera.position.set(
          THREE.MathUtils.lerp(1.4, 0.5, u),
          THREE.MathUtils.lerp(4.2, 2.0, u),
          THREE.MathUtils.lerp(4.6, 3.6, u)
        );
        camera.lookAt(0, THREE.MathUtils.lerp(0.4, 0.2, u), 0);
        cityGroup.rotation.y = THREE.MathUtils.lerp(1.25, 1.6, u);

        // Greening Transformation in 3D
        ambLight.color.setHex(0x07281f);
        dirLight.color.setHex(0x34d399);

        // Trees expand & bloom
        const tScale = THREE.MathUtils.lerp(1.0, 1.55, u);
        treeMeshes.forEach(t => t.scale.set(tScale, tScale, tScale));

        // Cool roofs shimmer with reflective coating
        coolRoofMaterials.forEach(rm => {
          rm.opacity = THREE.MathUtils.lerp(0.15, 0.82, u);
          rm.color.setHex(0xe0f2fe);
        });

        // Heat plumes dissipate completely
        thermalPlumes.forEach(pl => {
          pl.mat.opacity = THREE.MathUtils.lerp(0.12, 0.03, u);
          pl.mat.color.setHex(0x10b981);
        });
      }
      else {
        // SCENE 5 -> 6: Cooling the City -> Satellite Data & Audit
        const u = p - 4.0;
        planetGroup.visible = false;
        cityGroup.visible = (u < 0.95);
        satelliteGroup.visible = (u > 0.05);

        // City sinks into cloud layer
        cityGroup.position.y = -32 * u;

        // Satellite orbital stage enters
        satelliteGroup.position.y = THREE.MathUtils.lerp(32, 0.0, u);

        camera.position.set(
          THREE.MathUtils.lerp(0.5, 0.0, u),
          THREE.MathUtils.lerp(2.0, 5.8, u),
          THREE.MathUtils.lerp(3.6, 7.2, u)
        );
        camera.lookAt(0, THREE.MathUtils.lerp(0.2, 0.0, u), 0);

        ambLight.color.setHex(0x03120c);
        dirLight.color.setHex(0x06b6d4);
      }
    }

    // Gentle city particle float
    cityParticles.rotation.y += 0.0008;

    renderer.render(scene, camera);
  }
  renderFrame();

  // Resize Handling
  window.addEventListener('resize', () => {
    width = window.innerWidth;
    height = window.innerHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  });
}

// -----------------------------------------------------------------------------
// SCENE OBSERVER & SCROLL REVEALS
// -----------------------------------------------------------------------------
function initScrollReveal() {
  const scenes = document.querySelectorAll('.cinematic-scene');
  const revealElements = document.querySelectorAll('.scroll-reveal');
  const navLinks = document.querySelectorAll('.side-nav .nav-link');

  const sceneObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        if (id === 'map-section' && state.map) {
          setTimeout(() => {
            state.map.invalidateSize();
          }, 150);
        }
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, { threshold: 0.25 });

  scenes.forEach(s => sceneObserver.observe(s));

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, { threshold: 0.12 });

  revealElements.forEach(el => revealObserver.observe(el));
}

// -----------------------------------------------------------------------------
// Spatial Map Explorer (Leaflet GIS)
// -----------------------------------------------------------------------------
function initMap() {
  if (typeof L === 'undefined') {
    console.warn("Leaflet library unavailable.");
    return;
  }

  // Initialize map centered on Mumbai study extent
  state.map = L.map('map', {
    center: [19.0760, 72.8777],
    zoom: 11,
    zoomControl: true,
    scrollWheelZoom: false
  });

  // Working tile layer configurations with resilient, keyless public providers
  state.mapLayers = {
    'osm-dark': L.layerGroup([
      L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 16,
        attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
      }),
      L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 16,
        attribution: ''
      })
    ]),
    'satellite': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 18,
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    }),
    'osm-standard': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
    }),
    'topo': L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17,
      attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, SRTM | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>'
    })
  };

  // Attach error and success hooks to each layer (supporting single layers and layerGroups)
  Object.values(state.mapLayers).forEach(layer => {
    const bindEvents = (tileLayer) => {
      tileLayer.on('tileerror', () => {
        const notice = $('tile-error-notice');
        if (notice) notice.style.display = 'flex';
      });
      tileLayer.on('load', () => {
        const notice = $('tile-error-notice');
        if (notice) notice.style.display = 'none';
      });
    };

    if (layer.eachLayer) {
      layer.eachLayer(bindEvents);
    } else {
      bindEvents(layer);
    }
  });

  const initialLayerKey = 'osm-dark';
  state.mapLayers[initialLayerKey].addTo(state.map);

  if (initialLayerKey === 'osm-dark') {
    $('map').classList.add('dark-tiles');
  } else {
    $('map').classList.remove('dark-tiles');
  }

  // Ensure dimensions calculate correctly after DOM settles
  setTimeout(() => {
    if (state.map) state.map.invalidateSize();
  }, 250);

  // Layer change handler
  $('map-layer-select').addEventListener('change', (e) => {
    setMapLayer(e.target.value);
  });

  // Map resize handler
  window.addEventListener('resize', () => {
    if (state.map) state.map.invalidateSize();
  });
}

function setMapLayer(layerKey) {
  if (!state.map || !state.mapLayers[layerKey]) return;
  Object.values(state.mapLayers).forEach(layer => {
    if (state.map.hasLayer(layer)) {
      state.map.removeLayer(layer);
    }
  });

  const mapEl = $('map');
  if (layerKey === 'osm-dark') {
    mapEl.classList.add('dark-tiles');
  } else {
    mapEl.classList.remove('dark-tiles');
  }

  state.map.addLayer(state.mapLayers[layerKey]);
  setTimeout(() => {
    if (state.map) state.map.invalidateSize();
  }, 50);
}

function markerColor(score) {
  if (score < 35) return '#10b981'; // Emerald
  if (score < 65) return '#f59e0b'; // Amber
  return '#ef4444'; // Crimson
}

async function loadMapLocations(queryParam = 'scope=core') {
  try {
    const res = await fetch(`/api/locations?${queryParam}`);
    if (!res.ok) throw new Error('Failed to load study locations');
    const locations = await res.json();

    const badge = $('location-count-badge');
    if (badge) {
      const scopeLabel = queryParam.includes('all') ? 'All Pan-India (23)' :
                         queryParam.includes('city=Mumbai') ? 'MMR Metropolitan (15)' :
                         queryParam.includes('metros') ? 'Major Metros (8)' :
                         `${locations.length} Sites`;
      badge.textContent = scopeLabel;
    }

    // Clear existing circular markers (preserve user selection marker if any)
    state.markers.forEach(m => m.remove());
    state.markers = [];

    locations.forEach(loc => {
      if (!state.map) return;
      const color = markerColor(loc.score);
      const radius = 8 + (loc.impervious_pct / 22);

      const marker = L.circleMarker([loc.lat, loc.lon], {
        radius: radius,
        fillColor: color,
        color: '#ffffff',
        weight: 1.8,
        opacity: 0.9,
        fillOpacity: 0.85
      }).addTo(state.map);

      const tooltipHtml = `
        <div style="font-family:'Plus Jakarta Sans',sans-serif; min-width:180px;">
          <strong style="color:#fff; font-size:13px;">${loc.name}</strong><br>
          <span style="font-size:11px; color:#8ca3a6;">${loc.city || 'Mumbai'} · ${loc.zone_type || 'Study Zone'}</span>
          <div style="margin-top:6px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11px; font-weight:700; color:${color};">${loc.risk_tier}</span>
            <strong style="font-size:14px; color:#fff;">${loc.score}/100</strong>
          </div>
          <small style="font-size:9px; color:#5f7578; display:block; margin-top:4px;">Click to inspect place profile</small>
        </div>
      `;

      marker.bindTooltip(tooltipHtml, { direction: 'top', offset: [0, -6], className: 'custom-map-tooltip' });
      marker.on('click', () => {
        selectPlace(loc);
      });

      state.markers.push(marker);
    });

    if (locations.length > 0 && !state.selectedLocation) {
      selectPlace(locations[0]);
    }
  } catch (err) {
    console.warn('Map locations note:', err.message);
  }
}

function selectPlace(loc) {
  state.selectedLocation = loc;
  displaySelectedPlaceHUD(loc);
  highlightSelectedMarker(loc.lat, loc.lon, loc.name);
}

function highlightSelectedMarker(lat, lon, title) {
  if (!state.map) return;
  if (state.selectedPlaceMarker) {
    state.selectedPlaceMarker.remove();
    state.selectedPlaceMarker = null;
  }

  state.selectedPlaceMarker = L.circleMarker([lat, lon], {
    radius: 16,
    color: '#06b6d4',
    fillColor: '#06b6d4',
    fillOpacity: 0.25,
    weight: 3,
    dashArray: '4, 4'
  }).addTo(state.map);

  state.selectedPlaceMarker.bindPopup(`<strong>${title}</strong><br><small>Active Selected Place</small>`).openPopup();
}

function displaySelectedPlaceHUD(loc) {
  const hud = $('selected-place-hud');
  if (!hud) return;

  $('hud-place-name').textContent = loc.name;
  const cityState = loc.city ? `${loc.city}, ${loc.state || 'India'}` : 'Mumbai Metropolitan Region';
  $('hud-place-subtitle').textContent = `${cityState} · ${loc.zone_type || 'Micro Study Zone'}`;

  const provBadge = $('hud-provenance-badge');
  if (provBadge) {
    provBadge.textContent = loc.data_source || 'Synthetic Micro Study Point';
    if (loc.is_synthetic) {
      provBadge.className = 'hud-badge amber';
    } else {
      provBadge.className = 'hud-badge green';
    }
  }

  const riskBadge = $('hud-risk-badge');
  if (riskBadge) {
    riskBadge.textContent = `Risk: ${loc.score ? loc.score.toFixed(1) : '50.0'} / 100 (${loc.risk_tier || 'Benchmark'})`;
  }

  $('hud-ndvi-val').textContent = loc.ndvi !== undefined ? loc.ndvi.toFixed(2) : '0.25';
  $('hud-impervious-val').textContent = loc.impervious_pct !== undefined ? `${Math.round(loc.impervious_pct)}%` : '70%';
  $('hud-canopy-val').textContent = loc.tree_canopy_pct !== undefined ? `${Math.round(loc.tree_canopy_pct)}%` : '15%';
  $('hud-albedo-val').textContent = loc.albedo !== undefined ? loc.albedo.toFixed(2) : '0.18';
  $('hud-temp-val').textContent = loc.air_temp_c !== undefined ? `${loc.air_temp_c.toFixed(1)} °C` : '34.0 °C';
  $('hud-humidity-val').textContent = loc.relative_humidity_pct !== undefined ? `${Math.round(loc.relative_humidity_pct)}%` : '65%';

  const appBox = $('hud-applicability-text');
  if (appBox) {
    if (loc.model_applicability) {
      appBox.textContent = loc.model_applicability;
    } else if (loc.city && loc.city !== 'Mumbai') {
      appBox.textContent = `Regional Benchmark Context for ${loc.city}. Note: HeatLens Random Forest is trained specifically for Mumbai coastal microclimates; model inference here is illustrative.`;
    } else {
      appBox.textContent = 'Direct local model fit for Mumbai study domain. Evaluated with 220-tree Random Forest regressor.';
    }
  }

  hud.style.display = 'block';
}

function loadLocationIntoPredictor(loc) {
  state.selectedLocation = loc;
  setPredictorInputs({
    ndvi: loc.ndvi,
    impervious_pct: loc.impervious_pct,
    tree_canopy_pct: loc.tree_canopy_pct,
    albedo: loc.albedo,
    air_temp_c: loc.air_temp_c,
    relative_humidity_pct: loc.relative_humidity_pct
  });
  executePrediction();
  showToast(`Loaded parameters for ${loc.name} into Risk Estimator.`);
  $('inference-section').scrollIntoView({ behavior: 'smooth' });
}

// -----------------------------------------------------------------------------
// City & Place Explorer Search & Filters
// -----------------------------------------------------------------------------
function initPlaceExplorer() {
  const searchInput = $('place-search-input');
  const clearBtn = $('btn-clear-search');
  const dropdown = $('search-suggestions-dropdown');

  let searchDebounce = null;

  if (searchInput && dropdown) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.trim();
      if (clearBtn) clearBtn.style.display = q ? 'block' : 'none';

      clearTimeout(searchDebounce);
      if (!q) {
        dropdown.style.display = 'none';
        dropdown.innerHTML = '';
        return;
      }

      searchDebounce = setTimeout(async () => {
        try {
          const res = await fetch(`/api/places/search?q=${encodeURIComponent(q)}`);
          if (!res.ok) return;
          const results = await res.json();

          if (results.length === 0) {
            dropdown.innerHTML = `<div class="search-suggestion-item" style="color:var(--text-muted); cursor:default;">No matching places found. Try city name or lat,lon coordinates.</div>`;
            dropdown.style.display = 'block';
            return;
          }

          dropdown.innerHTML = results.slice(0, 8).map(place => `
            <div class="search-suggestion-item" data-place-id="${place.id}">
              <div>
                <strong style="color:#fff;">${place.name}</strong>
                <small style="display:block; color:var(--text-muted);">${place.city || ''} (${place.lat.toFixed(3)}, ${place.lon.toFixed(3)}) · ${place.zone_type || 'Study Zone'}</small>
              </div>
              <span class="hud-badge ${place.is_synthetic ? 'amber' : 'green'}" style="font-size:0.68rem;">${place.is_synthetic ? 'Demo Point' : 'Regional'}</span>
            </div>
          `).join('');

          dropdown.style.display = 'block';

          // Click item in dropdown
          dropdown.querySelectorAll('.search-suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
              const placeId = item.getAttribute('data-place-id');
              const found = results.find(r => String(r.id) === String(placeId));
              if (found) {
                searchInput.value = found.name;
                dropdown.style.display = 'none';
                selectPlace(found);
                if (state.map) {
                  state.map.setView([found.lat, found.lon], 12);
                }
              }
            });
          });
        } catch (err) {
          console.warn('Place search error:', err);
        }
      }, 200);
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearBtn.style.display = 'none';
        dropdown.style.display = 'none';
        dropdown.innerHTML = '';
      });
    }

    // Close dropdown on click outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.place-search-container')) {
        dropdown.style.display = 'none';
      }
    });
  }

  // Filter Pills Handling
  const filterPills = document.querySelectorAll('#filter-pills-container .filter-pill');
  filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const scope = pill.getAttribute('data-scope');
      const city = pill.getAttribute('data-city');
      const cat = pill.getAttribute('data-cat');

      let query = 'scope=core';
      if (scope) query = `scope=${scope}`;
      else if (city) query = `city=${encodeURIComponent(city)}`;
      else if (cat) query = `category=${encodeURIComponent(cat)}`;

      state.activeFilterScope = query;
      loadMapLocations(query);

      // Re-center map if appropriate
      if (scope === 'all' || scope === 'metros') {
        state.map.setView([21.0, 78.0], 5);
      } else {
        state.map.setView([19.0760, 72.8777], 11);
      }
    });
  });

  // Map Click Listener for Coordinates and Point Discovery
  if (state.map) {
    state.map.on('click', async (e) => {
      const lat = e.latlng.lat;
      const lon = e.latlng.lng;
      try {
        const res = await fetch(`/api/places/search?q=${lat.toFixed(4)},${lon.toFixed(4)}`);
        if (res.ok) {
          const results = await res.json();
          if (results.length > 0) {
            const loc = results[0];
            selectPlace(loc);
            showToast(`Selected location at [${lat.toFixed(4)}, ${lon.toFixed(4)}]`);
          }
        }
      } catch (err) {
        console.warn('Map click search error:', err);
      }
    });
  }

  // HUD Action Buttons
  const btnLoad = $('btn-place-load-estimator');
  if (btnLoad) {
    btnLoad.addEventListener('click', () => {
      if (state.selectedLocation) {
        loadLocationIntoPredictor(state.selectedLocation);
      }
    });
  }

  const btnZoom = $('btn-place-zoom');
  if (btnZoom) {
    btnZoom.addEventListener('click', () => {
      if (state.selectedLocation && state.map) {
        state.map.setView([state.selectedLocation.lat, state.selectedLocation.lon], 13);
      }
    });
  }

  const btnClear = $('btn-place-clear');
  if (btnClear) {
    btnClear.addEventListener('click', () => {
      const hud = $('selected-place-hud');
      if (hud) hud.style.display = 'none';
      if (state.selectedPlaceMarker) {
        state.selectedPlaceMarker.remove();
        state.selectedPlaceMarker = null;
      }
      state.selectedLocation = null;
    });
  }
}

// -----------------------------------------------------------------------------
// Predictor Form & Sliders
// -----------------------------------------------------------------------------
function readPredictorInputs() {
  return {
    ndvi: parseFloat($('slider-ndvi').value),
    impervious_pct: parseFloat($('slider-impervious').value),
    tree_canopy_pct: parseFloat($('slider-canopy').value),
    albedo: parseFloat($('slider-albedo').value),
    air_temp_c: parseFloat($('slider-airtemp').value),
    relative_humidity_pct: parseFloat($('slider-humidity').value)
  };
}

function setPredictorInputs(vals) {
  if (vals.ndvi !== undefined) {
    $('slider-ndvi').value = vals.ndvi;
    $('val-ndvi-display').textContent = vals.ndvi.toFixed(2);
  }
  if (vals.impervious_pct !== undefined) {
    $('slider-impervious').value = vals.impervious_pct;
    $('val-impervious-display').textContent = `${Math.round(vals.impervious_pct)}%`;
  }
  if (vals.tree_canopy_pct !== undefined) {
    $('slider-canopy').value = vals.tree_canopy_pct;
    $('val-canopy-display').textContent = `${Math.round(vals.tree_canopy_pct)}%`;
  }
  if (vals.albedo !== undefined) {
    $('slider-albedo').value = vals.albedo;
    $('val-albedo-display').textContent = vals.albedo.toFixed(2);
  }
  if (vals.air_temp_c !== undefined) {
    $('slider-airtemp').value = vals.air_temp_c;
    $('val-airtemp-display').textContent = `${vals.air_temp_c.toFixed(1)}°C`;
  }
  if (vals.relative_humidity_pct !== undefined) {
    $('slider-humidity').value = vals.relative_humidity_pct;
    $('val-humidity-display').textContent = `${Math.round(vals.relative_humidity_pct)}%`;
  }
  state.currentBaselineInputs = readPredictorInputs();
}

function initSliderListeners() {
  const fields = [
    { id: 'slider-ndvi', label: 'val-ndvi-display', format: (v) => parseFloat(v).toFixed(2) },
    { id: 'slider-impervious', label: 'val-impervious-display', format: (v) => `${Math.round(v)}%` },
    { id: 'slider-canopy', label: 'val-canopy-display', format: (v) => `${Math.round(v)}%` },
    { id: 'slider-albedo', label: 'val-albedo-display', format: (v) => parseFloat(v).toFixed(2) },
    { id: 'slider-airtemp', label: 'val-airtemp-display', format: (v) => `${parseFloat(v).toFixed(1)}°C` },
    { id: 'slider-humidity', label: 'val-humidity-display', format: (v) => `${Math.round(v)}%` },
  ];

  fields.forEach(f => {
    const el = $(f.id);
    if (!el) return;
    el.addEventListener('input', (e) => {
      $(f.label).textContent = f.format(e.target.value);
      state.currentBaselineInputs = readPredictorInputs();
      debouncePrediction();
    });
  });

  // Archetype preset dropdown
  $('preset-selector').addEventListener('change', (e) => {
    const key = e.target.value;
    if (key && ARCHETYPES[key]) {
      setPredictorInputs(ARCHETYPES[key]);
      executePrediction();
      showToast(`Applied archetype: ${ARCHETYPES[key].name}`);
    }
  });

  // Archetype Quick Chips
  const chipContainer = $('archetype-chips-container');
  if (chipContainer) {
    chipContainer.querySelectorAll('.archetype-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const presetKey = chip.getAttribute('data-preset');
        if (presetKey && ARCHETYPES[presetKey]) {
          setPredictorInputs(ARCHETYPES[presetKey]);
          $('preset-selector').value = presetKey;
          executePrediction();
          showToast(`Applied archetype preset: ${ARCHETYPES[presetKey].name}`);
        }
      });
    });
  }

  // Reset Predictor Inputs Button
  const resetBtn = $('btn-reset-inputs');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      setPredictorInputs(ARCHETYPES.commercial);
      $('preset-selector').value = 'commercial';
      executePrediction();
      showToast("Reset sliders to BKC commercial baseline.");
    });
  }

  // Form Submit
  $('prediction-form').addEventListener('submit', (e) => {
    e.preventDefault();
    executePrediction();
  });
}

let debounceTimer = null;
function debouncePrediction() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    executePrediction();
  }, 180);
}

// -----------------------------------------------------------------------------
// Live Inference Call
// -----------------------------------------------------------------------------
async function executePrediction() {
  const payload = readPredictorInputs();
  state.currentBaselineInputs = payload;

  const loadingEl = $('pred-loading');
  const errorEl = $('pred-error');
  if (loadingEl) loadingEl.style.display = 'block';
  if (errorEl) errorEl.style.display = 'none';

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (loadingEl) loadingEl.style.display = 'none';

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || 'Prediction failed');
    }

    const data = await res.json();
    renderPredictionResult(data);
    renderWaterfallChart(payload, data);
    logPredictionHistory(payload, data);

    // Trigger scenario simulation comparison with latest baseline
    runScenarioSimulation();
  } catch (err) {
    if (loadingEl) loadingEl.style.display = 'none';
    if (errorEl) {
      errorEl.style.display = 'block';
      errorEl.textContent = `⚠️ Inference warning: ${err.message}`;
    }
    console.error('Prediction error:', err);
    showToast(`Prediction warning: ${err.message}`);
  }
}

function renderPredictionResult(data) {
  $('res-score').textContent = data.score.toFixed(1);
  $('res-risk-tier').textContent = data.risk_tier;
  $('res-risk-tier').style.color = data.badge_color;
  $('res-risk-tier').style.background = `${data.badge_color}25`;

  const ci = data.tree_dispersion_interval || data.confidence_interval_95;
  if (ci) {
    $('res-ci').textContent = `[${ci.lower} – ${ci.upper}]`;
    $('res-std').textContent = `± ${data.uncertainty_std} σ (tree ensemble dispersion)`;
  }

  $('res-interpretation').textContent = data.interpretation;

  // Local feature driver pills
  const driversWrap = $('res-drivers-container');
  if (driversWrap && data.local_feature_drivers) {
    driversWrap.innerHTML = data.local_feature_drivers
      .slice(0, 3)
      .map(d => {
        const isElevate = d.influence === 'Elevates Risk';
        const cls = isElevate ? 'elevate' : 'mitigate';
        const sign = d.delta_from_median > 0 ? '+' : '';
        const nameClean = d.feature.replace('_pct', '').replace('_c', '');
        return `<span class="driver-pill ${cls}">${nameClean}: ${sign}${d.delta_from_median} (${isElevate ? 'Elevates' : 'Mitigates'})</span>`;
      }).join('');
  }
}

// Local Sensitivity Waterfall
function renderWaterfallChart(inputs, data) {
  const container = $('waterfall-bars-list');
  if (!container) return;

  // Benchmark medians
  const medians = {
    impervious_pct: 50.0,
    tree_canopy_pct: 25.0,
    ndvi: 0.35,
    albedo: 0.20,
    air_temp_c: 33.0,
    relative_humidity_pct: 65.0
  };

  // Sensitivity contributions (illustrative model weights)
  const items = [
    {
      name: "Impervious Cover",
      delta: (inputs.impervious_pct - medians.impervious_pct) * 0.28,
      unit: "%"
    },
    {
      name: "Tree Canopy",
      delta: -(inputs.tree_canopy_pct - medians.tree_canopy_pct) * 0.32,
      unit: "%"
    },
    {
      name: "Surface Albedo",
      delta: -(inputs.albedo - medians.albedo) * 45.0,
      unit: ""
    },
    {
      name: "Vegetation (NDVI)",
      delta: -(inputs.ndvi - medians.ndvi) * 18.0,
      unit: ""
    },
    {
      name: "Air Temperature",
      delta: (inputs.air_temp_c - medians.air_temp_c) * 0.85,
      unit: "°C"
    }
  ];

  container.innerHTML = items.map(item => {
    const isWarming = item.delta > 0;
    const absDelta = Math.abs(item.delta);
    const barWidth = Math.min(100, (absDelta / 15) * 50);
    const cls = isWarming ? 'warming' : 'cooling';
    const sign = isWarming ? '+' : '−';

    return `
      <div class="waterfall-bar-row">
        <span class="waterfall-feature-name">${item.name}</span>
        <div class="waterfall-track">
          <div class="waterfall-center-line"></div>
          <div class="waterfall-bar ${cls}" style="width: ${barWidth}%;"></div>
        </div>
        <span class="waterfall-delta ${cls}">${sign}${absDelta.toFixed(1)}</span>
      </div>
    `;
  }).join('');
}

// Session Prediction History
function logPredictionHistory(inputs, data) {
  const historyList = $('prediction-history-list');
  const countEl = $('history-count');
  if (!historyList) return;

  const entry = {
    id: Date.now(),
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
    score: data.score.toFixed(1),
    tier: data.risk_tier,
    badgeColor: data.badge_color,
    inputs: { ...inputs }
  };

  state.predictionHistory.unshift(entry);
  if (state.predictionHistory.length > 10) state.predictionHistory.pop();

  if (countEl) countEl.textContent = state.predictionHistory.length;

  historyList.innerHTML = state.predictionHistory.map(item => `
    <div class="history-row" data-history-id="${item.id}">
      <div>
        <span class="history-score" style="color: ${item.badgeColor};">${item.score}</span>
        <span style="color: var(--text-muted); margin-left: 6px;">${item.tier}</span>
        <small style="display: block; color: var(--text-subtle);">${item.time} · Imp: ${item.inputs.impervious_pct}%, Can: ${item.inputs.tree_canopy_pct}%, Alb: ${item.inputs.albedo}</small>
      </div>
      <button type="button" class="btn btn-xs btn-outline btn-replay-history" data-history-id="${item.id}">↺ Replay</button>
    </div>
  `).join('');

  historyList.querySelectorAll('.btn-replay-history').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = parseInt(btn.getAttribute('data-history-id'), 10);
      const found = state.predictionHistory.find(h => h.id === id);
      if (found) {
        setPredictorInputs(found.inputs);
        executePrediction();
        showToast(`Replayed session run from ${found.time} (Score: ${found.score})`);
      }
    });
  });
}

// -----------------------------------------------------------------------------
// SCENE 5: Cooling Intervention Simulator (Audited Arithmetic)
// -----------------------------------------------------------------------------
function initSimulator() {
  const canopySlider = $('sim-canopy-slider');
  const imperviousSlider = $('sim-impervious-slider');
  const albedoSlider = $('sim-albedo-slider');

  canopySlider.addEventListener('input', (e) => {
    $('sim-canopy-val').textContent = `+${e.target.value}%`;
    state.currentSimulationDeltas.delta_tree_canopy_pct = parseFloat(e.target.value);
    runScenarioSimulation();
  });

  imperviousSlider.addEventListener('input', (e) => {
    $('sim-impervious-val').textContent = `−${e.target.value}%`;
    state.currentSimulationDeltas.delta_impervious_pct = -parseFloat(e.target.value);
    runScenarioSimulation();
  });

  albedoSlider.addEventListener('input', (e) => {
    $('sim-albedo-val').textContent = `+${parseFloat(e.target.value).toFixed(2)}`;
    state.currentSimulationDeltas.delta_albedo = parseFloat(e.target.value);
    runScenarioSimulation();
  });

  // Preset Chips
  const presets = [
    { id: 'btn-preset-canopy', name: 'Urban Canopy Expansion', canopy: 20, impervious: 0, albedo: 0.0 },
    { id: 'btn-preset-coolroof', name: 'Cool Roofs Initiative', canopy: 0, impervious: 0, albedo: 0.12 },
    { id: 'btn-preset-permeable', name: 'Permeable Pavement Transition', canopy: 0, impervious: 15, albedo: 0.0 },
    { id: 'btn-preset-comprehensive', name: 'Comprehensive Greening', canopy: 20, impervious: 15, albedo: 0.10 },
  ];

  presets.forEach(p => {
    const btn = $(p.id);
    if (!btn) return;
    btn.addEventListener('click', () => {
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      canopySlider.value = p.canopy;
      $('sim-canopy-val').textContent = `+${p.canopy}%`;
      state.currentSimulationDeltas.delta_tree_canopy_pct = p.canopy;

      imperviousSlider.value = p.impervious;
      $('sim-impervious-val').textContent = `−${p.impervious}%`;
      state.currentSimulationDeltas.delta_impervious_pct = -p.impervious;

      albedoSlider.value = p.albedo;
      $('sim-albedo-val').textContent = `+${p.albedo.toFixed(2)}`;
      state.currentSimulationDeltas.delta_albedo = p.albedo;

      state.currentSimulationDeltas.preset_name = p.name;
      runScenarioSimulation();
      showToast(`Simulating: ${p.name}`);
    });
  });

  // Warming Comparison Preset 1: Canopy Loss & Heat Sprawl
  const deforestBtn = $('btn-preset-deforestation');
  if (deforestBtn) {
    deforestBtn.addEventListener('click', () => {
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));
      deforestBtn.classList.add('active');

      canopySlider.value = 0;
      $('sim-canopy-val').textContent = `−15%`;
      state.currentSimulationDeltas.delta_tree_canopy_pct = -15.0;

      imperviousSlider.value = 15;
      $('sim-impervious-val').textContent = `+15%`;
      state.currentSimulationDeltas.delta_impervious_pct = 15.0;

      albedoSlider.value = 0;
      $('sim-albedo-val').textContent = `−0.04`;
      state.currentSimulationDeltas.delta_albedo = -0.04;

      state.currentSimulationDeltas.preset_name = "Canopy Loss & Heat Sprawl";
      runScenarioSimulation();
      showToast("Simulating warming comparison: Canopy Loss & Sprawl");
    });
  }

  // Warming Comparison Preset 2: Asphalt Sprawl
  const sprawlBtn = $('btn-preset-sprawl');
  if (sprawlBtn) {
    sprawlBtn.addEventListener('click', () => {
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));
      sprawlBtn.classList.add('active');

      canopySlider.value = 0;
      $('sim-canopy-val').textContent = `+0%`;
      state.currentSimulationDeltas.delta_tree_canopy_pct = 0.0;

      imperviousSlider.value = 20;
      $('sim-impervious-val').textContent = `+20%`;
      state.currentSimulationDeltas.delta_impervious_pct = 20.0;

      albedoSlider.value = 0;
      $('sim-albedo-val').textContent = `−0.05`;
      state.currentSimulationDeltas.delta_albedo = -0.05;

      state.currentSimulationDeltas.preset_name = "Asphalt Paving Sprawl";
      runScenarioSimulation();
      showToast("Simulating warming comparison: Asphalt Sprawl");
    });
  }

  // Reset Simulator Button
  const resetSimBtn = $('btn-reset-simulator');
  if (resetSimBtn) {
    resetSimBtn.addEventListener('click', () => {
      canopySlider.value = 0;
      $('sim-canopy-val').textContent = `+0%`;
      state.currentSimulationDeltas.delta_tree_canopy_pct = 0.0;

      imperviousSlider.value = 0;
      $('sim-impervious-val').textContent = `−0%`;
      state.currentSimulationDeltas.delta_impervious_pct = 0.0;

      albedoSlider.value = 0;
      $('sim-albedo-val').textContent = `+0.00`;
      state.currentSimulationDeltas.delta_albedo = 0.0;

      state.currentSimulationDeltas.preset_name = "Baseline Zero (No Intervention)";
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));
      runScenarioSimulation();
      showToast("Reset simulator to zero delta baseline.");
    });
  }

  // Open Intervention Evidence Catalogue
  const openCatBtn = $('btn-open-interventions-catalogue');
  if (openCatBtn) {
    openCatBtn.addEventListener('click', () => {
      const modal = $('modal-interventions');
      if (modal) modal.style.display = 'grid';
    });
  }
}

async function runScenarioSimulation() {
  const payload = {
    baseline: state.currentBaselineInputs,
    delta_tree_canopy_pct: state.currentSimulationDeltas.delta_tree_canopy_pct,
    delta_impervious_pct: state.currentSimulationDeltas.delta_impervious_pct,
    delta_albedo: state.currentSimulationDeltas.delta_albedo,
    preset_name: state.currentSimulationDeltas.preset_name
  };

  try {
    const res = await fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Simulation failed');
    const sim = await res.json();

    $('sim-base-score').textContent = sim.baseline.score.toFixed(1);
    $('sim-base-tier').textContent = sim.baseline.risk_tier;

    $('sim-scen-score').textContent = sim.scenario.score.toFixed(1);
    $('sim-scen-tier').textContent = sim.scenario.risk_tier;

    // Audited Arithmetic:
    // Risk reduction points = baseline score - scenario score
    const baseScore = sim.baseline.score;
    const scenScore = sim.scenario.score;
    const reductionPoints = (sim.delta && typeof sim.delta.risk_reduction_points === 'number')
      ? sim.delta.risk_reduction_points
      : (baseScore - scenScore);
    const pctReduction = (sim.delta && typeof sim.delta.percentage_reduction === 'number')
      ? sim.delta.percentage_reduction
      : (baseScore > 0 ? ((baseScore - scenScore) / baseScore * 100) : 0.0);

    const deltaTitle = $('sim-delta-title');
    const deltaScoreEl = $('sim-delta-score');
    const deltaPctEl = $('sim-delta-pct');

    if (reductionPoints > 0) {
      if (deltaTitle) deltaTitle.textContent = "NET RISK REDUCTION";
      deltaScoreEl.textContent = `−${Math.abs(reductionPoints).toFixed(1)}`;
      deltaScoreEl.style.color = '#10b981';
      deltaPctEl.textContent = `−${Math.abs(pctReduction).toFixed(1)}%`;
      deltaPctEl.style.color = '#10b981';
    } else if (reductionPoints < 0) {
      if (deltaTitle) deltaTitle.textContent = "NET RISK INCREASE";
      deltaScoreEl.textContent = `+${Math.abs(reductionPoints).toFixed(1)}`;
      deltaScoreEl.style.color = '#ef4444';
      deltaPctEl.textContent = `+${Math.abs(pctReduction).toFixed(1)}%`;
      deltaPctEl.style.color = '#ef4444';
    } else {
      if (deltaTitle) deltaTitle.textContent = "NO NET CHANGE";
      deltaScoreEl.textContent = "0.0";
      deltaScoreEl.style.color = '#86a69a';
      deltaPctEl.textContent = "0.0%";
      deltaPctEl.style.color = '#86a69a';
    }

    $('sim-mechanism-text').textContent = sim.mechanism_explanation;

    // Direct 3D scene visual feedback on intervention update
    if (window.update3DInterventionVisuals) {
      window.update3DInterventionVisuals(
        state.currentSimulationDeltas.delta_tree_canopy_pct,
        state.currentSimulationDeltas.delta_albedo
      );
    }
  } catch (err) {
    console.error('Simulator error:', err);
  }
}

// -----------------------------------------------------------------------------
// Explainable AI & Feature Importance
// -----------------------------------------------------------------------------
async function loadFeatureImportance() {
  try {
    const res = await fetch('/api/feature-importance');
    if (!res.ok) throw new Error('Failed to load importance metrics');
    state.importanceData = await res.json();
    renderImportanceChart();
  } catch (err) {
    console.warn('Feature importance note:', err.message);
  }
}

function renderImportanceChart() {
  const container = $('importance-chart-wrapper');
  if (!container || !state.importanceData.length) return;

  const isPerm = state.activeImportanceMetric === 'perm';
  const valKey = isPerm ? 'importance_mean' : 'gini_importance';

  const maxVal = Math.max(...state.importanceData.map(d => d[valKey] || 0.001));

  container.innerHTML = state.importanceData.map(item => {
    const rawVal = item[valKey] || 0;
    const pct = Math.max(5, (rawVal / maxVal) * 100);
    const scoreStr = isPerm ? rawVal.toFixed(3) : (rawVal * 100).toFixed(1) + '%';
    const cleanName = item.feature.replaceAll('_pct', '').replaceAll('_c', '').toUpperCase();

    return `
      <div class="importance-bar-row" title="${item.description}">
        <span class="importance-feature-name">${cleanName}</span>
        <div class="importance-track">
          <div class="importance-fill" style="width: ${pct}%;"></div>
        </div>
        <span class="importance-score">${scoreStr}</span>
      </div>
    `;
  }).join('');
}

function initImportanceToggles() {
  const btnPerm = $('btn-toggle-perm');
  const btnGini = $('btn-toggle-gini');

  btnPerm.addEventListener('click', () => {
    btnPerm.classList.add('active');
    btnGini.classList.remove('active');
    state.activeImportanceMetric = 'perm';
    renderImportanceChart();
  });

  btnGini.addEventListener('click', () => {
    btnGini.classList.add('active');
    btnPerm.classList.remove('active');
    state.activeImportanceMetric = 'gini';
    renderImportanceChart();
  });
}

// -----------------------------------------------------------------------------
// Summary & Diagnostics Card Updates
// -----------------------------------------------------------------------------
async function loadSummaryDiagnostics() {
  try {
    const res = await fetch('/api/summary');
    if (!res.ok) throw new Error('Failed to fetch summary metrics');
    const data = await res.json();

    if (data.n_total_samples) {
      $('kpi-total-samples').textContent = data.n_total_samples.toLocaleString();
    }
    if (data.n_train_samples && data.n_test_samples) {
      const trainPct = Math.round((data.n_train_samples / data.n_total_samples) * 100);
      const testPct = 100 - trainPct;
      $('kpi-split-ratio').textContent = `${trainPct}% Train / ${testPct}% Test`;
    }
    if (data.test_metrics) {
      $('kpi-mae').textContent = data.test_metrics.mae.toFixed(2);
      $('kpi-r2').textContent = data.test_metrics.r2.toFixed(3);
    }
  } catch (err) {
    console.warn('Summary diagnostics note:', err.message);
  }
}

// -----------------------------------------------------------------------------
// Real Observed Environmental Data (NASA POWER)
// -----------------------------------------------------------------------------
async function loadObservedEnvironmentalData() {
  const panel = $('nasa-observed-panel');
  if (!panel) return;

  const loadingEl = $('obs-loading');
  const errorEl = $('obs-error');
  const statsGrid = $('obs-stats-grid');
  const toggleBtn = $('btn-toggle-daily-table');
  const tableContainer = $('daily-observations-container');
  const tbody = $('daily-observations-tbody');

  // Display loading state
  if (loadingEl) loadingEl.style.display = 'block';
  if (errorEl) errorEl.style.display = 'none';

  try {
    const res = await fetch('/api/environmental-data');
    if (!res.ok) throw new Error(`HTTP ${res.status}: Dataset endpoint unavailable`);
    const data = await res.json();

    // Hide loading
    if (loadingEl) loadingEl.style.display = 'none';

    // Populate validated KPI cards
    const stats = data.summary_statistics;
    if (stats) {
      if ($('obs-mean-temp')) {
        const meanTemp = stats.monthly_mean_daily_avg_temp_c !== undefined ? stats.monthly_mean_daily_avg_temp_c : stats.mean_temp_c;
        $('obs-mean-temp').textContent = `${meanTemp} °C`;
      }
      if ($('obs-mean-max-temp')) {
        const meanMax = stats.monthly_mean_daily_max_temp_c !== undefined ? stats.monthly_mean_daily_max_temp_c : (stats.mean_daily_max_temp_c || 39.23);
        $('obs-mean-max-temp').textContent = `${meanMax} °C`;
      }
      if ($('obs-max-temp')) {
        const peakMax = stats.peak_single_day_max_temp_c !== undefined ? stats.peak_single_day_max_temp_c : (stats.max_temp_c || 40.86);
        $('obs-max-temp').textContent = `${peakMax} °C`;
      }
      if ($('obs-mean-humidity')) {
        $('obs-mean-humidity').textContent = `${stats.mean_humidity_pct} %`;
      }
      if ($('obs-mean-solar')) {
        $('obs-mean-solar').textContent = `${stats.mean_solar_irradiance_mj_m2} MJ/m²`;
      }
      if ($('obs-day-count')) {
        const days = (data.temporal_coverage && data.temporal_coverage.days_recorded) ||
                     (data.daily_observations ? data.daily_observations.length : 31);
        $('obs-day-count').textContent = `${days} Days`;
      }
    }

    // Populate daily observations table (with empty state handling)
    if (tbody) {
      if (!data.daily_observations || data.daily_observations.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="7" style="text-align: center; padding: 20px; color: var(--text-muted);">
              No daily observations found in the stored environmental dataset.
            </td>
          </tr>`;
      } else {
        tbody.innerHTML = data.daily_observations.map(d => `
          <tr>
            <td><strong>${d.date}</strong></td>
            <td>${Number(d.T2M).toFixed(1)} °C</td>
            <td style="color: #f59e0b; font-weight: 600;">${Number(d.T2M_MAX).toFixed(1)} °C</td>
            <td>${Number(d.T2M_MIN).toFixed(1)} °C</td>
            <td>${Math.round(Number(d.RH2M))} %</td>
            <td>${Number(d.ALLSKY_SFC_SW_DWN).toFixed(2)} MJ/m²</td>
            <td>${Number(d.WS2M).toFixed(1)} m/s</td>
          </tr>
        `).join('');
      }
    }

    // Toggle button handler with full accessibility (click + keyboard Enter & Space)
    if (toggleBtn && tableContainer) {
      const toggleTable = () => {
        const isHidden = tableContainer.style.display === 'none' || tableContainer.style.display === '';
        tableContainer.style.display = isHidden ? 'block' : 'none';
        toggleBtn.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
        const count = data.daily_observations ? data.daily_observations.length : 31;
        const span = toggleBtn.querySelector('span');
        if (span) {
          span.textContent = isHidden
            ? 'Hide Daily Observations ▲'
            : `View ${count} Daily Observations ▼`;
        }
      };

      toggleBtn.onclick = (e) => {
        e.preventDefault();
        toggleTable();
      };

      toggleBtn.onkeydown = (e) => {
        if (e.key === 'Enter' || e.key === ' ' || e.code === 'Space') {
          e.preventDefault();
          toggleTable();
        }
      };
    }

    // Update topbar status badge
    const statusLabel = $('api-status-label');
    if (statusLabel) {
      statusLabel.textContent = 'FASTAPI LIVE · NASA OBSERVED READY';
    }
  } catch (err) {
    console.warn('Observed environmental data notice:', err.message);
    if (loadingEl) loadingEl.style.display = 'none';
    if (errorEl) {
      errorEl.style.display = 'block';
      errorEl.innerHTML = `<span>⚠️ Could not load environmental dataset: ${err.message}. Run <code>python scripts/ingest_real_data.py</code> to regenerate cache.</span>`;
    }
  }

  // Wire Return to Living Planet Scene link (smooth scroll to #hero)
  const returnTopBtn = $('btn-return-top');
  if (returnTopBtn && !returnTopBtn.dataset.bound) {
    returnTopBtn.dataset.bound = 'true';
    returnTopBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const hero = $('hero');
      if (hero) {
        hero.scrollIntoView({ behavior: 'smooth' });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  }
}

// Baseline Comparison Drawer
function initBaselineDrawer() {
  const drawer = $('baseline-drawer');
  $('btn-show-baselines').addEventListener('click', () => {
    drawer.style.display = drawer.style.display === 'none' ? 'block' : 'none';
  });
  $('close-baselines-btn').addEventListener('click', () => {
    drawer.style.display = 'none';
  });
}

// -----------------------------------------------------------------------------
// Modal Dialogs & Report Export
// -----------------------------------------------------------------------------
function initModals() {
  // Environmental Glossary Modal
  const glossaryModal = $('modal-glossary');
  $('open-glossary-btn').addEventListener('click', () => glossaryModal.style.display = 'grid');
  $('close-glossary-modal').addEventListener('click', () => glossaryModal.style.display = 'none');

  // Satellite Data Sources Modal
  const sourcesModal = $('modal-sources');
  $('open-sources-btn').addEventListener('click', () => sourcesModal.style.display = 'grid');
  $('banner-learn-more').addEventListener('click', (e) => {
    e.preventDefault();
    sourcesModal.style.display = 'grid';
  });
  $('footer-sources-btn').addEventListener('click', () => sourcesModal.style.display = 'grid');
  $('close-sources-modal').addEventListener('click', () => sourcesModal.style.display = 'none');

  // Research Hub Modal
  const hubModal = $('modal-research-hub');
  const openHubBtn = $('open-research-hub-btn');
  const closeHubBtn = $('close-hub-modal');
  if (openHubBtn && hubModal) {
    openHubBtn.addEventListener('click', () => hubModal.style.display = 'grid');
  }
  if (closeHubBtn && hubModal) {
    closeHubBtn.addEventListener('click', () => hubModal.style.display = 'none');
  }

  // Research Hub Tab Switching
  const hubTabBtns = document.querySelectorAll('.hub-tab-btn');
  hubTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      hubTabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const targetTab = btn.getAttribute('data-hub-tab');
      document.querySelectorAll('.hub-tab-pane').forEach(pane => {
        pane.classList.remove('active');
      });
      const targetPane = $(`hub-tab-${targetTab}`);
      if (targetPane) targetPane.classList.add('active');
    });
  });

  // Intervention Evidence Catalogue Modal
  const interventionsModal = $('modal-interventions');
  const openInterventionsBtn = $('open-interventions-catalogue-btn');
  const closeInterventionsBtn = $('close-interventions-modal');
  if (openInterventionsBtn && interventionsModal) {
    openInterventionsBtn.addEventListener('click', () => interventionsModal.style.display = 'grid');
  }
  if (closeInterventionsBtn && interventionsModal) {
    closeInterventionsBtn.addEventListener('click', () => interventionsModal.style.display = 'none');
  }

  // Printable Assessment Report Preview Modal
  const printModal = $('modal-print-report');
  const openPrintBtn = $('open-print-report-btn');
  const previewPrintBtn = $('btn-preview-printable-report');
  const closePrintBtn = $('close-print-modal');
  const triggerPrintBtn = $('btn-trigger-print');

  const openPrintPreview = () => {
    renderPrintableReport();
    if (printModal) printModal.style.display = 'grid';
  };

  if (openPrintBtn) openPrintBtn.addEventListener('click', openPrintPreview);
  if (previewPrintBtn) previewPrintBtn.addEventListener('click', openPrintPreview);
  if (closePrintBtn && printModal) {
    closePrintBtn.addEventListener('click', () => printModal.style.display = 'none');
  }
  if (triggerPrintBtn) {
    triggerPrintBtn.addEventListener('click', () => {
      window.print();
    });
  }

  // Footer Viva Guide link
  $('footer-viva-btn').addEventListener('click', () => {
    window.open('/docs', '_blank');
  });

  // Close modals on clicking overlay outside window
  window.addEventListener('click', (e) => {
    if (e.target === glossaryModal) glossaryModal.style.display = 'none';
    if (e.target === sourcesModal) sourcesModal.style.display = 'none';
    if (e.target === hubModal) hubModal.style.display = 'none';
    if (e.target === interventionsModal) interventionsModal.style.display = 'none';
    if (e.target === printModal) printModal.style.display = 'none';
  });

  // Mobile sidebar toggle
  const sidebar = $('sidebar');
  $('sidebar-toggle').addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Export Assessment Report (Connected to both sidebar & Scene 6 button)
  const triggerExport = async () => {
    try {
      const payload = {
        location_name: state.selectedLocation ? state.selectedLocation.name : "Custom Study Point",
        notes: "Generated by HeatLens AI urban microclimate decision support platform.",
        inputs: state.currentBaselineInputs,
        simulation: {
          baseline: state.currentBaselineInputs,
          delta_tree_canopy_pct: state.currentSimulationDeltas.delta_tree_canopy_pct,
          delta_impervious_pct: state.currentSimulationDeltas.delta_impervious_pct,
          delta_albedo: state.currentSimulationDeltas.delta_albedo,
          preset_name: state.currentSimulationDeltas.preset_name
        }
      };

      const res = await fetch('/api/export-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Export failed');
      const reportData = await res.json();

      // Trigger client-side JSON download
      const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `heatlens_environmental_report_${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);

      showToast("Environmental assessment report exported successfully!");
    } catch (err) {
      console.error('Export error:', err);
      showToast(`Export failed: ${err.message}`);
    }
  };

  $('open-export-btn').addEventListener('click', triggerExport);
  const transExportBtn = $('transparency-export-btn');
  if (transExportBtn) transExportBtn.addEventListener('click', triggerExport);
}

// Dynamically Render Printable Assessment Report
function renderPrintableReport() {
  const container = $('printable-report-content');
  if (!container) return;

  const loc = state.selectedLocation || {
    name: "Mumbai Metropolitan Study Core",
    city: "Mumbai",
    lat: 19.0760,
    lon: 72.8777,
    zone_type: "Commercial Core",
    data_source: "Synthetic Micro Study Data",
    is_synthetic: true
  };

  const inputs = state.currentBaselineInputs;
  const score = $('res-score') ? $('res-score').textContent : '58.4';
  const tier = $('res-risk-tier') ? $('res-risk-tier').textContent : 'Moderate Risk';
  const ci = $('res-ci') ? $('res-ci').textContent : '[53.7 – 63.1]';

  const simBase = $('sim-base-score') ? $('sim-base-score').textContent : score;
  const simScen = $('sim-scen-score') ? $('sim-scen-score').textContent : '45.2';
  const simDelta = $('sim-delta-score') ? $('sim-delta-score').textContent : '−13.2';
  const simPct = $('sim-delta-pct') ? $('sim-delta-pct').textContent : '−22.6%';
  const preset = state.currentSimulationDeltas.preset_name;

  container.innerHTML = `
    <div class="report-header-banner">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <h2>HeatLens AI — Urban Microclimate Assessment Report</h2>
          <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px;">Environmental Decision Support &amp; Urban Heat Intelligence System</p>
        </div>
        <div style="text-align:right; font-size:0.78rem; color:#94a3b8;">
          <strong>Report ID:</strong> HL-${Date.now().toString(36).toUpperCase()}<br>
          <strong>Date Generated:</strong> ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>

    <div class="report-meta-grid">
      <div class="report-meta-item">
        <small>Target Location</small>
        <strong>${loc.name} (${loc.city || 'Mumbai'})</strong>
      </div>
      <div class="report-meta-item">
        <small>Geographic Coordinates</small>
        <strong>${loc.lat.toFixed(4)}°N, ${loc.lon.toFixed(4)}°E</strong>
      </div>
      <div class="report-meta-item">
        <small>Analytical Model</small>
        <strong>Random Forest Regressor (220 Trees)</strong>
      </div>
      <div class="report-meta-item">
        <small>Dataset Provenance</small>
        <strong>${loc.data_source || 'Synthetic Demonstration Baseline'}</strong>
      </div>
    </div>

    <div class="report-section">
      <h4>1. Baseline Biophysical &amp; Meteorological Parameters</h4>
      <table class="report-table">
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Value</th>
            <th>Units</th>
            <th>Benchmark Context</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Normalized Difference Vegetation Index (NDVI)</td>
            <td><strong>${inputs.ndvi.toFixed(2)}</strong></td>
            <td>Unitless index [−0.2, 1.0]</td>
            <td>ESA Sentinel-2 MSI Level-2A (B8/B4) spectral reflectance proxy</td>
          </tr>
          <tr>
            <td>Impervious Surface Coverage</td>
            <td><strong>${inputs.impervious_pct}%</strong></td>
            <td>Percentage [%]</td>
            <td>Paved roads, asphalt, and concrete structural footprint</td>
          </tr>
          <tr>
            <td>Tree Canopy Coverage</td>
            <td><strong>${inputs.tree_canopy_pct}%</strong></td>
            <td>Percentage [%]</td>
            <td>Overhead foliage shade and active transpiration volume</td>
          </tr>
          <tr>
            <td>Surface Solar Albedo</td>
            <td><strong>${inputs.albedo.toFixed(2)}</strong></td>
            <td>Solar reflectance [0.05, 0.60]</td>
            <td>Surface solar reflectivity (cool roofs vs dark asphalt)</td>
          </tr>
          <tr>
            <td>Ambient Air Temperature</td>
            <td><strong>${inputs.air_temp_c.toFixed(1)} °C</strong></td>
            <td>Degrees Celsius [°C]</td>
            <td>2-metre atmospheric temperature boundary condition (NASA POWER)</td>
          </tr>
          <tr>
            <td>Relative Humidity</td>
            <td><strong>${inputs.relative_humidity_pct}%</strong></td>
            <td>Percentage [%]</td>
            <td>Ambient atmospheric moisture content</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="report-section">
      <h4>2. Machine Learning Inference &amp; Uncertainty Quantification</h4>
      <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); padding: 14px; border-radius: 6px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <span style="font-size:0.8rem; color:#94a3b8; display:block;">ESTIMATED MICROCLIMATE RISK SCORE</span>
            <strong style="font-size:1.8rem; color:#fff;">${score} <span style="font-size:1rem; color:#94a3b8;">/ 100</span></strong>
          </div>
          <div>
            <span style="font-size:0.8rem; color:#94a3b8; display:block;">RISK CLASSIFICATION</span>
            <strong style="font-size:1.2rem; color:var(--color-mint);">${tier}</strong>
          </div>
          <div>
            <span style="font-size:0.8rem; color:#94a3b8; display:block;">TREE-DISPERSION INTERVAL (±1.96 σ)</span>
            <strong style="font-size:1.1rem; color:#38bdf8;">${ci}</strong>
          </div>
        </div>
        <p style="font-size:0.8rem; color:#94a3b8; margin-top:10px;">
          * Note: Uncertainty interval represents standard deviation dispersion across 220 decorrelated decision trees in the ensemble.
        </p>
      </div>
    </div>

    <div class="report-section">
      <h4>3. Urban Cooling Policy Intervention Scenario</h4>
      <table class="report-table">
        <thead>
          <tr>
            <th>Scenario Package</th>
            <th>Baseline Index</th>
            <th>Scenario Index</th>
            <th>Net Score Change</th>
            <th>Relative Reduction</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>${preset}</strong></td>
            <td>${simBase}</td>
            <td>${simScen}</td>
            <td><strong style="color:var(--color-mint);">${simDelta}</strong></td>
            <td><strong style="color:var(--color-mint);">${simPct}</strong></td>
          </tr>
        </tbody>
      </table>
      <p style="font-size:0.82rem; color:#94a3b8; margin-top:8px;">
        <strong>Mechanism:</strong> ${$('sim-mechanism-text') ? $('sim-mechanism-text').textContent : 'Expanded tree crowns intercept incoming shortwave solar radiation and dissipate sensible heat via latent evapotranspiration.'}
      </p>
    </div>

    <div class="report-section">
      <h4>4. Scientific Limitations &amp; Real Remote Sensing Roadmap</h4>
      <p style="font-size:0.82rem; line-height:1.55; color:#94a3b8;">
        <strong>Academic Disclosure:</strong> This document was generated by HeatLens AI for educational and decision support prototype demonstration. 
        The calculated 0–100 score is a relative unitless vulnerability index—it does NOT represent measured Celsius temperatures or municipal regulatory forecasts.
        To graduate to operational forecasting: (1) acquire USGS Landsat 8/9 Level-2 Surface Temperature (Band 10) ground-truth rasters; (2) apply QA_PIXEL bitmasking for cloud and shadow screening; (3) calibrate tree canopy cover with LiDAR height data; and (4) validate using spatial block cross-validation.
      </p>
    </div>
  `;
}

// -----------------------------------------------------------------------------
// App Initialization
// -----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  initAmbientCanvas();
  initMasterCinematic3D();
  initScrollReveal();
  initMap();
  initPlaceExplorer();
  initSliderListeners();
  initSimulator();
  initImportanceToggles();
  initBaselineDrawer();
  initModals();
  animateCounters();

  // Load backend data concurrently
  await Promise.all([
    loadSummaryDiagnostics(),
    loadFeatureImportance(),
    loadMapLocations(),
    loadObservedEnvironmentalData()
  ]);

  // Execute initial live prediction
  executePrediction();
});
