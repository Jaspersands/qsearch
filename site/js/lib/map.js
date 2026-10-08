export const TRACK_COLORS = {
  "CODE-COSET-COLLECTIVE": "#3b6ea5",
  "DHS-GOWERS-SIEVE": "#c2410c",
  "HYP-LIT-HIDDEN-SHIFT-SIEVE": "#6b8e23",
  "HYP-LIT-COSET-OBSERVABLES": "#8e5ea2",
  OTHER: "#9ca3af",
};

// Smaller tracks win so they stay visible inside the large codes-and-cosets cloud.
const TRACK_PRIORITY = [
  "HYP-LIT-HIDDEN-SHIFT-SIEVE",
  "HYP-LIT-COSET-OBSERVABLES",
  "DHS-GOWERS-SIEVE",
  "CODE-COSET-COLLECTIVE",
];

export function trackOf(tags) {
  return TRACK_PRIORITY.find((track) => tags.includes(track)) || "OTHER";
}

export function projectPoints(points, width, height, pad) {
  return points.map((point) => [pad + point.x * (width - 2 * pad), pad + point.y * (height - 2 * pad)]);
}

export function nearestIndex(screen, mx, my, include, maxDist = 10) {
  let best = -1;
  let bestDistance = maxDist * maxDist + 1e-9;
  screen.forEach(([x, y], index) => {
    if (!include(index)) return;
    const distance = (x - mx) ** 2 + (y - my) ** 2;
    if (distance < bestDistance) {
      best = index;
      bestDistance = distance;
    }
  });
  return best;
}
