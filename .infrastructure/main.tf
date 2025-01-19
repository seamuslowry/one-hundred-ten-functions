terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4.0"
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
  subscription_id = "0d1c4cc3-d445-4591-8a25-0c4279b7dd17"
  features {}
}

provider "github" {}