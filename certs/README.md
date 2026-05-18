```shell
# Генерация rsa приватного ключа 
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Генерация публичного ключа на основа приватного 
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem 
```