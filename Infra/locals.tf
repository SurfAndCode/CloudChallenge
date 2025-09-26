locals {
  # Stable, readable names per env
  rg_name   = "rg-${var.name_prefix}-${var.env}"
  swa_name  = "${var.name_prefix}-${var.env}-swa"
  plan_name = "asp-${var.name_prefix}-${var.env}"
  func_name = "${var.name_prefix}-${var.env}-func"

  # Storage account base: only [a-z0-9], keep room for a 6-char random suffix
  sa_base_raw   = lower("${var.name_prefix}${var.env}sa")
  # keep only [a-z0-9] characters
  sa_base_clean = join("", regexall("[a-z0-9]", local.sa_base_raw))
  sa_base       = substr(local.sa_base_clean, 0, 18)  # 18 + 6 suffix = 24 max

  tags = {
    env = var.env
    app = var.name_prefix
  }
}
