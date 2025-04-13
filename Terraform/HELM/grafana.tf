resource "helm_release" "Grafana" {
  name = "Grafana"
  chart = "grafana"
  namespace = kubernetes_namespace.Grafana.metadata[0].name
  create_namespace = true
  repository = "https://grafana.github.io/helm-charts"
  depends_on = [ kubernetes_namespace.Grafana ]
}