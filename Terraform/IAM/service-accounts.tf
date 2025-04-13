resource "kubernetes_service_account" "LB-SA" {
  metadata {
    name = "LB-SA"
    namespace = "kube-system"
    annotations = {
      "eks.amazonaws.com/role-arn" = ""
    }
  }
}

resource "kubernetes_service_account" "EXTDNS-SA" {
  metadata {
    name = "EXTDNS-SA"
    namespace = "kube-system"
    annotations = {
      "eks.amazonaws.com/role-arn" = ""
    }
  }
}