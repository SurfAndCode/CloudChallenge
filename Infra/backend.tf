terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"   
    storage_account_name = "cctfstatestorage"
    container_name       = "tfstate"
    key                  = "cloudchallenge.tfstate" 
  }
}
