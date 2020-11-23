# Deploying Models via Flask

This is just a very quick demo using Flask to deploy a classification model.  We simply import a Resnet classifier with pre-trained weights, and then provide a simple endpoint which accepts an uploaded image, classifies it, and returns the top 5 classes.

Flask applications are relatively straightforward to containerise, and a Dockerfile is provided.  To build:

```bash
docker build -t resnet .
```

To run the service, in this case on port 5003 and with a volume mounted to persist the classification model between restarts:

```bash
docker run -d --rm \
  --name resnet \
  -p 5000:5000 \
  -v $PWD/model:/app/model \
  resnet
```

# Usage

From a terminal, run:

```bash
curl -F "file=@/path/to/image/cat.jpg" https://cmhh.hopto.org/resnet/predict
```

If just using GET, for example, by visiting the link in a web browser, an upload form will be displayed.

# Examples

<table style="width: 100%">
<tr>
<td style="width: 50%;">
<a href="https://pm1.narvii.com/6233/68d8ca3ac1be4305e82caf6413b8a18db9114c0f_hq.jpg" target="_blank"><img src="https://pm1.narvii.com/6233/68d8ca3ac1be4305e82caf6413b8a18db9114c0f_hq.jpg"></a>
</td>
<td style="width: 50%;">
<pre><code class="json hljs">[["n02123597","Siamese_cat",0.9997847676277161],["n02123394","Persian_cat",0.0001417139865225181],["n02127052","lynx",6.384297012118623e-05],["n02328150","Angora",3.227661181881558e-06],["n02124075","Egyptian_cat",2.405418399575865e-06]]</code></pre>
</td>
</tr>
<tr>
<td style="width: 50%;">
<a href="https://www.petguide.com/wp-content/uploads/2017/02/Earthpassage-668x445.jpg" target="_blank"><img src="https://www.petguide.com/wp-content/uploads/2017/02/Earthpassage-668x445.jpg"></a>
</td>
<td style="width: 50%;">
<pre><code class="json hljs">[["n02093428","American_Staffordshire_terrier",0.7422895431518555],["n02099849","Chesapeake_Bay_retriever",0.15990932285785675],["n02093256","Staffordshire_bullterrier",0.03410174325108528],["n02108422","bull_mastiff",0.023535776883363724],["n02099712","Labrador_retriever",0.01739639975130558]]</code></pre>
</td>
</tr>
</table>