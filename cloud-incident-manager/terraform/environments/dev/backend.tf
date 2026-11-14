terraform {
  backend "s3" {
    bucket       = "cloud-incident-manager-tfstate-795734304267"
    key          = "cloud-incident-manager/dev/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}