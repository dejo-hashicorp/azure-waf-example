provider "azurerm" {
  features {}
}

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

  custom_rules {
    name      = "AllowRule1"
    priority  = 1000
    action    = "Allow"
    rule_type = "MatchRule"

    match_conditions {
      match_variables {
        variable_name = "RemoteAddr"
      }
      operator = "IPMatch"
      match_values = ["10.0.0.0/8", "192.168.0.0/16"]
    }
  }

  custom_rules {
    name      = "AllowRule2"
    priority  = 2000
    action    = "Allow"
    rule_type = "MatchRule"

    match_conditions {
      match_variables {
        variable_name = "RemoteAddr"
      }
      operator = "IPMatch"
      match_values = ["10.0.0.0/8", "192.168.0.0/16"]
    }
  }
}
