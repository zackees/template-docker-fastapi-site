FROM --platform=linux/amd64 nikolaik/python-nodejs:python3.11-nodejs20-alpine 
# Might be necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
# All the useful binary commands.
RUN apk update && apk add --no-cache \
    ca-certificates \
    bash \
    curl \
    && rm -rf /var/cache/apk/*


WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
# for sending files to other devices
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m pip install --no-cache-dir -e .

WORKDIR /app/www
RUN npm install
RUN npm run build

WORKDIR /app
# Expose the port and then launch the app.
EXPOSE 80
CMD ["/bin/bash", "prod"]
