resource "github_actions_secret" "app_publish_profile" {
  repository      = "hundred-and-ten-serverless"
  secret_name     = "AZURE_PUBLISH_PROFILE"
  plaintext_value = data.external.publish_profile.result.profile
}
