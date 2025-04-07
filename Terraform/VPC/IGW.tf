resource "aws_internet_gateway" "HOMA-IGW" {
  vpc_id = aws_vpc.homavpc.id
  tags = {
    Name = "Hospital Management IGW"
  }
}