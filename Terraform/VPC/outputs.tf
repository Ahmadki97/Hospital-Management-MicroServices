output "HOMA-Public-Subnets" {
  value = aws_subnet.HOMA-Public-Subnet[*].id
}

output "HOMA-Private-Subnets" {
  value = aws_subnet.HOMA-Private-Subnet[*].id
  
}

output "HOMA-VPC-ID" {
  value = aws_vpc.homavpc.id
}