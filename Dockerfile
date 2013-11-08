FROM stackbrew/ubuntu:raring

MAINTAINER Philipp Bosch, hello@pb.io

RUN apt-get update && apt-get install -y software-properties-common git python-pip
RUN add-apt-repository -y ppa:chrysn/openscad
RUN apt-get update && apt-get install -y openscad
RUN git clone https://github.com/beyond-prototyping/openscad2stl.git /app && pip install -r /app/requirements.txt

ENV OPENSCAD_BINARY /usr/bin/openscad
ENTRYPOINT ["python", "/app/app.py"]
EXPOSE 5000
