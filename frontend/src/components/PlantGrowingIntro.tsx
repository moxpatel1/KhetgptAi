import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { Sprout } from 'lucide-react';
import { type Language } from '../i18n/translations';

interface PlantGrowingIntroProps {
  onComplete: () => void;
  language: Language;
}

export const PlantGrowingIntro: React.FC<PlantGrowingIntroProps> = ({ onComplete, language }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [fadingOut, setFadingOut] = useState(false);
  const [showBrand, setShowBrand] = useState(false);
  const isFinishedRef = useRef(false);

  const taglines = {
    gu: {
      brand: 'KhetGPT',
      tagline: 'AI વડે સ્માર્ટ ખેતીનો ઉદય',
      skip: 'Skip ✕',
    },
    hi: {
      brand: 'KhetGPT',
      tagline: 'AI से स्मार्ट खेती का नया सवेरा',
      skip: 'Skip ✕',
    },
    en: {
      brand: 'KhetGPT',
      tagline: 'Growing Smarter Farming with AI',
      skip: 'Skip ✕',
    },
  }[language];

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
    }, 5500);

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
      // Graceful instant fallback to homepage
      clearTimeout(safetyTimer);
      onComplete();
      return;
    }

    // ---------------- THREE.JS CINEMATIC 3D SCENE ----------------
    let width = container.clientWidth || window.innerWidth;
    let height = container.clientHeight || window.innerHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0c0906); // Dark fertile loam background

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 50);
    // Camera positioned at cross-section level
    camera.position.set(0, 0.15, 2.5);

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
    renderer.toneMappingExposure = 1.1;
    container.appendChild(renderer.domElement);

    // ---------------- LIGHTING ----------------
    // 1. Soft atmospheric dawn ambient light
    const ambientLight = new THREE.AmbientLight(0xfef3c7, 0.6);
    scene.add(ambientLight);

    // 2. Rising Golden Sunlight (Directional beam illuminating sprout)
    const sunLight = new THREE.DirectionalLight(0xfff7ed, 0.2);
    sunLight.position.set(3.5, 6.0, 3.0);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    scene.add(sunLight);

    // 3. Gentle Backlight for translucent green leaf radiance
    const backGlow = new THREE.PointLight(0x86efac, 0.1, 5);
    backGlow.position.set(0, 0.8, -0.6);
    scene.add(backGlow);

    // ---------------- SOIL SURFACE & UNDERGROUND CROSS-SECTION ----------------
    // Top Soil Surface Plane (y = 0.0)
    const soilTopGeo = new THREE.PlaneGeometry(8, 6, 24, 24);
    const topPos = soilTopGeo.attributes.position;
    for (let i = 0; i < topPos.count; i++) {
      const x = topPos.getX(i);
      const y = topPos.getY(i);
      // Subtle earthy furrow undulations
      topPos.setZ(i, Math.sin(x * 4.0) * 0.04 + Math.cos(y * 3.0) * 0.03);
    }
    soilTopGeo.computeVertexNormals();

    const soilTopMat = new THREE.MeshStandardMaterial({
      color: 0x271910, // Dark rich humus soil
      roughness: 0.95,
      metalness: 0.02,
      flatShading: true,
    });
    const soilTop = new THREE.Mesh(soilTopGeo, soilTopMat);
    soilTop.rotation.x = -Math.PI / 2.2;
    soilTop.position.set(0, 0.0, -0.2);
    soilTop.receiveShadow = true;
    scene.add(soilTop);

    // Subterranean Soil Cross-Section (shows seed and root bed below y = 0.0)
    const soilBedGeo = new THREE.PlaneGeometry(8, 3.5, 12, 12);
    const soilBedMat = new THREE.MeshStandardMaterial({
      color: 0x1a110a, // Deep moist earth below surface
      roughness: 0.98,
      metalness: 0.0,
    });
    const soilBed = new THREE.Mesh(soilBedGeo, soilBedMat);
    soilBed.position.set(0, -1.0, -0.3);
    scene.add(soilBed);

    // Soil particles / crumbs around germination point
    const crumbGroup = new THREE.Group();
    const crumbGeo = new THREE.DodecahedronGeometry(0.025, 0);
    const crumbMat = new THREE.MeshStandardMaterial({ color: 0x3b2416, roughness: 0.9 });
    for (let i = 0; i < 28; i++) {
      const crumb = new THREE.Mesh(crumbGeo, crumbMat);
      const angle = Math.random() * Math.PI * 2;
      const r = 0.06 + Math.random() * 0.5;
      crumb.position.set(Math.cos(angle) * r, 0.01 + Math.random() * 0.03, Math.sin(angle) * r * 0.6);
      const s = 0.5 + Math.random() * 0.8;
      crumb.scale.set(s, s * 0.7, s);
      crumbGroup.add(crumb);
    }
    scene.add(crumbGroup);

    // ---------------- 1. THE SEED ----------------
    // Planted beneath the soil at y = -0.25
    const seedGroup = new THREE.Group();
    seedGroup.position.set(0, -0.25, 0.02);

    const seedGeo = new THREE.SphereGeometry(0.065, 16, 16);
    seedGeo.scale(1.1, 1.45, 0.85); // Natural oval seed bean
    const seedMat = new THREE.MeshStandardMaterial({
      color: 0x4a2e1b, // Natural seed coat
      roughness: 0.65,
      metalness: 0.08,
    });
    const seedMesh = new THREE.Mesh(seedGeo, seedMat);
    seedMesh.castShadow = true;
    seedGroup.add(seedMesh);
    scene.add(seedGroup);

    // ---------------- 2. ROOT SYSTEM (GROWING DOWNWARD) ----------------
    const rootMat = new THREE.MeshStandardMaterial({
      color: 0xf5f0e1, // Translucent ivory-white rootlet
      roughness: 0.45,
      transparent: true,
      opacity: 0.9,
    });
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // Primary taproot & lateral branch curves
    const rootSplines = [
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, -0.32, 0.02),
        new THREE.Vector3(0.02, -0.5, 0.01),
        new THREE.Vector3(-0.03, -0.72, 0.0),
        new THREE.Vector3(0.02, -0.98, -0.01),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.01, -0.44, 0.01),
        new THREE.Vector3(-0.12, -0.62, -0.04),
        new THREE.Vector3(-0.2, -0.82, -0.06),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0.01, -0.48, 0.01),
        new THREE.Vector3(0.14, -0.66, 0.03),
        new THREE.Vector3(0.22, -0.88, 0.05),
      ]),
    ];

    // ---------------- 3. SPROUT STEM (GROWING UPWARD) ----------------
    const stemSpline = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, -0.25, 0.02),
      new THREE.Vector3(0.01, -0.05, 0.01),
      new THREE.Vector3(0.04, 0.22, 0.0),
      new THREE.Vector3(-0.03, 0.55, 0.02),
      new THREE.Vector3(0.01, 0.92, 0.0),
    ]);

    const stemMat = new THREE.MeshStandardMaterial({
      color: 0x4ade80, // Fresh tender green
      roughness: 0.35,
      metalness: 0.04,
    });
    let stemMesh: THREE.Mesh | null = null;

    // ---------------- 4. LEAVES (UNFURLING & SWAYING) ----------------
    const leafShape = new THREE.Shape();
    leafShape.moveTo(0, 0);
    leafShape.bezierCurveTo(0.14, 0.08, 0.22, 0.26, 0.0, 0.52); // Right side
    leafShape.bezierCurveTo(-0.22, 0.26, -0.14, 0.08, 0, 0);    // Left side

    const leafGeo = new THREE.ExtrudeGeometry(leafShape, {
      depth: 0.006,
      bevelEnabled: true,
      bevelSegments: 2,
      steps: 1,
      bevelSize: 0.003,
      bevelThickness: 0.003,
    });
    // Natural concave leaf curve
    const leafPos = leafGeo.attributes.position;
    for (let i = 0; i < leafPos.count; i++) {
      const y = leafPos.getY(i);
      const x = leafPos.getX(i);
      const dip = Math.sin((y / 0.52) * Math.PI) * 0.045 - Math.abs(x) * 0.03;
      leafPos.setZ(i, leafPos.getZ(i) + dip);
    }
    leafGeo.computeVertexNormals();

    const leafMat = new THREE.MeshStandardMaterial({
      color: 0x22c55e, // Radiant emerald leaf
      roughness: 0.28,
      metalness: 0.05,
      side: THREE.DoubleSide,
    });

    const leafGroup = new THREE.Group();
    leafGroup.scale.set(0, 0, 0);

    const leftLeaf = new THREE.Mesh(leafGeo, leafMat);
    leftLeaf.castShadow = true;
    leftLeaf.rotation.set(0.25, 0.4, -0.6);

    const rightLeaf = new THREE.Mesh(leafGeo, leafMat);
    rightLeaf.castShadow = true;
    rightLeaf.rotation.set(0.25, -0.4, 0.6);

    leafGroup.add(leftLeaf);
    leafGroup.add(rightLeaf);
    scene.add(leafGroup);

    // ---------------- 5. ATMOSPHERIC GOLDEN PARTICLES ----------------
    const particleCount = width < 768 ? 45 : 90;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleSpeeds: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 2.8;
      particlePositions[i * 3 + 1] = -0.2 + Math.random() * 1.8;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 1.8;
      particleSpeeds.push(0.0015 + Math.random() * 0.003);
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xfef08a, // Soft golden morning light
      size: width < 768 ? 0.03 : 0.04,
      transparent: true,
      opacity: 0.0,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // ---------------- ANIMATION LOOP (TIMELINE: 0 to 4.2s) ----------------
    let startTime: number | null = null;
    let animationFrameId: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000; // in seconds

      // 1. Stage 0.0s - 0.8s: Soil & Seed Swell
      if (elapsed <= 1.0) {
        const swell = Math.min(1.0, elapsed / 0.8);
        seedGroup.scale.setScalar(1.0 + swell * 0.15);
        sunLight.intensity = THREE.MathUtils.lerp(0.2, 0.8, swell);
      }

      // 2. Stage 0.6s - 2.2s: Roots Sprout & Drive Downward into Soil
      if (elapsed >= 0.6 && elapsed <= 2.4) {
        const rootProgress = THREE.MathUtils.smoothstep(elapsed, 0.6, 2.2);
        rootGroup.clear();

        rootSplines.forEach((spline) => {
          const ptCount = Math.max(2, Math.floor(rootProgress * 16));
          const subPts: THREE.Vector3[] = [];
          for (let p = 0; p <= ptCount; p++) {
            subPts.push(spline.getPoint((p / 16) * rootProgress));
          }
          if (subPts.length >= 2) {
            const curve = new THREE.CatmullRomCurve3(subPts);
            const tubeGeo = new THREE.TubeGeometry(curve, 16, 0.014, 6, false);
            const rMesh = new THREE.Mesh(tubeGeo, rootMat);
            rootGroup.add(rMesh);
          }
        });
      }

      // 3. Stage 1.4s - 3.2s: Shoot Emerges from Soil & Grows Upward
      if (elapsed >= 1.2 && elapsed <= 3.8) {
        const stemProgress = THREE.MathUtils.smoothstep(elapsed, 1.2, 3.2);
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
          const stemGeo = new THREE.TubeGeometry(activeCurve, 28, 0.03, 8, false);
          stemMesh = new THREE.Mesh(stemGeo, stemMat);
          stemMesh.castShadow = true;
          scene.add(stemMesh);

          // Track growing tip for leaves
          const tip = activePts[activePts.length - 1];
          leafGroup.position.copy(tip);
        }
      }

      // 4. Stage 2.5s - 3.8s: Leaves Unfurl in Morning Sun & Sway
      if (elapsed >= 2.4) {
        const leafProgress = THREE.MathUtils.smoothstep(elapsed, 2.4, 3.6);
        leafGroup.scale.setScalar(leafProgress);

        // Leaves gently unfolding open
        leftLeaf.rotation.z = THREE.MathUtils.lerp(-1.1, -0.45, leafProgress);
        rightLeaf.rotation.z = THREE.MathUtils.lerp(1.1, 0.45, leafProgress);

        // Subtle wind breeze sway once opened
        if (elapsed > 3.4) {
          const sway = Math.sin((elapsed - 3.4) * 3.5) * 0.035;
          leafGroup.rotation.z = sway;
        }

        // Sunlight radiance blooms
        sunLight.intensity = THREE.MathUtils.lerp(0.8, 2.2, leafProgress);
        backGlow.intensity = THREE.MathUtils.lerp(0.1, 1.2, leafProgress);
        particleMat.opacity = THREE.MathUtils.lerp(0.0, 0.75, leafProgress);
      }

      // 5. Golden Pollen Movement
      const pArr = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        pArr[i * 3 + 1] += particleSpeeds[i];
        if (pArr[i * 3 + 1] > 2.0) {
          pArr[i * 3 + 1] = 0.0;
        }
      }
      particleGeo.attributes.position.needsUpdate = true;

      // 6. Camera Glides Upward (Focusing from Soil to Blooming Plant)
      const camProgress = THREE.MathUtils.smoothstep(elapsed, 0.5, 3.6);
      camera.position.y = THREE.MathUtils.lerp(0.08, 0.48, camProgress);
      camera.position.z = THREE.MathUtils.lerp(2.4, 2.6, camProgress);
      camera.lookAt(0, THREE.MathUtils.lerp(-0.1, 0.38, camProgress), 0);

      // 7. Brand Reveal at 3.2s
      if (elapsed >= 3.2 && !showBrand) {
        setShowBrand(true);
      }

      // 8. Auto Transition to Homepage at 4.2s
      if (elapsed >= 4.2 && !isFinishedRef.current) {
        handleFinish();
        return;
      }

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      width = container.clientWidth || window.innerWidth;
      height = container.clientHeight || window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup on unmount
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
  }, [handleFinish, onComplete, showBrand]);

  return (
    <div
      className={`fixed inset-0 z-50 overflow-hidden bg-slate-950 select-none transition-opacity duration-700 ease-out ${
        fadingOut ? 'opacity-0 pointer-events-none' : 'opacity-100'
      }`}
      aria-label="KhetGPT Loading Animation"
    >
      {/* 3D WebGL Canvas Container */}
      <div ref={mountRef} className="absolute inset-0 w-full h-full" />

      {/* Subtle Golden Dawn Sky Glow in Top Horizon */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_70%_25%,rgba(251,191,36,0.18)_0%,transparent_60%)]" />

      {/* Unobtrusive Skip Button in Top Right */}
      <div className="absolute top-4 right-4 sm:top-6 sm:right-6 z-10">
        <button
          onClick={handleFinish}
          className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full bg-black/40 hover:bg-black/60 backdrop-blur-md border border-white/10 text-white/70 hover:text-white transition-all text-xs font-medium cursor-pointer"
        >
          <span>{taglines.skip}</span>
        </button>
      </div>

      {/* Cinematic Brand Reveal (Floats in as plant finishes blooming) */}
      <div
        className={`absolute bottom-8 sm:bottom-12 left-0 right-0 px-4 text-center pointer-events-none transition-all duration-700 transform ${
          showBrand ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
        }`}
      >
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-400/20 backdrop-blur-md mb-2">
          <Sprout className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span className="text-xs uppercase tracking-wider text-emerald-300 font-semibold">KhetGPT AI</span>
        </div>

        <h1 className="text-2xl sm:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-200 via-green-100 to-amber-200 tracking-tight drop-shadow">
          {taglines.brand}
        </h1>

        <p className="text-sm sm:text-base font-medium text-emerald-100/90 mt-1 max-w-md mx-auto">
          {taglines.tagline}
        </p>

        {/* Minimalist Progress Indicator */}
        <div className="w-24 h-0.5 bg-white/10 rounded-full mx-auto mt-3 overflow-hidden">
          <div className="w-full h-full bg-gradient-to-r from-emerald-400 to-amber-300 animate-[pulse_1.5s_ease-in-out_infinite]" />
        </div>
      </div>
    </div>
  );
};

