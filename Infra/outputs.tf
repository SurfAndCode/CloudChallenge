# Expose the site URL so CI can read it with `terraform output -raw site_url`
output "site_url" {
  value = var.site_url
}

output "rg_name" {
  value = azurerm_resource_group.rg.name
}

output "function_app_name" {
  value = azurerm_linux_function_app.func.name
}

output "function_default_hostname" {
  value = azurerm_linux_function_app.func.default_hostname
}

output "swa_name" {
  value = azurerm_static_web_app.swa.name
}

output "swa_default_hostname" {
  value = azurerm_static_web_app.swa.default_host_name
}

output "cosmos_primary_sql_connection_string" {
  value     = azurerm_cosmosdb_account.cosmos.primary_sql_connection_string
  sensitive = true
}

# TXT records per custom domain: name + token (useful for Cloudflare)
output "custom_domains_txt_records" {
  value = {
    for d, r in azurerm_static_web_app_custom_domain.domains :
    d => {
      name  = "_dnsauth.${d}"
      value = r.validation_token
    }
  }
  sensitive = true
}

# CNAME target for all custom domains
output "custom_domains_cname_target" {
  value = azurerm_static_web_app.swa.default_host_name
}
