FROM mcr.microsoft.com/dotnet/sdk:8.0
RUN cp /bin/bash /bin/sh
RUN apt-get update -y && apt-get install python3 python3-venv python3-pip git -y
RUN apt-get install unixodbc-dev -y
RUN git clone https://github.com/lvovan/CS-IMC.git
WORKDIR CS-IMC/TP-Bdd-src
RUN python3 -m venv .venv && \
    source .venv/bin/activate && \
    pip install -r requirements.txt
COPY . .

