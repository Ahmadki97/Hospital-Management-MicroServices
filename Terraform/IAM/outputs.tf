output "EKS-Role" {
  value = aws_iam_role.HOMA-EKS-Role.arn
}


output "ND-Role" {
  value = aws_iam_role.HOMA-NodeGroup-Role.arn
}

