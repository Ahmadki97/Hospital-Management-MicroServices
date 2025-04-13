resource "aws_iam_role" "HOMA-EKS-Role" {
  name = "HOMA-EKS-Role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "eks.amazonaws.com"
            }
        }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "EKSCluster-Attachments" {
  for_each = toset(var.EKS-Policies-ARNs)  
  role = aws_iam_role.HOMA-EKS-Role.name
  policy_arn = each.value
}



resource "aws_iam_role" "HOMA-NodeGroup-Role" {
  name = "HOMA-NodeGroup-Role"
  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}


resource "aws_iam_role_policy_attachment" "ND-Attachments" {
  for_each = toset(var.EKS-NodeGroup-Policies-ARNs)
  role = aws_iam_role.HOMA-NodeGroup-Role.name
  policy_arn = each.value
}



