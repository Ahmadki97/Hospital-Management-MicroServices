variable "AZs" {
  type = list(string)
  default = [ "us-east-1a", "us-east-1b" ]
}

variable "SubCount" {
  type = number
  default = 2
}