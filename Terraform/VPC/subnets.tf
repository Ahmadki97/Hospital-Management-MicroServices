resource "aws_subnet" "HOMA-Public-Subnet" {
  count = var.SubCount
  vpc_id = aws_vpc.homavpc.id
  cidr_block = "10.0.${count.index}.0/24"
  availability_zone = element(var.AZs, count.index)
  tags = {
    Name = "Hospital Management Public Subnet 0${count.index}"
  }
}


resource "aws_subnet" "HOMA-Private-Subnet" {
  count = var.SubCount
  vpc_id = aws_vpc.homavpc.id
  cidr_block = "10.0.${count.index + 2}.0/24"
  availability_zone = element(var.AZs, count.index)
  tags = {
    Name = "Hospital Management Private Subnet 0${count.index + 2}"
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/HOMA-Cluster" = "owned"
  }
}