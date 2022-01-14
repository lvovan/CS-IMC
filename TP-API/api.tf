provider "azurerm" {
    features {}
}

resource "azurerm_resource_group" "rg" {
    name     = "[A COMPLETER]-api-rg"
    location = "France Central"
    tags = {
       tpapi = "1"
    }
}

resource "azurerm_storage_account" "storage" {
    name                     = "[A COMPLETER]apisto"
    resource_group_name      = azurerm_resource_group.rg.name
    location                 = azurerm_resource_group.rg.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "serviceplan" {
    name                = "[A COMPLETER]-api-service-plan"
    location            = [A COMPLETER - référencer la location du groupe de ressource]
    resource_group_name = [A COMPLETER - référencer la location du groupe de ressource]
    kind                = "elastic"
    reserved            = "true"
    sku {
      tier = "Dynamic"
      size = "Y1"
    }
}

resource "azurerm_function_app" "functionapp" {
    name                       = "[A COMPLETER]-api-fa"
    location                   = [A COMPLETER - référencer la location du groupe de ressource]
    resource_group_name        = [A COMPLETER - référencer la location du groupe de ressource]
    app_service_plan_id        = azurerm_app_service_plan.serviceplan.id
    storage_account_name       = azurerm_storage_account.storage.name
    storage_account_access_key = azurerm_storage_account.storage.primary_access_key
    os_type                    = "linux"
    version                    = "~3"
    app_settings = {
        "FUNCTIONS_WORKER_RUNTIME" = "python",
        "TPBDD_SERVER" = [A COMPLETER]
        "TPBDD_DB" = "tp2bdd-movies-sql",
        "TPBDD_USERNAME" = "sqladmin",
        "TPBDD_PASSWORD" = [A COMPLETER]
        "TPBDD_NEO4J_SERVER" = [A COMPLETER]
        "TPBDD_NEO4J_USER" = "neo4j",
        "TPBDD_NEO4J_PASSWORD" = [A COMPLETER]
    }
}