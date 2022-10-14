FROM registry.access.redhat.com/ubi8/python-39
USER root
RUN dnf -y install java-1.8.0-openjdk maven
USER default
RUN wget https://dlcdn.apache.org/spark/spark-3.2.2/spark-3.2.2-bin-hadoop3.2.tgz
RUN tar xvfz spark-3.2.2-bin-hadoop3.2.tgz
ENV SPARK_HOME=/opt/app-root/src/spark-3.2.2-bin-hadoop3.2
ENV PATH=$PATH:$SPARK_HOME/bin
RUN git clone https://github.com/CODAIT/stocator.git
RUN cd /opt/app-root/src/stocator && git checkout v1.1.5
RUN cd /opt/app-root/src/stocator && mvn clean package -Pall-in-one
RUN cd /opt/app-root/src/stocator && mvn dependency:tree
#ADD spark-sql-interactive/stocator-1.1.5-jar-with-dependencies.jar .
RUN pip install pyspark==3.3.0 ipython nbformat jupyter nbconvert
ADD spark-sql-interactive.ipynb .
RUN jupyter nbconvert --to script spark-sql-interactive.ipynb  
CMD ["python ./spark-sql-interactive.py"]