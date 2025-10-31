// Solar System objects with positions (in parsecs from Sun at origin)
// 1 AU = 4.84814e-6 parsecs

export const SOLAR_SYSTEM = {
  sun: {
    name: "Sun",
    x: 0,
    y: 0,
    z: 0,
    type: "star",
    color: [1.0, 0.95, 0.7], // Bright yellow-white
    size: 35,
    magnitude: -26.74,
  },
  mercury: {
    name: "Mercury",
    x: 0.387 * 4.84814e-6, // 0.387 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.6, 0.6, 0.6], // Gray
    size: 10,
    magnitude: -2.48,
  },
  venus: {
    name: "Venus",
    x: 0.723 * 4.84814e-6, // 0.723 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.95, 0.9, 0.7], // Pale yellow
    size: 14,
    magnitude: -4.92,
  },
  earth: {
    name: "Earth",
    x: 1.0 * 4.84814e-6, // 1.0 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.2, 0.5, 1.0], // Blue
    size: 14,
    magnitude: -3.99,
  },
  mars: {
    name: "Mars",
    x: 1.524 * 4.84814e-6, // 1.524 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.95, 0.35, 0.25], // Red
    size: 12,
    magnitude: -2.94,
  },
  jupiter: {
    name: "Jupiter",
    x: 5.203 * 4.84814e-6, // 5.203 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.9, 0.75, 0.55], // Orange-tan
    size: 28,
    magnitude: -2.94,
  },
  saturn: {
    name: "Saturn",
    x: 9.537 * 4.84814e-6, // 9.537 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.95, 0.9, 0.7], // Pale gold
    size: 26,
    magnitude: -0.55,
  },
  uranus: {
    name: "Uranus",
    x: 19.191 * 4.84814e-6, // 19.191 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.55, 0.85, 0.95], // Light cyan
    size: 18,
    magnitude: 5.38,
  },
  neptune: {
    name: "Neptune",
    x: 30.069 * 4.84814e-6, // 30.069 AU
    y: 0,
    z: 0,
    type: "planet",
    color: [0.25, 0.45, 0.95], // Deep blue
    size: 18,
    magnitude: 7.67,
  },
};

// Label styling for solar system (matches star label style)
export const SOLAR_SYSTEM_LABEL_COLORS = {
  star: "#ffd700", // Gold for Sun
  planet: "#00d4ff", // Bright cyan for planets
};

export const SOLAR_SYSTEM_SCALE = 1000000; // Scale factor to make planets visible (1 million times larger)
