<div
align="center">
<img width="313" alt="Logo_Cooky2" src="https://user-images.githubusercontent.com/46084416/168781713-ce8fdb9e-aea9-4dfc-b0f6-c4c8a4dff6b5.png">
</div>
#  Automatic Recipe Suggestion

The main aim of the project is to build a user-friendly application that allows users to synchronise their personal pantry and receive tailored recipe suggestions. 

- online recipes
- user rating
- custom recommendations
- virtual pantry for enhanced functionalities

For more information see ```docs``` folder

## Usage

### Database
```
docker container run -p 5432:5432 --name cooky -e POSTGRES_PASSWORD=1234 postgres:12.2 
```

### Server
```
python3 ./src/Cooky/api.py development
```

### Client
```
cd ./app/cooky
npm install
npm run serve
```


### Development: 

Postgres DB with docker

```bash
docker container run -p 5432:5432 --name cooky -e POSTGRES_PASSWORD=1234 postgres:12.2 

docker container run -p 5432:5432 --name cooky -e POSTGRES_PASSWORD=1234 -v C:/Projects/Cooky/data/part_dataset.csv:/tmp/full_dataset.csv postgres:12.2

```

Dataset download [here](https://recipenlg.cs.put.poznan.pl/dataset) and unzip it into '/data'.


### Remarks
Food_extractor is part of FoodBert and not developed by this group. Original can be found [here](https://github.com/chambliss/foodbert) and [here](https://huggingface.co/chambliss/distilbert-for-food-extraction?text=1+large+whole+chicken).

### Documentation

The PDF with the project report is in the folder docs.
It includes the One-Pager which documents the contribution of each team member.
