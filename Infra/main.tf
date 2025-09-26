# ---------------- RG & helpers ----------------
resource "azurerm_resource_group" "rg" {
  name     = local.rg_name
  location = var.location
  tags     = local.tags
}

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  numeric = true
  special = false
  keepers = { env = var.env }  # same suffix within an env
}

# ---------------- Cosmos DB (SQL) ----------------
resource "azurerm_cosmosdb_account" "cosmos" {
  name                = "${var.name_prefix}-${var.env}-cdb${random_string.suffix.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  # 👇 required by your current azurerm schema
  offer_type          = "Standard"

  kind                = "GlobalDocumentDB"
  free_tier_enabled   = var.cosmos_free_tier

  consistency_policy {
    consistency_level = "Session"
  }

  # Serverless capability (mutually exclusive with Free Tier)
  dynamic "capabilities" {
    for_each = var.cosmos_serverless ? [1] : []
    content {
      name = "EnableServerless"
    }
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }

  lifecycle {
    precondition {
      condition     = !(var.cosmos_serverless && var.cosmos_free_tier)
      error_message = "Cosmos Serverless and Free Tier cannot both be true."
    }
  }
}

resource "azurerm_cosmosdb_sql_database" "db" {
  name                = var.cosmos_db_name
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmos.name
  # When serverless: do NOT set throughput / autoscale
}

resource "azurerm_cosmosdb_sql_container" "container" {
  name                  = var.cosmos_container
  resource_group_name   = azurerm_resource_group.rg.name
  account_name          = azurerm_cosmosdb_account.cosmos.name
  database_name         = azurerm_cosmosdb_sql_database.db.name
  partition_key_paths   = [var.cosmos_partition] # v4 expects a LIST
  partition_key_version = 2
}

# ---------------- Function App (Linux, Consumption Y1) ----------------
resource "azurerm_storage_account" "func_sa" {
  name                     = "${local.sa_base}${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  allow_nested_items_to_be_public = false
  tags                     = local.tags
}

resource "azurerm_service_plan" "plan" {
  name                = local.plan_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"         # Consumption
  tags                = local.tags
}

resource "azurerm_linux_function_app" "func" {
  name                       = local.func_name
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  service_plan_id            = azurerm_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.func_sa.name
  storage_account_access_key = azurerm_storage_account.func_sa.primary_access_key
  https_only                 = true
  functions_extension_version = "~4"
  tags                        = local.tags

  site_config {
    application_stack {
      python_version = var.functions_language == "python" ? var.python_version : null
    }
  }

  app_settings = {
    "CosmosDbConnectionString" = azurerm_cosmosdb_account.cosmos.primary_sql_connection_string
    "CosmosDbName"             = azurerm_cosmosdb_sql_database.db.name
    "CosmosContainer"          = azurerm_cosmosdb_sql_container.container.name
    # add your own runtime vars here (e.g., COUNTER_ID)
  }
}

# ---------------- Static Web App (Free) ----------------
resource "azurerm_static_web_app" "swa" {
  name                = local.swa_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.swa_location     # must be supported SWA Free region
  sku_tier            = "Free"
  sku_size            = "Free"
  preview_environments_enabled  = true
  public_network_access_enabled = true
  tags                          = local.tags

}

# ---------------- Custom domain for SWA (DNS validation) ----------------
# ---------------------------
# Custom domains on SWA (external DNS)
# ---------------------------

# Create 0..N custom domains, driven by var.custom_domains
resource "azurerm_static_web_app_custom_domain" "domains" {
  for_each            = toset(var.custom_domains) # [] = none
  static_web_app_id   = azurerm_static_web_app.swa.id
  domain_name         = each.key
  validation_type     = "dns-txt-token"
}
# ---------------------------
# Helpful outputs to paste into your DNS provider
# ---------------------------

output "apex_target_note" {
  value = "Use ALIAS/ANAME/CNAME flattening at apex pointing to ${azurerm_static_web_app.swa.default_host_name}. If your registrar lacks ALIAS/flattening, follow Microsoft’s A-record option (reduced anycast benefits)."
}
