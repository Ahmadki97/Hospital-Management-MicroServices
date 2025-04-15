module "VPC" {
  source = "./VPC"
}


module "IAM" {
  source = "./IAM"
}

module "EKS" {
  source = "./EKS"
  HOMA-Private-Subnets = module.VPC.HOMA-Private-Subnets
  HOMA-EKS-Role = module.IAM.EKS-Role
  HOMA-ND-Role = module.IAM.ND-Role
}

module "HELM" {
  source = "./HELM"
  HOMA-VPC-ID = module.VPC.HOMA-VPC-ID
  LB-SA = module.IAM.LB-SA
  EXTDNS-SA = module.IAM.EXTDNS-SA
}