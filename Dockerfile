FROM registry.eiffage.com/python:3.9

WORKDIR /app

#à copier avant le reste des fichiers sources (pour éviter un pip install à chaque fois qu'un fichier source est modifié)
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000