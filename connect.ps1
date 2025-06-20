$envVars = Get-Content .env | ForEach-Object {
  if ($_ -match "^([^=]+)=(.*)$") {
    $name = $matches[1]
    $value = $matches[2]
    [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
  }
}
mongosh "mongodb+srv://$env:MONGO_USER:$env:MONGO_PASS@sylvr-financial-cluster.jz9cn66.mongodb.net/admin"
