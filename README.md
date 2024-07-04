# Exercicio1

Comandos a executar

docker build -t exercicio1 .

docker run -d --name exercicio1 -v /home/ricardo/Exercicio1/mnt/backups:/mnt/backups:Z --network=host exercicio1:latest