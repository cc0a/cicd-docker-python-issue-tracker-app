terraform {
  backend "s3" {
    bucket       = "REPLACE_WITH_YOUR_UNIQUE_BUCKET_NAME"
    key          = "cloud-incident-manager/dev/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}