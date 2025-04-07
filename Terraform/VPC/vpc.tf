resource "aws_vpc" "homavpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "Hospital Management VPC"
  }
}

