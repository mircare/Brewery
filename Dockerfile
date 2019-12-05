FROM debian:stable-slim
LABEL maintainer <torrisimirko@yahoo.com>

# satisfy the requirements
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git python3 python3-numpy hhsuite ncbi-blast+ -y
RUN apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# get Brewery
RUN git clone https://github.com/mircare/Brewery/ --depth 1 && rm -rf Brewery/.git
RUN git clone http://github.com/soedinglab/hh-suite

ENV HHLIB=/hh-suite
ENV PATH="$HHLIB/bin:$HHLIB/scripts:${PATH}"

# initialize Brewery
RUN echo "[DEFAULT]" >> Brewery/scripts/config.ini
RUN echo "psiblast = psiblast" >> Brewery/scripts/config.ini
RUN echo "uniref90 = /uniref90/uniref90.fasta" >> Brewery/scripts/config.ini
RUN echo "hhblits = hhblits" >> Brewery/scripts/config.ini
RUN echo "uniprot20 = /uniprot20/uniprot20_2016_02" >> Brewery/scripts/config.ini

WORKDIR /Brewery/scripts/Predict_BRNN
RUN chmod a+x Predict && cd .. && bash set_models.sh

WORKDIR /Brewery
