const PATH = "/visit";
const allowMutation = Cypress.env("ALLOW_MUTATION");

const expectJson = (res) => {
  expect((res.headers["content-type"] || "").toLowerCase()).to.include("application/json");
};

describe("Visit counter", () => {
  it("GET returns { count: number }", () => {
    cy.request(PATH).then((res) => {
      expect(res.status).to.equal(200);
      expectJson(res);
      expect(res.body).to.have.property("count");
      expect(res.body.count).to.be.a("number");
    });
  });

  (allowMutation ? it : it.skip)("POST increments: default +1 and inc=2", () => {
    cy.request(PATH).then((get0) => {
      const c0 = get0.body.count;

      cy.request("POST", PATH).its("body.count").should("equal", c0 + 1);
      cy.request("POST", `${PATH}?inc=2`).its("body.count").should("equal", c0 + 3);
      cy.request("POST", `${PATH}?inc=abc`).its("body.count").should("equal", c0 + 4);
    });
  });

  it("Latency < 1500ms (best-effort)", () => {
    const t0 = Date.now();
    cy.request(PATH).then(() => {
      expect(Date.now() - t0).to.be.lessThan(1500);
    });
  });
});
