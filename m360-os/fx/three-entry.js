/* three.js for the 3D office (src/js/91-office3d.js): the named pieces the office uses, and nothing else, so the
   bundle stays small and holds no loader. fx/build.sh bundles this file with --global-name=M3D into
   src/vendor/three.vendor.js; build.py wraps that in window.M360_3D = function () { ... return M3D; }, so
   nothing of it runs until the office asks for it. Never `import * as THREE`, never a loader. */
export {
  WebGLRenderer, Scene, PerspectiveCamera, Group, Mesh, Object3D, HemisphereLight, DirectionalLight,
  MeshStandardMaterial, MeshPhysicalMaterial, MeshBasicMaterial,
  PlaneGeometry, CircleGeometry, SphereGeometry, CapsuleGeometry, CylinderGeometry, ConeGeometry, TorusGeometry,
  LatheGeometry, BoxGeometry, ExtrudeGeometry, Shape, BufferGeometry, BufferAttribute, Float32BufferAttribute,
  CanvasTexture, PMREMGenerator, Raycaster, Plane, Vector2, Vector3, Matrix4, Quaternion, Euler, Color, Box3, Timer, MathUtils,
  NeutralToneMapping, SRGBColorSpace, VSMShadowMap, PCFShadowMap, DoubleSide, FrontSide, AdditiveBlending, NormalBlending,
  RepeatWrapping, LinearFilter, LinearMipmapLinearFilter, REVISION
} from 'three';
export {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
export {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
export {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
export {mergeGeometries, mergeVertices} from 'three/examples/jsm/utils/BufferGeometryUtils.js';
