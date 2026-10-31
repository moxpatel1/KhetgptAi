import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { Sprout, Volume2, VolumeX } from 'lucide-react';
import { type Language } from '../i18n/translations';

interface IntroAnimationProps {
  onComplete: () => void;
  language: Language;
}

export const IntroAnimation: React.FC<IntroAnimationProps> = ({ onComplete, language }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [skipFade, setSkipFade] = useState(false);
  const [showBrand, setShowBrand] = useState(false);
  const [webglSupported, setWebglSupported] = useState(true);
  const [ambientSound, setAmbientSound] = useState(false);
  const audioCtxRef = useRef<AudioContext | null>(null);

  // Localized taglines
  const taglines = {
    gu: {
      brand: 'KhetGPT',
      tagline: 'AI વડે સ્માર્ટ ખેતીનો ઉદય',
      sub: 'Growing Smarter Farming with AI',
      skip: 'મુખ્ય પેજ પર જાઓ (Skip)',
    },
    hi: {
      brand: 'KhetGPT',
      tagline: 'AI से स्मार्ट खेती का नया सवेरा',
      sub: 'Growing Smarter Farming with AI',
      skip: 'सीधे मुख्य पृष्ठ पर जाएं (Skip)',
    },
    en: {
      brand: 'KhetGPT',
      tagline: 'Growing Smarter Farming with AI',
      sub: 'Empowering Indian Agriculture through Generative AI & Vision',
      skip: 'Skip Intro',
    },
  }[language];

  // Optional subtle morning birds & breeze synthesis using Web Audio API (zero external audio file dependency!)
  const toggleAmbientSound = () => {
    if (!ambientSound) {
      try {
        const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        if (AudioContextClass) {
          const ctx = new AudioContextClass();
          audioCtxRef.current = ctx;

          // Pink noise breeze generator
          const bufferSize = ctx.sampleRate * 2;
          const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
          const output = noiseBuffer.getChannelData(0);
          let b0 = 0, b1 = 0, b2 = 0;
          for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            b0 = 0.99886 * b0 + white * 0.0555179;
            b1 = 0.99332 * b1 + white * 0.0750759;
            b2 = 0.96900 * b2 + white * 0.1538520;
            output[i] = (b0 + b1 + b2) * 0.04;
          }
          const whiteNoise = ctx.createBufferSource();
          whiteNoise.buffer = noiseBuffer;
          whiteNoise.loop = true;

          const filter = ctx.createBiquadFilter();
          filter.type = 'lowpass';
          filter.frequency.setValueAtTime(320, ctx.currentTime);

          const gain = ctx.createGain();
          gain.gain.setValueAtTime(0.01, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.3, ctx.currentTime + 2.0);

          whiteNoise.connect(filter);
          filter.connect(gain);
          gain.connect(ctx.destination);
          whiteNoise.start();
          setAmbientSound(true);
        }
      } catch {
        // Fallback silently if audio context is blocked by browser policy
      }
    } else {
      if (audioCtxRef.current) {
        audioCtxRef.current.close().catch(() => {});
        audioCtxRef.current = null;
      }
      setAmbientSound(false);
    }
  };

  const handleFinish = useCallback(() => {
    setSkipFade(true);
    if (audioCtxRef.current) {
      try {
        audioCtxRef.current.close().catch(() => {});
      } catch {
        // Ignore close error
      }
      audioCtxRef.current = null;
    }
    setTimeout(() => {
      onComplete();
    }, 600);
  }, [onComplete]);

  useEffect(() => {
    // Check reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const timer = setTimeout(() => {
        onComplete();
      }, 1500);
      return () => clearTimeout(timer);
    }

    const container = mountRef.current;
    if (!container) return;

    // Check WebGL availability
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (!gl) {
        setWebglSupported(false);
        const timer = setTimeout(onComplete, 2000);
        return () => clearTimeout(timer);
      }
    } catch {
      setWebglSupported(false);
      const timer = setTimeout(onComplete, 2000);
      return () => clearTimeout(timer);
    }

    // ---------------- THREE.JS INITIALIZATION ----------------
    let width = container.clientWidth || window.innerWidth;
    let height = container.clientHeight || window.innerHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0f0d); // Deep fertile twilight
    scene.fog = new THREE.FogExp2(0x0a0f0d, 0.22);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 50);
    // Initial camera position (ground-level perspective)
    camera.position.set(0, 0.35, 2.4);

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    container.appendChild(renderer.domElement);

    // ---------------- LIGHTING ----------------
    // 1. Ambient skylight (cool morning twilight)
    const ambientLight = new THREE.HemisphereLight(0x90caf9, 0x2e1e12, 0.85);
    scene.add(ambientLight);

    // 2. Rising Morning Sun (Warm Golden Directional beam)
    const sunLight = new THREE.DirectionalLight(0xffecd2, 0.1);
    sunLight.position.set(4.5, 7.5, 3.5);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.bias = -0.001;
    scene.add(sunLight);

    // 3. Subsurface Sprout Rim Light (creates glowing translucent leaf edges)
    const rimLight = new THREE.PointLight(0x81c784, 0.2, 6);
    rimLight.position.set(0, 1.2, -0.6);
    scene.add(rimLight);

    // ---------------- FERTILE SOIL BED ----------------
    // Create undulating soil surface
    const soilGeo = new THREE.PlaneGeometry(12, 12, 40, 40);
    const posAttr = soilGeo.attributes.position;
    for (let i = 0; i < posAttr.count; i++) {
      const x = posAttr.getX(i);
      const y = posAttr.getY(i);
      // Subtle organic furrow ridges
      const distFromCenter = Math.sqrt(x * x + y * y);
      const bump = Math.sin(x * 3.5) * 0.05 + Math.cos(y * 2.8) * 0.04 - Math.exp(-distFromCenter * 1.5) * 0.08;
      posAttr.setZ(i, bump);
    }
    soilGeo.computeVertexNormals();

    const soilMat = new THREE.MeshStandardMaterial({
      color: 0x231811, // Rich dark humus soil
      roughness: 0.94,
      metalness: 0.04,
      flatShading: true,
    });
    const soilMesh = new THREE.Mesh(soilGeo, soilMat);
    soilMesh.rotation.x = -Math.PI / 2;
    soilMesh.position.y = 0.0;
    soilMesh.receiveShadow = true;
    scene.add(soilMesh);

    // Soil crumbs/pebbles scattered around seed sprouting point
    const crumbGroup = new THREE.Group();
    const crumbGeo = new THREE.DodecahedronGeometry(0.04, 0);
    const crumbMat = new THREE.MeshStandardMaterial({
      color: 0x332014,
      roughness: 0.9,
    });
    for (let i = 0; i < 35; i++) {
      const crumb = new THREE.Mesh(crumbGeo, crumbMat);
      const angle = Math.random() * Math.PI * 2;
      const radius = 0.12 + Math.random() * 0.85;
      crumb.position.set(Math.cos(angle) * radius, 0.02 + Math.random() * 0.03, Math.sin(angle) * radius);
      const s = 0.4 + Math.random() * 0.9;
      crumb.scale.set(s, s * 0.7, s);
      crumb.rotation.set(Math.random(), Math.random(), Math.random());
      crumbGroup.add(crumb);
    }
    scene.add(crumbGroup);

    // ---------------- THE SEED ----------------
    // Bean/Seed resting right under soil surface
    const seedGroup = new THREE.Group();
    seedGroup.position.set(0, -0.06, 0);

    const seedGeo = new THREE.SphereGeometry(0.09, 16, 16);
    seedGeo.scale(1.2, 1.6, 0.85); // Natural oval seed shape
    const seedMat = new THREE.MeshStandardMaterial({
      color: 0x4a2e1b, // Organic seed coat
      roughness: 0.65,
      metalness: 0.1,
    });
    const seedMesh = new THREE.Mesh(seedGeo, seedMat);
    seedMesh.castShadow = true;
    seedGroup.add(seedMesh);
    scene.add(seedGroup);

    // ---------------- ROOT SYSTEM (DOWNWARD GROWTH) ----------------
    const rootMat = new THREE.MeshStandardMaterial({
      color: 0xeee8d5, // Pale ivory rootlet
      roughness: 0.5,
      transparent: true,
      opacity: 0.85,
    });
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // 3 procedural root curves extending into the soil
    const rootCurves = [
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, -0.15, 0),
        new THREE.Vector3(0.03, -0.35, 0.02),
        new THREE.Vector3(-0.02, -0.65, -0.03),
        new THREE.Vector3(0.05, -0.95, 0.01),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.02, -0.25, 0.01),
        new THREE.Vector3(-0.15, -0.45, -0.08),
        new THREE.Vector3(-0.25, -0.7, -0.12),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0.02, -0.3, -0.01),
        new THREE.Vector3(0.18, -0.52, 0.08),
        new THREE.Vector3(0.24, -0.78, 0.14),
      ]),
    ];
    let rootMeshes: THREE.Mesh[] = [];

    // ---------------- STEM & SPROUT (UPWARD GROWTH) ----------------
    const stemSpline = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, -0.1, 0),
      new THREE.Vector3(0.01, 0.08, 0.02),
      new THREE.Vector3(0.08, 0.42, -0.04),
      new THREE.Vector3(-0.05, 0.88, 0.03),
      new THREE.Vector3(0.02, 1.35, 0.0),
    ]);

    const stemMat = new THREE.MeshStandardMaterial({
      color: 0x43a047, // Fresh seedling green
      roughness: 0.38,
      metalness: 0.05,
    });
    let stemMesh: THREE.Mesh | null = null;

    // ---------------- LEAVES (UNFURLING & FLOURISHING) ----------------
    // Organic leaf geometry creation
    const createLeafGeometry = () => {
      const shape = new THREE.Shape();
      shape.moveTo(0, 0);
      shape.bezierCurveTo(0.18, 0.12, 0.28, 0.35, 0.0, 0.65); // Right leaf curved edge to apex
      shape.bezierCurveTo(-0.28, 0.35, -0.18, 0.12, 0, 0);   // Left leaf edge returning to petiole
      const geom = new THREE.ExtrudeGeometry(shape, {
        depth: 0.008,
        bevelEnabled: true,
        bevelSegments: 2,
        steps: 1,
        bevelSize: 0.004,
        bevelThickness: 0.004,
      });
      // Gently cup the leaf downwards like a real seedling cotyledon
      const pos = geom.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        const y = pos.getY(i);
        const x = pos.getX(i);
        const curveDown = Math.sin((y / 0.65) * Math.PI) * 0.06 - Math.abs(x) * 0.04;
        pos.setZ(i, pos.getZ(i) + curveDown);
      }
      geom.computeVertexNormals();
      return geom;
    };

    const leafMat = new THREE.MeshStandardMaterial({
      color: 0x2e7d32, // Vibrant emerald agricultural green
      roughness: 0.28,
      metalness: 0.08,
      side: THREE.DoubleSide,
    });

    const leafGroup = new THREE.Group();
    leafGroup.scale.set(0, 0, 0); // Initially hidden inside the bud

    const leafGeo1 = createLeafGeometry();
    const leafMesh1 = new THREE.Mesh(leafGeo1, leafMat);
    leafMesh1.castShadow = true;
    leafMesh1.position.set(0, 0, 0);
    leafMesh1.rotation.set(0.3, 0.5, -0.7);

    const leafGeo2 = createLeafGeometry();
    const leafMesh2 = new THREE.Mesh(leafGeo2, leafMat);
    leafMesh2.castShadow = true;
    leafMesh2.position.set(0, 0, 0);
    leafMesh2.rotation.set(0.3, -0.5, 0.7);

    // Third central emerging leaflet for botanical realism
    const leafGeo3 = createLeafGeometry();
    const leafMesh3 = new THREE.Mesh(leafGeo3, leafMat);
    leafMesh3.scale.set(0.65, 0.65, 0.65);
    leafMesh3.position.set(0, 0.05, 0);
    leafMesh3.rotation.set(-0.4, 0, 0);

    leafGroup.add(leafMesh1);
    leafGroup.add(leafMesh2);
    leafGroup.add(leafMesh3);
    scene.add(leafGroup);

    // ---------------- FLOATING SUNLIT PARTICLES (POLLEN & MIST) ----------------
    const particleCount = width < 768 ? 60 : 120;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleVelocities: { x: number; y: number; z: number }[] = [];

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 3.5;
      particlePositions[i * 3 + 1] = Math.random() * 2.5;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 3.0;
      particleVelocities.push({
        x: (Math.random() - 0.5) * 0.003,
        y: 0.002 + Math.random() * 0.005,
        z: (Math.random() - 0.5) * 0.003,
      });
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xffe082, // Golden morning light pollen
      size: width < 768 ? 0.035 : 0.045,
      transparent: true,
      opacity: 0.0,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // ---------------- PARALLAX INTERACTION ----------------
    let mouseX = 0;
    let mouseY = 0;
    const handlePointerMove = (e: PointerEvent) => {
      mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
    };
    window.addEventListener('pointermove', handlePointerMove);

    // ---------------- RESIZE HANDLER ----------------
    const handleResize = () => {
      if (!container) return;
      width = container.clientWidth || window.innerWidth;
      height = container.clientHeight || window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener('resize', handleResize);

    // ---------------- ANIMATION LOOP (TIMELINE: 0 to 6.2s) ----------------
    let startTime: number | null = null;
    let animationFrameId: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000; // in seconds

      // 1. Stage 0.0s - 1.2s: Calm fertile ground & warm sun breaks through
      if (elapsed < 1.2) {
        const sunWarmth = Math.min(1.0, elapsed / 1.2);
        sunLight.intensity = THREE.MathUtils.lerp(0.1, 1.2, sunWarmth);
        rimLight.intensity = THREE.MathUtils.lerp(0.1, 0.6, sunWarmth);
        seedGroup.scale.setScalar(1.0 + sunWarmth * 0.12); // Seed absorbs moisture
      }

      // 2. Stage 1.0s - 2.8s: Seed germinates & roots drive downward
      if (elapsed >= 0.8 && elapsed <= 3.0) {
        const rootProgress = THREE.MathUtils.smoothstep(elapsed, 0.8, 2.8);
        rootGroup.clear();
        rootMeshes = [];

        rootCurves.forEach((curve) => {
          const pointsCount = Math.max(2, Math.floor(rootProgress * 20));
          const curvePoints: THREE.Vector3[] = [];
          for (let p = 0; p <= pointsCount; p++) {
            curvePoints.push(curve.getPoint(p / 20));
          }
          if (curvePoints.length >= 2) {
            const subCurve = new THREE.CatmullRomCurve3(curvePoints);
            const tube = new THREE.TubeGeometry(subCurve, 16, 0.016, 6, false);
            const mesh = new THREE.Mesh(tube, rootMat);
            rootGroup.add(mesh);
            rootMeshes.push(mesh);
          }
        });
      }

      // 3. Stage 1.8s - 4.4s: Emerald shoot pushes through soil and rises
      if (elapsed >= 1.6 && elapsed <= 5.2) {
        const stemProgress = THREE.MathUtils.smoothstep(elapsed, 1.6, 4.4);
        if (stemMesh) {
          scene.remove(stemMesh);
          stemMesh.geometry.dispose();
        }

        const pointCount = Math.max(3, Math.floor(stemProgress * 32));
        const activeStemPoints: THREE.Vector3[] = [];
        for (let i = 0; i <= pointCount; i++) {
          activeStemPoints.push(stemSpline.getPoint((i / 32) * stemProgress));
        }

        if (activeStemPoints.length >= 2) {
          const activeCurve = new THREE.CatmullRomCurve3(activeStemPoints);
          const stemGeo = new THREE.TubeGeometry(activeCurve, 32, 0.038, 8, false);
          stemMesh = new THREE.Mesh(stemGeo, stemMat);
          stemMesh.castShadow = true;
          scene.add(stemMesh);

          // Position leaf group precisely at the rising shoot tip
          const tipPoint = activeStemPoints[activeStemPoints.length - 1];
          leafGroup.position.copy(tipPoint);
        }
      }

      // 4. Stage 3.2s - 5.2s: Leaves unfurl and stretch toward the sunlight
      if (elapsed >= 3.0) {
        const leafProgress = THREE.MathUtils.smoothstep(elapsed, 3.0, 4.8);
        const leafScale = leafProgress * 1.0;
        leafGroup.scale.set(leafScale, leafScale, leafScale);

        // Natural leaf unfurling rotations
        leafMesh1.rotation.z = THREE.MathUtils.lerp(-1.3, -0.45, leafProgress);
        leafMesh2.rotation.z = THREE.MathUtils.lerp(1.3, 0.45, leafProgress);
        leafMesh1.rotation.x = THREE.MathUtils.lerp(0.9, 0.35, leafProgress);
        leafMesh2.rotation.x = THREE.MathUtils.lerp(0.9, 0.35, leafProgress);

        // Wind sway after leaves have opened
        if (elapsed > 4.6) {
          const sway = Math.sin((elapsed - 4.6) * 3.0) * 0.04;
          leafGroup.rotation.z = sway;
          leafGroup.rotation.x = Math.cos((elapsed - 4.6) * 2.5) * 0.03;
        }

        // Sunlight peaks in radiance
        sunLight.intensity = THREE.MathUtils.lerp(1.2, 2.6, leafProgress);
        rimLight.intensity = THREE.MathUtils.lerp(0.6, 1.8, leafProgress);
        particleMat.opacity = THREE.MathUtils.lerp(0.0, 0.85, leafProgress);
      }

      // 5. Particles movement (rising in warm air current)
      const posArr = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        posArr[i * 3 + 1] += particleVelocities[i].y;
        posArr[i * 3] += particleVelocities[i].x;
        posArr[i * 3 + 2] += particleVelocities[i].z;

        // Wrap around when rising above ceiling
        if (posArr[i * 3 + 1] > 2.8) {
          posArr[i * 3 + 1] = 0.05;
          posArr[i * 3] = (Math.random() - 0.5) * 3.0;
          posArr[i * 3 + 2] = (Math.random() - 0.5) * 2.5;
        }
      }
      particleGeo.attributes.position.needsUpdate = true;

      // 6. Cinematic Camera Dolly & Tilt
      const camProgress = THREE.MathUtils.smoothstep(elapsed, 0.0, 5.2);
      // Crane up from ground level (y: 0.35 -> 1.15) and pull back slightly (z: 2.4 -> 2.9)
      const targetCamY = THREE.MathUtils.lerp(0.35, 1.15, camProgress);
      const targetCamZ = THREE.MathUtils.lerp(2.4, 2.9, camProgress);
      const targetCamX = THREE.MathUtils.lerp(0.0, 0.25, camProgress) + mouseX * 0.12;

      camera.position.x = THREE.MathUtils.lerp(camera.position.x, targetCamX, 0.05);
      camera.position.y = THREE.MathUtils.lerp(camera.position.y, targetCamY, 0.05);
      camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetCamZ, 0.05);

      const lookY = THREE.MathUtils.lerp(0.05, 0.85, camProgress) - mouseY * 0.08;
      camera.lookAt(0, lookY, 0);

      // 7. Brand Reveal at 4.6s
      if (elapsed >= 4.6 && !showBrand) {
        setShowBrand(true);
      }

      // 8. Auto completion transition at 6.0s
      if (elapsed >= 6.0 && !skipFade) {
        handleFinish();
        return;
      }

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);

    // ---------------- RESOURCE CLEANUP ----------------
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('pointermove', handlePointerMove);

      // Clean up geometries and materials to prevent WebGL leaks
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
  }, [handleFinish, showBrand, skipFade, onComplete]);

  // Fallback for devices without WebGL
  if (!webglSupported) {
    return (
      <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-gradient-to-b from-emerald-950 to-slate-950 text-white p-6">
        <div className="w-16 h-16 rounded-2xl bg-emerald-500/20 border border-emerald-400/30 flex items-center justify-center mb-6 animate-pulse">
          <Sprout className="w-9 h-9 text-emerald-400" />
        </div>
        <h1 className="text-3xl font-black tracking-tight text-white mb-2">KhetGPT</h1>
        <p className="text-emerald-200/80 text-sm">{taglines.tagline}</p>
      </div>
    );
  }

  return (
    <div
      className={`fixed inset-0 z-50 overflow-hidden bg-slate-950 select-none transition-opacity duration-700 ${
        skipFade ? 'opacity-0 pointer-events-none' : 'opacity-100'
      }`}
    >
      {/* 3D Canvas Mount */}
      <div ref={mountRef} className="absolute inset-0 w-full h-full cursor-grab active:cursor-grabbing" />

      {/* Atmospheric Horizon Gradient Overlay (Golden Dawn Sun Glow) */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_75%_20%,rgba(245,158,11,0.18)_0%,transparent_60%)]" />

      {/* Top Controls: Sound Toggle & Skip Intro */}
      <div className="absolute top-4 sm:top-6 left-4 right-4 sm:left-8 sm:right-8 flex items-center justify-between z-10 pointer-events-auto">
        {/* Subtle Ambient Sound Toggle */}
        <button
          onClick={toggleAmbientSound}
          className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-black/40 backdrop-blur-md border border-white/10 text-white/70 hover:text-white hover:bg-black/60 transition-all text-xs"
          title={ambientSound ? 'Mute ambient breeze' : 'Play ambient breeze'}
        >
          {ambientSound ? <Volume2 className="w-3.5 h-3.5 text-emerald-400" /> : <VolumeX className="w-3.5 h-3.5" />}
          <span className="hidden sm:inline">{ambientSound ? 'Sound On' : 'Ambient Breeze'}</span>
        </button>

        {/* Minimalist Skip Button */}
        <button
          onClick={handleFinish}
          className="group flex items-center space-x-2 px-4 py-2 rounded-full bg-emerald-950/60 hover:bg-emerald-900/80 backdrop-blur-md border border-emerald-500/30 text-emerald-200 hover:text-white transition-all text-xs font-medium shadow-lg hover:shadow-emerald-900/30 active:scale-95"
        >
          <span>{taglines.skip}</span>
          <span className="inline-block transition-transform group-hover:translate-x-0.5">→</span>
        </button>
      </div>

      {/* Cinematic Brand Reveal Overlay (Appears as plant blooms) */}
      <div
        className={`absolute bottom-10 sm:bottom-16 left-0 right-0 px-4 text-center pointer-events-none transition-all duration-1000 transform ${
          showBrand ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
        }`}
      >
        <div className="inline-flex items-center justify-center space-x-2.5 mb-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-400/20 backdrop-blur-md">
          <Sprout className="w-4 h-4 text-emerald-400 animate-pulse" />
          <span className="text-xs uppercase tracking-widest text-emerald-300 font-semibold">AI Agriculture Platform</span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-200 via-green-100 to-amber-200 tracking-tight drop-shadow-sm mb-1.5">
          {taglines.brand}
        </h1>

        <p className="text-base sm:text-xl font-medium text-emerald-100/90 tracking-wide max-w-xl mx-auto drop-shadow">
          {taglines.tagline}
        </p>

        <p className="text-xs sm:text-sm text-emerald-300/70 mt-1 max-w-md mx-auto hidden sm:block">
          {taglines.sub}
        </p>

        {/* Subtle Progress Bar */}
        <div className="w-32 h-0.5 bg-white/10 rounded-full mx-auto mt-4 overflow-hidden">
          <div className="w-full h-full bg-gradient-to-r from-emerald-500 to-amber-400 origin-left animate-[pulse_2s_ease-in-out_infinite]" />
        </div>
      </div>
    </div>
  );
};
