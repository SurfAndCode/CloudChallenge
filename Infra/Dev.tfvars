# --- environment / naming ---
env         = "dev"
name_prefix = "cloudchallenge"

# --- regions ---
location     = "australiaeast"  # RG + Cosmos
swa_location = "eastasia"       # SWA Free-supported region

# --- DNS (set zone_rg to the RG that hosts your zoltanolasz.com zone) ---
domain_zone = "zoltanolasz.com"
custom_host = "dev.zoltanolasz.com"

# --- Cosmos DB (dev-friendly defaults) ---
cosmos_free_tier  = false   # set true only if your subscription's free-tier slot is unused
cosmos_serverless = true
cosmos_db_name    = "ClickCounter"
cosmos_container  = "Counts"
cosmos_partition  = "/id"

# --- Functions runtime ---
functions_language = "python"   # python | node | dotnet
python_version     = "3.11"

