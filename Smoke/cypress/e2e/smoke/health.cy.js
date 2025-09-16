// Health check: expects { ok: true }
const HEALTH_PATH = Cypress.env("HEALTH_PATH") || "/health";

describe("Health", () => {
  it("GET returns 200 + JSON { ok: true }", () => {
    cy.request({ method: "GET", url: HEALTH_PATH, headers: { accept: "application/json" } }).then((res) => {
      expect(res.status).to.equal(200);
      expect((res.headers["content-type"] || "").toLowerCase()).to.include("application/json");
      expect(res.body).to.deep.equal({ ok: true });
    });
  });
});
