import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { Sprout } from 'lucide-react';
import { type Language } from '../i18n/translations';

interface PlantGrowingIntroProps {
  onComplete: () => void;
  language?: Language;
}

export const PlantGrowingIntro: React.FC<PlantGrowingIntroProps> = ({ onComplete }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const welcomeRef = useRef<HTMLDivElement>(null);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;
  const isFinishedRef = useRef(false);

  const handleSkip = () => {
    if (isFinishedRef.current) return;
    isFinishedRef.current = true;
    if (overlayRef.current) {
      overlayRef.current.style.opacity = '0';
      overlayRef.current.style.pointerEvents = 'none';
    }
    setTimeout(() => {
      onCompleteRef.current();
    }, 400);
  };

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Safety fallback timer: Ensure app is NEVER blocked even if WebGL fails
    const safetyTimer = setTimeout(() => {
      if (!isFinishedRef.current) {
        isFinishedRef.current = true;
        onCompleteRef.current();
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
      onCompleteRef.current();
      return;
    }

    // ---------------- THREE.JS 3D CINEMATIC SCENE ----------------
    let width = container.clientWidth || window.innerWidth;
    let height = container.clientHeight || window.innerHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x061510); // Rich dawn emerald-slate atmosphere

    // Camera positioned with the plant comfortably centered in the lower-middle half
    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 50);
    camera.position.set(0, -0.05, 2.65);
    camera.lookAt(0, -0.10, 0);

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

    // ---------------- LIGHTING ----------------
    const ambientLight = new THREE.AmbientLight(0xfff7ed, 0.85);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xffedd5, 2.4);
    sunLight.position.set(3.5, 4.8, 3.0);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0xa7f3d0, 0.6);
    fillLight.position.set(-3.0, 2.0, 2.0);
    scene.add(fillLight);

    const leafGlow = new THREE.PointLight(0x86efac, 1.5, 5);
    leafGlow.position.set(0, 0.15, -0.35);
    scene.add(leafGlow);

    // ---------------- SOIL LEVEL AT y = -0.45 ----------------
    const soilTopGeo = new THREE.PlaneGeometry(9.5, 6.5, 32, 32);
    const topPos = soilTopGeo.attributes.position;
    for (let i = 0; i < topPos.count; i++) {
      const x = topPos.getX(i);
      const y = topPos.getY(i);
      topPos.setZ(i, Math.sin(x * 3.4) * 0.04 + Math.cos(y * 2.8) * 0.03);
    }
    soilTopGeo.computeVertexNormals();

    const soilTopMat = new THREE.MeshStandardMaterial({
      color: 0x4a2e1b,
      roughness: 0.88,
      metalness: 0.03,
      flatShading: true,
    });
    const soilTop = new THREE.Mesh(soilTopGeo, soilTopMat);
    soilTop.rotation.x = -Math.PI / 2.22;
    soilTop.position.set(0, -0.45, -0.15);
    soilTop.receiveShadow = true;
    scene.add(soilTop);

    // Subterranean Bed below ground level
    const soilBedGeo = new THREE.PlaneGeometry(9.5, 3.5, 12, 12);
    const soilBedMat = new THREE.MeshStandardMaterial({
      color: 0x26160c,
      roughness: 0.95,
      metalness: 0.0,
    });
    const soilBed = new THREE.Mesh(soilBedGeo, soilBedMat);
    soilBed.position.set(0, -1.25, -0.3);
    scene.add(soilBed);

    // Soil crumbs / particles around sprout
    const crumbGroup = new THREE.Group();
    const crumbGeo = new THREE.DodecahedronGeometry(0.024, 0);
    const crumbMat = new THREE.MeshStandardMaterial({ color: 0x5a3620, roughness: 0.85 });
    const crumbMeshes: { mesh: THREE.Mesh; basePos: THREE.Vector3 }[] = [];
    for (let i = 0; i < 32; i++) {
      const crumb = new THREE.Mesh(crumbGeo, crumbMat);
      const angle = Math.random() * Math.PI * 2;
      const r = 0.05 + Math.random() * 0.45;
      const x = Math.cos(angle) * r;
      const z = Math.sin(angle) * r * 0.65;
      const y = -0.44 + Math.random() * 0.03;
      crumb.position.set(x, y, z);
      const s = 0.45 + Math.random() * 0.85;
      crumb.scale.set(s, s * 0.75, s);
      crumb.castShadow = true;
      crumbGroup.add(crumb);
      crumbMeshes.push({ mesh: crumb, basePos: new THREE.Vector3(x, y, z) });
    }
    scene.add(crumbGroup);

    // ---------------- SEED AT y = -0.65 ----------------
    const seedGroup = new THREE.Group();
    seedGroup.position.set(0, -0.65, 0.05);

    const cotyledonGeo = new THREE.SphereGeometry(0.075, 18, 18);
    cotyledonGeo.scale(0.7, 1.35, 0.9);
    const seedMat = new THREE.MeshStandardMaterial({
      color: 0x854d27,
      roughness: 0.55,
      metalness: 0.08,
    });

    const seedLeft = new THREE.Mesh(cotyledonGeo, seedMat);
    seedLeft.position.set(-0.022, 0, 0);
    seedLeft.castShadow = true;
    seedGroup.add(seedLeft);

    const seedRight = new THREE.Mesh(cotyledonGeo, seedMat);
    seedRight.position.set(0.022, 0, 0);
    seedRight.castShadow = true;
    seedGroup.add(seedRight);

    scene.add(seedGroup);

    // ---------------- DOWNWARD ROOTS ----------------
    const rootMat = new THREE.MeshStandardMaterial({
      color: 0xfef9c3,
      roughness: 0.4,
      metalness: 0.02,
    });

    const rootSplines = [
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, -0.71, 0.04),
        new THREE.Vector3(0.02, -0.90, 0.03),
        new THREE.Vector3(-0.03, -1.10, 0.01),
        new THREE.Vector3(0.02, -1.35, -0.01),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.01, -0.84, 0.03),
        new THREE.Vector3(-0.13, -1.02, -0.03),
        new THREE.Vector3(-0.22, -1.22, -0.05),
      ]),
      new THREE.CatmullRomCurve3([
        new THREE.Vector3(0.01, -0.88, 0.03),
        new THREE.Vector3(0.15, -1.06, 0.04),
        new THREE.Vector3(0.24, -1.28, 0.05),
      ]),
    ];

    const rootMeshes: { geo: THREE.TubeGeometry; maxIndices: number }[] = [];
    const rootGroup = new THREE.Group();
    rootSplines.forEach((spline, idx) => {
      const radius = idx === 0 ? 0.017 : 0.012;
      const geo = new THREE.TubeGeometry(spline, 20, radius, 8, false);
      geo.setDrawRange(0, 0);
      const mesh = new THREE.Mesh(geo, rootMat);
      rootGroup.add(mesh);
      rootMeshes.push({ geo, maxIndices: geo.index ? geo.index.count : 0 });
    });
    scene.add(rootGroup);

    // ---------------- PLANT STEM & LEAVES (GROUND AT -0.45, GROWS TO y = 0.18) ----------------
    const stemSpline = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, -0.65, 0.04),
      new THREE.Vector3(0.01, -0.45, 0.02),
      new THREE.Vector3(0.035, -0.22, 0.0),
      new THREE.Vector3(-0.02, 0.02, 0.012),
      new THREE.Vector3(0.01, 0.18, 0.0),
    ]);

    const stemGeo = new THREE.TubeGeometry(stemSpline, 36, 0.028, 8, false);
    stemGeo.setDrawRange(0, 0);
    const stemMat = new THREE.MeshStandardMaterial({
      color: 0x4ade80,
      roughness: 0.32,
      metalness: 0.05,
    });
    const stemMesh = new THREE.Mesh(stemGeo, stemMat);
    stemMesh.castShadow = true;
    scene.add(stemMesh);
    const stemMaxIndices = stemGeo.index ? stemGeo.index.count : 0;

    // Cotyledon Leaves
    const leafShape = new THREE.Shape();
    leafShape.moveTo(0, 0);
    leafShape.bezierCurveTo(0.14, 0.08, 0.22, 0.24, 0.0, 0.48);
    leafShape.bezierCurveTo(-0.22, 0.24, -0.14, 0.08, 0, 0);

    const leafGeo = new THREE.ExtrudeGeometry(leafShape, {
      depth: 0.007,
      bevelEnabled: true,
      bevelSegments: 2,
      steps: 1,
      bevelSize: 0.003,
      bevelThickness: 0.003,
    });
    const leafPos = leafGeo.attributes.position;
    for (let i = 0; i < leafPos.count; i++) {
      const y = leafPos.getY(i);
      const x = leafPos.getX(i);
      const dip = Math.sin((y / 0.48) * Math.PI) * 0.045 - Math.abs(x) * 0.03;
      leafPos.setZ(i, leafPos.getZ(i) + dip);
    }
    leafGeo.computeVertexNormals();

    const leafMat = new THREE.MeshStandardMaterial({
      color: 0x22c55e,
      roughness: 0.25,
      metalness: 0.04,
      side: THREE.DoubleSide,
    });

    const leafGroup = new THREE.Group();
    leafGroup.scale.set(0, 0, 0);

    const leftLeaf = new THREE.Mesh(leafGeo, leafMat);
    leftLeaf.castShadow = true;
    leftLeaf.rotation.set(0.2, 0.35, -0.55);
    leafGroup.add(leftLeaf);

    const rightLeaf = new THREE.Mesh(leafGeo, leafMat);
    rightLeaf.castShadow = true;
    rightLeaf.rotation.set(0.2, -0.35, 0.55);
    leafGroup.add(rightLeaf);

    // Young true-leaf bud at crown
    const budGeo = new THREE.ConeGeometry(0.03, 0.12, 6);
    const budMat = new THREE.MeshStandardMaterial({ color: 0x86efac, roughness: 0.3 });
    const budMesh = new THREE.Mesh(budGeo, budMat);
    budMesh.position.set(0, 0.04, 0);
    leafGroup.add(budMesh);

    scene.add(leafGroup);

    // ---------------- FLOATING GOLDEN MORNING DUST ----------------
    const particleCount = width < 768 ? 45 : 80;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleSpeeds: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 3.2;
      particlePositions[i * 3 + 1] = -0.5 + Math.random() * 2.0;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 2.0;
      particleSpeeds.push(0.0015 + Math.random() * 0.0028);
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xfef08a,
      size: width < 768 ? 0.032 : 0.042,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // ---------------- 0 to 5s EXACT TIMELINE ----------------
    // 0.0 - 3.5s: Plant grows continuously from soil, leaves unfold in sync
    // 3.5 - 4.5s: Welcome text fades in above fully grown plant
    // 4.5 - 5.0s: Plant & welcome text remain stable together
    // 5.0 - 5.5s: Smooth fade into homepage
    let startTime: number | null = null;
    let animationFrameId: number;
    let welcomeShown = false;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000; // in seconds

      // 1. Seed Swelling (0.0s - 1.2s)
      if (elapsed <= 1.4) {
        const swell = THREE.MathUtils.smoothstep(elapsed, 0.0, 1.0);
        seedGroup.scale.setScalar(1.0 + swell * 0.2);

        const split = THREE.MathUtils.smoothstep(elapsed, 0.2, 1.2) * 0.035;
        seedLeft.position.x = -0.022 - split;
        seedLeft.rotation.z = split * 2.5;
        seedRight.position.x = 0.022 + split;
        seedRight.rotation.z = -split * 2.5;
      }

      // 2. Downward Roots: continuous smooth growth (0.2s - 2.5s)
      if (elapsed >= 0.2 && elapsed <= 2.6) {
        const rootProgress = THREE.MathUtils.smoothstep(elapsed, 0.2, 2.5);
        rootMeshes.forEach(({ geo, maxIndices }) => {
          const count = Math.min(maxIndices, Math.floor(rootProgress * 20) * 48);
          geo.setDrawRange(0, count);
        });
      }

      // 3. Upward Stem: continuous fluid growth from 0.6s to 3.5s (Reaches 100% full height at 3.5s)
      const stemProgress = THREE.MathUtils.smoothstep(elapsed, 0.6, 3.5);
      const stemCount = Math.min(stemMaxIndices, Math.floor(stemProgress * 36) * 48);
      stemGeo.setDrawRange(0, stemCount);

      // Leaves track the tip of the growing stem
      const currentTip = stemSpline.getPoint(Math.max(0.01, stemProgress));
      leafGroup.position.copy(currentTip);

      // Soil displacement reaction as shoot breaches ground level (1.0s to 2.2s)
      if (elapsed >= 0.9 && elapsed <= 2.2) {
        const breach = THREE.MathUtils.smoothstep(elapsed, 0.9, 1.8);
        crumbMeshes.forEach(({ mesh, basePos }) => {
          const dist = Math.sqrt(basePos.x * basePos.x + basePos.z * basePos.z);
          if (dist < 0.22) {
            const push = (0.22 - dist) * 0.42 * breach;
            mesh.position.y = basePos.y + push;
            mesh.rotation.x = push * 3.5;
          }
        });
      }

      // 4. Leaves unfold naturally in sync with stem growth (1.6s to 3.5s)
      if (elapsed >= 1.6) {
        const leafProgress = THREE.MathUtils.smoothstep(elapsed, 1.6, 3.5);
        leafGroup.scale.setScalar(leafProgress);

        leftLeaf.rotation.z = THREE.MathUtils.lerp(-1.1, -0.38, leafProgress);
        rightLeaf.rotation.z = THREE.MathUtils.lerp(1.1, 0.38, leafProgress);

        // Continuous natural wind sway (starts gently, fully organic)
        const breeze = Math.sin(elapsed * 2.4) * 0.035 * stemProgress;
        leafGroup.rotation.z = breeze;
        leafGroup.rotation.x = Math.cos(elapsed * 2.0) * 0.02 * stemProgress;
      }

      // Floating dust particles
      const pArr = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        pArr[i * 3 + 1] += particleSpeeds[i];
        if (pArr[i * 3 + 1] > 1.8) {
          pArr[i * 3 + 1] = -0.5;
        }
      }
      particleGeo.attributes.position.needsUpdate = true;

      // 5. AT EXACTLY 3.5s: Plant is fully grown -> Welcome Text smoothly fades in above plant
      if (elapsed >= 3.5 && !welcomeShown) {
        welcomeShown = true;
        if (welcomeRef.current) {
          welcomeRef.current.style.opacity = '1';
          welcomeRef.current.style.transform = 'translateY(0)';
        }
      }

      // 6. AT 5.0s: Scene completes -> smoothly fade out overlay into homepage
      if (elapsed >= 5.0 && !isFinishedRef.current) {
        isFinishedRef.current = true;
        if (overlayRef.current) {
          overlayRef.current.style.opacity = '0';
          overlayRef.current.style.pointerEvents = 'none';
        }
        setTimeout(() => {
          onCompleteRef.current();
        }, 500);
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
  }, []); // EMPTY DEPENDENCY ARRAY - NEVER RESTART OR TEAR DOWN 3D SCENE!

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-[9999] overflow-hidden bg-gradient-to-b from-[#05140f] via-[#0b241a] to-[#170e08] select-none transition-opacity duration-500 ease-out opacity-100"
      aria-label="Welcome to KhetGPT Intro"
    >
      {/* 3D WebGL Canvas Container */}
      <div ref={mountRef} className="absolute inset-0 w-full h-full" />

      {/* Atmospheric Sunrise Golden Radial Glow in Upper Sky */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_50%_30%,rgba(245,158,11,0.22)_0%,rgba(16,185,129,0.1)_45%,transparent_70%)]" />

      {/* Unobtrusive "Skip Intro" Button in Top Right */}
      <div className="absolute top-4 right-4 sm:top-6 sm:right-6 z-20">
        <button
          onClick={handleSkip}
          className="flex items-center space-x-1.5 px-3.5 py-1.5 sm:px-4 sm:py-2 rounded-full bg-black/50 hover:bg-black/75 active:scale-95 backdrop-blur-md border border-white/20 text-white/90 hover:text-white transition-all text-xs sm:text-sm font-medium cursor-pointer shadow-xl"
          title="Skip Intro"
        >
          <span>Skip Intro</span>
        </button>
      </div>

      {/* Welcome Text: Pure CSS Transition smoothly fading in at 3.5s above the fully grown plant */}
      <div
        ref={welcomeRef}
        style={{
          opacity: 0,
          transform: 'translateY(18px)',
          transition: 'opacity 0.9s cubic-bezier(0.16, 1, 0.3, 1), transform 0.9s cubic-bezier(0.16, 1, 0.3, 1)',
        }}
        className="absolute top-10 sm:top-14 md:top-18 left-0 right-0 px-4 text-center pointer-events-none"
      >
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/30 backdrop-blur-md mb-2 sm:mb-2.5 shadow-lg shadow-emerald-950/50">
          <Sprout className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-400 animate-pulse" />
          <span className="text-[10px] sm:text-xs uppercase tracking-widest text-emerald-300 font-bold">
            Smart Agriculture AI
          </span>
        </div>

        {/* EXACT REQUIRED TEXT: Welcome to KhetGPT */}
        <h1 className="text-3xl sm:text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-100 via-green-50 to-amber-100 tracking-tight drop-shadow-[0_4px_20px_rgba(0,0,0,0.9)] font-sans">
          Welcome to KhetGPT
        </h1>

        <p className="text-xs sm:text-base font-medium text-emerald-200/90 mt-1 sm:mt-1.5 max-w-md mx-auto tracking-wide drop-shadow">
          Growing Smarter Farming with AI
        </p>
      </div>
    </div>
  );
};
