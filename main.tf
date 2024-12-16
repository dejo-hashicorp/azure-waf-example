resource "azurerm_web_application_firewall_policy" "example" {
  name                = "example-waf-policy"
  resource_group_name = "example-resource-group"
  location            = "US East"
  policy_settings {
    mode = "Prevention"
  }

  managed_rules {
    managed_rule_set {
      type    = "OWASP"
      version = "3.2"
    }
  }

    custom_rule {
      name      = "AllowRule1"
      priority  = 1000
      action    = "Allow"

      match_condition {
        match_variables {
          variable_name = "RemoteAddr"
        }
        operator = "IPMatch"
        values   = ["10.0.0.0/8", "192.168.0.0/16"]
      }
    }

    custom_rule {
      name      = "AllowRule2"
      priority  = 2000
      action    = "Allow"

      match_condition {
        match_variables {
          variable_name = "RemoteAddr"
        }
        operator = "IPMatch"
        values   = ["10.0.0.0/8", "192.168.0.0/16"]
      }
    }
}
