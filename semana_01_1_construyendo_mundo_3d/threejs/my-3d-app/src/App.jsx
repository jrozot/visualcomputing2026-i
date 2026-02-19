import { Canvas } from "@react-three/fiber"
import { OrbitControls, useGLTF } from "@react-three/drei"
import { useEffect } from "react"
import * as THREE from "three"

function Model() {
  const { scene } = useGLTF("/model.glb")

  useEffect(() => {
    scene.traverse((child) => {
      if (child.isMesh) {
        // Solid material
        child.material = new THREE.MeshStandardMaterial({
          color: "orange",
          transparent: false,
        })

        // Add wireframe overlay
        const wireframe = new THREE.LineSegments(
          new THREE.WireframeGeometry(child.geometry),
          new THREE.LineBasicMaterial({ color: "black" })
        )
        child.add(wireframe)

        // Add vertices as points
        const points = new THREE.Points(
          child.geometry,
          new THREE.PointsMaterial({
            color: "red",
            size: 0.05,
          })
        )
        child.add(points)
      }
    })
  }, [scene])

  return <primitive object={scene} />
}

export default function App() {
  return (
    <Canvas camera={{ position: [0, 2, 5], fov: 60 }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 5, 5]} intensity={1} />

      <Model />

      <OrbitControls />
    </Canvas>
  )
}
