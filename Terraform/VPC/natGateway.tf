resource "aws_nat_gateway" "HOMA-NateGateway" {
  allocation_id = aws_eip.HOMA-EIP.id
  subnet_id = aws_subnet.HOMA-Public-Subnet[0].id
  tags = {
    Name = "Hospital Management Nat Gateway"
  }
}