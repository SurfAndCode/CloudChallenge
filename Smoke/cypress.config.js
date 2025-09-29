// Smoke/cypress.config.js
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl:
      process.env.CYPRESS_apiBaseUrl ||      
      process.env.CYPRESS_BASE_URL   ||     
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
