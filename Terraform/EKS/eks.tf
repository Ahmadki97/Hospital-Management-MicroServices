resource "aws_eks_cluster" "HOMA-Cluster" {
  name = "HOMA-Cluster"
  role_arn = var.HOMA-EKS-Role
  vpc_config {
    subnet_ids = var.HOMA-Private-Subnets
    endpoint_private_access = true
  }
}