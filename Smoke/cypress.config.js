// Smoke/cypress.config.js
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    // <- THIS is what cy.request('/api/...') uses
    baseUrl:
      process.env.CYPRESS_apiBaseUrl ||      // camelCase (what your job sets)
      process.env.CYPRESS_BASE_URL   ||      // uppercase fallback
      '',

    env: {
      healthPath: process.env.CYPRESS_HEALTH_PATH || '/health',
      functionKey: process.env.CYPRESS_functionKey || '',
    },

    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    video: false,
    defaultCommandTimeout: 8000,
    requestTimeout: 8000,
    supportFile: false,

    setupNodeEvents(on, config) {
      if (!config.baseUrl) {
        throw new Error('CYPRESS_apiBaseUrl (or CYPRESS_BASE_URL) not set — baseUrl is required')
      }
      return config
    },
  },
})
