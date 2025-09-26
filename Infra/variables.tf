##############################
# variables.tf
##############################

variable "auth_mode" {
  description = "Auth mode: 'cli' (local) or 'oidc' (CI)."
  type        = string
  default     = "cli"
}

variable "env" {
  description = "Deployment environment name."
  type        = string

  validation {
    condition     = can(regex("^(dev|prod)$", var.env))
    error_message = "env must be 'dev' or 'prod'."
  }
}

variable "name_prefix" {
  description = "Prefix used in resource names (e.g., 'cloudchallenge')."
  type        = string
}

variable "location" {
  description = "Azure region for RG/Functions/Cosmos (e.g., 'australiaeast')."
  type        = string
}

variable "swa_location" {
  description = "Azure region for Static Web Apps (e.g., 'eastasia')."
  type        = string
}

# ---------------- Cosmos DB ----------------

variable "cosmos_free_tier" {
  description = "Enable Cosmos DB Free Tier (cannot be true if cosmos_serverless is also true)."
  type        = bool
  default     = true
}

variable "cosmos_serverless" {
  description = "Enable Cosmos DB Serverless (cannot be true if cosmos_free_tier is also true)."
  type        = bool
  default     = false
}

variable "cosmos_db_name" {
  description = "Cosmos SQL database name."
  type        = string
  default     = "ClickCounter"
}

variable "cosmos_container" {
  description = "Cosmos SQL container name."
  type        = string
  default     = "Counts"
}

variable "cosmos_partition" {
  description = "Cosmos SQL partition key path."
  type        = string
  default     = "/id"
}

# ---------------- Function App ----------------

variable "functions_language" {
  description = "Function App language (this stack assumes Python unless you extend main.tf)."
  type        = string
  default     = "python"

  validation {
    condition     = var.functions_language == "python"
    error_message = "Only 'python' is supported by the current main.tf site_config. Update main.tf if using another language."
  }
}

variable "python_version" {
  description = "Python runtime version for the Function App."
  type        = string
  default     = "3.11"
}

# ---------------- Static Web App ----------------

variable "custom_domains" {
  description = "Optional list of custom domains for the SWA (DNS TXT validation)."
  type        = list(string)
  default     = []
}
