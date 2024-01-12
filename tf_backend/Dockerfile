FROM python:3.10-slim-bullseye

# Copy the application source code
COPY . /tf_backend
WORKDIR /tf_backend

# Install Python dependencies
RUN apt-get update && apt-get install -y git \
    && python -m pip install -r ./requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Expose the port the app runs on
EXPOSE 8888

# Run the application
ENTRYPOINT ["python", "-m", "tf_backend"]


# FROM python:3.10-slim-bullseye 


# # Pyppeteer
# RUN apt-get update && apt-get install -y \
#     apt-transport-https \
#     ca-certificates \
#     curl \
#     gnupg \
#     --no-install-recommends \
#     && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get update && apt-get install -y \
#     google-chrome-stable \
#     --no-install-recommends

# # It won't run from the root user.
# RUN groupadd chrome && useradd -g chrome -s /bin/bash -G audio,video chrome \
#     && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

# COPY . /tf_backend 
# WORKDIR /tf_backend 

# RUN apt-get update && apt-get install -y git

# RUN python3.10 -m pip install -r ./requirements.txt  

# EXPOSE 8888

# ENTRYPOINT ["python", "-m", "tf_backend"]
 