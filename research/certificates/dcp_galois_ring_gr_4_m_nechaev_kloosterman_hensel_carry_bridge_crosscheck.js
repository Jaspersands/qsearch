// Independent Node.js crosscheck for Subsystem 148: Galois Ring GR(4, 2) Teichmuller Carry
const fs = require("fs");
const path = require("path");

const certPath = path.join(__dirname, "..", "reductions", "dcp_galois_ring_gr_4_m_nechaev_kloosterman_hensel_carry_bridge.json");
const cert = JSON.parse(fs.readFileSync(certPath, "utf8"));

const T2 = [[0, 0], [1, 0], [0, 1], [3, 3]];
function mul(u, v) {
  return [
    (u[0] * v[0] + 3 * u[1] * v[1]) % 4,
    (u[0] * v[1] + u[1] * v[0] + 3 * u[1] * v[1]) % 4
  ];
}
for (const a of T2) {
  const a4 = mul(mul(a, a), mul(a, a));
  if (a4[0] !== a[0] || a4[1] !== a[1]) {
    throw new Error("Teichmuller a^4 = a failed in JS");
  }
}
if (!cert.all_checks_passed || cert.gr4_2_verification.cardinality !== 16) {
  throw new Error("Subsystem 148 certificate checks failed");
}
console.log("Subsystem 148 JS crosscheck PASSED");
