```bash
docker build -t aifaq .
```
Now run this image from this command
```bash
docker run --gpus all -p 3000:3000 -p 8080:8080 aifaq
```

### To check the frontend running on the lightining ai studio.
1. Click on this add icon.

![alt text](image-3.png)

2. Install the web port from here .

![alt text](image.png)

3. Now click on this icon.

![alt text](image-1.png)

4. Now update the port 3000 in here.

![alt text](image-2.png)

### The Backend can be checked using this curl request on the new terminal by this curl request.

```console
curl --header "Content-Type: application/json" --request POST --data '{"text": "How to install Hyperledger fabric?"}' http://127.0.0.1:8080/query
```