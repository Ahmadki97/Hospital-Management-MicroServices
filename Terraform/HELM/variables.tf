variable "LB-SA" {
  type = string
  description = "Name of the aws lb service account"
}

variable "HOMA-VPC-ID" {
  type = string
  description = "The ID of the VPC where the aws lb controller will be created"
}

variable "EXTDNS-SA" {
  type = string
  description = "Name of the external-dns service account"
}