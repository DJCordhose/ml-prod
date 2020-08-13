FROM continuumio/miniconda3
# FROM continuumio/anaconda3

# https://medium.com/@chadlagore/conda-environments-with-docker-82cdc9d25754
# WORKDIR /app
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

ARG conda_env=ml-prod
RUN echo "source activate ${conda_env}" > ~/.bashrc
ENV PATH /opt/conda/envs/${conda_env}/bin:$PATH

COPY . .

# EXPOSE 8888
# ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]
