resource "aws_route_table" "HOMA-Public-Table" {
  vpc_id = aws_vpc.homavpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.HOMA-IGW.id
  }
  tags = {
    Name = "Public Route Table"
  }
}


resource "aws_route_table" "HOMA-Private-Table" {
  vpc_id = aws_vpc.homavpc.id
  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.HOMA-NateGateway.id
  }
  tags = {
    Name = "Private Route Table"
  }
}


resource "aws_route_table_association" "Public-Subnets-Association" {
  count = var.SubCount
  subnet_id = aws_subnet.HOMA-Public-Subnet[count.index].id
  route_table_id = aws_route_table.HOMA-Public-Table.id
}


resource "aws_route_table_association" "Private-Subnets-Association" {
  count = var.SubCount
  subnet_id = aws_subnet.HOMA-Private-Subnet[count.index].id
    route_table_id = aws_route_table.HOMA-Private-Table.id
}