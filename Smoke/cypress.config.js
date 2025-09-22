const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    env: {
      baseUrl: process.env.CYPRESS_apiBaseUrl || ''
    },
    specPattern: "cypress/e2e/**/*.cy.{js,ts}",
    video: false,
    defaultCommandTimeout: 8000,
    requestTimeout: 8000,
    supportFile: false,
    setupNodeEvents(on, config) {
      config.env.HEALTH_PATH = process.env.CYPRESS_HEALTH_PATH || config.env.HEALTH_PATH || "/health";
      config.env.ALLOW_MUTATION = (process.env.CYPRESS_ALLOW_MUTATION || "true").toLowerCase() === "true";
      return config;
    },
  },
});
