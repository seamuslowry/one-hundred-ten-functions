terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }

    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }

  }

  backend "azurerm" {
      resource_group_name  = "tofu"
      storage_account_name = "tofuinfra"
      container_name       = "state"
      key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

provider "github" {}