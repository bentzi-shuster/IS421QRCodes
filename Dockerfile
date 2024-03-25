FROM python:3.12-slim-bullseye

WORKDIR /app 
# the current working directory is /app

RUN useradd -m myuser
# add a non-root user

COPY requirements.txt ./
# copy the requirements file to the working directory

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir logs qr_codes && chown myuser:myuser qr_codes logs
# install the requirements and create the logs and qr_codes directories

COPY --chown=myuser:myuser . .
# copy the rest of the files to the working directory

USER myuser
# change the user to myuser
ENTRYPOINT ["python", "main.py"]
# run the main.py file
CMD ["--url","http://github.com/bentzi-shuster"]
# pass the url argument to the main.py file - this is the default value but can be changed when running the container