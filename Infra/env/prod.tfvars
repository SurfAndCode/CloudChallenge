env            = "prod"
name_prefix    = "cloudchallenge"
location       = "australiaeast"
swa_location   = "eastasia"                         # match your prod SWA region
cosmos_free_tier  = true                           # often off in prod
cosmos_serverless = false                           # pick one, not both (precondition)
custom_domains = ["zoltanolasz.com", "www.zoltanolasz.com"]
