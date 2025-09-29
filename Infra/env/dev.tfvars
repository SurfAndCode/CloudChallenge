env            = "dev"
name_prefix    = "cloudchallenge"
location       = "australiaeast"
swa_location   = "eastasia"                         # SWA Free region you used
cosmos_free_tier  = true
cosmos_serverless = false
custom_domains = ["dev.zoltanolasz.com"]            # or [] if you add later
auth_mode  = "oidc" # or "cli" if you run TF locally
site_url   = "https://dev.zoltanolasz.com"

