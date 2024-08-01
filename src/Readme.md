```bash
docker build -t aifaq .
```
Now run this image from this command
```bash
docker run --gpus all -p 3000:3000 -p 8080:8080 aifaq
```