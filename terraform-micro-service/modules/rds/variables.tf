variable "db_subnet_name" {
  type = string
  description = "Name of db subnet"
}

variable "private_subnets" {
  type = list(string)
  description = "list of subnets"
}
variable "db_identifier" {
  type = string
  description = "name of db identifier"
}

variable "db_name" {
  type = string
  description = "name of database"
}
variable "db_password" {
  type = string
  description = "password for database"
}

variable "db_username" {
  type = string
  description = "username for database"
}

variable "db_engine" {
  type = string
  description = "database engine"
}

variable "storage_type" {
  type = string
  description = "storage type"
}

variable "db_instance_class" {
  type = string
  description = "database instance type"
}

variable "db_security_group" {
  type = string
  description = "security for database"
}

variable "secret_id" {
  type        = string
  description = "The ID of the secret to update after DB is created"
}

variable "db_port" {}
  