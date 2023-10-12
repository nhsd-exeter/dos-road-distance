locals {
  standard_tags = {
    "Programme"   = var.programme
    "Service"     = "core-dos"
    "SharedService" = "dos"
    "Product"     = "core-dos"
    "Environment" = var.profile
  }
}
