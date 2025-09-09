# Smoke tests (Cypress) — separate folder

This package contains API smoke tests for your backend.

## Layout
- `/smoke/package.json`
- `/smoke/cypress.config.js`
- `/smoke/cypress/e2e/smoke/*.cy.js`
- `/.github/workflows/cypress-api-smoke.yml` (in repo root)

## Run locally
```bash
cd smoke
npm ci
npm run test:smoke
# or override env:
CYPRESS_BASE_URL=https://counterapi-a5aeacedhma9ecev.australiasoutheast-01.azurewebsites.net npm run test:smoke
CYPRESS_HEALTH_PATH=/api/health npm run test:smoke
CYPRESS_ALLOW_MUTATION=false npm run test:smoke   # skip POST tests
```

## Notes
- `CYPRESS_ALLOW_MUTATION=false` can be used on PRs to avoid changing counters.
