resource "aws_eks_node_group" "HOMA-ND" {
  cluster_name = aws_eks_cluster.HOMA-Cluster.name
  node_role_arn = var.HOMA-ND-Role
  subnet_ids = var.HOMA-Private-Subnets
  instance_types = ["t3.medium"] # This is Default Value
  scaling_config {
    desired_size = 2
    max_size = 3
    min_size = 1
  }
}