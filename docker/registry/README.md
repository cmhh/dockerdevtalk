We use `docker-compose` here to get a local docker registry running with a basic UI, using images `registry:2` and `joxit/docker-registry-ui:static`.  To start the registry from the `registry` folder:

```bash
docker-compose up -d
```

To stop the registry:

```bash
docker-compose down
```

![](img/registryui.png)