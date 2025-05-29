output "db_username" {
  value = local.db_creds.username
}

output "db_password" {
  value = local.db_creds.password
}

output "db_port" {
  value = local.db_creds.port
}

output "db_name" {
  value = local.db_creds.dbname
}

output "secret_id" {
  value = data.aws_secretsmanager_secret.db_credentials.id
}

output "raw_secret" {
  value     = data.aws_secretsmanager_secret_version.db_credentials_version.secret_string
  sensitive = true
}
