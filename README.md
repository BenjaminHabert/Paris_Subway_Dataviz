# RATP_Dataviz

build a small multiple plot of the Paris subway network

# Development

```
$ git clone git@github.com:BenjaminHabert/RATP_Dataviz.git
$ make install
$ make pipeline
```

## Pipeline steps

- get the list of stations and lines from [wikipedia](https://fr.wikipedia.org/wiki/Liste_des_stations_du_m%C3%A9tro_de_Paris)
- for each line: get the color of the line by looking at the proper div in
it's [own wikipedia page](https://fr.wikipedia.org/wiki/Ligne_9_du_m%C3%A9tro_de_Paris)
