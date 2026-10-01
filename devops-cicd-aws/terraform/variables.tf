variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "instance_type" {
  type    = string
  default = "t2.micro" # Free Tier eligible in most regions
}

variable "key_name" {
  type        = string
  description = "Name of an existing EC2 key pair"
}

variable "my_ip_cidr" {
  type        = string
  description = "Your public IP in CIDR form, e.g. 203.0.113.10/32"
}
