// Babylon.js Setup for Emergent Network Simulation
import * as BABYLON from 'babylonjs';

export default class NetworkScene {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.engine = new BABYLON.Engine(this.canvas, true);
        this.scene = new BABYLON.Scene(this.engine);
        this.packets = [];
        this.setupScene();
        this.setupWebSocket();
        this.engine.runRenderLoop(() => this.scene.render());
        window.addEventListener("resize", () => this.engine.resize());
    }

    setupScene() {
        // Camera Setup
        this.camera = new BABYLON.ArcRotateCamera("Camera", Math.PI / 2, Math.PI / 4, 50, BABYLON.Vector3.Zero(), this.scene);
        this.camera.attachControl(this.canvas, true);

        // Light Setup
        this.light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), this.scene);
        this.light.intensity = 0.7;

        // Start update loop
        this.scene.onBeforeRenderObservable.add(() => this.updatePacketPositions());
    }

    setupWebSocket() {
        this.socket = new WebSocket("ws://127.0.0.1:5000");
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.createPacket(data);
        };
    }

    createPacket(data) {
        let packet = BABYLON.MeshBuilder.CreateSphere("packet", { diameter: 1 }, this.scene);
        packet.position = new BABYLON.Vector3(Math.random() * 10 - 5, Math.random() * 10 - 5, Math.random() * 10 - 5);
        packet.density = data.density;
        packet.latency = data.latency;
        packet.adjustment = data.adjustment;
        packet.lifespan = 300; // Decay over time

        let material = new BABYLON.StandardMaterial("packetMaterial", this.scene);
        material.diffuseColor = new BABYLON.Color3(1 - packet.density, packet.density, packet.latency);
        material.emissiveColor = new BABYLON.Color3(0.2, 0.2, packet.latency * 5);
        material.alpha = 0.8; // Slight transparency for blending
        packet.material = material;

        // Create particle trails for high-mass packets
        if (packet.density > 0.8) {
            this.createParticleTrail(packet);
        }

        this.packets.push(packet);
    }

    createParticleTrail(packet) {
        let particleSystem = new BABYLON.ParticleSystem("particles", 100, this.scene);
        particleSystem.particleTexture = new BABYLON.Texture("https://www.babylonjs-playground.com/textures/flare.png", this.scene);
        particleSystem.emitter = packet;
        particleSystem.minEmitPower = 0.5;
        particleSystem.maxEmitPower = 2;
        particleSystem.minSize = 0.1;
        particleSystem.maxSize = 0.5;
        particleSystem.emitRate = 20;
        particleSystem.start();
    }

    updatePacketPositions() {
        for (let i = 0; i < this.packets.length; i++) {
            let packet = this.packets[i];
            let leftNeighbor = this.packets[i - 1] || null;
            let rightNeighbor = this.packets[i + 1] || null;

            let leftAdjustment = leftNeighbor ? leftNeighbor.adjustment : 0;
            let rightAdjustment = rightNeighbor ? rightNeighbor.adjustment : 0;

            let netAdjustment = (leftAdjustment - rightAdjustment) * 0.1;

            // Apply repulsion effect when packets get too close
            this.applyRepulsion(packet, i);

            // Smooth position updates
            packet.position.x += netAdjustment * 0.05;
            packet.position.y += (packet.density - packet.latency) * 0.02;
            packet.scaling.y = BABYLON.Scalar.Lerp(packet.scaling.y, packet.density * 5, 0.1);
            packet.adjustment *= 0.98;
            packet.lifespan -= 1;

            if (packet.lifespan <= 0) {
                packet.dispose();
                this.packets.splice(i, 1);
            }
        }
    }

    applyRepulsion(packet, index) {
        for (let j = 0; j < this.packets.length; j++) {
            if (j !== index) {
                let otherPacket = this.packets[j];
                let distance = BABYLON.Vector3.Distance(packet.position, otherPacket.position);

                if (distance < 1.5) { // If too close, apply a push force
                    let pushVector = packet.position.subtract(otherPacket.position).normalize().scale(0.05);
                    packet.position.addInPlace(pushVector);
                }
            }
        }
    }
}
