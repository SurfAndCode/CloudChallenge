terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = ">= 4.30.0" }
    random  = { source = "hashicorp/random",  version = ">= 3.6.2" }
  }
}
provider "azurerm" {
  features {}
  use_cli  = true
  # use_oidc = var.auth_mode == "oidc"
  subscription_id = "ba91f935-e393-4fff-9d00-5c5ceefd144f"
  # tenant_id       = var.tenant_id
}