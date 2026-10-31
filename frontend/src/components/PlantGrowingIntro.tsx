import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { Sprout } from 'lucide-react';
import { type Language } from '../i18n/translations';

interface PlantGrowingIntroProps {
  onComplete: () => void;
  language?: Language;
}

export const PlantGrowingIntro: React.FC<PlantGrowingIntroProps> = ({ onComplete }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [fadingOut, setFadingOut] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);
  const isFinishedRef = useRef(false);

  const handleFinish = useCallback(() => {
    if (isFinishedRef.current) return;
    isFinishedRef.current = true;
    setFadingOut(true);
    setTimeout(() => {
      onComplete();
    }, 650);
  }, [onComplete]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Safety fallback timer: Ensure homepage is NEVER blocked under any circumstance
    const safetyTimer = setTimeout(() => {
      if (!isFinishedRef.current) {
        handleFinish();
      }
    }, 6500);

    // Verify WebGL availability
    let glAvailable = false;
    try {
      const testCanvas = document.createElement('canvas');
      const gl = testCanvas.getContext('webgl') || testCanvas.getContext('experimental-webgl');
      glAvailable = !!gl;
    } catch {
      glAvailable = false;
    }

    if (!glAvailable) {
      clearTimeout(safetyTimer);
      onComplete();
      return;
    }

    // ---------------- THREE.JS 3D CINEMATIC SCENE SETUP ----------------
    let width = container.clientWidth || window.innerWidth;
    let height = container.clientHeight || window.innerHeight;

    const scene = new THREE.Scene();
    // Warm morning sky background
    scene.background = new THREE.Color(0x0a1612);

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 50);
    camera.position.set(0, 0.18, 2.5);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: 'high-performance',
      alpha: true,
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;
    container.appendChild(renderer.domElement);

    // ---------------- LIGHTING (VIBRANT & WARM MORNING SUN) ----------------
    // 1. Warm dawn ambient light
    const ambientLight = new THREE.AmbientLight(0xfff7ed, 0.85);
    scene.add(ambientLight);

    // 2. Rising Golden Sunlight (Directional beam casting crisp shadows)
    const sunLight = new THREE.DirectionalLight(0xffedd5, 2.2);
    sunLight.position.set(3.5, 5.2, 3.0);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    scene.add(sunLight);

    // 3. Sky-blue fill light for realistic 3D depth in shadows
    const fillLight = new THREE.DirectionalLight(0xa7f3d0, 0.65);
    fillLight.position.set(-3.0, 2.5, 2.0);
    scene.add(fillLight);

    // 4. Backlight for translucent green leaf glow
    const leafGlow = new THREE.PointLight(0x86efac, 1.4, 5);
    leafGlow.position.set(0, 0.7, -0.4);
    scene.add(leafGlow);

    // ---------------- SCENE 1: FERTILE SOIL & UNDERGROUND STRATA ----------------
    // Top Soil Surface Plane with organic furrows (y = 0.0)
    const soilTopGeo = new THREE.PlaneGeometry(9, 6.5, 32, 32);
    const topPos = soilTopGeo.attributes.position;
    for (let i = 0; i < topPos.count; i++) {
      const x = topPos.getX(i);
      const y = topPos.getY(i);
      topPos.setZ(i, Math.sin(x * 3.5) * 0.045 + Math.cos(y * 3.0) * 0.035);
    }
    soilTopGeo.computeVertexNormals();

    const soilTopMat = new THREE.MeshStandardMaterial({
      color: 0x4a2e1b, // Rich warm fertile agricultural brown
      roughness: 0.88,
      metalness: 0.04,
      flatShading: true,
    });
    const soilTop = new THREE.Mesh(soilTopGeo, soilTopMat);
    soilTop.rotation.x = -Math.PI / 2.22;
    soilTop.position.set(0, 0.0, -0.15);
    soilTop.receiveShadow = true;
    scene.add(soilTop);

    // Subterranean Cross-Section (shows seed and roots below surface)
    const soilBedGeo = new THREE.PlaneGeometry(9, 3.5, 12, 12);
    const soilBedMat = new THREE.MeshStandardMaterial({
      color: 0x2e1a0e, // Deep moist earth below surface
      roughness: 0.95,
      metalness: 0.0,
    });
    const soilBed = new THREE.Mesh(soilBedGeo, soilBedMat);
    soilBed.position.set(0, -1.05, -0.3);
    scene.add(soilBed);

    // Soil crumbs / particles around the seed & emergence point
    const crumbGroup = new THREE.Group();
    const crumbGeo = new THREE.DodecahedronGeometry(0.026, 0);
    const crumbMat = new THREE.MeshStandardMaterial({ color: 0x5c3822, roughness: 0.85 });
    const crumbMeshes: { mesh: THREE.Mesh; basePos: THREE.Vector3 }[] = [];
    for (let i = 0; i < 36; i++) {
      const crumb = new THREE.Mesh(crumbGeo, crumbMat);
      const angle = Math.random() * Math.PI * 2;
      const r = 0.06 + Math.random() * 0.52;
      const x = Math.cos(angle) * r;
      const z = Math.sin(angle) * r * 0.65;
      const y = 0.015 + Math.random() * 0.035;
      crumb.position.set(x, y, z);
      const s = 0.45 + Math.random() * 0.85;
      crumb.scale.set(s, s * 0.75, s);
      crumb.castShadow = true;
      crumbGroup.add(crumb);
      crumbMeshes.push({ mesh: crumb, basePos: new THREE.Vector3(x, y, z) });
    }
    scene.add(crumbGroup);

    // ---------------- SCENE 2: PROMINENT SEED & GERMINATION ----------------
    // Seed bean resting prominently at y = -0.22, clearly visible in cutaway
    const seedGroup = new THREE.Group();
    seedGroup.position.set(0, -0.22, 0.05);

    const cotyledonGeo = new THREE.SphereGeometry(0.08, 18, 18);
    cotyledonGeo.scale(0.7, 1.4, 0.9);
    const seedMat = new THREE.MeshStandardMaterial({
      color: 0x854d27, // Golden-brown seed coat, illuminated & clear
      roughness: 0.55,
      metalness: 0.08,
    });

    const seedLeft = new THREE.Mesh(cotyledonGeo, seedMat);
    seedLeft.position.set(-0.025, 0, 0);
    seedLeft.castShadow = true;
    seedGroup.add(seedLeft);

    const seedRight = new THREE.Mesh(cotyledonGeo, seedMat);
    seedRight.position.set(0.025, 0, 0);
    seedRight.castShadow = true;
    seedGroup.add(seedRight);

    scene.add(seedGroup);

    // Downward root system (Ivory-white roots branching into soil)
    const rootMat = new THREE.MeshStandardMaterial({
      color: 0xfef9c3, // Translucent ivory-white rootlet
      roughness: 0.4,
      metalness: 0.02,
    });

    const rootSplines = [
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, -0.28, 0.04),
        new THREE.Vector3(0.02, -0.48, 0.03),
        new THREE.Vector3(-0.03, -0.72, 0.01),
        new THREE.Vector3(0.02, -1.02, -0.01),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.01, -0.42, 0.03),
        new THREE.Vector3(-0.14, -0.62, -0.03),
        new THREE.Vector3(-0.24, -0.84, -0.05),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0.01, -0.46, 0.03),
        new THREE.Vector3(0.16, -0.66, 0.04),
        new THREE.Vector3(0.26, -0.90, 0.05),
      ]),
    ];

    // Pre-create root tube meshes with setDrawRange for zero-allocation 60 FPS growth
    const rootMeshes: { mesh: THREE.Mesh; geo: THREE.TubeGeometry; maxIndices: number }[] = [];
    const rootGroup = new THREE.Group();
    rootSplines.forEach((spline, idx) => {
      const radius = idx === 0 ? 0.018 : 0.013;
      const geo = new THREE.TubeGeometry(spline, 20, radius, 8, false);
      geo.setDrawRange(0, 0); // Initially hidden
      const mesh = new THREE.Mesh(geo, rootMat);
      rootGroup.add(mesh);
      rootMeshes.push({ mesh, geo, maxIndices: geo.index ? geo.index.count : 0 });
    });
    scene.add(rootGroup);

    // ---------------- SCENE 3: SPROUT STEM & LEAVES EMERGENCE ----------------
    const stemSpline = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, -0.22, 0.04),
      new THREE.Vector3(0.01, -0.02, 0.02),
      new THREE.Vector3(0.04, 0.22, 0.0),
      new THREE.Vector3(-0.025, 0.52, 0.015),
      new THREE.Vector3(0.01, 0.88, 0.0),
    ]);

    const stemGeo = new THREE.TubeGeometry(stemSpline, 32, 0.032, 8, false);
    stemGeo.setDrawRange(0, 0); // Initially hidden
    const stemMat = new THREE.MeshStandardMaterial({
      color: 0x4ade80, // Fresh vivid green
      roughness: 0.32,
      metalness: 0.05,
    });
    const stemMesh = new THREE.Mesh(stemGeo, stemMat);
    stemMesh.castShadow = true;
    scene.add(stemMesh);
    const stemMaxIndices = stemGeo.index ? stemGeo.index.count : 0;

    // Organic Leaf Geometry
    const leafShape = new THREE.Shape();
    leafShape.moveTo(0, 0);
    leafShape.bezierCurveTo(0.16, 0.1, 0.25, 0.28, 0.0, 0.56); // Right contour
    leafShape.bezierCurveTo(-0.25, 0.28, -0.16, 0.1, 0, 0);    // Left contour

    const leafGeo = new THREE.ExtrudeGeometry(leafShape, {
      depth: 0.008,
      bevelEnabled: true,
      bevelSegments: 2,
      steps: 1,
      bevelSize: 0.004,
      bevelThickness: 0.004,
    });
    const leafPos = leafGeo.attributes.position;
    for (let i = 0; i < leafPos.count; i++) {
      const y = leafPos.getY(i);
      const x = leafPos.getX(i);
      const dip = Math.sin((y / 0.56) * Math.PI) * 0.05 - Math.abs(x) * 0.035;
      leafPos.setZ(i, leafPos.getZ(i) + dip);
    }
    leafGeo.computeVertexNormals();

    const leafMat = new THREE.MeshStandardMaterial({
      color: 0x22c55e, // Radiant agricultural emerald green
      roughness: 0.25,
      metalness: 0.05,
      side: THREE.DoubleSide,
    });

    const leafGroup = new THREE.Group();
    leafGroup.scale.set(0, 0, 0);

    // Left leaf
    const leftLeaf = new THREE.Mesh(leafGeo, leafMat);
    leftLeaf.castShadow = true;
    leftLeaf.rotation.set(0.25, 0.4, -0.6);
    leafGroup.add(leftLeaf);

    // Right leaf
    const rightLeaf = new THREE.Mesh(leafGeo, leafMat);
    rightLeaf.castShadow = true;
    rightLeaf.rotation.set(0.25, -0.4, 0.6);
    leafGroup.add(rightLeaf);

    scene.add(leafGroup);

    // ---------------- FLOATING GOLDEN MORNING DUST PARTICLES ----------------
    const particleCount = width < 768 ? 50 : 90;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleSpeeds: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 3.2;
      particlePositions[i * 3 + 1] = -0.3 + Math.random() * 2.2;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 2.0;
      particleSpeeds.push(0.0016 + Math.random() * 0.003);
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xfef08a,
      size: width < 768 ? 0.035 : 0.045,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // ---------------- ANIMATION TIMELINE (4.8 SECONDS) ----------------
    let startTime: number | null = null;
    let animationFrameId: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000; // in seconds

      // SCENE 1: Soil & Seed Swell (0.0s - 1.0s)
      if (elapsed <= 1.2) {
        const swell = Math.min(1.0, elapsed / 0.85);
        seedGroup.scale.setScalar(1.0 + swell * 0.22);
      }

      // SCENE 2: Seed Opens & Roots Sprout Downward (0.3s - 2.2s)
      if (elapsed >= 0.3) {
        const split = THREE.MathUtils.smoothstep(elapsed, 0.3, 1.6) * 0.04;
        seedLeft.position.x = -0.025 - split;
        seedLeft.rotation.z = split * 2.5;
        seedRight.position.x = 0.025 + split;
        seedRight.rotation.z = -split * 2.5;
      }

      if (elapsed >= 0.3 && elapsed <= 2.5) {
        const rootProgress = THREE.MathUtils.smoothstep(elapsed, 0.3, 2.2);
        rootMeshes.forEach(({ geo, maxIndices }) => {
          // 48 indices per tubular segment
          const count = Math.min(maxIndices, Math.floor(rootProgress * 20) * 48);
          geo.setDrawRange(0, count);
        });
      }

      // SCENE 3: Shoot Emerges from Soil & Grows Upward (0.8s - 3.2s)
      if (elapsed >= 0.8 && elapsed <= 3.8) {
        const stemProgress = THREE.MathUtils.smoothstep(elapsed, 0.8, 3.0);
        const count = Math.min(stemMaxIndices, Math.floor(stemProgress * 32) * 48);
        stemGeo.setDrawRange(0, count);

        // Position leaves directly at the growing shoot tip
        const currentTip = stemSpline.getPoint(Math.max(0.01, stemProgress));
        leafGroup.position.copy(currentTip);

        // Soil reaction: Crumbs lift and displace as sprout breaks surface
        if (elapsed >= 1.1 && elapsed <= 2.2) {
          const breachProgress = THREE.MathUtils.smoothstep(elapsed, 1.1, 2.0);
          crumbMeshes.forEach(({ mesh, basePos }) => {
            const dist = Math.sqrt(basePos.x * basePos.x + basePos.z * basePos.z);
            if (dist < 0.24) {
              const push = (0.24 - dist) * 0.5 * breachProgress;
              mesh.position.y = basePos.y + push;
              mesh.rotation.x = push * 3.5;
            }
          });
        }
      }

      // SCENE 3 cont: Leaves Unfold One by One & Sway in Morning Breeze (2.0s - 4.6s)
      if (elapsed >= 1.8) {
        const overallLeaf = THREE.MathUtils.smoothstep(elapsed, 1.8, 3.4);
        leafGroup.scale.setScalar(overallLeaf);

        // Left leaf unfolds
        const leftProg = THREE.MathUtils.smoothstep(elapsed, 1.8, 2.9);
        leftLeaf.rotation.z = THREE.MathUtils.lerp(-1.1, -0.42, leftProg);
        leftLeaf.scale.setScalar(THREE.MathUtils.lerp(0.3, 1.0, leftProg));

        // Right leaf unfolds slightly after
        const rightProg = THREE.MathUtils.smoothstep(elapsed, 2.2, 3.2);
        rightLeaf.rotation.z = THREE.MathUtils.lerp(1.1, 0.42, rightProg);
        rightLeaf.scale.setScalar(THREE.MathUtils.lerp(0.3, 1.0, rightProg));

        // Gentle organic wind breeze
        if (elapsed > 3.0) {
          const sway = Math.sin((elapsed - 3.0) * 3.0) * 0.04;
          leafGroup.rotation.z = sway;
          leafGroup.rotation.x = Math.cos((elapsed - 3.0) * 2.5) * 0.025;
        }
      }

      // Floating golden dust movement
      const pArr = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        pArr[i * 3 + 1] += particleSpeeds[i];
        if (pArr[i * 3 + 1] > 2.2) {
          pArr[i * 3 + 1] = -0.2;
        }
      }
      particleGeo.attributes.position.needsUpdate = true;

      // Camera glides gracefully to frame the blooming plant
      const camProgress = THREE.MathUtils.smoothstep(elapsed, 0.3, 3.2);
      camera.position.y = THREE.MathUtils.lerp(0.12, 0.36, camProgress);
      camera.position.z = THREE.MathUtils.lerp(2.4, 2.5, camProgress);
      camera.lookAt(0, THREE.MathUtils.lerp(-0.08, 0.32, camProgress), 0);

      // SCENE 4: Welcome Text Appearance (Triggered at 2.4s as leaves unfurl)
      if (elapsed >= 2.4 && !showWelcome) {
        setShowWelcome(true);
      }

      // SCENE 5: Transition to Homepage (At 4.8s, smoothly fade into homepage)
      if (elapsed >= 4.8 && !isFinishedRef.current) {
        handleFinish();
        return;
      }

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);

    // Responsive Resize Handler
    const handleResize = () => {
      if (!container) return;
      width = container.clientWidth || window.innerWidth;
      height = container.clientHeight || window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup on unmount (prevent memory leaks)
    return () => {
      clearTimeout(safetyTimer);
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);

      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh) {
          obj.geometry.dispose();
          if (Array.isArray(obj.material)) {
            obj.material.forEach((m) => m.dispose());
          } else {
            obj.material.dispose();
          }
        }
      });
      renderer.dispose();
      if (container && renderer.domElement.parentNode === container) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [handleFinish, onComplete, showWelcome]);

  return (
    <div
      className={`fixed inset-0 z-50 overflow-hidden bg-gradient-to-b from-[#061a14] via-[#0d281e] to-[#1a0f08] select-none transition-opacity duration-700 ease-out ${
        fadingOut ? 'opacity-0 pointer-events-none' : 'opacity-100'
      }`}
      aria-label="Welcome to KhetGPT Intro"
    >
      {/* 3D WebGL Canvas Container */}
      <div ref={mountRef} className="absolute inset-0 w-full h-full" />

      {/* Atmospheric Golden Dawn Sun Horizon Glow in Upper Center */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_50%_35%,rgba(245,158,11,0.25)_0%,rgba(16,185,129,0.12)_45%,transparent_70%)]" />

      {/* Unobtrusive "Skip Intro" Button in Top Right */}
      <div className="absolute top-4 right-4 sm:top-6 sm:right-6 z-20">
        <button
          onClick={handleFinish}
          className="flex items-center space-x-1.5 px-3.5 py-1.5 sm:px-4 sm:py-2 rounded-full bg-black/50 hover:bg-black/75 active:scale-95 backdrop-blur-md border border-white/20 text-white/90 hover:text-white transition-all text-xs sm:text-sm font-medium cursor-pointer shadow-xl"
          title="Skip Intro"
        >
          <span>Skip Intro</span>
        </button>
      </div>

      {/* SCENE 4: Welcome Text (Positioned ABOVE the growing plant with smooth fade-in and upward glide) */}
      <div
        className={`absolute top-12 sm:top-16 md:top-20 left-0 right-0 px-4 text-center pointer-events-none transition-all duration-1000 ease-out transform ${
          showWelcome ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
        }`}
      >
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/30 backdrop-blur-md mb-2 sm:mb-3 shadow-lg shadow-emerald-950/50">
          <Sprout className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-400 animate-pulse" />
          <span className="text-[10px] sm:text-xs uppercase tracking-widest text-emerald-300 font-bold">
            Smart Agriculture AI
          </span>
        </div>

        {/* EXACT REQUIRED TEXT: Welcome to KhetGPT */}
        <h1 className="text-3xl sm:text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-100 via-green-50 to-amber-100 tracking-tight drop-shadow-[0_4px_20px_rgba(0,0,0,0.9)] font-sans">
          Welcome to KhetGPT
        </h1>

        <p className="text-xs sm:text-base font-medium text-emerald-200/90 mt-1 sm:mt-2 max-w-md mx-auto tracking-wide drop-shadow">
          Growing Smarter Farming with AI
        </p>
      </div>
    </div>
  );
};
