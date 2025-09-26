terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"         # adjust to your state RG
    storage_account_name = "cctfstatestorage"     # adjust to your state SA
    container_name       = "tfstate"
    key                  = "cloudchallenge.tfstate" 
  }
}
