variable "name" {
  type = string
}

variable "security_groups" {
  type = list(string)
}

variable "subnets" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

variable "target_group_name" {
  type = string
}

variable "target_group_port" {
  type = number
  default = 80
}

variable "health_check_path" {
  type    = string
  default = "/"
}

variable "acm_cert_arn" {
  type = string
}

