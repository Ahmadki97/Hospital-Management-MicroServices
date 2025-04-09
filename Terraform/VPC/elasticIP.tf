resource "aws_eip" "HOMA-EIP" {
  domain = "vpc"
  tags = {
    Name = "Hospital Management Elastic IP"
  }
}