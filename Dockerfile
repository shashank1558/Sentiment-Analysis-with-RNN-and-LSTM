FROM continuumio/miniconda3

WORKDIR /home/ubuntu/deploy/

COPY requirements.txt ./

COPY environment.yml ./

COPY model ./

COPY data ./

COPY src ./

COPY main.py ./

COPY project.py ./

COPY boot.sh ./
 
RUN chmod +x boot.sh

RUN conda env create -f environment.yml

RUN echo "source activate sentiment_analysis" > ~/.bashrc
ENV PATH /opt/conda/envs/sentiment_analysis/bin:$PATH

RUN conda develop project.py

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]




