resource "kubernetes_namespace" "Prometheus" {
  metadata {
    name = "Prometheus"
  }
}

resource "kubernetes_namespace" "Grafana" {
  metadata {
    name = "Grafana"
  }
}

