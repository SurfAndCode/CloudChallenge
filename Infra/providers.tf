terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.30.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.6.2"
    }
  }
}

# Supports both local CLI auth and OIDC in CI
provider "azurerm" {
  features {}

  use_cli  = var.auth_mode == "cli"
  use_oidc = var.auth_mode == "oidc"

  # optional: if you pass these, they'll be used; otherwise az CLI / OIDC context supplies them
  subscription_id = try(trim(var.subscription_id), "") != "" ? var.subscription_id : null
  tenant_id       = try(trim(var.tenant_id), "")       != "" ? var.tenant_id       : null
}
