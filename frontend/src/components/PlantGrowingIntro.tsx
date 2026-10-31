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
    // Accessibility check: Skip immediately if user prefers reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      onComplete();
      return;
    }

    const container = mountRef.current;
    if (!container) return;

    // Safety fallback timer: Ensure homepage is NEVER blocked under any circumstance
    const safetyTimer = setTimeout(() => {
      if (!isFinishedRef.current) {
        handleFinish();
      }
    }, 6200);

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

    // ---------------- THREE.JS CINEMATIC 3D SCENE ----------------
    let width = container.clientWidth || window.innerWidth;
    let height = container.clientHeight || window.innerHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0705); // Rich deep dark agricultural loam background

    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 50);
    // Position camera focused slightly low near soil level initially
    camera.position.set(0, 0.12, 2.5);

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
    renderer.toneMappingExposure = 1.15;
    container.appendChild(renderer.domElement);

    // ---------------- LIGHTING (SCENE 1: SOFT DAWN TO GOLDEN SUN) ----------------
    // 1. Soft atmospheric dawn ambient light
    const ambientLight = new THREE.AmbientLight(0xfef3c7, 0.55);
    scene.add(ambientLight);

    // 2. Rising Golden Sunlight (Directional beam illuminating sprout & leaves)
    const sunLight = new THREE.DirectionalLight(0xffedd5, 0.25);
    sunLight.position.set(3.2, 5.5, 2.8);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    scene.add(sunLight);

    // 3. Gentle Backlight for translucent green leaf radiance
    const leafBackGlow = new THREE.PointLight(0x86efac, 0.1, 4);
    leafBackGlow.position.set(0, 0.7, -0.5);
    scene.add(leafBackGlow);

    // ---------------- SCENE 1: FERTILE SOIL & UNDERGROUND CROSS-SECTION ----------------
    // Top Soil Surface Plane (y = 0.0)
    const soilTopGeo = new THREE.PlaneGeometry(9, 6.5, 28, 28);
    const topPos = soilTopGeo.attributes.position;
    for (let i = 0; i < topPos.count; i++) {
      const x = topPos.getX(i);
      const y = topPos.getY(i);
      // Realistic earthy furrow undulations and organic irregularities
      topPos.setZ(i, Math.sin(x * 3.8) * 0.045 + Math.cos(y * 3.2) * 0.035 + (Math.random() - 0.5) * 0.012);
    }
    soilTopGeo.computeVertexNormals();

    const soilTopMat = new THREE.MeshStandardMaterial({
      color: 0x26170d, // Dark rich humus agricultural soil
      roughness: 0.96,
      metalness: 0.01,
      flatShading: true,
    });
    const soilTop = new THREE.Mesh(soilTopGeo, soilTopMat);
    soilTop.rotation.x = -Math.PI / 2.22;
    soilTop.position.set(0, 0.0, -0.2);
    soilTop.receiveShadow = true;
    scene.add(soilTop);

    // Subterranean Soil Cross-Section (shows seed and roots below surface y < 0)
    const soilBedGeo = new THREE.PlaneGeometry(9, 3.8, 14, 14);
    const soilBedMat = new THREE.MeshStandardMaterial({
      color: 0x160e08, // Moist deep earth below surface
      roughness: 0.98,
      metalness: 0.0,
    });
    const soilBed = new THREE.Mesh(soilBedGeo, soilBedMat);
    soilBed.position.set(0, -1.1, -0.32);
    scene.add(soilBed);

    // Realistic soil particles / crumbs clustered around the emergence point
    const crumbGroup = new THREE.Group();
    const crumbGeo = new THREE.DodecahedronGeometry(0.024, 0);
    const crumbMat = new THREE.MeshStandardMaterial({ color: 0x3d2415, roughness: 0.92 });
    const crumbMeshes: { mesh: THREE.Mesh; basePos: THREE.Vector3 }[] = [];
    for (let i = 0; i < 32; i++) {
      const crumb = new THREE.Mesh(crumbGeo, crumbMat);
      const angle = Math.random() * Math.PI * 2;
      const r = 0.05 + Math.random() * 0.48;
      const x = Math.cos(angle) * r;
      const z = Math.sin(angle) * r * 0.65;
      const y = 0.01 + Math.random() * 0.03;
      crumb.position.set(x, y, z);
      const s = 0.4 + Math.random() * 0.8;
      crumb.scale.set(s, s * 0.75, s);
      crumb.castShadow = true;
      crumbGroup.add(crumb);
      crumbMeshes.push({ mesh: crumb, basePos: new THREE.Vector3(x, y, z) });
    }
    scene.add(crumbGroup);

    // ---------------- SCENE 2: THE SEED & GERMINATION ----------------
    // Planted beneath the soil at y = -0.28
    const seedGroup = new THREE.Group();
    seedGroup.position.set(0, -0.28, 0.02);

    // Two cotyledon halves of the seed that can crack open
    const cotyledonGeo = new THREE.SphereGeometry(0.062, 16, 16);
    cotyledonGeo.scale(0.65, 1.35, 0.85);
    const seedMat = new THREE.MeshStandardMaterial({
      color: 0x4a2c18, // Natural seed coat brown
      roughness: 0.65,
      metalness: 0.06,
    });

    const seedLeft = new THREE.Mesh(cotyledonGeo, seedMat);
    seedLeft.position.set(-0.02, 0, 0);
    seedLeft.castShadow = true;
    seedGroup.add(seedLeft);

    const seedRight = new THREE.Mesh(cotyledonGeo, seedMat);
    seedRight.position.set(0.02, 0, 0);
    seedRight.castShadow = true;
    seedGroup.add(seedRight);

    scene.add(seedGroup);

    // Roots growing downward into soil
    const rootMat = new THREE.MeshStandardMaterial({
      color: 0xfaf5ea, // Tender ivory-white rootlet
      roughness: 0.45,
      transparent: true,
      opacity: 0.92,
    });
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // Main taproot & fine lateral branches
    const rootSplines = [
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, -0.34, 0.02),
        new THREE.Vector3(0.02, -0.52, 0.01),
        new THREE.Vector3(-0.03, -0.75, 0.0),
        new THREE.Vector3(0.02, -1.02, -0.01),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.01, -0.46, 0.01),
        new THREE.Vector3(-0.13, -0.65, -0.04),
        new THREE.Vector3(-0.22, -0.85, -0.05),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0.01, -0.50, 0.01),
        new THREE.Vector3(0.15, -0.68, 0.03),
        new THREE.Vector3(0.24, -0.92, 0.04),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.02, -0.62, 0.0),
        new THREE.Vector3(-0.08, -0.76, 0.02),
        new THREE.Vector3(-0.14, -0.95, 0.01),
      ]),
    ];

    // ---------------- SCENE 3: SPROUT STEM & LEAF EMERGENCE ----------------
    const stemSpline = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, -0.28, 0.02),
      new THREE.Vector3(0.01, -0.04, 0.01),
      new THREE.Vector3(0.035, 0.22, 0.0),
      new THREE.Vector3(-0.025, 0.52, 0.015),
      new THREE.Vector3(0.01, 0.88, 0.0),
    ]);

    const stemMat = new THREE.MeshStandardMaterial({
      color: 0x4ade80, // Fresh tender green
      roughness: 0.35,
      metalness: 0.04,
    });
    let stemMesh: THREE.Mesh | null = null;

    // Organic Leaf Shape
    const leafShape = new THREE.Shape();
    leafShape.moveTo(0, 0);
    leafShape.bezierCurveTo(0.15, 0.09, 0.23, 0.27, 0.0, 0.54); // Right contour
    leafShape.bezierCurveTo(-0.23, 0.27, -0.15, 0.09, 0, 0);    // Left contour

    const leafGeo = new THREE.ExtrudeGeometry(leafShape, {
      depth: 0.007,
      bevelEnabled: true,
      bevelSegments: 2,
      steps: 1,
      bevelSize: 0.003,
      bevelThickness: 0.003,
    });
    // Add natural leaf curve/dish curvature
    const leafPos = leafGeo.attributes.position;
    for (let i = 0; i < leafPos.count; i++) {
      const y = leafPos.getY(i);
      const x = leafPos.getX(i);
      const dip = Math.sin((y / 0.54) * Math.PI) * 0.048 - Math.abs(x) * 0.032;
      leafPos.setZ(i, leafPos.getZ(i) + dip);
    }
    leafGeo.computeVertexNormals();

    const leafMat = new THREE.MeshStandardMaterial({
      color: 0x22c55e, // Radiant agricultural green
      roughness: 0.26,
      metalness: 0.04,
      side: THREE.DoubleSide,
    });

    const leafGroup = new THREE.Group();
    leafGroup.scale.set(0, 0, 0);

    // Left leaf
    const leftLeaf = new THREE.Mesh(leafGeo, leafMat);
    leftLeaf.castShadow = true;
    leftLeaf.rotation.set(0.25, 0.4, -0.6);
    leafGroup.add(leftLeaf);

    // Right leaf (opens slightly after left leaf)
    const rightLeaf = new THREE.Mesh(leafGeo, leafMat);
    rightLeaf.castShadow = true;
    rightLeaf.rotation.set(0.25, -0.4, 0.6);
    leafGroup.add(rightLeaf);

    scene.add(leafGroup);

    // ---------------- ATMOSPHERIC FLOATING PARTICLES (GOLDEN MORNING DUST) ----------------
    const particleCount = width < 768 ? 48 : 88;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleSpeeds: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 3.0;
      particlePositions[i * 3 + 1] = -0.3 + Math.random() * 2.0;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 2.0;
      particleSpeeds.push(0.0014 + Math.random() * 0.0028);
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xfef08a, // Soft morning sunlight dust
      size: width < 768 ? 0.032 : 0.042,
      transparent: true,
      opacity: 0.0,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // ---------------- ANIMATION TIMELINE (0.0s to 5.0s) ----------------
    let startTime: number | null = null;
    let animationFrameId: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000; // in seconds

      // SCENE 1: Soil Close-Up & Seed Moisture Swell (0.0s - 1.0s)
      if (elapsed <= 1.2) {
        const swell = Math.min(1.0, elapsed / 0.9);
        seedGroup.scale.setScalar(1.0 + swell * 0.18);
        sunLight.intensity = THREE.MathUtils.lerp(0.25, 0.75, swell);
      }

      // SCENE 2: Seed Opens & Roots Sprout Downward (0.6s - 2.4s)
      if (elapsed >= 0.6) {
        // Cotyledons split open slightly as root & shoot emerge
        const split = THREE.MathUtils.smoothstep(elapsed, 0.6, 1.8) * 0.035;
        seedLeft.position.x = -0.02 - split;
        seedLeft.rotation.z = split * 3.0;
        seedRight.position.x = 0.02 + split;
        seedRight.rotation.z = -split * 3.0;
      }

      if (elapsed >= 0.6 && elapsed <= 2.6) {
        const rootProgress = THREE.MathUtils.smoothstep(elapsed, 0.6, 2.3);
        rootGroup.clear();

        rootSplines.forEach((spline) => {
          const ptCount = Math.max(2, Math.floor(rootProgress * 16));
          const subPts: THREE.Vector3[] = [];
          for (let p = 0; p <= ptCount; p++) {
            subPts.push(spline.getPoint((p / 16) * rootProgress));
          }
          if (subPts.length >= 2) {
            const curve = new THREE.CatmullRomCurve3(subPts);
            const tubeGeo = new THREE.TubeGeometry(curve, 16, 0.013, 6, false);
            const rMesh = new THREE.Mesh(tubeGeo, rootMat);
            rootGroup.add(rMesh);
          }
        });
      }

      // SCENE 3: Shoot Emerges, Soil Reacts, Stem Grows (1.2s - 3.4s)
      if (elapsed >= 1.2 && elapsed <= 4.0) {
        const stemProgress = THREE.MathUtils.smoothstep(elapsed, 1.2, 3.3);
        if (stemMesh) {
          scene.remove(stemMesh);
          stemMesh.geometry.dispose();
        }

        const stemCount = Math.max(3, Math.floor(stemProgress * 28));
        const activePts: THREE.Vector3[] = [];
        for (let i = 0; i <= stemCount; i++) {
          activePts.push(stemSpline.getPoint((i / 28) * stemProgress));
        }

        if (activePts.length >= 2) {
          const activeCurve = new THREE.CatmullRomCurve3(activePts);
          const stemGeo = new THREE.TubeGeometry(activeCurve, 28, 0.028, 8, false);
          stemMesh = new THREE.Mesh(stemGeo, stemMat);
          stemMesh.castShadow = true;
          scene.add(stemMesh);

          // Position leaves at growing shoot tip
          const tip = activePts[activePts.length - 1];
          leafGroup.position.copy(tip);
        }

        // Soil reaction: Crumbs lift and displace slightly around y=0 as shoot breaches surface
        if (elapsed >= 1.4 && elapsed <= 2.5) {
          const breachProgress = THREE.MathUtils.smoothstep(elapsed, 1.4, 2.2);
          crumbMeshes.forEach(({ mesh, basePos }) => {
            const dist = Math.sqrt(basePos.x * basePos.x + basePos.z * basePos.z);
            if (dist < 0.22) {
              const push = (0.22 - dist) * 0.45 * breachProgress;
              mesh.position.y = basePos.y + push;
              mesh.rotation.x = push * 4.0;
            }
          });
        }
      }

      // SCENE 3 cont: Leaves Unfold One by One & Sway in Morning Breeze (2.4s - 4.6s)
      if (elapsed >= 2.4) {
        const overallLeafProgress = THREE.MathUtils.smoothstep(elapsed, 2.4, 3.6);
        leafGroup.scale.setScalar(overallLeafProgress);

        // Left leaf unfolds first (2.4s to 3.3s)
        const leftProgress = THREE.MathUtils.smoothstep(elapsed, 2.4, 3.3);
        leftLeaf.rotation.z = THREE.MathUtils.lerp(-1.15, -0.42, leftProgress);
        leftLeaf.scale.setScalar(THREE.MathUtils.lerp(0.2, 1.0, leftProgress));

        // Right leaf unfolds slightly after (2.7s to 3.6s)
        const rightProgress = THREE.MathUtils.smoothstep(elapsed, 2.7, 3.6);
        rightLeaf.rotation.z = THREE.MathUtils.lerp(1.15, 0.42, rightProgress);
        rightLeaf.scale.setScalar(THREE.MathUtils.lerp(0.2, 1.0, rightProgress));

        // Gentle organic wind breeze once plant has emerged
        if (elapsed > 3.2) {
          const sway = Math.sin((elapsed - 3.2) * 3.2) * 0.038;
          leafGroup.rotation.z = sway;
          leafGroup.rotation.x = Math.cos((elapsed - 3.2) * 2.8) * 0.02;
        }

        // Golden sunlight warms and illuminates the growing plant
        sunLight.intensity = THREE.MathUtils.lerp(0.75, 2.3, overallLeafProgress);
        leafBackGlow.intensity = THREE.MathUtils.lerp(0.1, 1.35, overallLeafProgress);
        particleMat.opacity = THREE.MathUtils.lerp(0.0, 0.85, overallLeafProgress);
      }

      // Floating golden morning dust movement
      const pArr = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        pArr[i * 3 + 1] += particleSpeeds[i];
        if (pArr[i * 3 + 1] > 2.2) {
          pArr[i * 3 + 1] = -0.1;
        }
      }
      particleGeo.attributes.position.needsUpdate = true;

      // Camera glides smoothly upward to focus on the growing plant
      const camProgress = THREE.MathUtils.smoothstep(elapsed, 0.4, 3.5);
      camera.position.y = THREE.MathUtils.lerp(0.08, 0.38, camProgress);
      camera.position.z = THREE.MathUtils.lerp(2.4, 2.5, camProgress);
      camera.lookAt(0, THREE.MathUtils.lerp(-0.1, 0.32, camProgress), 0);

      // SCENE 4: Welcome Text Appearance (Triggered at 2.8s as plant unfurls)
      if (elapsed >= 2.8 && !showWelcome) {
        setShowWelcome(true);
      }

      // SCENE 5: Transition to Homepage (At ~4.8s, smoothly fade into homepage)
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
      className={`fixed inset-0 z-50 overflow-hidden bg-[#0a0705] select-none transition-opacity duration-700 ease-out ${
        fadingOut ? 'opacity-0 pointer-events-none' : 'opacity-100'
      }`}
      aria-label="Welcome to KhetGPT Intro"
    >
      {/* 3D WebGL Canvas Container */}
      <div ref={mountRef} className="absolute inset-0 w-full h-full" />

      {/* Atmospheric Golden Morning Dawn Radial Glow in Upper Sky */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_65%_20%,rgba(251,191,36,0.22)_0%,transparent_65%)]" />

      {/* Unobtrusive "Skip Intro" Button in Top Right */}
      <div className="absolute top-4 right-4 sm:top-6 sm:right-6 z-20">
        <button
          onClick={handleFinish}
          className="flex items-center space-x-1.5 px-3.5 py-1.5 sm:px-4 sm:py-2 rounded-full bg-black/45 hover:bg-black/65 active:scale-95 backdrop-blur-md border border-white/15 text-white/80 hover:text-white transition-all text-xs sm:text-sm font-medium cursor-pointer shadow-lg"
          title="Skip Intro"
        >
          <span>Skip Intro</span>
        </button>
      </div>

      {/* SCENE 4: Welcome Text (Positioned ABOVE the growing plant with smooth fade-in and upward glide) */}
      <div
        className={`absolute top-14 sm:top-18 md:top-22 left-0 right-0 px-4 text-center pointer-events-none transition-all duration-1000 ease-out transform ${
          showWelcome ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
        }`}
      >
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-400/25 backdrop-blur-md mb-2 sm:mb-3 shadow-lg shadow-emerald-950/40">
          <Sprout className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-400 animate-pulse" />
          <span className="text-[10px] sm:text-xs uppercase tracking-widest text-emerald-300 font-bold">
            Smart Agriculture AI
          </span>
        </div>

        {/* EXACT REQUIRED TEXT: Welcome to KhetGPT */}
        <h1 className="text-3xl sm:text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-100 via-green-50 to-amber-100 tracking-tight drop-shadow-[0_4px_18px_rgba(0,0,0,0.85)] font-sans">
          Welcome to KhetGPT
        </h1>

        <p className="text-xs sm:text-base font-medium text-emerald-200/90 mt-1.5 sm:mt-2 max-w-md mx-auto tracking-wide drop-shadow">
          Growing Smarter Farming with AI
        </p>
      </div>
    </div>
  );
};
