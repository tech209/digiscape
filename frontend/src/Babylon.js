// Babylon.js Setup for Emergent Network Simulation
import * as BABYLON from 'babylonjs';

export default function initNetworkScene() {
    // Create Babylon.js Engine and Scene
    const canvas = document.getElementById("renderCanvas");
    const engine = new BABYLON.Engine(canvas, true);
    const scene = new BABYLON.Scene(engine);

    // Camera Setup
    const camera = new BABYLON.ArcRotateCamera("Camera", Math.PI / 2, Math.PI / 4, 50, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvas, true);

    // Light Setup
    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
    light.intensity = 0.7;

    // Store Packets in Simulation
    let packets = [];

    // Function to Create a New Packet with Visual Enhancements
    function createPacket(data) {
        let packet = BABYLON.MeshBuilder.CreateSphere("packet", { diameter: 1 }, scene);
        packet.position = new BABYLON.Vector3(Math.random() * 10 - 5, Math.random() * 10 - 5, Math.random() * 10 - 5);
        packet.density = data.density;
        packet.latency = data.latency;
        packet.adjustment = data.adjustment;
        packet.stabilized = false;
        packet.lifespan = 300; // Decay over time

        // Assign dynamic material color based on density
        let material = new BABYLON.StandardMaterial("packetMaterial", scene);
        material.diffuseColor = new BABYLON.Color3(1 - packet.density, packet.density, packet.latency);
        material.emissiveColor = new BABYLON.Color3(0.2, 0.2, packet.latency * 5); // Glow effect based on latency
        packet.material = material;

        // High-mass packets get particle effects
        if (packet.density > 0.8) {
            let particleSystem = new BABYLON.ParticleSystem("particles", 100, scene);
            particleSystem.particleTexture = new BABYLON.Texture("https://www.babylonjs-playground.com/textures/flare.png", scene);
            particleSystem.emitter = packet;
            particleSystem.minEmitPower = 1;
            particleSystem.maxEmitPower = 2;
            particleSystem.start();
        }

        packets.push(packet);
    }

    // Function to Update Packet Positions Based on Emergent Behavior
    function updatePacketPositions() {
        for (let i = 0; i < packets.length; i++) {
            let packet = packets[i];
            let leftNeighbor = packets[i - 1] || null;
            let rightNeighbor = packets[i + 1] || null;

            let leftAdjustment = leftNeighbor ? leftNeighbor.adjustment : 0;
            let rightAdjustment = rightNeighbor ? rightNeighbor.adjustment : 0;

            let netAdjustment = (leftAdjustment - rightAdjustment) * 0.1;

            // Smooth position updates
            packet.position.x += netAdjustment * 0.05;
            packet.position.y += (packet.density - packet.latency) * 0.02;

            // Interpolated scaling
            packet.scaling.y = BABYLON.Scalar.Lerp(packet.scaling.y, packet.density * 5, 0.1);

            // Gradual adjustment decay over time
            packet.adjustment *= 0.98;

            // Lifespan decay & removal
            packet.lifespan -= 1;
            if (packet.lifespan <= 0) {
                packet.dispose();
                packets.splice(i, 1);
            }
        }
    }

    // Babylon.js Render Loop
    scene.onBeforeRenderObservable.add(updatePacketPositions);

    // WebSocket Connection to Backend for Real-Time Data
    const socket = new WebSocket("ws://127.0.0.1:5000");

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        createPacket(data);
    };

    // Run the Engine
    engine.runRenderLoop(() => {
        scene.render();
    });

    // Resize Handling
    window.addEventListener("resize", () => {
        engine.resize();
    });
}
