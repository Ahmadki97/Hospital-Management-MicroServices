resource "helm_release" "AWS-LB-Controller" {
  name = "load-lb-controller"
  namespace = "kube-system"
  repository = "https://aws.github.io/eks-charts"
  chart = "aws-load-balancer-controller"
  set {
    name = "clusterName"
    value = "HOMA-Cluster"
  }
  set {
    name = "serviceAccount.create"
    value = "false"
  }
  set {
    name = "serviceAccount.name"
    value = ""
  }
  set {
    name = "region"
    value = "us-east-1"
  }
  set {
    name = "vpcId"
    value = var.HOMA-VPC-ID
  }
}