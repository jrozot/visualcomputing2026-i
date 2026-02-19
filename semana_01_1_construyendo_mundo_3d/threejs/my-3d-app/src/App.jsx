import { Canvas } from "@react-three/fiber"
import { OrbitControls, Edges, useGLTF } from "@react-three/drei"

function Model() {
  const { scene } = useGLTF("/model.glb")
  return (
    <primitive object={scene} />
  )
}

export default function App() {
  return (
    <Canvas camera={{ position: [0, 2, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      
      <Model />

      <OrbitControls />
    </Canvas>
  )
}
